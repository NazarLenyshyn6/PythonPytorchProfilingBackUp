"""Structured call graph profiling results."""

from typing import Type, Callable, Any
from types import BuiltinFunctionType, FunctionType

from dataclasses import dataclass

from python_profiling import _base_profiling_result

@dataclass
class CallGraphProfilerResult(_base_profiling_result.BaseProfilingResult):
    """Structured profiling result for call graph profiling.
    
    Attributes:
        profiler: A class implementing CallGraphProfilerI.
        profiled_func: Profiled function.
        func_kwargs: Keyword arguments of profiled funciton.
        func_result: Profiled function result.
        output_file: file with call graph profiling result.
        func_exception: Exception raised during execution, if any.
    """
    profiler: Type
    profiled_func: BuiltinFunctionType | FunctionType
    func_kwargs: dict
    func_result: Any
    output_file: str
    func_exception: Any | None = None
    
    def __str__(self) -> str:
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Output file: {self.output_file}\n"
                f"Function Exception: {self.func_exception or 'None'}")
        
    def __repr__(self) -> str:
        return f'CallGraphProfilerResult(profiler={self.profiler.__class__.__name__}, profiled_func={self.profiled_func.__name__})'