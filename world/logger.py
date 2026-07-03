# world/logger.py

import csv


def log_event(world, agent, action: dict, result: str):
    world.event_log.append({
        "tick": world.tick,
        "agent_id": agent.agent_id,
        "personality": agent.personality,
        "position": (agent.x, agent.y),
        "inventory": agent.inventory,
        "action_type": action.get("type"),
        "action_detail": str(action),
        "result": result,
        "message": action.get("message", agent.last_message),
        "resources_remaining": int(world.resources.sum()),
    })
    printEventLog(world, agent, action, result)

def printEventLog(world, agent, action: dict, result: str):
    print(
    f"[T{world.tick:03d}] {agent.agent_id} ({agent.personality[:4]}) "
    f"| {action.get('type'):10s} | {result:30s} "
    f"| inv={agent.inventory} | res={int(world.resources.sum())}"
    f"| msg='{agent.last_message}'"
    )


def save_log(world, path: str):

    if not world.event_log:
        return

    keys = world.event_log[0].keys()

    with open(path, "w", newline="") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=keys,
        )

        writer.writeheader()
        writer.writerows(world.event_log)

    print(f"Log saved to {path}")