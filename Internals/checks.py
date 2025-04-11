from typing import Any, Callable
from Internals.exceptions import InvalidInputTypeError
from functools import wraps
from dataclasses import dataclass
from enum import Enum
from inspect import isclass


class ValidateType:
    def __init__(self, expected: tuple[str, Any] | list[tuple[str, Any]], handle: bool = False):
        self.expected = expected
        self.handle = handle
    
    @staticmethod
    def _validate_arg(arg: Any, expected_type: Any) -> InvalidInputTypeError | None:
        if not isinstance(arg, expected_type) and not (isclass(arg) and issubclass(arg, expected_type)):
            raise InvalidInputTypeError(input_=arg,
                                        expected_type=expected_type)            
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not kwargs:
                raise Exception('Provide all parameters as keywords')
            
            if isinstance(self.expected, list):
                for arg, expected_type in self.expected:
                    self._validate_arg(kwargs[arg], expected_type)   
            else:
                self._validate_arg(kwargs[self.expected[0]], self.expected[1])
                
            return func(*args, **kwargs)
        return wrapper
        
    