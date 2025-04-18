import  pytest
import contextlib
import tracemalloc
import pydantic

from python_profiling.memory_profiling  import  peak_memory_profiler

@pytest.mark.parametrize(
	''' 
 nframes,  
 key_type, 
 top_n, 
 func, 
 func_kwargs, 
 func_result,
 func_exception, 
 raised_exception_ctx
 ''',
 [
	 (1, 'lineno',  3, lambda  x:  x + 1, {'x': 1}, 2, None, contextlib.nullcontext()),
     (1, 'traceback',  3, lambda  x:  x + 1, {'x': 1}, 2, None, contextlib.nullcontext()),
	 (1, 'invalid', 3, lambda  x:  x + 1, {'x': 1}, 2, None, pytest.raises(pydantic.ValidationError)),
     (1, 'filename', 3, lambda  x:  1 / x, {'x': 0}, None, ZeroDivisionError, contextlib.nullcontext()),
 ]
)
def test_PeakMemoryProfiler(
    nframes,  
    key_type, 
    top_n, 
    func, 
	func_kwargs, 
	func_result,
	func_exception, 
	raised_exception_ctx
):
    with raised_exception_ctx:
        profiler =  peak_memory_profiler.PeakMemoryProfiler(nframes=nframes,
															key_type=key_type,
															top_n=top_n)
        result = profiler.profile(func=func, **func_kwargs)
        assert result.profiler == peak_memory_profiler.PeakMemoryProfiler
        assert result.profiled_func == func
        assert result.func_kwargs ==  func_kwargs
        assert result.func_result == func_result
        assert isinstance(result.current_memory, (float, int))
        assert isinstance(result.peak_memory, (float, int))
        assert type(result.allocation_before) == tracemalloc.Snapshot
        assert type(result.allocation_after) == tracemalloc.Snapshot
        assert result.func_exception == func_exception
        
        
    