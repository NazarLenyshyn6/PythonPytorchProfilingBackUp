"""Fixtures for mocking python profiling configs."""

import pytest

from python_profiling import python_profiling_configs
from python_profiling import python_profiling_enums
from tests import test_enums

DEFAULT_FILE_MODE = 'w'

@pytest.fixture(scope='session')
def common_storage(common_file_path):
    return python_profiling_configs.StorageConfig(
        serializers_strategies=[
            python_profiling_enums.SerializerStrategy.JSON, 
            python_profiling_enums.SerializerStrategy.TXT,
            python_profiling_enums.SerializerStrategy.YAML],
        file_paths=[
            common_file_path[test_enums.FilePath.JSON], 
            common_file_path[test_enums.FilePath.TXT], 
            common_file_path[test_enums.FilePath.YAML]
            ],
        modes=[DEFAULT_FILE_MODE] * 3
        )