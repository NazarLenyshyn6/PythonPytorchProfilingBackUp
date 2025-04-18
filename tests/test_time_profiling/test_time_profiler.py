import time

import pytest

from python_profiling.time_profiling import time_profiler


@pytest.mark.parametrize(
    'profiling_timer, func, kwargs, func_result, func_exception',
    [
        (time.time, lambda x: x + 2, {'x': 1}, 3, None),
        (time.time, lambda x: 1 / x, {'x': 0}, None, ZeroDivisionError)
        ]
    )
def test_TimeProfiler(
    profiling_timer, 
    func, 
    kwargs, 
    func_result, 
    func_exception, 
    ):
    
    profiler = time_profiler.TimeProfiler(profiling_timer=profiling_timer)
    result = profiler.profile(func=func, **kwargs)
    assert result.profiler == profiler
    assert result.profiled_func == func
    assert result.func_args == None
    assert result.func_kwargs == kwargs
    assert result.func_result == func_result
    assert type(result.func_execution_time) == float
    assert result.func_exception == func_exception
    
    
@pytest.mark.parametrize(
    'func, kwargs, func_result, func_exception',
    [
        (lambda x: x + 2, {'x': 1}, None, None),
        (lambda x: 1 / x, {'x': 0}, None, None)
        ]
    )
def test_ThreadBasedTimeProfiler(
    func,
    kwargs,
    func_result,
    func_exception,
    ):
    result = time_profiler.ThreadBasedTimeProfiler.profile(func=func, **kwargs)
    assert result.profiler == time_profiler.ThreadBasedTimeProfiler
    assert result.profiled_func == func
    assert result.func_args == None
    assert result.func_kwargs == kwargs
    assert result.func_result == func_result
    assert type(result.func_execution_time) == float
    assert result.func_exception == func_exception
