"""Line by line memory profiling with memory_profiler module."""

from typing import Literal
from types import BuiltinFunctionType, FunctionType

import memory_profiler
import pydantic

from python_profiling.memory_profiling import memory_profiling_results
from Internals import checks
from Internals import context_managers

class LineMemoryProfiler(pydantic.BaseModel):
    """.
    
    Attributes:
        interval: The time interval (in seconds) between consecutive memory measurements.
        timeout: Specifies the maximum duration (in seconds) to collect memory measurements. 
            If exceeded, measurement is terminated.
        backed: Etermines the backend method for acquiring memory usage data.
        include_children: If True, includes memory usage of all child processes 
        
    Raises:
        ValidationError: If attribute of wrong type.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    
    interval: int | float = pydantic.Field(default=0.2)
    timeout: int = pydantic.Field(default=5)
    backed: Literal['psutil', 'ps'] = pydantic.Field(default='psutil')
    include_children: bool = pydantic.Field(default=True)
    
    @staticmethod
    def _get_memory_stats(memory: list[float | int]) -> tuple[float | int]:
        """Extract start, end, peak memory, max memory increase from provide memory usage list."""
        start_memory = memory[0]
        peak_memory = max(memory)
        end_memory = memory[-1]
        max_memory_increase = peak_memory - start_memory
        return start_memory, peak_memory, end_memory, max_memory_increase
    
    @checks.ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    def profile(self, func: BuiltinFunctionType | FunctionType, **kwargs):
        """Profile Memory usage over time during function execution.
        
        Args:
            func: Profiled function.
            **kwargs:  Keyword arguments to pass to the function.
            
        Returns:
            LineMemoryProfilerResult:  Structured profiling result.
            
        Raises:
            InvalidInputTypeError: If the function is not of the correct type.
        """
        with context_managers.LineMemoryProfilerManager() as line_memory_profiler_manager:
            memory, func_result = memory_profiler.memory_usage(
                (func, (), kwargs), 
                interval=self.interval,
                timeout=self.timeout,
                backend=self.backed,
                retval=True,
                include_children=self.include_children,
                )
        if line_memory_profiler_manager.exception:
            start_memory, peak_memory, end_memory, max_memory_increase, memory = 0, 0, 0, 0, []
        else:
            start_memory, peak_memory, end_memory, max_memory_increase = self._get_memory_stats(memory)
        return memory_profiling_results.LineMemoryProfilerResult(
            profiler=LineMemoryProfiler,
            profiled_func=func,
            func_kwargs=kwargs,
            func_result=func_result if not line_memory_profiler_manager.exception else None,
            start_memory=start_memory,
            peak_memory=peak_memory,
            end_memory=end_memory,
            max_memory_increase=max_memory_increase,
            memory_timeline=memory,
            func_exception=line_memory_profiler_manager.func_exception
            )
