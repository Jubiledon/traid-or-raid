import random

from config import PERSONALITIES


def get_personalities(
    condition: str,
    n_agents: int,
) -> list:

    if condition == "llm_comms_mixed":
        return mixed_personalities(n_agents)

    if condition == "llm_comms_coop":
        return uniform_personalities(
            "cooperative",
            n_agents,
        )

    if condition == "llm_comms_aggr":
        return uniform_personalities(
            "aggressive",
            n_agents,
        )

    return random_personalities(n_agents)


def mixed_personalities(
    n_agents: int,
) -> list:

    base = [
        "cooperative",
        "aggressive",
        "deceptive",
        "neutral",
    ]

    return [
        base[i % len(base)]
        for i in range(n_agents)
    ]


def uniform_personalities(
    personality: str,
    n_agents: int,
) -> list:

    return [personality] * n_agents


def random_personalities(
    n_agents: int,
) -> list:

    return [
        random.choice(PERSONALITIES)
        for _ in range(n_agents)
    ]