from typing import Any, Dict, Type
from enum import Enum


class InvalidInputTypeError(Exception):
    def __init__(self,input_: Any, expected_type: Any):
        super().__init__(f'Input {input_} has to be of type {expected_type}, got intead: {type(input_)}.')
        
        
class MissingArgumentError(Exception):
    def __init__(self, missing_arg: str):
        super().__init__(f"Missing required argument: {missing_arg}")
        self.missing_arg = missing_arg
        