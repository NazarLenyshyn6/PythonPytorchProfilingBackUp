from typing import Any, Callable
from Internals.exceptions import InvalidInputTypeError, MissingArgumentError
from functools import wraps
from dataclasses import dataclass
from enum import Enum
from inspect import isclass


class ValidateType:
    def __init__(self, expected: tuple[str, Any] | list[tuple[str, Any]]):
        self.expected = expected
    
    @staticmethod
    def _validate_arg(arg: Any, expected_type: Any) -> InvalidInputTypeError | None:
        if not isinstance(arg, expected_type) and not (isclass(arg) and issubclass(arg, expected_type)):
            raise InvalidInputTypeError(input_=arg,
                                        expected_type=expected_type)    
      
    @staticmethod      
    def _check_missing_arguments(expected, provided):
        if not isinstance(expected, list):
            expected = [expected]
            
        for arg, _ in expected:
            if not arg in provided:
                raise MissingArgumentError(arg)
                    
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            self._check_missing_arguments(self.expected, kwargs)
            
            if isinstance(self.expected, list):
                for arg, expected_type in self.expected:
                    self._validate_arg(kwargs[arg], expected_type)   
            else:
                self._validate_arg(kwargs[self.expected[0]], self.expected[1])
                
            return func(*args, **kwargs)
        return wrapper
        
    