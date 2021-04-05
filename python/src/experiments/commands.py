import os
from pathlib import Path

from common import read_yaml
from .runner import run_experiment, get_runs
from .utils import prompt


def find_all_experiments(directory):
    for path in [str(path) for path in Path(directory).rglob('*.yaml') if "wandb\\" not in str(path)]:
        config = read_yaml(path)
        name = config.name
        if name is not None:
            yield name, path


def list_found(experiments):
    print(f"Found {len(experiments)} experiments")

    max_length = max([len(name) for name, *_ in experiments.items()])

    for name, path in experiments.items():
        print("{name:>{length}}".format(name=name, length=max_length) + f" : {path}")


def delete_runs(runs):
    if len(runs) < 1:
        print("No runs to delete")
        return

    if prompt(f"Delete {len(runs)} runs? (y|[n])"):
        for run in runs:
            run.delete()


def delete_all_runs():
    defaults = read_yaml("defaults.yaml")
    username, project = defaults.username, defaults.project
    runs = get_runs(username, project)

    if len(runs) == 0:
        print(f"No runs found for the project \"{username}/{project}\"")
        return

    delete_runs(runs)


def delete_runs_by_name(name):
    defaults = read_yaml("defaults.yaml")
    username, project = defaults.username, defaults.project
    runs = get_runs(username, project, name)

    if len(runs) == 0:
        print(f"No runs with name \"{name}\" found for the project \"{username}/{project}\"")
        return

    delete_runs(runs)


def run_one(config_location, args):
    if args.console is None:
        args.console = False

    if args.wandb is None:
        args.wandb = False

    if args.silent is None:
        args.silent = False

    if args.parallel is None:
        args.parallel = True

    if args.console + args.wandb + args.silent > 1:
        raise ValueError("Only one of --[console|wandb|silent] can be specified")

    # Default values for configs
    defaults = read_yaml("defaults.yaml")

    # Read config
    config = read_yaml(config_location)
    experiment_name = config.name

    experiment_file = config.file if "file" in config else defaults.file
    main_name = config.main if "main" in config else defaults.main

    if "username" not in config:
        config.username = defaults.username

    if "project" not in config:
        config.project = defaults.project

    experiment_path = os.path.join(Path(os.path.dirname(config_location)).resolve(), experiment_file)

    # Override stuff in config based on command line arguments
    if args.console:
        config.log = "console"
    elif args.wandb:
        config.log = "wandb"
    elif args.silent:
        config.log = "none"

    if args.append:
        config.append = True

    if "display_name" not in config:
        config.display_name = experiment_name.replace("_", " ").capitalize()

    args_overrides = args.args if "args" in args else dict()

    run_experiment(main_name, config, experiment_path, defaults.config, parallel=args.parallel, **args_overrides)
