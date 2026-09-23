"""Stage 6: assemble the clean (caption-free) master render.

Concatenates each beat's visual (photo gets Ken Burns pan/zoom, video gets a
straight cut to length) synced to that beat's VO duration, applies the
brand color-grade LUT, ducks a music bed under the narration, overlays the
watermark, and outputs one clean MP4. Captions are burned in as a separate
pass in captioner.py (needs word-level timestamps from the clean voice
track first — see docs/03).

This module shells out to ffmpeg directly (via subprocess) rather than a
higher-level wrapper, since the beat-by-beat Ken Burns + concat logic is
easier to reason about as an explicit filter_complex graph than through an
abstraction layer.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from mutagen.mp3 import MP3  # lightweight way to read audio duration

from pipeline.config import Config, CACHE_DIR

FPS = 30
WIDTH, HEIGHT = 1080, 1920  # 9:16


def _audio_duration_sec(path: Path) -> float:
    return MP3(path).info.length


def _ken_burns_clip(image_path: Path, duration_sec: float, out_path: Path, zoom_in: bool = True) -> None:
    """Slow pan/zoom on a still image for `duration_sec`, cropped to 9:16."""
    frames = int(duration_sec * FPS)
    zoom_expr = "zoom+0.0015" if zoom_in else "1.5-0.0015*on"
    filter_str = (
        f"scale=8000:-1,"
        f"zoompan=z='{zoom_expr}':d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS}"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
            "-vf", filter_str, "-t", str(duration_sec),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path),
        ],
        check=True,
    )


def _video_clip_to_length(video_path: Path, duration_sec: float, out_path: Path) -> None:
    """Trims/loops a stock video clip to match the beat's VO duration and
    crops/scales to 9:16.
    """
    filter_str = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT}"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-stream_loop", "-1", "-i", str(video_path),
            "-t", str(duration_sec), "-vf", filter_str,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(out_path),
        ],
        check=True,
    )


def build_beat_clips(script: dict, audio_files: dict, visual_files: dict, job_dir: Path) -> list[Path]:
    """One silent video clip per beat, timed to that beat's VO duration."""
    beat_keys = ["hook"] + [f"body_beat_{i}" for i in range(len(script["body_beats"]))] + ["payoff"]
    audio_lookup = {
        "hook": audio_files["hook"],
        **{f"body_beat_{i}": p for i, p in enumerate(audio_files["body_beats"])},
        "payoff": audio_files["payoff"],
    }

    clips = []
    for key in beat_keys:
        visual = visual_files.get(key)
        if visual is None:
            raise RuntimeError(
                f"No visual sourced for beat '{key}' — resolve via pipeline/visuals.py "
                f"or manual sourcing before assembling (see docs/04)."
            )
        duration = _audio_duration_sec(audio_lookup[key]) + 0.3  # small pad between beats
        out_path = job_dir / f"clip_{key}.mp4"
        if visual.suffix.lower() in (".jpg", ".jpeg", ".png"):
            _ken_burns_clip(visual, duration, out_path)
        else:
            _video_clip_to_length(visual, duration, out_path)
        clips.append(out_path)
    return clips


def concat_clips(clips: list[Path], out_path: Path) -> Path:
    concat_list_path = out_path.parent / "concat_list.txt"
    concat_list_path.write_text("\n".join(f"file '{c.resolve()}'" for c in clips))
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
            "-c", "copy", str(out_path),
        ],
        check=True,
    )
    return out_path


def concat_audio(audio_files: dict, out_path: Path) -> Path:
    ordered = [audio_files["hook"], *audio_files["body_beats"], audio_files["payoff"]]
    concat_list_path = out_path.parent / "concat_audio_list.txt"
    concat_list_path.write_text("\n".join(f"file '{p.resolve()}'" for p in ordered))
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
            "-c", "copy", str(out_path),
        ],
        check=True,
    )
    return out_path


def mix_with_music_and_watermark(
    config: Config, video_path: Path, voice_track: Path, music_path: Path | None, out_path: Path
) -> Path:
    """Mixes ducked music under the voice track, overlays the watermark, and
    writes the final clean (caption-free) master render.
    """
    watermark = config.watermark_path
    inputs = ["-i", str(video_path), "-i", str(voice_track)]
    filter_parts = []
    if watermark.exists():
        inputs += ["-i", str(watermark)]
        filter_parts.append("[0:v][2:v]overlay=W-w-24:H-h-24[vout]")
        video_map = "[vout]"
    else:
        video_map = "0:v"

    if music_path and music_path.exists():
        inputs += ["-i", str(music_path)]
        # duck music under narration; music input index depends on whether watermark was added
        music_idx = 3 if watermark.exists() else 2
        filter_parts.append(
            f"[{music_idx}:a]volume=0.15[music];[1:a][music]amix=inputs=2:duration=first[aout]"
        )
        audio_map = "[aout]"
    else:
        audio_map = "1:a"

    cmd = ["ffmpeg", "-y", *inputs]
    if filter_parts:
        cmd += ["-filter_complex", ";".join(filter_parts)]
    cmd += ["-map", video_map, "-map", audio_map, "-c:v", "libx264", "-c:a", "aac", str(out_path)]
    subprocess.run(cmd, check=True)
    return out_path


def assemble(config: Config, script: dict, audio_files: dict, visual_files: dict, job_dir: Path) -> Path:
    clips = build_beat_clips(script, audio_files, visual_files, job_dir)
    silent_video = concat_clips(clips, job_dir / "silent_master.mp4")
    voice_track = concat_audio(audio_files, job_dir / "voice_master.mp3")
    music_path = None  # TODO: pick from config.raw["music"]["mood_pool"] by pillar once tracks are added
    final = mix_with_music_and_watermark(
        config, silent_video, voice_track, music_path, job_dir / "clean_master.mp4"
    )
    return final


if __name__ == "__main__":
    print(
        "Run via pipeline.orchestrator, not standalone — this stage needs "
        "script + rendered audio + sourced visuals as inputs."
    )
