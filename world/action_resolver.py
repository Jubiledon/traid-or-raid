# world/action_resolver.py

from world.movement import move_agent
from world.resource_manager import collect_resource
from world.raid_resolver import resolve_raid
from world.logger import log_event


def resolve_action(world, agent, action: dict) -> str:

    action_type = action.get("type", "wait")

    result = "wait"

    if action_type == "move":

        result = move_agent(
            world,
            agent,
            action.get("direction", "N"),
        )

    elif action_type == "collect":

        result = collect_resource(
            world,
            agent,
        )

    elif action_type == "raid":

        result = resolve_raid(
            world,
            agent,
            action.get("target_id", ""),
        )

    elif action_type == "broadcast":

        agent.last_message = action.get("message", "")[:150]
        result = "broadcast"

    elif action_type == "wait":

        result = "wait"

    agent.last_action = result

    log_event(
        world,
        agent,
        action,
        result,
    )

    return result