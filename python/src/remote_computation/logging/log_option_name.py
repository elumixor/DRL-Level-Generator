from enum import Enum


class LogOptionName(int, Enum):
    TrajectoryReward = 0,
    TrainingLoss = 1,
