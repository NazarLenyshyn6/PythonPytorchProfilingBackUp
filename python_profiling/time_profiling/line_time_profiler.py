"""Time profiling of Python functions with line_profiler module."""

import io
from types import BuiltinFunctionType, FunctionType

import line_profiler

from python_profiling.time_profiling import time_profiling_results
from Internals import checks
from Internals import context_managers


class LineTimeProfiler:
    """Time profiler based on line_profile module."""
    
    @staticmethod
    def _init_line_profiler():
        """Initialize new instance ot LineProfiler class."""
        return line_profiler.LineProfiler()
    
    @staticmethod
    def _get_profiling_result(line_profiler_: line_profiler.LineProfiler) -> str:
        """ Returns the line-by-line profiling results as a string.
        
        Args:
			line_profiler_ (LineProfiler): Instance of LineProfiler class.
   
		Returns:
			str: A formatted string containing the profiling statistics.
        """
        stream = io.StringIO()
        line_profiler_.print_stats(stream=stream)
        return stream.getvalue()
        
    @classmethod
    @checks.ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    def profile(
        self, 
        func: BuiltinFunctionType | FunctionType,
        **kwargs
        ) -> time_profiling_results.LineTimeProfilerResult:
        """Profile the execution time of a function.
        
        Args:
            func (BuiltinFunctionType | FunctionType): Function to profile.
            **kwargs:  Keyword arguments to pass to the function.
        Returns:
            LineTimeProfilerResult:  Structured profiling result.
            
        Raises:
            InvalidInputTypeError: If the function is not of the correct type.
        """
        line_profiler_ = self._init_line_profiler()
        
        with context_managers.LineTimeProfilerManager(line_profiler_=line_profiler_, profiled_func=func) as line_time_profiler_manager:
            profiling_result = func(**kwargs)
        
        return time_profiling_results.LineTimeProfilerResult(
            profiler=self,
            profiled_func=func,
            func_kwargs=kwargs,
            func_result=profiling_result if not line_time_profiler_manager.exception else None,
            func_profiling_result=self._get_profiling_result(line_profiler_),
            func_exception=line_time_profiler_manager.func_exception
            )