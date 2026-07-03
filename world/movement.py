# world/movement.py

DIRS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}


def move_agent(world, agent, direction: str) -> str:
    dx, dy = DIRS.get(direction.upper(), (0, 0))

    nx = agent.x + dx
    ny = agent.y + dy

    if (
        0 <= nx < world.size
        and 0 <= ny < world.size
        and not world.cell_occupied(nx, ny)
    ):
        agent.x = nx
        agent.y = ny
        return f"moved_{direction}"

    return "move_blocked"