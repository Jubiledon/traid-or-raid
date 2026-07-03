# simulation/experiment_runner.py

import os
import random
import csv
from statistics import mean
import json
from simulation.simulation_runner import SimulationRunner
from simulation.experiment_config import ExperimentConfig

from world.world import GridWorld

from agents.brains import (
    DummyBrain,
    SimpleBrain,
    LLMBrain,
)

from simulation.conditions import get_personalities

from config import (
    RESOURCE_COUNT,
    PERSONALITIES,
)


class ExperimentRunner:

    def run_trials(self, config: ExperimentConfig) -> list[dict]:

        self._create_log_directory()

        seeds = self._resolve_seeds(config)

        results = []

        for i in range(config.n_trials):

            result = self._run_trial(
                config,
                i,
                seeds[i],
            )

            results.append(result)

            self._save_partial_results(
                config,
                results,
            )

        return results

    def _create_log_directory(self):
        os.makedirs("logs", exist_ok=True)
        os.makedirs("logs/runs", exist_ok=True)
        os.makedirs("logs/runs/simple", exist_ok=True)
        os.makedirs("logs/runs/llm_silent", exist_ok=True)
        os.makedirs("logs/runs/llm_comms", exist_ok=True)
        os.makedirs("logs/runs/llm_comms_mixed", exist_ok=True)
        os.makedirs("logs/runs/llm_comms_coop", exist_ok=True)
        os.makedirs("logs/runs/llm_comms_aggr", exist_ok=True)
        os.makedirs("logs/summaries", exist_ok=True)

    def _resolve_seeds(self, config: ExperimentConfig) -> list:
        if config.seeds:
            print(f"Using provided seeds: {config.seeds}")
            return config.seeds

        return self._default_seeds(config.n_trials)

    def _default_seeds(self, n_trials: int) -> list:

        return list(range(1, n_trials + 1))

    def _run_trial(self, config: ExperimentConfig, trial: int, seed: int) -> dict:

        random.seed(seed)

        world = self._create_world()

        brains = self._populate_world(
            world,
            config,
        )

        result = self._run_simulation(
            world,
            brains,
            config,
            seed,
        )

        return self._add_trial_metadata(
            result,
            config,
            trial,
            seed,
        )

    def _create_world(self) -> GridWorld:
        world = GridWorld()
        world.spawn_resources(RESOURCE_COUNT)
        return world

    def _populate_world(
            self, world: GridWorld, config: ExperimentConfig,
    ) -> dict:

        personalities = get_personalities(config.condition, config.n_agents)

        return {
            self._agent_id(i): self._create_agent(
                world,
                self._agent_id(i),
                personalities[i],
                config,
            )
            for i in range(config.n_agents)
        }

    def _create_agent(
        self,
        world: GridWorld,
        agent_id: str,
        personality: str,
        config: ExperimentConfig,
    ):

        world.add_agent(agent_id, personality)

        return self._make_brain(
            config.agent_type,
            personality,
            config.condition,
        )

    def _agent_id(
        self,
        index: int,
    ) -> str:

        return f"A{index + 1}"

    def _make_brain(
        self,
        agent_type: str,
        personality: str,
        condition: str,
    ):

        if agent_type == "simple":
            return SimpleBrain()

        if agent_type == "dummy":
            return DummyBrain()

        return self._create_llm_brain(
            personality,
            condition,
        )

    def _create_llm_brain(
        self,
        personality: str,
        condition: str,
    ) -> LLMBrain:

        return LLMBrain(
            personality=personality,
            communication_on=self._communication_enabled(
                condition,
            ),
        )

    def _communication_enabled(
        self,
        condition: str,
    ) -> bool:

        return "comms" in condition

    def _run_simulation(
        self,
        world: GridWorld,
        brains: dict,
        config: ExperimentConfig,
        seed: int,
    ) -> dict:

        log_path = self._log_path(config.condition,seed)

        return SimulationRunner(
            world,
            brains,
            config.headless,
            log_path=log_path,
        ).run()

    def _log_path(self, condition: str, seed: int) -> str:
        return f"logs/runs/{condition}/{condition}_seed{seed:03d}.csv"

    def _add_trial_metadata(
        self,
        result: dict,
        config: ExperimentConfig,
        trial: int,
        seed: int,
    ) -> dict:

        result["trial"] = trial + 1
        result["seed"] = seed
        result["condition"] = config.condition

        return result

    def summarise(
        self,
        results: list[dict],
    ) -> dict:

        efficiencies = self._efficiencies(results)

        return {
            "condition": self._condition(results),
            "trials": len(results),
            "mean_efficiency": round(
                mean(efficiencies),
                4,
            ),
            "max_efficiency": round(
                max(efficiencies),
                4,
            ),
            "min_efficiency": round(
                min(efficiencies),
                4,
            ),
        }

    def _efficiencies(
        self,
        results: list[dict],
    ) -> list:

        return [
            r["collective_efficiency"]
            for r in results
        ]

    def _condition(
        self,
        results: list[dict],
    ) -> str:

        return results[0].get(
            "condition",
            "unknown",
        )
    
    def print_trial_results(
        self,
        results: list[dict],
    ):
        for result in results:
            self._print_trial_result(result)

    def _print_trial_result(
        self,
        result: dict,
    ):
        print(
            f"[Trial {result['trial']:02d}] "
            f"seed={result['seed']} | "
            f"efficiency={result['collective_efficiency']:.4f}"
        )

    def _print_summary(
        self,
        summary: dict,
    ):
        print("\n── Experiment Summary ──")

        for key, value in summary.items():
            print(f"{key}: {value}")
        
    def _summary_path(
        self,
        results: list[dict],
    ) -> str:

        condition = results[0]["condition"]
        return f"logs/summaries/{condition}.csv"
    
    def _write_summary_csv(
        self,
        results: list[dict],
        path: str,
    ):
        os.makedirs("logs/summaries", exist_ok=True)

        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    def print_summary(
        self,
        results: list[dict],
    ):
        summary = self.summarise(results)
        self._print_summary(summary)

    def save_summary(
        self,
        results: list[dict],
    ):
        path = self._summary_path(results)
        self._write_summary_csv(results, path)

    def _partial_results_path(
        self,
        config: ExperimentConfig,
    ) -> str:

        return (
            f"logs/summaries/"
            f"{config.condition}_partial.json"
        )
    
    def _save_partial_results(
        self,
        config: ExperimentConfig,
        results: list[dict],
    ):

        path = self._partial_results_path(config)

        with open(path, "w") as f:
            json.dump(results, f, indent=2)