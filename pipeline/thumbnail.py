"""Stage 8 (long-form only): composite hook text over a selected frame/photo
for the YouTube thumbnail, per the thumbnail style guide in docs/03.

MVP implementation uses Pillow directly. Adobe Express (already connected in
this workspace via the Adobe for Creativity MCP server) is a strong upgrade
path for a more polished, templated thumbnail system — see docs/09 Phase 0.
This module stays framework-agnostic so swapping in an Adobe Express
template-fill call later doesn't require touching the rest of the pipeline.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from pipeline.config import Config

THUMB_SIZE = (1280, 720)


def build_thumbnail(config: Config, base_image_path: Path, hook_text: str, out_path: Path) -> Path:
    img = Image.open(base_image_path).convert("RGB")
    img = img.resize(THUMB_SIZE)

    # Darken bottom third for text legibility.
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle(
        [(0, THUMB_SIZE[1] - 260), (THUMB_SIZE[0], THUMB_SIZE[1])],
        fill=(0, 0, 0, 140),
    )
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)
    font_path = config.raw["branding"].get("font_headline") or None
    try:
        font = ImageFont.truetype(font_path, 84) if font_path else ImageFont.load_default()
    except OSError:
        font = ImageFont.load_default()

    draw.text((48, THUMB_SIZE[1] - 200), hook_text, font=font, fill="#FFFFFF")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=95)
    return out_path


if __name__ == "__main__":
    print("Import build_thumbnail() from pipeline.orchestrator for long-form runs.")
