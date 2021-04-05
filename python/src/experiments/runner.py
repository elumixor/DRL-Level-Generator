import gc
import inspect
import multiprocessing
import os
import shutil
from importlib.util import spec_from_file_location, module_from_spec
from multiprocessing.pool import ThreadPool
from pathlib import Path
from threading import Thread

import torch
import wandb

from common import read_yaml, DotDict
from common.dot_dict import from_dot_dict, to_dot_dict
from .context import Context


def extend_dict(parent, child):
    if not isinstance(parent, DotDict) or not isinstance(child, DotDict):
        return child

    for key, value in child.items():
        if key not in parent:
            parent[key] = value
        else:
            # override and extend
            previous = parent[key]
            parent[key] = extend_dict(previous, value)

    return parent


def unwrap(args):
    if isinstance(args, DotDict):
        if "linspace" in args:
            linspace = args.linspace

            _min = linspace.min if "min" in linspace else 0
            n = linspace.n
            _max = linspace.max if "max" in linspace else (n - 1)

            values = torch.linspace(_min, _max, n).unsqueeze(1)
            return list(values)

        elif "random" in args:
            random = args.random
            _min, _max, repeat = random.min, random.max, random.repeat
            shape = [1] if "shape" not in random else random.shape
            return [torch.rand(shape) * (_max - _min) + _min for _ in range(repeat)]

        elif "random" in args:
            random = args.random
            _min, _max, repeat = random.min, random.max, random.repeat
            shape = [1] if "shape" not in random else random.shape
            return [torch.rand(shape) * (_max - _min) + _min for _ in range(repeat)]

        else:
            for name, value in args.items():
                args[name] = unwrap(value)

            return args

    elif isinstance(args, list):
        result = []
        for item in args:
            if isinstance(item, DotDict) and ("linspace" in item or "random" in item):
                result += unwrap(item)
            else:
                result.append(unwrap(item))
        return result

    return args


def sample_randoms(entry):
    if not isinstance(entry, DotDict) or "random" not in entry:
        return entry

    parameters = entry.random
    shape = parameters.shape
    r_min = parameters.min
    r_max = parameters.max

    return torch.rand(shape) * (r_max - r_min) + r_min


def get_runs(username, project, name=None):
    api = wandb.Api()

    if name is not None:
        runs = api.runs(f"{username}/{project}", filters={f"config.name": name})
    else:
        runs = api.runs(f"{username}/{project}")

    return list(runs)


def execute_run(i, config, arg_names, total_len, main_name, path):
    spec = spec_from_file_location("module.name", path)
    foo = module_from_spec(spec)
    spec.loader.exec_module(foo)
    main = foo.__getattribute__(main_name)

    config = to_dot_dict(config)
    args = config.args

    with Context(project=config.project,
                 name=config.name,
                 display_name=config.display_name,
                 log=config.log,
                 arguments={name: value for name, value in zip(arg_names, args)},
                 current=i,
                 total=total_len,
                 elapsed=0) as context:
        main(context, *args)


def run_experiment(main_name, config, path, config_name, parallel=True, **args_overrides):
    spec = spec_from_file_location("module.name", path)
    foo = module_from_spec(spec)
    spec.loader.exec_module(foo)
    main = foo.__getattribute__(main_name)

    # Collect all configs, with inherited
    configs = [config]
    current_path = os.path.dirname(path)
    while "inherits" in configs[-1]:
        inherit_path = configs[-1].inherits
        if os.path.isabs(inherit_path):
            current_path = inherit_path
        else:
            current_path = (Path(current_path) / os.path.dirname(inherit_path)).resolve()

        configs.append(read_yaml(f"{current_path}/{config_name}"))

    # Override entries
    config = DotDict()
    for c in reversed(configs):
        config = extend_dict(config, c)

    # Get the argument names and indices of the function
    arg_names = list(inspect.signature(main).parameters)[1:]

    # Override args from run_current()
    args = [args_overrides[arg_name] if arg_name in args_overrides else config.arguments[arg_name]
            for arg_name in arg_names]

    # Unwrap linspaces, randoms
    args = unwrap(args)

    iterate_on = []
    for arg_index, arg in enumerate(args):
        if isinstance(arg, list):
            iterate_on.append((arg_index, arg))
            continue

    def remove_runs():
        if config.log == "wandb" and ("append" not in config or not config.append):
            runs = get_runs(config.username, config.project, config.name)

            if len(runs) > 0:
                print(f"Removing previous runs ({len(runs)})")

            for run in runs:
                run.delete()

    remove_thread = Thread(target=remove_runs)
    remove_thread.start()

    skip = config.skip if "skip" in config else DotDict()

    experiments_configurations = []

    def collect_configurations(iterables, selected):
        if len(iterables) == 0:
            selected_dict = {arg_names[i]: value for i, value in selected}

            # skip if `skip` contains the pair of items in current config
            do_skip = False
            for s in skip:
                found_names = []
                for name, value in s.items():
                    if name in selected_dict:
                        if selected_dict[name] != value:
                            break
                        else:
                            found_names.append(name)

                if len(found_names) == len(s):
                    do_skip = True
                    break

            if do_skip:
                return

            for arg_index, value in selected:
                args[arg_index] = value

            experiments_configurations.append(DotDict(
                project=config.project,
                name=config.name,
                display_name=config.display_name,
                log=config.log if "log" in config else "none",
                repeat=config.repeat if "repeat" in config else 1,
                args=args[:],
            ))

            return

        current, *remaining = iterables
        arg_index, values = current

        for value in values:
            collect_configurations(remaining, selected + [(arg_index, value)])

    collect_configurations(iterate_on, [])

    elapsed = 0

    # for multiprocessing we must convert DotDicts back into dict,
    # as the __getitem__ and stuff will be used
    experiments_configurations = from_dot_dict(experiments_configurations)
    total = len(experiments_configurations)

    if parallel:
        gc.collect()
        with MyPool(20) as pool:
            pool.starmap(execute_run, [(i, config, arg_names, total, main_name, path)
                                       for i, config in enumerate(experiments_configurations)])
    else:
        for i, config in enumerate(experiments_configurations):
            execute_run(i, config, arg_names, total, main_name, path)

    # remove local wandb folder
    path_to_wandb = os.path.join(os.path.dirname(path), "wandb")
    if os.path.exists(path_to_wandb) and os.path.isdir(path_to_wandb):
        shutil.rmtree(path_to_wandb)

    remove_thread.join()


class NoDaemonProcess(multiprocessing.Process):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    def __init__(self, *args, **kwargs):
        kwargs['context'] = NoDaemonContext()
        super(MyPool, self).__init__(*args, **kwargs)
