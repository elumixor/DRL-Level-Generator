import os
import shutil
from typing import Optional, List

import wandb as _wandb


class Run:
    @staticmethod
    def get(name: Optional[str] = None):
        api = _wandb.Api()

        if name is not None:
            runs = api.runs(f"elumixor/Level Generator", filters={f"config.name": name})
        else:
            runs = api.runs(f"elumixor/Level Generator")

        return list(runs)

    @staticmethod
    def clean_wandb_directory():
        cwd = os.getcwd()
        path_to_wandb = os.path.join(cwd, "wandb")
        if os.path.exists(path_to_wandb) and os.path.isdir(path_to_wandb):
            shutil.rmtree(path_to_wandb)

    def __init__(self, name: str, tags: Optional[List[str]] = None, wandb: bool = True, clean: bool = True):
        self.wandb = wandb
        self.run: Optional[_wandb.run] = None
        self.clean = clean
        self.name = name
        self.tags = tags

        if self.clean and self.wandb:
            for run in Run.get(self.name):
                run.delete()

        if self.wandb:
            self.run = _wandb.init(project="Level Generator", name=self.name, tags=self.tags)

    def finish(self):
        if self.wandb:
            self.run.finish()

    def log(self, **values):
        if self.wandb:
            self.run.log(values)
        else:
            print(values)
