# agents/agent.py

from dataclasses import dataclass


@dataclass
class Agent:

    agent_id: str
    personality: str

    x: int
    y: int

    inventory: int = 0

    last_message: str = ""

    last_action: str = ""

    def manhattan_distance(self, other: "Agent") -> int:

        return (
            abs(self.x - other.x)
            + abs(self.y - other.y)
        )