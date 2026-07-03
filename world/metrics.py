# world/metrics.py

RESOURCE_COUNT = 30


def collective_efficiency(world) -> float:

    total = sum(agent.inventory for agent in world.agents)

    return total / max(1, RESOURCE_COUNT)


def build_summary(world) -> dict:

    return {
        "ticks": world.tick,
        "collective_efficiency": collective_efficiency(world),
        "agent_scores": {
            agent.agent_id: agent.inventory
            for agent in world.agents
        },
        "resources_remaining": int(world.resources.sum()),
    }