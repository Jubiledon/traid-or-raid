# world/world.py

from dataclasses import dataclass
import numpy as np

from world.spawning import (
    spawn_resources,
    add_agent,
)

from world.percept_builder import build_percept

from world.action_resolver import resolve_action

from world.metrics import (
    collective_efficiency,
    build_summary,
)

from world.logger import save_log


GRID_SIZE = 10


@dataclass
class GridWorld:

    size: int = GRID_SIZE

    def __post_init__(self):

        self.resources = np.zeros(
            (self.size, self.size),
            dtype=np.int8,
        )

        self.agents = []

        self.tick = 0

        self.event_log = []

    # ---------------------------------------------------------
    # occupancy
    # ---------------------------------------------------------

    def cell_occupied(self, x: int, y: int) -> bool:

        return any(
            a.x == x and a.y == y
            for a in self.agents
        )

    # ---------------------------------------------------------
    # setup
    # ---------------------------------------------------------

    def spawn_resources(self, count: int):

        spawn_resources(
            self,
            count,
        )

    def add_agent(self, agent_id: str, personality: str):

        add_agent(
            self,
            agent_id,
            personality,
        )

    # ---------------------------------------------------------
    # perception
    # ---------------------------------------------------------

    def get_percept(self, agent):

        return build_percept(
            self,
            agent,
        )

    # ---------------------------------------------------------
    # actions
    # ---------------------------------------------------------

    def resolve_action(self, agent, action: dict):

        return resolve_action(
            self,
            agent,
            action,
        )

    # ---------------------------------------------------------
    # logging
    # ---------------------------------------------------------

    def save_log(self, path: str):

        save_log(
            self,
            path,
        )

    # ---------------------------------------------------------
    # metrics
    # ---------------------------------------------------------

    def collective_efficiency(self):
        return collective_efficiency(self)

    def summary(self):
        return build_summary(self)
    
    def resources_remaining(self) -> int:
        return int(self.resources.sum())