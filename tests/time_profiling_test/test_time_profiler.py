import pytest, time
from python_profiling.time_profiling.time_profiler import TimeProfiler, ThreadBasedTimeProfiler
from tests.fixtures.time_profiler_fixtures import check_time_profiling_result


@pytest.mark.parametrize('profiling_timer, func, kwargs, func_result, func_exception',
                         [(time.time, lambda x: x + 2, {'x': 1}, 3, None),
                          (time.time, lambda x: 1 / x, {'x': 0}, None, ZeroDivisionError)])
def test_TimeProfiler(profiling_timer, func, kwargs, func_result, func_exception, check_time_profiling_result):
    profiler = TimeProfiler(profiling_timer=profiling_timer)
    result = profiler.profile(func=func, **kwargs)
    check_time_profiling_result(result, profiler, func, kwargs, func_result, func_exception)
    
    
    
@pytest.mark.parametrize('func, kwargs, func_result, func_exception',
                         [(lambda x: x + 2, {'x': 1}, None, None),
                          (lambda x: 1 / x, {'x': 0}, None, None)])
def test_ThreadBasedTimeProfiler(func, kwargs, func_result, func_exception, check_time_profiling_result):
    result = ThreadBasedTimeProfiler.profile(func=func, **kwargs)
    check_time_profiling_result(result, ThreadBasedTimeProfiler, func, kwargs, func_result, func_exception)