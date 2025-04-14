"""Custom context managers for profiling processes."""

import timeit
from typing import Callable
from dataclasses import dataclass
from functools import wraps


class BaseManager:
    """Contains functions that are common for all profiling context managers."""
    
    @staticmethod
    def handle_exception(obj, exc_type) -> None:
        """Base method for handling exception that occurs during profiling process.
        
        Args:
            obj: The profiling manager instance.
            exc_type: Type of raised exception.
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
        
        BaseManager.handle_exception(self, exc_type)
        return True
    
    def __repr__(self) -> str:
        return f'TimeProfilingManager(profiling_timer={self.profiling_timer})'
    
    
# Implementation of context manager for TimeIt Profiler
class TimeItProfilerManager:        
    """Contest manager for profiling processes of TimeItProfiler class."""
    
    def __enter__(self) -> 'TimeItProfilerManager':
        """Enter context.
        
        Returns:
            TimeItProfilerManager: The current instance.
        """
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
        BaseManager.handle_exception(self, exc_type)
        return True