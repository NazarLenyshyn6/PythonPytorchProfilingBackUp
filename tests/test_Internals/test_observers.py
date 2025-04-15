"""Tests for observers module."""

import os
import pytest

from Internals import observers


def test_ProfilingObserver(
    remove_dummy_file, 
    common_file_path, 
    dummy_TimeProfilerResult, 
    common_storage
    ):    
    
    valid = True
    observers.ProfilingObserver(storages=common_storage).dump(dummy_TimeProfilerResult)
    
    for file_path in common_storage.file_paths:
        if not os.path.exists(file_path): 
            valid = False
        remove_dummy_file(file_path)
        
    assert valid
    
    