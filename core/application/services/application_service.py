from typing import TypeVar, Generic, Optional
from abc import ABC, abstractmethod
from ..results.result import Result

T = TypeVar('T')
E = TypeVar('E')

class Service(ABC, Generic[T,E]):

    @abstractmethod
    def execute(data: Optional[T] = None) -> Result[E]:
        pass