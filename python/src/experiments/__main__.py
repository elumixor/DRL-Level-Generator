import argparse

from .commands import find_all_experiments, list_found, delete_all_runs, delete_runs_by_name, run_one
from .utils import prompt

if __name__ == '__main__':
    # ./experiment <experiment-name>                (simply run selected experiment)
    #                                 --append      (not to delete previous runs)
    #                                 --console     (force output to console)
    #                                 --wandb       (force output to wandb)
    #                                 --silent      (force no output)
    #                                 --show-config (force no output)
    #
    # ./experiment --list (list all experiments)
    #              --help (display help message)
    #              --all  (run all experiments)
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment", nargs="?", help="Id of the experiment to run", type=str)

    # arguments for empty query
    parser.add_argument("--list", help="List all experiments", action="store_true")
    parser.add_argument("--directory", help="Base directory for the runs. Defaults to \"experiments\"",
                        default="experiments", type=str, metavar="")
    parser.add_argument("--delete", help="Deletes runs with this name", type=str, metavar="")
    parser.add_argument("--all", help="Runs all experiments", action="store_true")

    # arguments for query with a run
    parser.add_argument("--append", help="Keeps the previous runs for this experiment", action="store_true")
    parser.add_argument("--wandb", help="Force output to wandb", action="store_true")
    parser.add_argument("--console", help="Force output to console", action="store_true")
    parser.add_argument("--silent", help="Force no output", action="store_true")
    parser.add_argument("--show-config", help="Shows a config for experiment", action="store_true")

    args = parser.parse_args()

    # Find all experiments
    all_experiments = {name: path for name, path in find_all_experiments(f"../{args.directory}")}

    # List all found experiments (searches for config files)
    if args.list:
        list_found(all_experiments)
        exit()

    # Delete experiment(-s)
    if args.delete is not None:
        if args.delete == "all":
            delete_all_runs()
            exit()

        delete_runs_by_name(args.delete)
        exit()

    # Run all experiments
    if args.all:
        if not prompt(f"Run all experiments ({len(all_experiments)})? ([y]|n)"):
            exit()

        for experiment_name, config_path in all_experiments.items():
            run_one(experiment_name, config_path, args)

        exit()

    # If the experiment name is specified
    experiment_name = args.experiment
    if experiment_name is not None:
        experiment_config_location = all_experiments[experiment_name]

        if args.show_config:
            with open(experiment_config_location) as file:
                print(file.read())

            exit()

        run_one(experiment_name, experiment_config_location, args)
        exit()
