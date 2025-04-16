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
    check_line_time_profiling_result
    ):
    result =  line_time_profiler.LineTimeProfiler.profile(func=profiled_func, **func_kwargs)
    check_line_time_profiling_result(
        result, 
        line_time_profiler.LineTimeProfiler,
        profiled_func,
        func_kwargs,
        func_result,
        str,
        func_exception
        )
    