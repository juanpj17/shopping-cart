from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from .publisher import Publisher

T = TypeVar('T')

class Subscriber(ABC, Generic[T]):

    @abstractmethod
    def update(self, data: T):
        pass