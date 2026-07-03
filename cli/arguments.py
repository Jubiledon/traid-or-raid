# cli/arguments.py

import argparse
from simulation.experiment_config import ExperimentConfig

def parse_arguments() -> ExperimentConfig:
    parser = argparse.ArgumentParser()

    _add_trial_argument(parser)
    _add_agent_argument(parser)
    _add_headless_argument(parser)
    _add_agent_type_argument(parser)
    _add_condition_argument(parser)

    args = parser.parse_args()

    return ExperimentConfig(
        n_trials=args.trials,
        n_agents=args.agents,
        headless=args.headless,
        agent_type=args.agent_type,
        condition=args.condition,
        seeds=list(range(1, args.trials + 1)),
    )

def _add_trial_argument(parser):
    parser.add_argument(
        "--trials", "-t",
        type=int,
        default=1,
    )

def _add_agent_argument(parser):
    parser.add_argument(
        "--agents", "-a",
        type=int,
        default=4,
    )

def _add_headless_argument(parser):
    parser.add_argument(
        "--headless", "-H",
        action="store_true",
    )

def _add_agent_type_argument(parser):
    # simple, silent, llm, mixed
    parser.add_argument(
        "--agent_type", "-T",
        type=str,
        default="simple",
    )

def _add_condition_argument(parser):
    parser.add_argument(
        "--condition", "-c",
        type=str,
        default="default",
    )