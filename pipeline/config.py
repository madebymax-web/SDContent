"""Loads channel_config.yaml + .env into a single Config object used by every
pipeline stage. Centralizing this means every module reads settings the same
way instead of re-parsing YAML/env everywhere.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config" / "channel_config.yaml"
FACTS_DB_PATH = REPO_ROOT / "data" / "facts_database.csv"
REVIEW_QUEUE_DIR = REPO_ROOT / "data" / "review_queue"
CACHE_DIR = REPO_ROOT / "assets" / "cache"


@dataclass
class Config:
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls) -> "Config":
        load_dotenv(REPO_ROOT / ".env")
        with open(CONFIG_PATH, "r") as f:
            raw = yaml.safe_load(f)
        return cls(raw=raw)

    # --- convenience accessors -------------------------------------------------
    @property
    def review_required(self) -> bool:
        return bool(self.raw["automation"]["review_required"])

    @property
    def pillar_weights(self) -> dict[str, float]:
        return dict(self.raw["pillars"])

    @property
    def voice_provider(self) -> str:
        return os.getenv("TTS_PROVIDER", self.raw["voice"]["provider"])

    @property
    def voice_id(self) -> str:
        vid = os.getenv("ELEVENLABS_VOICE_ID") or self.raw["voice"]["voice_id"]
        if not vid:
            raise RuntimeError(
                "No voice_id set. Fill config/channel_config.yaml voice.voice_id "
                "or ELEVENLABS_VOICE_ID in .env — see docs/09 Phase 0 setup."
            )
        return vid

    @property
    def target_length_sec_shorts(self) -> int:
        return int(self.raw["script"]["target_length_sec_shorts"])

    @property
    def watermark_path(self) -> Path:
        return REPO_ROOT / self.raw["branding"]["watermark_path"]

    def env(self, key: str, required: bool = True) -> str:
        val = os.getenv(key)
        if required and not val:
            raise RuntimeError(f"Missing required environment variable: {key} "
                                f"(see .env.example)")
        return val or ""
