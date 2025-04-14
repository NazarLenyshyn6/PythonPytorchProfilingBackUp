import pytest, json, yaml, os
from Internals.serialization import *
from python_profiling.enums import SerializerStrategy
from tests.enums import FilePath
from contextlib import nullcontext
from Internals.exceptions import InvalidInputTypeError



def check_written_to_json(file_path, data):
    with open(file_path, 'r') as f:
        return json.load(f) == data


def check_written_to_yaml(file_path, data):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f) == data


def check_written_to_txt(file_path, data):
    with open(file_path, 'r') as f:
      for key, value in data.items():
          if not f"{key}: {value}" in f.read():
              return False
    return True
    

@pytest.mark.parametrize(
    'serializer, data, file_path, mode, check_func, raise_exception', 
    [
        (JSONSerializer, {'x': 1}, FilePath.JSON, 'w',check_written_to_json, False),
        (TXTSerializer, {'x': 1}, FilePath.TXT, 'a',check_written_to_txt, False),
        (YAMLSerializer, {'x': 1}, FilePath.YAML, 'w',check_written_to_yaml, False),
        (TXTSerializer, {1: 1}, 'hello', 'a', check_written_to_txt,True),
        (TXTSerializer, {1: 1}, FilePath.TXT, 'kk', check_written_to_txt,True),
        (JSONSerializer, {1: lambda : 1}, FilePath.JSON, 'w', check_written_to_json,True)
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
        ({1: 1}, FilePath.JSON, 'w', SerializerStrategy.JSON),
        ({1: 1}, FilePath.TXT, 'w', SerializerStrategy.TXT),
        ({1: 1}, FilePath.YAML, 'w', SerializerStrategy.YAML)
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
    SerializationHandler.dump(data=data, 
                              file_path=common_file_path[file_path], 
                              mode=mode, 
                              serializer_strategy=serializer_strategy)
    assert os.path.exists(common_file_path[file_path])
    remove_dummy_file(common_file_path[file_path])
    
    
@pytest.mark.parametrize(
    'serializer_name, serializer, raised_exception',
    [
        ('new_serializer', JSONSerializer, pytest.raises(InvalidInputTypeError)),
        ('new_serializer', lambda x: x, pytest.raises(InvalidInputTypeError)),
        (SerializerStrategy.JSON, JSONSerializer, nullcontext())
        ]
    )
def test_SerializationHandler_add_serializer(
    serializer, 
    serializer_name, 
    raised_exception,
    reset_serializers
    ):
    with raised_exception:
        SerializationHandler._add_serializer(serializer_name=serializer_name, 
                                             serializer=serializer)
        assert serializer_name in SerializationHandler._avaliable_serializers
            
            
@pytest.mark.parametrize('serializer_name',['invalid_name', SerializerStrategy.TXT])
def test_SerializationHandler_remove_serializer(serializer_name, reset_serializers):
    SerializationHandler._remove_serializer(serializer_name=serializer_name)
    assert serializer_name not in SerializationHandler._avaliable_serializers