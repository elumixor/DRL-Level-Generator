from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TStaticConfiguration = TypeVar('TStaticConfiguration')
TDynamicConfiguration = TypeVar('TDynamicConfiguration')


class ConfigurableObject(Generic[TStaticConfiguration, TDynamicConfiguration], ABC):
    @abstractmethod
    def update(self, configuration: TDynamicConfiguration):
        ...
