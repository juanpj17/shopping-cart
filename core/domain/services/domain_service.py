from typing import TypeVar, Generic, Optional
from abc import ABC, abstractmethod

T = TypeVar('T')
E = TypeVar('E')

class DomainService(ABC, Generic[T,E]):

    @abstractmethod
    def execute(data: Optional[T] = None) -> E:
        pass