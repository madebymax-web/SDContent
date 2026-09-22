"""Runs the full pipeline end-to-end for one Short: topic -> script -> voice
-> visuals -> assembly -> captions -> review queue (or direct publish, once
config.review_required is False — see docs/04's phase-out plan).

Usage:
    python -m pipeline.orchestrator --mode daily          # produce today's short
    python -m pipeline.orchestrator --mode daily --publish-directly  # skip review queue regardless of config

This is what .github/workflows/daily-content.yml calls on schedule.
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

from pipeline.assembler import assemble
from pipeline.captioner import caption_video
from pipeline.config import CACHE_DIR, Config, REVIEW_QUEUE_DIR
from pipeline.publisher import publish_to_instagram, upload_to_youtube
from pipeline.script_writer import write_script
from pipeline.topic_selector import already_produced_ids, select_next
from pipeline.tts import render_script_audio
from pipeline.visuals import source_all_visuals


def produce_one_short(config: Config) -> dict:
    fact = select_next(config, exclude_ids=already_produced_ids())
    print(f"[1/6] Selected fact #{fact.id} [{fact.pillar}]")

    script = write_script(config, fact)
    print(f"[2/6] Script written: \"{script['title']}\"")

    job_dir = CACHE_DIR / f"fact_{fact.id}_{datetime.now():%Y%m%d_%H%M%S}"
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "script.json").write_text(json.dumps(script, indent=2))

    audio_files = render_script_audio(config, script, job_dir)
    print("[3/6] Voiceover rendered")

    visual_files = source_all_visuals(config, script, job_dir)
    missing = [k for k, v in visual_files.items() if v is None]
    if missing:
        raise RuntimeError(
            f"Missing visuals for beats {missing} on fact #{fact.id} — "
            f"resolve manually before this video can proceed (see docs/04)."
        )
    print("[4/6] Visuals sourced")

    clean_master = assemble(config, script, audio_files, visual_files, job_dir)
    print("[5/6] Assembled clean master render")

    final_video = caption_video(config, clean_master, job_dir / "voice_master.mp3", job_dir)
    print("[6/6] Captions burned in — final render ready")

    return {
        "fact_id": fact.id,
        "script": script,
        "job_dir": job_dir,
        "final_video": final_video,
    }


def route_to_review_or_publish(config: Config, result: dict, publish_directly: bool = False) -> None:
    script = result["script"]
    final_video = result["final_video"]

    if config.review_required and not publish_directly:
        REVIEW_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        dest = REVIEW_QUEUE_DIR / f"{result['fact_id']}_{final_video.parent.name}.mp4"
        shutil.copy(final_video, dest)
        metadata_dest = dest.with_suffix(".json")
        metadata_dest.write_text(json.dumps(script, indent=2))
        print(
            f"Video routed to review queue: {dest}\n"
            f"Approve/reject per the checklist in docs/08-daily-operations-sop.md "
            f"before it's published."
        )
        return

    print("Publishing directly (review_required=False or --publish-directly)...")
    youtube_id = upload_to_youtube(
        config,
        final_video,
        title=script["title"],
        description=script["caption"],
        tags=script["hashtags"],
        is_short=True,
    )
    print(f"Published to YouTube: https://youtube.com/shorts/{youtube_id}")

    public_url = f"{config.env('MEDIA_HOST_PUBLIC_BASE_URL')}/{final_video.name}"
    print(
        f"NOTE: Instagram publishing requires the render at a public URL first. "
        f"Upload {final_video} to your media host, then confirm it's reachable at "
        f"{public_url} before calling publish_to_instagram()."
    )
    # ig_id = publish_to_instagram(config, public_url, script["caption"])
    # print(f"Published to Instagram: {ig_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["daily"], default="daily")
    parser.add_argument("--publish-directly", action="store_true")
    args = parser.parse_args()

    config = Config.load()
    result = produce_one_short(config)
    route_to_review_or_publish(config, result, publish_directly=args.publish_directly)


if __name__ == "__main__":
    main()
