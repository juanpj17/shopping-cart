from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')

class IdGenerator(ABC, Generic[T]):

    @abstractmethod
    def generate_id() -> T:
        pass