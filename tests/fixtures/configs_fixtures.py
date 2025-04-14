import pytest
from python_profiling.configs import StorageConfig
from tests.enums import FilePath
from python_profiling.enums import SerializerStrategy



@pytest.fixture(scope='session')
def common_storage(common_file_path):
    return StorageConfig(serializers_strategies=[SerializerStrategy.JSON, 
                                                     SerializerStrategy.TXT,
                                                     SerializerStrategy.YAML],
                             file_paths=[common_file_path[FilePath.JSON], 
                                         common_file_path[FilePath.TXT], 
                                         common_file_path[FilePath.YAML]],
                             modes=['w', 'w', 'w'])