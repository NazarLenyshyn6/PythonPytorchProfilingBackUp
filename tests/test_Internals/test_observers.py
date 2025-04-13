import pytest, os
from Internals.observers import ProfilingObserver
from python_profiling.configs import StorageConfig
from tests.fixtures.file_fixtures import common_file_path
from tests.fixtures.profiling_results_fixtures import dummy_TimeProfilerResult
from python_profiling.enums import SerializerStrategy
from tests.enums import FilePath


def test_ProfilingObserver(remove_dummy_file, common_file_path, dummy_TimeProfilerResult):
    storages = StorageConfig(serializers_strategies=[SerializerStrategy.JSON, 
                                                     SerializerStrategy.TXT,
                                                     SerializerStrategy.YAML],
                             file_paths=[common_file_path[FilePath.JSON], 
                                         common_file_path[FilePath.TXT], 
                                         common_file_path[FilePath.YAML]],
                             modes=['w', 'w', 'w'])
    
    valid = True
    ProfilingObserver(storages=storages).dump(dummy_TimeProfilerResult)
    
    for file_path in storages.file_paths:
        if not os.path.exists(file_path): 
            valid = False
            
        remove_dummy_file(file_path)
            
    assert valid
    
    