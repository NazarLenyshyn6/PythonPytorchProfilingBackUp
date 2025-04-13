import pytest, time
from python_profiling.time_profiling.timeit_profiler import TimeItProfiler
from contextlib import nullcontext
from pydantic import ValidationError
from Internals.exceptions import InvalidInputTypeError


@pytest.mark.parametrize('timer, number, repeat, func, func_result, kwargs, has_exception, raised_exception, func_exception',
                         [(time.time, 10000, 5, lambda x: x + 1, 2, {'x': 1}, False, nullcontext(), None),
                          (time.time, 'hello', 5, lambda x: x + 1, 2, {'x': 1}, True, pytest.raises(ValidationError), None),
                          (time.time, 10000, 5, 11, 2, {'x': 1}, True, pytest.raises(InvalidInputTypeError), None),
                          (time.time, 10000, 5, lambda x: 1/x, None, {'x': 0}, False, nullcontext(), ZeroDivisionError)
                          ])
def test_TimeItProfiler(timer, number, repeat, func, func_result, kwargs, has_exception, raised_exception, func_exception):
    with raised_exception:
        profiler = TimeItProfiler(timer=timer, number=number, repeat=repeat)
        result = profiler.profile(func=func, **kwargs)
        if not has_exception:
            assert result.profiler == profiler
            assert result.profiled_func == func
            assert result.func_kwargs == kwargs
            assert result.func_result == func_result
            assert isinstance(result.min_func_execution_time, (int, float))
            assert isinstance(result.avg_func_execution_time, (int, float))
            assert isinstance(result.max_func_execution_time, (int, float)) 
            assert result.func_exception == func_exception
        