from typing import Protocol
from abc import abstractmethod


class Ingestor(Protocol):
    @abstractmethod
    def get_metadata(self):
        ...
    @abstractmethod
    def ingest(self, kwargs):
        ...