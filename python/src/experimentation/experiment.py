import functools
from inspect import signature
from typing import Optional, List, Dict

from experimentation import Run
from utils import DotDict


def experiment(name: str, tags: Optional[List[str]] = None, args: Optional[Dict] = None, wandb: bool = True,
               clean: bool = True):
    if tags is None:
        tags = []

    if args is None:
        args = []

    def wrapper(target):
        arg_names = list(signature(target).parameters)[1:]
        arg_values = [args[n] for n in arg_names]

        experiments_configurations = get_configurations(arg_names, arg_values)

        @functools.wraps(target)
        def wrapped(*_args):
            for i, args in enumerate(experiments_configurations):
                run = Run(name, tags, wandb, clean)

                print(f"Run {i + 1}/{len(experiments_configurations)}")
                for n, v in zip(arg_names, args):
                    print(n, ":", v)

                try:
                    target(run, *args)
                    run.finish()
                except Exception as e:
                    Run.clean_wandb_directory()
                    raise e

            Run.clean_wandb_directory()

        return wrapped

    return wrapper


def get_configurations(arg_names, arg_values):
    iterate_on = []
    for arg_index, arg in enumerate(arg_values):
        if hasattr(arg, '__iter__'):
            iterate_on.append((arg_index, arg))
            continue

    experiments_configurations = []

    skip = DotDict()

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
                arg_values[arg_index] = value

            experiments_configurations.append(arg_values[:])

            return

        current, *remaining = iterables
        arg_index, values = current

        for value in values:
            collect_configurations(remaining, selected + [(arg_index, value)])

    collect_configurations(iterate_on, [])

    return experiments_configurations
