"""Stage 3: render narration audio from a script's VO lines.

Two providers supported per config/channel_config.yaml `voice.provider`:
- elevenlabs (default, requires ELEVENLABS_API_KEY + a locked voice_id)
- higgsfield (fallback — this workspace already has Higgsfield MCP access;
  when running the pipeline from inside a Claude session with that MCP
  server available, call its text2speech_v2 model via generate_audio
  instead of this HTTP path. This module's `render_elevenlabs` is what a
  standalone cron/CI run uses.)

Renders one clean, caption-free voice file per beat AND one concatenated
full track — the assembler needs beat-level timing to sync visual cuts to
the VO, and the captioner needs the clean full track for Whisper timing
(never the music-mixed final, per docs/03's captioning note).
"""
from __future__ import annotations

from pathlib import Path

import requests

from pipeline.config import Config, CACHE_DIR

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def render_elevenlabs(config: Config, text: str, out_path: Path) -> Path:
    api_key = config.env("ELEVENLABS_API_KEY")
    voice_id = config.voice_id
    resp = requests.post(
        ELEVENLABS_TTS_URL.format(voice_id=voice_id),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        },
        timeout=60,
    )
    resp.raise_for_status()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.content)
    return out_path


def render_script_audio(config: Config, script: dict, job_dir: Path) -> dict:
    """Renders one audio file per beat (hook, each body beat, payoff) plus a
    manifest of which file maps to which beat — the assembler uses this to
    place each visual cue against its matching VO segment.

    Returns: {"hook": Path, "body_beats": [Path, ...], "payoff": Path}
    """
    job_dir.mkdir(parents=True, exist_ok=True)
    provider = config.voice_provider

    if provider != "elevenlabs":
        raise NotImplementedError(
            "Higgsfield TTS path: run this stage from inside a Claude session "
            "with the Higgsfield MCP server attached, calling generate_audio "
            "with model text2speech_v2 and the locked voice_id from "
            "config/channel_config.yaml. Not implemented as a standalone HTTP "
            "call here since Higgsfield's MCP tools aren't a public REST API."
        )

    result = {"hook": None, "body_beats": [], "payoff": None}
    result["hook"] = render_elevenlabs(config, script["hook"]["vo"], job_dir / "vo_hook.mp3")
    for i, beat in enumerate(script["body_beats"]):
        p = render_elevenlabs(config, beat["vo"], job_dir / f"vo_beat_{i}.mp3")
        result["body_beats"].append(p)
    result["payoff"] = render_elevenlabs(config, script["payoff"]["vo"], job_dir / "vo_payoff.mp3")
    return result


if __name__ == "__main__":
    import json
    import sys

    cfg = Config.load()
    script = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else None
    if not script:
        print("Usage: python -m pipeline.tts <path_to_script.json>")
        raise SystemExit(1)
    job_dir = CACHE_DIR / f"fact_{script['fact_id']}"
    files = render_script_audio(cfg, script, job_dir)
    print(files)
