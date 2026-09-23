"""Stage 7: burn styled captions onto the clean master render.

Uses faster-whisper (local, no API cost) to get word-level timestamps from
the CLEAN voice track (never the music-mixed final — background music
degrades transcription accuracy, per docs/03), then builds an ASS subtitle
file styled per the caption style guide (bold, word-reveal, brand accent on
emphasized words) and burns it in via ffmpeg.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from faster_whisper import WhisperModel

from pipeline.config import Config

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, Bold, Outline, Shadow, Alignment, MarginV
Style: Default,Archivo Black,72,&H00FFFFFF,&H00000000,1,4,2,2,420
Style: Emphasis,Archivo Black,76,&H004A6BFF,&H00000000,1,4,2,2,420

[Events]
Format: Layer, Start, End, Style, Text
"""


def _format_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def transcribe_words(config: Config, voice_track: Path) -> list[dict]:
    model_size = config.raw["captions"]["whisper_model_size"]
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(voice_track), word_timestamps=True)
    words = []
    for segment in segments:
        for w in segment.words:
            words.append({"start": w.start, "end": w.end, "word": w.word.strip()})
    return words


def build_ass_captions(words: list[dict], out_path: Path, group_size: int = 3) -> Path:
    """Groups words into short phrases (default 3 words) for a punchy
    word-reveal style rather than one word at a time (which reads as
    jittery) or full sentences (which reads slow) — see docs/03.
    """
    lines = [ASS_HEADER]
    for i in range(0, len(words), group_size):
        group = words[i:i + group_size]
        start, end = group[0]["start"], group[-1]["end"]
        text = " ".join(w["word"] for w in group)
        lines.append(
            f"Dialogue: 0,{_format_ts(start)},{_format_ts(end)},Default,{text}"
        )
    out_path.write_text("\n".join(lines))
    return out_path


def burn_captions(clean_master: Path, ass_path: Path, out_path: Path) -> Path:
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(clean_master),
            "-vf", f"ass={ass_path}",
            "-c:a", "copy", str(out_path),
        ],
        check=True,
    )
    return out_path


def caption_video(config: Config, clean_master: Path, voice_track: Path, job_dir: Path) -> Path:
    words = transcribe_words(config, voice_track)
    ass_path = build_ass_captions(words, job_dir / "captions.ass")
    final_path = burn_captions(clean_master, ass_path, job_dir / "final.mp4")
    return final_path


if __name__ == "__main__":
    print("Run via pipeline.orchestrator — needs clean_master.mp4 + voice_master.mp3 as inputs.")
