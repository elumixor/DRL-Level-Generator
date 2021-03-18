from typing import Dict, Union

import torch
import wandb

from common.printing import style


class Context:
    def __init__(self, project, name, display_name, arguments, log=...):
        self.project = project
        self.wandb = log == "wandb"
        self.console = log == "console"
        self.run_name = display_name
        self.name = name
        self.run = None
        self.arguments: Dict = arguments

        if self.wandb:
            def log_function(values: Dict[str, Union[int, float, torch.Tensor]]):
                self.run.log(values)

        elif self.console:
            def log_function(values: Dict[str, Union[int, float, torch.Tensor]]):
                print(values)

        else:
            def log_function(*args):
                ...

        self.log_function = log_function
        self.config = {
            "name": name,
            "display_name": display_name,
            **arguments
        }

    def __enter__(self):
        self.print_header()

        if self.wandb:
            self.run = wandb.init(project=self.project, config=self.config, name=self.run_name)

        return self

    def __exit__(self, *args):
        if self.wandb:
            self.run.finish()

    def print_header(self):
        project = style(f"{self.project}", bold=True, r=200, g=220, b=250)
        name = style(f"{self.name}", bold=True, r=250, g=200, b=100)
        run_name = style(f"({self.run_name})", italic=True, r=100, g=100, b=100)

        print(f"project=[{project}] experiment=[{name}] {run_name}")

        if not self.arguments:
            return

        max_len = max([len(name) for name in self.arguments.keys()])

        for name, value in self.arguments.items():
            print("{name:>{max_len}} = ".format(name=name, max_len=max_len) + style(f"{value}", italic=True, bold=True))

        print()

    def log(self, values: Dict[str, Union[int, float, torch.Tensor]]):
        self.log_function(values)
