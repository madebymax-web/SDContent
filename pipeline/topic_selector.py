"""Stage 1: pick the next fact to produce.

Reads data/facts_database.csv, filters to status in {verified} (researching
rows are NOT eligible — see docs/05's hard verification gate), and picks one
per pillar-weighted random selection, favoring facts that haven't been used
yet and pillars that are under-represented in recent publish history.
"""
from __future__ import annotations

import csv
import random
from dataclasses import dataclass

from pipeline.config import Config, FACTS_DB_PATH

ELIGIBLE_STATUSES = {"verified"}


@dataclass
class Fact:
    id: str
    pillar: str
    fact: str
    hook_angle: str
    source: str
    status: str
    sensitivity_flag: str
    notes: str


def load_facts() -> list[Fact]:
    with open(FACTS_DB_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Fact(**row) for row in reader]


def eligible_facts(facts: list[Fact], exclude_ids: set[str] | None = None) -> list[Fact]:
    exclude_ids = exclude_ids or set()
    return [
        f for f in facts
        if f.status in ELIGIBLE_STATUSES and f.id not in exclude_ids
    ]


def select_next(config: Config, exclude_ids: set[str] | None = None) -> Fact:
    """Weighted-random pick across eligible facts, weighted by the pillar's
    configured weight. Raises if the eligible queue is empty — that's a
    signal to run the topic researcher prompt and top up the database
    (see docs/08 weekly SOP: keep 2-3 weeks of verified facts buffered).
    """
    facts = eligible_facts(load_facts(), exclude_ids)
    if not facts:
        raise RuntimeError(
            "No eligible (status=verified) facts left to produce. "
            "Run the topic researcher + verification prompts to top up "
            "data/facts_database.csv — see docs/05 and docs/08."
        )
    weights = config.pillar_weights
    scored = [(f, weights.get(f.pillar, 1.0)) for f in facts]
    chosen = random.choices(
        population=[f for f, _ in scored],
        weights=[w for _, w in scored],
        k=1,
    )[0]
    return chosen


def already_produced_ids() -> set[str]:
    """Facts with status in {scripted, produced, published} should not be
    re-selected. In this CSV-backed MVP that's just reading the status
    column directly; once the review queue moves to Notion (docs/09 Phase 2)
    this can instead query the Notion database.
    """
    return {f.id for f in load_facts() if f.status not in ELIGIBLE_STATUSES and f.status != "researching"}


if __name__ == "__main__":
    cfg = Config.load()
    fact = select_next(cfg, exclude_ids=already_produced_ids())
    print(f"Selected fact #{fact.id} [{fact.pillar}]: {fact.fact}")
