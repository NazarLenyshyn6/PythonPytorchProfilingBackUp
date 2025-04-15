"""Custom context managers for profiling processes."""

import timeit
from typing import Callable
from types import BuiltinFunctionType, FunctionType

import line_profiler
        
class BaseProfilerManager:   
    """Base context manager for safe profiling processes."""
    
    def __enter__(self):
        """Enter context."""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Handle exceptions if occurs.
        
        Args:
            exc_type: The type of the exception.
            exc_value: The type of the exception.
            traceback: The traceback object.
        
        Returns:
            bool: Always returns True to suppress exceptions.
        """
        self.exception = True if exc_type else False
        self.func_exception = exc_type if exc_type else None
        return True
            

class TimeProfilerManager(BaseProfilerManager):
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
        super().__exit__(exc_type, exc_value, traceback)
        return True
    
    def __repr__(self) -> str:
        return f'TimeProfilingManager(profiling_timer={self.profiling_timer})'
    

class LineTimeProfilerManager(BaseProfilerManager):
    """Context manager for profiling process of  LineTimeProfiler class."""
    
    def __init__(
        self, 
        line_profiler_ : line_profiler.LineProfiler, 
        profiled_func: BuiltinFunctionType | FunctionType
        ):
        self.line_profiler_ = line_profiler_
        self.profiled_func = profiled_func
        
    def __enter__(self):
        self.line_profiler_.add_function(self.profiled_func)
        self.line_profiler_.enable_by_count()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.line_profiler_.disable_by_count()
        super().__exit__(exc_type, exc_value, traceback)
        return True
        
    

    