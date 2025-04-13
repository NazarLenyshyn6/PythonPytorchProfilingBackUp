import pytest 
from tests.enums import FileExtension, FilePath

@pytest.fixture(scope='session')
def common_file_path():
    return {FilePath.JSON: 'dummy.json',
            FilePath.TXT: 'dummy.txt',
            FilePath.YAML: 'dummy.yaml'}
    
    
@pytest.fixture(scope='session')
def common_file_extension():
    return {FileExtension.JSON: '.json',
            FileExtension.TXT: '.txt',
            FileExtension.YAML: '.yaml'}
