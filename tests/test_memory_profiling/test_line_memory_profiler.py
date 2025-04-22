import pytest
import contextlib
import pydantic

from python_profiling.memory_profiling import line_memory_profiler

@pytest.mark.parametrize(
	'''
 interval, 
 timeout, 
 backed, 
 include_children,
 func,
 func_kwargs,
 func_result,
 has_memory_stats,
 func_exception,
 raised_exception_ctx
 ''',
 [
     (0.2, 1, 'psutil', True, lambda x: x + 1, {'x': 1}, 2, True,  None, contextlib.nullcontext()),
     (0.2, 1, 'invalid', True, lambda x: x + 1, {'x': 1}, 2, True,  None, pytest.raises(pydantic.ValidationError)),
     (0.2, 1, 'psutil', True, lambda x: 1 / x, {'x': 0}, None, False,  ZeroDivisionError, contextlib.nullcontext()),
  ]
)
def test_LineMemoryProfiler(
    interval, 
	timeout, 
	backed, 
	include_children,
	func,
	func_kwargs,
	func_result,
	has_memory_stats,
	func_exception,
	raised_exception_ctx
 ):
    with raised_exception_ctx:
        memory_profiler = line_memory_profiler.LineMemoryProfiler(interval=interval,
                                                                  timeout=timeout,
                                                                  backed=backed,
                                                                  include_children=include_children)
        result = memory_profiler.profile(func=func, **func_kwargs)
        assert result.profiler == line_memory_profiler.LineMemoryProfiler
        assert result.profiled_func == func
        assert result.func_kwargs == func_kwargs
        assert result.func_result == func_result
        assert bool(result.start_memory) == has_memory_stats
        assert bool(result.peak_memory) == has_memory_stats
        assert bool(result.end_memory) == has_memory_stats
        assert bool(result.max_memory_increase) == has_memory_stats
        assert bool(result.memory_timeline) == has_memory_stats
        assert func_exception == func_exception
        
        