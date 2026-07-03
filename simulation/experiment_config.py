from dataclasses import dataclass

@dataclass
class ExperimentConfig:
    n_trials: int = 1
    n_agents: int = 4
    headless: bool = True
    agent_type: str = "simple"
    condition: str = "default"
    seeds: list | None = None