"""Memory Profiling of Python functions with tracemalloc module."""

import tracemalloc
from types import BuiltinFunctionType, FunctionType
from typing import Literal

import pydantic

from python_profiling import _base_profiling_result
from python_profiling.memory_profiling import memory_profiling_results
from Internals import checks
from Internals import context_managers


class PeakMemoryProfiler(pydantic.BaseModel):
    """Profile peak memory allocation during function execution.
    
    Attributes:
        nframes: Number of stack frames to include in each memory trace.
        key_type: Sorting method for snapshot comparisons.
        top_n: .
        
    Raises:
        ValidationError: If attribute of wrong type.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    
    nframes: int = pydantic.Field(default=1, ge=0)
    key_type: Literal['lineno', 'filename', 'traceback']  = pydantic.Field(default='lineno')
    top_n: int = pydantic.Field(default=5)
    
    @checks.ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    def profile(self, func: BuiltinFunctionType | FunctionType, **kwargs):
        """Profile peak memory allocation, memory differences, allocation by traceback during function exection.
        
        Args:
            func: Profiled function.
            **kwargs:  Keyword arguments to pass to the function.
            
        Returns:
            PeakMemoryProfilerResult:  Structured profiling result.
            
        Raises:
            InvalidInputTypeError: If the function is not of the correct type.
        """
        with context_managers.PeakMemoryProfilerManager(self.nframes)  as  peak_memory_profiler_manager:
            func_result =  func(**kwargs)
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        return memory_profiling_results.PeakMemoryProfilerResult(
            top_n=self.top_n,
            key_type=self.key_type,
            profiler=PeakMemoryProfiler,
            profiled_func=func,
            func_kwargs=kwargs,
            func_result=func_result if not peak_memory_profiler_manager.exception else None,
            current_memory=current_memory,
            peak_memory=peak_memory,
            allocation_before=peak_memory_profiler_manager.allocation_before,
            allocation_after=peak_memory_profiler_manager.allocation_after,
            func_exception=peak_memory_profiler_manager.func_exception
            )
    
    
    
    