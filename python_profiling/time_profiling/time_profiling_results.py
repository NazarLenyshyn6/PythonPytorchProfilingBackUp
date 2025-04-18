"""Structured time profiling results."""

from dataclasses import dataclass
from typing import Any, Type
from types import BuiltinFunctionType, FunctionType


from python_profiling import _base_profiling_result
from python_profiling import python_profiling_enums
from Internals import checks
from Internals import serialization
from Internals.logger import logger

   
@dataclass
class TimeProfilerResult(_base_profiling_result.BaseProfilingResult):
    """Structured profiling result for time profiling with time module.
    
    Attributes:
        profiler: A class implementing TimeProfilerI.
        profiled_func: Profiled function.
        func_args: Arguments of profiled function.
        func_kwargs: Keyword arguments of profiled funciton.
        func_result: Profiled function result.
        func_execution_time: Profiled function execution time.
        func_exception: Exception raised during execution, if any.
    """
    
    profiler: Type
    profiled_func: BuiltinFunctionType | FunctionType
    func_args: tuple
    func_kwargs: dict
    func_result: Any
    func_execution_time: int | float
    func_exception: str | None = None
    
    
    def __str__(self) -> str:
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Args: {self.func_args}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Function Executions Time: {self.func_execution_time:.6f} seconds\n"
                f"Function Exception: {self.func_exception or 'None'}")
        
    def __repr__(self) -> str:
        return f'TimeProfilerResult(profiler={self.profiler.__class__.__name__}, profiled_func={self.profiled_func.__name__})'
        
        
@dataclass
class TimeItProfilerResult(_base_profiling_result.BaseProfilingResult):
    """Structured profiling result for time profiling with timeit module.
    
    Args:
        profiler: An instance of TimeItProfiler.
        profiled_func: Profiled function.
        func_kwargs: Keyword arguments of profiled funciton.
        func_result: Profiled function result.
        repeat: Number of repetitions in the timeit loop.
        min_func_execution_time: Minimum execution time.
        avg_func_execution_time: Average execution time.
        max_func_execution_time:  Maximum execution time.
        func_exception: Exception raised during execution, if any.
    """
    
    profiler: Type
    profiled_func: BuiltinFunctionType | FunctionType
    func_kwargs: dict
    func_result: Any
    repeats: int
    min_func_execution_time: int | float
    avg_func_execution_time: int | float
    max_func_execution_time: int | float
    func_exception: str | None = None
    
    
    def __str__(self) -> str:
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Function Min Executions Time: {self.min_func_execution_time:.6f} seconds\n"
                f"Function Avg of {self.repeats} Executions Time: {self.avg_func_execution_time:.6f} seconds\n"
                f"Function Max Executions Time: {self.max_func_execution_time:.6f} seconds\n"
                f"Function Exception: {self.func_exception or 'None'}")
        
    def __repr__(self) -> str:
        return f'TimeItProfilerResult(profiler={self.profiler.__class__.__name__}, profiled_func={self.profiled_func})'
    
@dataclass
class LineTimeProfilerResult(_base_profiling_result.BaseProfilingResult):
    """Structured profiling result for time profiling with line_profiler module.
    
    Attributes:
        profiler: An instance of LineProfiler.
        profiled_func: Profiled function.
        func_kwargs: Keyword arguments of profiled function.
        func_result: Profiled function result.
        func_profiling_result: Structured profiling result.
        func_exception: Exception raised during execution, if any.
    """
    
    profiler: Type
    profiled_func: BuiltinFunctionType | FunctionType
    func_kwargs: dict
    func_result: Any
    func_profiling_result: str | None
    func_exception: str | None = None
    
    def __str__(self) -> str:
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Function Profiling Result: {self.func_profiling_result}\n"
                f"Function Exceptions: {self.func_exception}")
        
    def __repr__(self) -> str:
        return f'LineTimeProfilerResult(profiler={self.profiler.__class__.__name__}, profiled_func={self.profiled_func})'
    
    
@dataclass
class CallGraphTimeProfilerResult(_base_profiling_result.BaseProfilingResult):
    """Structured profiling result for time profiling with call_graph_time_profiler module.
    
    Attributes:
        profiler: An instance of LineProfiler.
        profiled_func: Profiled function.
        func_kwargs: Keyword arguments of profiled function.
        func_result: Profiled function result.
        func_profiling_result: Structured profiling result.
        func_exception: Exception raised during execution, if any.
    """
    
    
    profiler: Type
    profiled_func: BuiltinFunctionType | FunctionType
    func_kwargs: dict
    func_result: Any
    func_profiling_result: str | None
    func_exception: str |  None  = None
    
    def __str__(self) -> str:
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Function Profiling Result: {self.func_profiling_result}\n"
                f"Function Exceptions: {self.func_exception}")
        
    def __repr__(self) -> str:
        return f"CallGrapthTimeProfilerResult(profiler={self.profiler.__class__.__name__}, profiled_func={self.profiled_func})"
    