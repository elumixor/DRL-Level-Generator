import inspect
import os
import time
from pathlib import Path

import numpy as np
import wandb

from common import read_yaml
from .context import Context


def extend_dict(parent, child):
    if not isinstance(parent, dict) or not isinstance(child, dict):
        return child

    for key, value in child.items():
        if key not in parent:
            parent[key] = value
        else:
            # override and extend
            previous = parent[key]
            parent[key] = extend_dict(previous, value)

    return parent


def get_runs(username, project, name=None):
    api = wandb.Api()

    if name is not None:
        runs = api.runs(f"{username}/{project}", filters={f"config.name": name})
    else:
        runs = api.runs(f"{username}/{project}")

    return list(runs)


def run_experiment(main, config, path, config_name, **args_overrides):
    # Collect all configs, with inherited
    configs = [config]
    current_path = os.path.dirname(path)
    while "inherits" in configs[-1]:
        inherit_path = configs[-1]["inherits"]
        if os.path.isabs(inherit_path):
            current_path = inherit_path
        else:
            current_path = (Path(current_path) / os.path.dirname(inherit_path)).resolve()

        configs.append(read_yaml(f"{current_path}/{config_name}", dot_dict=False))

    # Override entries
    config = dict()
    for c in reversed(configs):
        config = extend_dict(config, c)

    iterate_on = []

    # Context is an object to manage the experiments
    arg_names = list(inspect.signature(main).parameters)[1:]

    args = [args_overrides[arg_name] if arg_name in args_overrides else config["arguments"][arg_name]
            for arg_name in arg_names]

    for arg_index, arg in enumerate(args):
        if isinstance(arg, dict):
            if "linspace" in arg:
                ls = arg["linspace"]
                iterate_on.append((arg_index, np.linspace(ls["min"], ls["max"], ls["n"])))
                continue

            continue

        elif isinstance(arg, list):
            iterate_on.append((arg_index, arg))
            continue

    if config["log"] == "wandb" and ("append" not in config or not config["append"]):
        runs = get_runs(config['username'], config['project'], config["name"])

        if len(runs) > 0:
            print(f"Removing previous runs ({len(runs)})")

        for run in runs:
            run.delete()

    experiments_configurations = []

    def collect_configurations(iterables, selected):
        if len(iterables) == 0:
            for arg_index, value in selected:
                args[arg_index] = value

            experiments_configurations.append({
                "project": config["project"],
                "name": config["name"],
                "display_name": config["display_name"],
                "log": config["log"] if "log" in config else "none",
                "args": args[:],
            })

            return

        current, *remaining = iterables
        arg_index, values = current

        for value in values:
            collect_configurations(remaining, selected + [(arg_index, value)])

    collect_configurations(iterate_on, [])

    elapsed = 0

    for i, config in enumerate(experiments_configurations):
        args = config["args"]

        start = time.time()

        with Context(project=config["project"],
                     name=config["name"],
                     display_name=config["display_name"],
                     log=config["log"],
                     arguments={name: value for name, value in zip(arg_names, args)},
                     current=i,
                     total=len(experiments_configurations),
                     elapsed=elapsed) as context:
            main(context, *args)

        elapsed += time.time() - start
