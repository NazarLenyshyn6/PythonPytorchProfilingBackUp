import pytest, os
from Internals.observers import ProfilingObserver
from python_profiling.configs import StorageConfig
from python_profiling.enums import SerializerStrategy
from tests.enums import FilePath


def test_ProfilingObserver(
    remove_dummy_file, 
    common_file_path, 
    dummy_TimeProfilerResult, 
    common_storage
    ):    
    
    valid = True
    ProfilingObserver(storages=common_storage).dump(dummy_TimeProfilerResult)
    
    for file_path in common_storage.file_paths:
        if not os.path.exists(file_path): 
            valid = False
            
        remove_dummy_file(file_path)
            
    assert valid
    
    