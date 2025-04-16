"""Fixtures for Python functions time profiling with time module."""

import pytest

@pytest.fixture
def check_time_profiling_result():
    def wrapper(result, profiler, func, kwargs, func_result, func_exception):
        """Validates TimeProfilerResult fields against expected values."""
        assert result.profiler == profiler
        assert result.profiled_func == func
        assert result.func_args == None
        assert result.func_kwargs == kwargs
        assert result.func_result == func_result
        assert type(result.func_execution_time) == float
        assert result.func_exception == func_exception
    return wrapper