"""Custom context managers for profiling processes."""

import timeit
import tracemalloc
from typing import Callable
from types import BuiltinFunctionType, FunctionType

import line_profiler
import cProfile

CALL_GRAPH_PROFILING_RESULT_FILE = 'result.prof'


def profiler_manager_base_exception_handling(obj, exc_type):
    """Expetion handling that is common accross all profilers.
    
    Args:
        obj: Instance of profiling context manager.
        exc_type: The type of the exception.
    """
    obj.exception = True if exc_type else False
    obj.func_exception = exc_type if exc_type else None
    
class TimeProfilerManager:
    """Context manager for profiling processes of classes that inherets from TimeProfilerI class.
    
    Args:
        profiling_time (Callable): Timer from time module which will measure function execution time.
    """
    
    def __init__(self, profiling_timer):
        self.profiling_timer = profiling_timer
    
    def __enter__(self) -> 'TimeProfilerManager':
        """Starts profiling time.
        
        Returns:
            TimeProfilerManager: The current instance.
        """
        self.profiling_start = self.profiling_timer()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Stops  profiling and handle exceptions if occurs.
        
        Args:
            exc_type: The type of the exception.
            exc_value: The exception instance.
            traceback: The traceback object.
        
        Returns:
            bool: Always returns True to suppress exceptions.
        """
        self.profiling_stop = self.profiling_timer()
        self.func_execution_time = self.profiling_stop - self.profiling_start
        profiler_manager_base_exception_handling(self, exc_type)
        return True
    
    def __repr__(self) -> str:
        return f'TimeProfilingManager(profiling_timer={self.profiling_timer})'
    
    
class TimeItProfilerManager:
    """Context manager for profiling process of  TimeItProfiler class."""
    
    def __enter__(self):
        """Enters context."""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Stops  profiling and handle exceptions if occurs.
        
        Args:
            exc_type: The type of the exception.
            exc_value: The exception instance.
            traceback: The traceback object.
        
        Returns:
            bool: Always returns True to suppress exceptions.
        """
        profiler_manager_base_exception_handling(self, exc_type)
        return True
    
class LineTimeProfilerManager:
    """Context manager for profiling process of  LineTimeProfiler class."""
    
    def __init__(
        self, 
        profiler : line_profiler.LineProfiler, 
        profiled_func: BuiltinFunctionType | FunctionType
        ):
        self.profiler = profiler
        self.profiled_func = profiled_func
        
    def __enter__(self):
        self.profiler.add_function(self.profiled_func)
        self.profiler.enable_by_count()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.profiler.disable_by_count()
        profiler_manager_base_exception_handling(self, exc_type)
        return True
    
class CallGraphTimeProfilerManager:
    """Context manager for profiling process of  CallGraphTimeProfiler class."""
    
    def __enter__(self):
        """Start the profiler."""
        self.profiler = cProfile.Profile()
        self.profiler.enable()
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        """Stop the profiler and dump stats if no exception occurred.

        Args:
            exc_type (Type[BaseException] | None): Exception class if raised.
            exc_value (BaseException | None): The exception instance.
            traceback (TracebackType | None): Traceback if exception occurred.

        Returns:
            bool: True to suppress exceptions.
        """
        self.profiler.disable()
        if not exc_type: 
            self.profiler.dump_stats(CALL_GRAPH_PROFILING_RESULT_FILE)
        profiler_manager_base_exception_handling(self, exc_type)
        return True
    
    
class PeakMemoryProfilerManager:
    """Context manager for profiling process of  CallGraphTimeProfiler class.
    
    Attributes:
        nframes: defines how many frames of traceback to record for each memory allocation.
    """
    
    def __init__(self, nframes: int):
        self.nframes = nframes
        
    def __enter__(self) -> 'PeakMemoryProfilerManager':
        """starts memory allocation tracing and  takes a snapshot of all memory allocations currently being traced."""
        tracemalloc.start(self.nframes)
        self.allocation_before = tracemalloc.take_snapshot()
        return self
        
    def __exit__(self, exc_type, exc_value,  traceback):
        """Captures final memory snapshot and handles any exceptions.

        Args:
            exc_type: Exception type, if any.
            exc_value: Exception instance, if any.
            traceback: Traceback object, if any.

        Returns:
            bool: True to suppress exceptions (consider returning False unless intended).
        """
        self.allocation_after = tracemalloc.take_snapshot()
        profiler_manager_base_exception_handling(self, exc_type)
        return True

        
    

    