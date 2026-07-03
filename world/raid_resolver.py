# world/raid_resolver.py

import random

RAID_RANGE = 1


def resolve_raid(world, attacker, target_id: str) -> str:

    target = next(
        (a for a in world.agents if a.agent_id == target_id),
        None,
    )

    if target is None:
        return "raid_no_target"

    if attacker.manhattan_distance(target) > RAID_RANGE:
        return "raid_out_of_range"

    if target.inventory == 0:
        return "raid_empty"

    stolen = random.randint(
        1,
        max(1, target.inventory // 2),
    )

    stolen = min(stolen, target.inventory)

    target.inventory -= stolen
    attacker.inventory += stolen

    return f"raided_{target_id}_stole_{stolen}"