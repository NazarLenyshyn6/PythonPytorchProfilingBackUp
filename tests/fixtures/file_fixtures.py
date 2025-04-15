"""Fixtures for mocking file relevent infomation."""

import pytest 

from tests import test_enums


@pytest.fixture(scope='session')
def common_file_path():
    return {test_enums.FilePath.JSON: 'dummy.json',
            test_enums.FilePath.TXT: 'dummy.txt',
            test_enums.FilePath.YAML: 'dummy.yaml'}
    
    
@pytest.fixture(scope='session')
def common_file_extension():
    return {test_enums.FileExtension.JSON: '.json',
            test_enums.FileExtension.TXT: '.txt',
            test_enums.FileExtension.YAML: '.yaml'}
