"""Fixtures for mocking profiling results."""

import pytest

from python_profiling.time_profiling import time_profiling_results

PROFILER = 'dummy_profiler'
PROFILED_FUNC = 'dummy_func'
FUNC_ARGS = 'dummy_args'
FUNC_KWARGS = 'dummy_kwargs'

@pytest.fixture(scope='session')
def dummy_TimeProfilerResult():
    return time_profiling_results.TimeProfilerResult(
        profiler=PROFILER,
        profiled_func=PROFILED_FUNC,
        func_args=FUNC_ARGS,
        func_kwargs=FUNC_KWARGS,
        func_result=None,
        func_execution_time=1,
        func_exception=None)
    
    
@pytest.fixture(scope='session')
def dummy_TimeItProfilerResult():
    return time_profiling_results.TimeItProfilerResult(
        profiler=PROFILER,
        profiled_func=PROFILED_FUNC,
        func_kwargs=FUNC_KWARGS,
        repeats=1,
        min_func_execution_time=0,
        avg_func_execution_time=0,
        max_func_execution_time=0,
        func_result=None,
        func_exception=None
        )