"""Call graph time profiling  of Python function with cProfile and pstats modules."""

import io
import os
from types import BuiltinFunctionType, FunctionType
from typing import Literal

import pydantic
import pstats

from python_profiling.time_profiling import time_profiling_results
from Internals import checks
from Internals import context_managers
from Internals.logger import logger


class CallGraphTimeProfiler(pydantic.BaseModel):
    """Call graph time profiler using cProfile and pstats.

    Attributes:
        sort_key (str): Metric to sort by (e.g., 'cumulative', 'time', etc.).
        func_filter (str | None): Optional function name to filter profiling output.
        top_n (int): Number of top entries to show in the profiling output.
    """
    
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    
    sort_key: Literal['time', 'cumulative', 'calls', 'name', 'file', 'line']  = pydantic.Field(default='cumulative')
    func_filter: str | None = pydantic.Field(default=None)
    top_n : int =  pydantic.Field(default=10)
    
    def _profile_to_string(self, profile_file: str):
        """Load profiling result and output as a string.
        
        Args:
            profile_file: File with profiling result.
            
        Returns:
            str: Profiling result in string format.
        """
        buf = io.StringIO()
        stats = pstats.Stats(profile_file, stream=buf)
        stats.strip_dirs().sort_stats(self.sort_key)
        stats.print_stats(self.top_n)
        if self.func_filter:
            stats.print_callers(self.func_filter)
            stats.print_callees(self.func_filter)
        return buf.getvalue()
 
    @checks.ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    def profile(
        self, 
        func: BuiltinFunctionType | FunctionType, 
        **kwargs
        ) -> time_profiling_results.CallGraphTimeProfilerResult:
        """Profile function execution call graph.
        
        Args:
            func (BuiltinFunctionType | FunctionType): Function to profile.
            **kwargs: Keyword arguments to pass to the function.
            
        Returns:
            CallGraphTimeProfilerResult: Structured profiling result.
        
        Raises:
            InvalidInputTypeError: If the function is not of the correct type.
        """
        with context_managers.CallGraphTimeProfilerManager() as call_graph_profiling_manager:
            func_result = func(**kwargs)
            
        if not call_graph_profiling_manager.exception:
            profiling_result = self._profile_to_string(context_managers.CALL_GRAPH_PROFILING_RESULT_FILE)
            os.remove(context_managers.CALL_GRAPH_PROFILING_RESULT_FILE)
            
        return time_profiling_results.CallGraphTimeProfilerResult(
            profiler=self,
            profiled_func=func,
            func_kwargs=kwargs,
            func_result=func_result if not call_graph_profiling_manager.exception else None,
            func_profiling_result=profiling_result if not call_graph_profiling_manager.exception else None,
            func_exception=call_graph_profiling_manager.func_exception
            )
            
        
            