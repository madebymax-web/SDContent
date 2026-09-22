"""Stage 4: source real photos/video clips matching each beat's visual_cue.

Default provider: Pexels (free API, good coverage of US city/coastal
imagery). Falls back to Pixabay if Pexels has no good match. Per docs/04's
core architecture decision, this stage sources REAL footage/photos —
AI-generated visuals are an explicit, sparingly-used exception handled
outside this module (flagged for manual/Higgsfield sourcing, never silently
substituted here).
"""
from __future__ import annotations

from pathlib import Path

import requests

from pipeline.config import Config, CACHE_DIR

PEXELS_PHOTO_SEARCH_URL = "https://api.pexels.com/v1/search"
PEXELS_VIDEO_SEARCH_URL = "https://api.pexels.com/videos/search"
PIXABAY_URL = "https://pixabay.com/api/"


def _search_pexels_photos(config: Config, query: str, per_page: int = 5) -> list[dict]:
    resp = requests.get(
        PEXELS_PHOTO_SEARCH_URL,
        headers={"Authorization": config.env("PEXELS_API_KEY")},
        params={"query": query, "per_page": per_page, "orientation": "portrait"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("photos", [])


def _search_pexels_videos(config: Config, query: str, per_page: int = 5) -> list[dict]:
    resp = requests.get(
        PEXELS_VIDEO_SEARCH_URL,
        headers={"Authorization": config.env("PEXELS_API_KEY")},
        params={"query": query, "per_page": per_page, "orientation": "portrait"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("videos", [])


def build_query(visual_cue: str, region_bias: str) -> str:
    """Bias every search toward San Diego/the described subject — stock
    libraries have limited San Diego-specific tagging, so cue text usually
    needs to degrade gracefully to a generic-but-relevant search (e.g. a
    specific unnamed canyon bridge -> "suspension bridge canyon").
    """
    cue = visual_cue.strip()
    if "san diego" in cue.lower() or any(
        landmark in cue.lower()
        for landmark in ["coronado", "la jolla", "balboa park", "gaslamp", "torrey pines"]
    ):
        return cue
    return f"{cue} {region_bias}"


def source_visual_for_cue(config: Config, visual_cue: str, job_dir: Path, index: int) -> Path | None:
    """Downloads the best-match asset for one visual_cue. Returns None (and
    the caller should flag the beat for manual review) if nothing usable is
    found — never silently substitutes an unrelated image, since a
    mismatched visual undercuts the fact being told (QC checklist in docs/08
    checks for this explicitly).
    """
    query = build_query(visual_cue, config.raw["visuals"]["search_region_bias"])
    videos = _search_pexels_videos(config, query, per_page=3)

    job_dir.mkdir(parents=True, exist_ok=True)
    if videos:
        # Prefer the HD portrait file if available, else the first file listed.
        video_files = videos[0]["video_files"]
        hd = next((v for v in video_files if v.get("quality") == "hd"), video_files[0])
        out_path = job_dir / f"visual_{index}.mp4"
        _download(hd["link"], out_path)
        return out_path

    photos = _search_pexels_photos(config, query, per_page=3)
    if photos:
        out_path = job_dir / f"visual_{index}.jpg"
        _download(photos[0]["src"]["large2x"], out_path)
        return out_path

    return None


def _download(url: str, out_path: Path) -> None:
    resp = requests.get(url, timeout=60, stream=True)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def source_all_visuals(config: Config, script: dict, job_dir: Path) -> dict:
    """Returns {beat_key: Path|None} for hook, each body beat, and payoff.
    Any None entries must be resolved (manual stock pick, or a sparing,
    clearly-illustrated AI fallback per docs/04) before assembly proceeds —
    orchestrator.py enforces this as a gate.
    """
    result = {}
    result["hook"] = source_visual_for_cue(config, script["hook"]["visual_cue"], job_dir, 0)
    for i, beat in enumerate(script["body_beats"]):
        result[f"body_beat_{i}"] = source_visual_for_cue(config, beat["visual_cue"], job_dir, i + 1)
    result["payoff"] = source_visual_for_cue(
        config, script["payoff"]["visual_cue"], job_dir, len(script["body_beats"]) + 1
    )
    return result


if __name__ == "__main__":
    import json
    import sys

    cfg = Config.load()
    script = json.loads(Path(sys.argv[1]).read_text())
    job_dir = CACHE_DIR / f"fact_{script['fact_id']}"
    visuals = source_all_visuals(cfg, script, job_dir)
    missing = [k for k, v in visuals.items() if v is None]
    print(visuals)
    if missing:
        print(f"MISSING VISUALS for beats: {missing} — flag for manual sourcing per docs/04")
