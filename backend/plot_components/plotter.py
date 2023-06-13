from typing import Protocol
from abc import abstractmethod


class Plotter(Protocol):
    @abstractmethod
    def get_metadata(self):
        ...
    @abstractmethod
    def plot(self, kwargs):
        ...