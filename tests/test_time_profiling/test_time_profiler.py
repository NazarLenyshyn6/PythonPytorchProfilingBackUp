"""Tests for time_profiler module."""

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
    check_time_profiling_result
    ):
    
    profiler = time_profiler.TimeProfiler(profiling_timer=profiling_timer)
    result = profiler.profile(func=func, **kwargs)
    check_time_profiling_result(
        result, 
        profiler, 
        func, 
        kwargs, 
        func_result, 
        func_exception
        )
    
    
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
    check_time_profiling_result
    ):
    
    result = time_profiler.ThreadBasedTimeProfiler.profile(func=func, **kwargs)
    check_time_profiling_result(
        result, 
        time_profiler.ThreadBasedTimeProfiler, 
        func, 
        kwargs, 
        func_result, 
        func_exception
        )