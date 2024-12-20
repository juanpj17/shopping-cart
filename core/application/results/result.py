from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Result(Generic[T]):

    def __init__(self, value: Optional[T] = None, error: Optional[Exception] = None):
        if value is not None and error is not None:
            raise ValueError("Either value or error should be provided")
        
        if value is None and error is None:
            raise ValueError("Either value or error should be provided")
        
        self.value = value
        self.error = error

    def is_success(self):
        return self.value is not None
    
    def is_failure(self):
        return self.error is not None 
    
    def unwrap(self):
        if self.error is not None:
            return self.error
        return self.value

    @staticmethod
    def make_success(value: T):
        return Result(value=value)
    
    @staticmethod
    def make_failure(error: Exception):
        return Result(error=error)