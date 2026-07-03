# simulation/turn_manager.py

import random


def run_turn(world, brains, display=None):

    world.tick += 1

    random.shuffle(world.agents)

    for agent in world.agents:
        agent.last_message = ""
        percept = world.get_percept(agent)

        action = brains[agent.agent_id].decide(percept)

        world.resolve_action(
            agent,
            action,
        )

        if (
            display
            and action.get("type") == "broadcast"
        ):
            display.push_message(
                agent.agent_id,
                action.get("message", ""),
            )