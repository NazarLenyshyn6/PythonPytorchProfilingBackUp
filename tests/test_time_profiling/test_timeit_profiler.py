import time
import contextlib

import pydantic
import pytest

from python_profiling.time_profiling import timeit_profiler
from Internals import exceptions

INVALID_NUMBER = 'hello'


@pytest.mark.parametrize(
    'timer, number, repeat, func, func_result, kwargs, raised_exception, func_exception',
    [
        (time.time, 10000, 5, lambda x: x + 1, 2, {'x': 1}, contextlib.nullcontext(), None),
        (time.time, INVALID_NUMBER, 5, lambda x: x + 1, 2, {'x': 1}, pytest.raises(pydantic.ValidationError), None),
        (time.time, 10000, 5, 11, 2, {'x': 1}, pytest.raises(exceptions.InvalidInputTypeError), None),
        (time.time, 10000, 5, lambda x: 1/x, None, {'x': 0}, contextlib.nullcontext(), ZeroDivisionError)
        ]
    )
def test_TimeItProfiler(
    timer,
    number,
    repeat,
    func,
    func_result,
    kwargs,
    raised_exception,
    func_exception
    ):
    with raised_exception:
        profiler = timeit_profiler.TimeItProfiler(timer=timer, number=number, repeat=repeat)
        result = profiler.profile(func=func, **kwargs)
        assert result.profiler == profiler
        assert result.profiled_func == func
        assert result.func_kwargs == kwargs
        assert result.func_result == func_result
        assert isinstance(result.min_func_execution_time, (int, float))
        assert isinstance(result.avg_func_execution_time, (int, float))
        assert isinstance(result.max_func_execution_time, (int, float)) 
        assert result.func_exception == func_exception
        