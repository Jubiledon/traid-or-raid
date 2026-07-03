from cli.arguments import parse_arguments
from simulation.experiment_runner import ExperimentRunner


def main():
    config = parse_arguments()
    runner = ExperimentRunner()
    results = run_experiment(runner, config)
    report_results(runner, results)


def run_experiment(runner, config):
    return runner.run_trials(config)


def report_results(runner, results):
    runner.print_trial_results(results)
    runner.print_summary(results)
    runner.save_summary(results)


if __name__ == "__main__":
    main()