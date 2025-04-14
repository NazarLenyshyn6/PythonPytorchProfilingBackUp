import pytest, json, yaml
from Internals.execution_guards import serialization_handler
from tests.enums import FilePath, FileExtension


def to_json(cls, data, file_path, mode):
    with open(file_path, mode=mode) as f:
        json.dump(data, f, indent=4)
        
        
def to_txt(cls, data: dict, file_path: str, mode: str):
    with open(file_path, mode=mode) as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
                   
                   
def to_yaml(cls, data: dict, file_path: str, mode: str):
    with open(file_path, mode=mode) as f:
        yaml.safe_dump(data, f) 
           

@pytest.mark.parametrize(
    'required_extension, file_path, data, mode, func, output_type',
    [
        (FileExtension.JSON, FilePath.JSON, {1: 1}, 'w', to_json, None),
        (FileExtension.JSON, FilePath.JSON, {'key': 'value'}, 'w', to_json, None),
        (FileExtension.TXT, FilePath.TXT, {'key': 'value'}, 'w', to_txt, str),
        (FileExtension.YAML, FilePath.YAML, {'key': 'value'}, 'w', to_yaml, None),
        (FileExtension.JSON, FilePath.JSON, {1: lambda: 0}, 'w', to_json, None),  
        (FileExtension.JSON, FilePath.JSON, {1: 'value'}, 'invalid_mode', to_json, None),
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
    
    new_func = serialization_handler(common_file_extension[required_extension])(func)
    result = new_func(None, data, common_file_path[file_path], mode)
    remove_dummy_file(common_file_path[file_path])
    assert type(result) == output_type or result == None

