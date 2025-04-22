"""Helper functions to validate provided data."""

from typing import Any, Callable
import inspect
import functools

from Internals import exceptions


class ValidateType:
    """Decorator to validate types of arguments provided to a function.
    
    Args:
        expected_type: (tuple[str, Any] | list[tuple[str, Any]]):  expected type for provided argument.
    """
    
    def __init__(self, expected_type: tuple[str, Any] | list[tuple[str, Any]]):
        self.expected_type = expected_type
    
    @staticmethod
    def _validate_arg(arg: Any, expected_type: Any) -> None:
        if not isinstance(arg, expected_type) and not (inspect.isclass(arg) and 
                                                       issubclass(arg, expected_type)):
            raise exceptions.InvalidInputTypeError(input_=arg, expected_type=expected_type)    
      
    @staticmethod      
    def _check_missing_arguments(expected_type, provided_type) -> None:
        # wrap extected type into list to avoid separate logic for not list case
        if not isinstance(expected_type, list):
            expected_type = [expected_type]
            
        for arg, _ in expected_type:
            if not arg in provided_type:
                raise exceptions.MissingArgumentError(arg)
              
    def __call__(self, func: Callable) -> Callable:
        """Decorator call method that applies validation logic."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self._check_missing_arguments(self.expected_type, kwargs)
            
            if isinstance(self.expected_type, list):
                for arg, expected_type in self.expected_type:
                    self._validate_arg(kwargs[arg], expected_type)   
            else:
                self._validate_arg(kwargs[self.expected_type[0]], self.expected_type[1])   
            return func(*args, **kwargs)
        return wrapper
        
    
    
