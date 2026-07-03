# world/percept_builder.py

def build_percept(world, agent) -> dict:

    nearby_resources = []

    for dx in range(-2, 3):
        for dy in range(-2, 3):

            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < world.size and 0 <= ny < world.size:

                if world.resources[nx, ny] == 1:
                    nearby_resources.append((nx, ny))

    nearby_agents = []

    for other in world.agents:

        if other.agent_id == agent.agent_id:
            continue

        distance = agent.manhattan_distance(other)

        if distance <= 3:

            nearby_agents.append({
                "id": other.agent_id,
                "personality_hint": other.personality,
                "distance": distance,
                "inventory": other.inventory,
                "last_message": other.last_message,
            })

    return {
        "agent_id": agent.agent_id,
        "personality": agent.personality,
        "position": (agent.x, agent.y),
        "inventory": agent.inventory,
        "nearby_resources": nearby_resources,
        "nearby_agents": nearby_agents,
        "tick": world.tick,
        "resources_remaining": int(world.resources.sum()),
    }