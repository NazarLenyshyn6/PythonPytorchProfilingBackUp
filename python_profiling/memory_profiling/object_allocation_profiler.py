"""Memory Profiling of Python functions with pympler module.

Tracking live object graphs, memory growth over time, and type-specific memory usage.
"""

from types import BuiltinFunctionType, FunctionType
from typing import Any

import pympler
import pympler.asizeof


from python_profiling.memory_profiling import memory_profiling_results
from Internals import checks
from Internals import context_managers


class ObjectAllocationProfiler:   
    """ Tracks live object graphs, memory growth over time, and type-specific memory usage with pympler module."""
    
    def __repr__(self):
        return f'ObjectAllocationProfiler()'
     
    @classmethod
    @checks.ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    def profile(cls, func: BuiltinFunctionType | FunctionType, **kwargs):
        """Profile memory allocation before and after function exection.
        
        Args:
            func: Profiled function.
            **kwargs:  Keyword arguments to pass to the function.
            
        Returns:
            ObjectAllocationProfilerResult:  Structured profiling result.
            
        Raises:
            InvalidInputTypeError: If the function is not of the correct type.
        """
        with context_managers.ObjectAllocationProfilerManager() as object_allocation_profiler_manager:
            func_result = func(**kwargs)
        return memory_profiling_results.ObjectAllocationProfilerResult(
            profiler=ObjectAllocationProfiler,
            profiled_func=func,
            func_kwargs=kwargs,
            func_result=func_result if not object_allocation_profiler_manager.exception else None,
            tracker=object_allocation_profiler_manager.tracker,
            before_memory_allocation=object_allocation_profiler_manager.before_memory_allocation,
            after_memory_allocation=object_allocation_profiler_manager.after_memory_allocation,
            func_exception=object_allocation_profiler_manager.func_exception
            )
        
        