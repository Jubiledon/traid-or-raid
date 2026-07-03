# world/resource_manager.py

def collect_resource(world, agent) -> str:

    if world.resources[agent.x, agent.y] == 1:
        world.resources[agent.x, agent.y] = 0
        agent.inventory += 1

        return "collected"

    return "nothing_to_collect"