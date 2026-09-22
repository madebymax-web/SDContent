"""Stage 2: turn a Fact into a structured script via the Anthropic API,
using prompts/script_writer_system_prompt.md as the system prompt.

Output shape matches templates/short_script_template.md's JSON example:
{
  "title": ..., "fact_id": ..., "pillar": ..., "target_length_sec": ...,
  "hook": {"vo": ..., "on_screen_text": ..., "visual_cue": ...},
  "body_beats": [{"vo": ..., "on_screen_text": ..., "visual_cue": ...}, ...],
  "payoff": {"vo": ..., "on_screen_text": ..., "visual_cue": ...},
  "cta": "Follow for daily San Diego facts",
  "caption": ..., "hashtags": [...], "source_citation": ...
}
"""
from __future__ import annotations

import json
from pathlib import Path

import anthropic

from pipeline.config import Config, REPO_ROOT
from pipeline.topic_selector import Fact

SYSTEM_PROMPT_PATH = REPO_ROOT / "prompts" / "script_writer_system_prompt.md"
SCRIPT_MODEL = "claude-sonnet-5"  # cost/quality tradeoff: cheaper Haiku-tier model is
                                   # also viable at scale once the prompt is proven out

JSON_SHAPE_INSTRUCTIONS = """
Return ONLY valid JSON (no markdown fences, no commentary) matching this shape:
{
  "title": "string",
  "fact_id": "string",
  "pillar": "string",
  "target_length_sec": int,
  "hook": {"vo": "string", "on_screen_text": "string", "visual_cue": "string"},
  "body_beats": [{"vo": "string", "on_screen_text": "string", "visual_cue": "string"}],
  "payoff": {"vo": "string", "on_screen_text": "string", "visual_cue": "string"},
  "cta": "Follow for daily San Diego facts",
  "caption": "string",
  "hashtags": ["string"],
  "source_citation": "string"
}
"""


def _client(config: Config) -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=config.env("ANTHROPIC_API_KEY"))


def write_script(config: Config, fact: Fact, target_length_sec: int | None = None) -> dict:
    target_length_sec = target_length_sec or config.target_length_sec_shorts
    system_prompt = SYSTEM_PROMPT_PATH.read_text()

    user_payload = {
        "fact_id": fact.id,
        "pillar": fact.pillar,
        "fact": fact.fact,
        "hook_angle": fact.hook_angle,
        "source": fact.source,
        "status": fact.status,
        "sensitivity_flag": fact.sensitivity_flag,
        "notes": fact.notes,
        "target_length_sec": target_length_sec,
    }

    client = _client(config)
    message = client.messages.create(
        model=SCRIPT_MODEL,
        max_tokens=1500,
        system=system_prompt + "\n\n" + JSON_SHAPE_INSTRUCTIONS,
        messages=[{"role": "user", "content": json.dumps(user_payload)}],
    )
    text = message.content[0].text
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Script writer returned non-JSON output, inspect raw response:\n{text}"
        ) from e


def full_vo_text(script: dict) -> str:
    """Concatenate every VO line in order — this is what gets sent to TTS."""
    lines = [script["hook"]["vo"]]
    lines += [beat["vo"] for beat in script["body_beats"]]
    lines.append(script["payoff"]["vo"])
    return " ".join(lines)


if __name__ == "__main__":
    from pipeline.topic_selector import select_next, already_produced_ids

    cfg = Config.load()
    fact = select_next(cfg, exclude_ids=already_produced_ids())
    script = write_script(cfg, fact)
    print(json.dumps(script, indent=2))
