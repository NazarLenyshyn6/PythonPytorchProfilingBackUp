"""Tests for serialization module."""

import os
import json
from typing import Any

import pytest
import yaml
import contextlib

from python_profiling import python_profiling_enums
from Internals import serialization
from Internals import exceptions
from tests import test_enums


FILE_WRITE_MODE = 'w'
FILE_APPEND_MODE = 'a'
INVALID_FILE_MODE = 'kk'
INVALID_FILE_PATH = 'hello'
NEW_SERIALIZER_NAME = 'new_serializer'
INVALID_SERIALIZER_NAME = 'invalid_name'


def check_written_to_json(file_path: str, expected_data: Any) -> bool:
    """Read JSON-formatted data from file and compare it to expected data.
    
    Args:
        file_path (str): Path to the file.
        expected_data (Any): Expected contents of the file.
        
    Returns:
        bool: True if contents match expected_data, else False.
    """
    with open(file_path, 'r') as f:
        return json.load(f) == expected_data


def check_written_to_yaml(file_path: str, expected_data: Any) -> bool:
    """Read YAML-formatted data from file and compare it to expected data.
    
    Args:
        file_path (str): Path to the file.
        expected_data (Any): Expected contents of the file.
        
    Returns:
        bool: True if contents match expected_data, else False.
    """
    with open(file_path, 'r') as f:
        return yaml.safe_load(f) == expected_data


def check_written_to_txt(file_path, data):
    """Read plain text data from file and compare it to expected key-value pairs.
    
    Args:
        file_path (str): Path to the file.
        expected_data (Any): Expected contents of the file.
        
    Returns:
        bool: True if all key-value pairs are in the file, else False.
    """
    with open(file_path, 'r') as f:
      for key, value in data.items():
          if not f"{key}: {value}" in f.read():
              return False
    return True
    

@pytest.mark.parametrize(
    'serializer, data, file_path, mode, check_func, raise_exception', 
    [
        (serialization.JSONSerializer, 
         {'x': 1}, 
         test_enums.FilePath.JSON, 
         FILE_WRITE_MODE,
         check_written_to_json, 
         False),
        
        (serialization.TXTSerializer, 
         {'x': 1}, 
         test_enums.FilePath.TXT, 
         FILE_APPEND_MODE,
         check_written_to_txt, 
         False),
        
        (serialization.YAMLSerializer, 
         {'x': 1}, 
         test_enums.FilePath.YAML, 
         FILE_WRITE_MODE,
         check_written_to_yaml, 
         False),
        
        (serialization.TXTSerializer, 
         {1: 1}, 
         INVALID_FILE_PATH, 
         FILE_APPEND_MODE, 
         check_written_to_txt,
         True),
        
        (serialization.TXTSerializer, 
         {1: 1}, 
         test_enums.FilePath.TXT, 
         INVALID_FILE_MODE, 
         check_written_to_txt,
         True),
        
        (serialization.JSONSerializer, 
         {1: lambda : 1}, 
         test_enums.FilePath.JSON, 
         FILE_WRITE_MODE, 
         check_written_to_json,
         True)
        ]
    )
def test_serializer(
    serializer,
    data,
    file_path,
    mode,
    check_func,
    raise_exception,
    common_file_path,
    remove_dummy_file
    ):
    file_path = file_path if file_path not in common_file_path else common_file_path[file_path]
    result = serializer.dump(data, file_path, mode)
    
    if not raise_exception:
        assert check_func(file_path, data)
         
    remove_dummy_file(file_path)

    
@pytest.mark.parametrize(
    'data, file_path, mode, serializer_strategy',
    [
        ({1: 1}, test_enums.FilePath.JSON, FILE_WRITE_MODE, python_profiling_enums.SerializerStrategy.JSON),
        ({1: 1}, test_enums.FilePath.TXT, FILE_WRITE_MODE, python_profiling_enums.SerializerStrategy.TXT),
        ({1: 1}, test_enums.FilePath.YAML, FILE_WRITE_MODE, python_profiling_enums.SerializerStrategy.YAML)
        ]
    )
def test_SerializationHandler_dump(
    data, 
    file_path, 
    mode, 
    serializer_strategy, 
    common_file_path, 
    remove_dummy_file
    ):
    (serialization.SerializationHandler
     .dump(
         data=data, 
         file_path=common_file_path[file_path], 
         mode=mode, 
         serializer_strategy=serializer_strategy)
     )
    assert os.path.exists(common_file_path[file_path])
    remove_dummy_file(common_file_path[file_path])
    
    
@pytest.mark.parametrize(
    'serializer_name, serializer, raised_exception',
    [
        (NEW_SERIALIZER_NAME, serialization.JSONSerializer, pytest.raises(exceptions.InvalidInputTypeError)),
        (NEW_SERIALIZER_NAME, lambda x: x, pytest.raises(exceptions.InvalidInputTypeError)),
        (python_profiling_enums.SerializerStrategy.JSON, serialization.JSONSerializer, contextlib.nullcontext())
        ]
    )
def test_SerializationHandler_add_serializer(
    serializer, 
    serializer_name, 
    raised_exception,
    reset_serializers
    ):
    with raised_exception:
        (serialization.SerializationHandler
         ._add_serializer(
             serializer_name=serializer_name, 
             serializer=serializer)
         )
        assert serializer_name in serialization.SerializationHandler._avaliable_serializers
            
            
@pytest.mark.parametrize('serializer_name',
                         [INVALID_SERIALIZER_NAME, python_profiling_enums.SerializerStrategy.TXT]
                         )
def test_SerializationHandler_remove_serializer(serializer_name, reset_serializers):
    serialization.SerializationHandler._remove_serializer(serializer_name=serializer_name)
    assert serializer_name not in serialization.SerializationHandler._avaliable_serializers