"""Custom exceptions that occurs in any stage of profiling."""

from typing import Any, Dict, Type


class InvalidInputTypeError(Exception):
    """Exception raised when an input argument has an invalid type.
    
    Args:
        input_ (Any): The input value that failed the type check.
        expected_type (Any): The expected type.
    """
    
    def __init__(self,input_: Any, expected_type: Any):
        super().__init__(f'Input {input_} has to be of type {expected_type}, got intead: {type(input_)}.')
        
        
class MissingArgumentError(Exception):
    """Exception raised when a required argument is missing.
    
    Args:
        missing_arg (str): The name of the argument that is missing.
    """
    
    def __init__(self, missing_arg: str):
        super().__init__(f"Missing required argument: {missing_arg}")
        self.missing_arg = missing_arg