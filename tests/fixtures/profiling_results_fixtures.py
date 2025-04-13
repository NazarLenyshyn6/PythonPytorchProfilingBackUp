import pytest
from python_profiling.time_profiling.time_profiling_results import TimeItProfilerResult, TimeProfilerResult


@pytest.fixture(scope='session')
def dummy_TimeProfilerResult():
    return TimeProfilerResult(profiler='dummy_profiler',
                              profiled_func='dummy_func',
                              func_args='dummy_args',
                              func_kwargs='dummy_kwargs',
                              func_result=None,
                              func_execution_time=1,
                              func_exception=None)
    
    
@pytest.fixture(scope='session')
def dummy_TimeItProfilerResult():
    return TimeItProfilerResult(profiler='dummy_profiler',
                                profiled_func='dummy_func',
                                func_kwargs='dummy_kwargs',
                                repeats=1,
                                min_func_execution_time=0,
                                avg_func_execution_time=0,
                                max_func_execution_time=0,
                                func_result=None,
                                func_exception=None)