from typing import Dict, Union

import torch
import wandb


class Context:
    def __init__(self, project, name, display_name, arguments, log=...):
        self.project = project
        self.wandb = log == "wandb"
        self.console = log == "console"
        self.run_name = display_name
        self.run = None

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
        if self.wandb:
            self.run = wandb.init(project=self.project, config=self.config, name=self.run_name)

        elif self.console:
            print(f"[{self.project}]\n"
                  f"Initializing new run with the following config:")
            print(self.config)

        return self

    def __exit__(self, *args):
        if self.wandb:
            self.run.finish()

    def log(self, values: Dict[str, Union[int, float, torch.Tensor]]):
        self.log_function(values)
