"""Time Profiling of Python functions with time module."""

import time
import threading
from abc import ABC, abstractmethod
from types import BuiltinFunctionType, FunctionType
from typing import Callable
from typing_extensions import override

from python_profiling.time_profiling import time_profiling_results


from Internals.context_managers import TimeProfilerManager
from Internals.checks import ValidateType


class TimeProfilerI(ABC):
    """Interface for time profilers using the time module."""
    
    @abstractmethod
    def profile(cls, func: BuiltinFunctionType | FunctionType, **kwargs) -> time_profiling_results.TimeProfilerResult:
        """Profile the execution time of a function.
        
        Args:
            func (BuiltinFunctionType | FunctionType): Function to profile.
            **kwargs:  Keyword arguments to pass to the function.
        Returns:
            TimeProfilerResult:  Structured profiling result.
            
        Raises:
            InvalidInputTypeError: If the function is not of the correct type.
        """
        
class TimeProfiler(TimeProfilerI):
    """Time profiler that uses a specified timer from the time module.
    
    Attributes:
        profiling_timer (Callable): Timer function used for profiling.
    """
    
    def __init__(self, profiling_timer: Callable):
        self.profilig_timer = profiling_timer
        
    @ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    @override
    def profile(self, func: BuiltinFunctionType | FunctionType, **kwargs) -> time_profiling_results.TimeProfilerResult:        
        with TimeProfilerManager(profiling_timer=self.profilig_timer) as time_profiler_manager:
            profiling_result = func(**kwargs)
            
        return time_profiling_results.TimeProfilerResult(
            profiler=self,
            profiled_func=func,
            func_args=None,
            func_kwargs=kwargs,
            func_result=profiling_result if not time_profiler_manager.exception else None,
            func_execution_time=time_profiler_manager.func_execution_time,
            func_exception=time_profiler_manager.func_exception
            )
        
    def __repr__(self) -> str:
        return f'TimeProfiler(profiling_timer={self.profilig_timer})'
        
    
class ThreadBasedTimeProfiler(TimeProfilerI):
    """Thread-based time profiler using the time module."""
    
    @classmethod
    @ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    @override
    def profile(cls, func: BuiltinFunctionType | FunctionType, **kwargs) -> time_profiling_results.TimeProfilerResult:
        """Profile the execution time of a function in a separate thread."""
        with TimeProfilerManager(profiling_timer=time.time) as time_profiler_manager:
            thread = threading.Thread(target=func, kwargs=kwargs)
            thread.start()
            thread.join()
            
        return time_profiling_results.TimeProfilerResult(
            profiler=cls,
            profiled_func=func,
            func_args=None,
            func_kwargs=kwargs,
            func_result=None,
            func_execution_time=time_profiler_manager.func_execution_time,
            func_exception=time_profiler_manager.func_exception
            )