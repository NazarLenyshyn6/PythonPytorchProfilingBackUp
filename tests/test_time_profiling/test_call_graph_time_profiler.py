"""Tests for call_graph_line_profiler module."""

import pytest
import pydantic
import contextlib

from python_profiling.time_profiling import call_graph_time_profiler

@pytest.mark.parametrize(
    '''
    sort_key, 
    func_filter, 
    top_n, 
    func, 
    func_kwargs, 
    func_result, 
    func_profiling_result_type,
    func_exception,
    raised_exception_ctx
    ''', 
    [
        ('cumulative', '', 10, lambda x: x + 1, {'x': 1}, 2,str, None, contextlib.nullcontext()), 
        ('cumulative', '', 10, lambda x: 1 / x, {'x': 0}, None, None, ZeroDivisionError, contextlib.nullcontext()),
        (11, '', 10, lambda x: 1 / x, {'x': 0}, None, None, pydantic.ValidationError, pytest.raises(pydantic.ValidationError)),
        ('invalid', '', 10, lambda x: 1 / x, {'x': 0}, None, None, pydantic.ValidationError, pytest.raises(pydantic.ValidationError))
        ]
    )
def test_CallGraphTimeProfiler(
    sort_key, 
    func_filter, 
    top_n, 
    func, 
    func_kwargs, 
    func_result,
    func_profiling_result_type,
    func_exception,
    raised_exception_ctx
    ):
    with raised_exception_ctx:
        profiler = call_graph_time_profiler.CallGraphTimeProfiler(sort_key=sort_key,
                                                              func_filter=func_filter,
                                                              top_n=top_n)
        result = profiler.profile(func=func, **func_kwargs)
        assert result.profiler == profiler
        assert result.profiled_func == func
        assert result.func_result == func_result
        assert type(result.func_profiling_result) == func_profiling_result_type or result.func_profiling_result == func_profiling_result_type
        assert result.func_exception == func_exception
    