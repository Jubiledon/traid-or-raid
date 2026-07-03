# world/spawning.py

import random
from agents.agent import Agent


def spawn_resources(world, count: int):

    world.resources[:] = 0

    placed = 0

    while placed < count:

        x = random.randint(0, world.size - 1)
        y = random.randint(0, world.size - 1)

        if world.resources[x, y] == 0:
            world.resources[x, y] = 1
            placed += 1


def add_agent(world, agent_id: str, personality: str):

    while True:

        x = random.randint(0, world.size - 1)
        y = random.randint(0, world.size - 1)

        if not world.cell_occupied(x, y):

            world.agents.append(
                Agent(
                    agent_id=agent_id,
                    personality=personality,
                    x=x,
                    y=y,
                )
            )

            break