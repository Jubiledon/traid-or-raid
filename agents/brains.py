# agents/brains.py

import random

from agents.llm_client import GemmaClient, AnthropicClient
from agents.percept_filter import PerceptFilter
from agents.prompt_builder import PromptBuilder
from agents.response_parser import ResponseParser


class DummyBrain:

    def decide(self, percept: dict) -> dict:
        return random.choice([
            {"type": "collect"},
            {"type": "wait"},
            self._move(),
        ])

    def _move(self):
        return {
            "type": "move",
            "direction": random.choice(["N", "S", "E", "W"]),
        }


class SimpleBrain:
    """
    Rule-based greedy agent. No LLM, no communication.

    Priority order each tick:
      1. Collect resource on current cell.
      2. Move toward nearest visible resource.
      3. Raid adjacent agent with strictly more inventory.
      4. Move in a random direction (exploration fallback).

    This agent is the experimental baseline. Its behaviour is fully
    deterministic given the same percept, so it has no personality.
    """

    def __init__(self, personality=None):
        self.personality = personality  # unused, but included for interface consistency with LLMBrain

    def decide(self, percept: dict) -> dict:
        pos        = percept["position"]          # (x, y)
        inventory  = percept["inventory"]
        resources  = percept["nearby_resources"]  # list of (x, y)
        agents     = percept["nearby_agents"]     # list of dicts

        px, py = pos

        # ── 1. collect if standing on a resource ─────────────────────────
        if (px, py) in resources:
            return {"type": "collect"}

        # ── 2. move toward nearest visible resource ───────────────────────
        if resources:
            nearest = min(resources, key=lambda r: _manhattan(px, py, r[0], r[1]))
            return {"type": "move", "direction": _direction_toward(px, py, *nearest)}

        # ── 3. raid adjacent agent with strictly more inventory ───────────
        adjacent_richer = [
            a for a in agents
            if a["distance"] == 1 and a["inventory"] > inventory
        ]
        if adjacent_richer:
            # target the richest adjacent agent
            target = max(adjacent_richer, key=lambda a: a["inventory"])
            return {"type": "raid", "target_id": target["id"]}

        # ── 4. random exploration fallback ────────────────────────────────
        return {"type": "move", "direction": random.choice(["N", "S", "E", "W"])}

class LLMBrain:

    def __init__(
        self,
        personality: str,
        communication_on: bool = True,
        model_path: str = "./google/gemma-3-1b-it-local",
        temperature: float = 0.7,
    ):

        self.personality = personality
        self.communication_on = communication_on

        self.client = AnthropicClient(
            model_path=model_path,
            temperature=temperature,
        )

        self.prompt_builder = PromptBuilder()
        self.response_parser = ResponseParser()

    def decide(self, percept: dict) -> dict:
        percept = self._filter_percept(percept)

        prompt = self._build_prompt(percept)
        raw = self.client.generate(prompt)

        return self._parse(raw, percept)

    def _filter_percept(self, percept: dict) -> dict:
        if self.communication_on:
            return percept

        return PerceptFilter.silence(percept)

    def _build_prompt(self, percept: dict) -> str:
        return self.prompt_builder.build(
            percept,
            self.communication_on,
            self.personality,
        )

    def _parse(
        self,
        raw: str,
        percept: dict,
    ) -> dict:

        return self.response_parser.parse(
            raw,
            percept,
            self.communication_on,
        )
    
# ── helpers ──────────────────────────────────────────────────────────────────

def _manhattan(x1, y1, x2, y2) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def _direction_toward(fx, fy, tx, ty) -> str:
    """Return the cardinal direction (N/S/E/W) that moves (fx,fy) closest to (tx,ty)."""
    dx = tx - fx
    dy = ty - fy
    if abs(dx) >= abs(dy):
        return "E" if dx > 0 else "W"
    else:
        return "S" if dy > 0 else "N"