"""Tests for line_time_profiler module."""

import pytest

from python_profiling.time_profiling import line_time_profiler


@pytest.mark.parametrize(
	'profiled_func, func_kwargs, func_result, func_exception',
 [
	 (lambda x: x + 1, {'x': 1}, 2, None),
  	 (lambda x: 1 / x, {'x': 0}, None, ZeroDivisionError)
 ]
)
def test_LineTimeProfiler(
    profiled_func, 
    func_kwargs,  
    func_result,
    func_exception,
    ):
    result =  line_time_profiler.LineTimeProfiler.profile(func=profiled_func, **func_kwargs)
    assert result.profiler == line_time_profiler.LineTimeProfiler
    assert result.profiled_func == profiled_func
    assert result.func_kwargs  ==  func_kwargs
    assert result.func_result == func_result
    assert isinstance(result.func_profiling_result, str)
    assert  func_exception  ==  func_exception

    