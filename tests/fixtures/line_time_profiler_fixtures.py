"""Fixtures for Python functions  line time  profiling with time module."""

import pytest

@pytest.fixture
def check_line_time_profiling_result():
    def wrapper(
        result,
        profiler, 
        profiled_func,  
        func_kwargs, 
        func_result, 
        func_profiling_result_type,  
        func_exception
        ) -> bool:
        """Validates LineTimeProfilerResult fields against expected values."""
        assert result.profiler == profiler
        assert result.profiled_func == profiled_func
        assert result.func_kwargs  ==  func_kwargs
        assert result.func_result == func_result
        assert isinstance(result.func_profiling_result, func_profiling_result_type)
        assert  func_exception  ==  func_exception
    return wrapper