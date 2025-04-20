import pytest
import contextlib
import pympler.tracker

from python_profiling.memory_profiling import object_allocation_profiler
from Internals import exceptions

@pytest.mark.parametrize(
	'''func, func_kwargs, func_result, func_exception, raised_exception_ctx''',
 [
	 (lambda x: x + 1, {'x': 1}, 2, None, contextlib.nullcontext()),
     (lambda x: 1 / x, {'x': 0}, None, ZeroDivisionError, contextlib.nullcontext()),
     (11, {'x': 1}, 2, None, pytest.raises(exceptions.InvalidInputTypeError))
 ]
)
def test_ObjectAllocationProfiler(
    func, 
    func_kwargs, 
    func_result, 
    func_exception, 
    raised_exception_ctx
    ):
    with raised_exception_ctx:
        result = object_allocation_profiler.ObjectAllocationProfiler.profile(func=func, **func_kwargs)
        assert result.profiler == object_allocation_profiler.ObjectAllocationProfiler
        assert result.profiled_func == func
        assert result.func_kwargs == func_kwargs
        assert result.func_result == func_result
        assert isinstance(result.tracker, pympler.tracker.SummaryTracker)
        assert isinstance(result.before_memory_allocation, str)
        assert isinstance(result.after_memory_allocation, str)
        assert result.func_exception == func_exception

