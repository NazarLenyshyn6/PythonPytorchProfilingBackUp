"""Test for execution_guards module."""

import pytest
import json
from typing import Any

import yaml

from Internals import execution_guards
from tests import test_enums


FILE_WRITE_MODE = 'w'
INVALID_FILE_MODE = 'invalid_mode'


def to_json(cls, data: Any, file_path: str, mode: str = 'w') -> None:
    """Write data in JSON format.
    
    Args:
        data (Any): Data to write.
        file_path (str): Output file path.
        mode (str): File mode, default is 'w' (write).
        
    Returns:
        None
    """
    with open(file_path, mode=mode) as f:
        json.dump(data, f, indent=4)
        
        
def to_txt(cls, data: dict, file_path: str, mode: str) -> None:
    """Write data in plain text format.
    
    Args:
        data (Any): Data to write.
        file_path (str): Output file path.
        mode (str): File mode, default is 'w' (write).
        
    Returns:
        None
    """
    with open(file_path, mode=mode) as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
                   
                   
def to_yaml(cls, data: dict, file_path: str, mode: str) -> None:
    """Write data in YAML format.
    
    Args:
        data (Any): Data to write.
        file_path (str): Output file path.
        mode (str): File mode, default is 'w' (write).
        
    Returns:
        None
    """
    with open(file_path, mode=mode) as f:
        yaml.safe_dump(data, f) 
           

@pytest.mark.parametrize(
    'required_extension, file_path, data, mode, func, output_type',
    [
        (test_enums.FileExtension.JSON, test_enums.FilePath.JSON, {1: 1}, FILE_WRITE_MODE, to_json, None),
        (test_enums.FileExtension.JSON, test_enums.FilePath.JSON, {'key': 'value'}, FILE_WRITE_MODE, to_json, None),
        (test_enums.FileExtension.TXT, test_enums.FilePath.TXT, {'key': 'value'}, FILE_WRITE_MODE, to_txt, str),
        (test_enums.FileExtension.YAML, test_enums.FilePath.YAML, {'key': 'value'}, FILE_WRITE_MODE, to_yaml, None),
        (test_enums.FileExtension.JSON, test_enums.FilePath.JSON, {1: lambda: 0}, FILE_WRITE_MODE, to_json, None),  
        (test_enums.FileExtension.JSON, test_enums.FilePath.JSON, {1: 'value'}, INVALID_FILE_MODE, to_json, None),
        ]
    )
def test_serialization_handler(
    required_extension, 
    file_path, 
    data, 
    mode, 
    func, 
    output_type, 
    remove_dummy_file,
    common_file_extension,
    common_file_path
    ):
    
    new_func = execution_guards.serialization_handler(common_file_extension[required_extension])(func)
    result = new_func(None, data, common_file_path[file_path], mode)
    remove_dummy_file(common_file_path[file_path])
    assert type(result) == output_type or result == None

