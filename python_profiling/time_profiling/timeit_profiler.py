"""Time Profiling of Python functions with timeit module."""

import timeit
import time
from types import FunctionType, BuiltinFunctionType

from pydantic import BaseModel, ConfigDict, Field

from Internals.checks import ValidateType
from python_profiling.time_profiling.time_profiling_results import TimeItProfilerResult
from Internals.context_managers import TimeItProfilerManager


class TimeItProfiler(BaseModel):
    """Time profiler that uses a specified timer from the time module and timeit module.
    
    Attributes:
        timer (FunctionType | BuiltinFunctionType): .
        number (int): Number of times to execute the function per repeat.
        repeat (int): Number of repetitions to run.
    """
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    timer: FunctionType | BuiltinFunctionType = Field(default=time.perf_counter)
    number: int = Field(default=10000)
    repeat: int = Field(default=1)
    
    def _get_time_profiler(self, func: FunctionType | BuiltinFunctionType, kwargs: dict) -> timeit.Timer:
        return timeit.Timer(stmt=lambda : func(**kwargs), timer=self.timer)
    
    @staticmethod
    def _profiling_stats(profiling_result: list[int | float]):
        return min(profiling_result), sum(profiling_result) / len(profiling_result), max(profiling_result)

    
    @ValidateType(('func', (FunctionType, BuiltinFunctionType)))
    def profile(self, func: FunctionType | BuiltinFunctionType ,**kwargs) -> TimeItProfilerResult:
        """Profile the execution time of a function.
        
        Args:
            func (BuiltinFunctionType | FunctionType): Function to profile.
            **kwargs:  Keyword arguments to pass to the function.
        Returns:
            TimeItProfilerResult:  Structured profiling result.
            
        Raises:
            InvalidInputTypeError: If the function is not of the correct type.
        """
        
        with TimeItProfilerManager() as time_profiler_manager:
            time_profiler = self._get_time_profiler(func, kwargs)
            func_result = func(**kwargs)
            profiling_result = time_profiler.repeat(repeat=self.repeat, number=self.number)
            func_profiling_stats= self._profiling_stats(profiling_result)
            
        if time_profiler_manager.exception:
            func_result = None
            func_profiling_stats = (-1,-1,-1)
            
        return TimeItProfilerResult(
            profiler=self,
            profiled_func=func,
            func_kwargs=kwargs,
            func_result=func_result,
            repeats=self.repeat,
            min_func_execution_time=func_profiling_stats[0],
            avg_func_execution_time=func_profiling_stats[1],
            max_func_execution_time=func_profiling_stats[2],
            func_exception=time_profiler_manager.func_exception
            )
    
    def __repr__(self):
        return f'TimeItProfiler(timer={self.timer}, number={self.number}, repeat={self.repeat})'
