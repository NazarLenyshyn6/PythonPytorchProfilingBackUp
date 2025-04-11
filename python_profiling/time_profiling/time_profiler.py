import time, threading
from abc import ABC, abstractmethod
from types import BuiltinFunctionType, FunctionType
from python_profiling.time_profiling.time_profiling_results import TimeProfilerResult
from Internals.context_managers import TimeProfilerManager
from Internals.checks import ValidateType
from typing import Callable


# Implementation of Time Profiler Interface
class TimeProfilerI(ABC):
    @abstractmethod
    def profile(cls, func: BuiltinFunctionType |  FunctionType, **kwargs) -> TimeProfilerResult:
        ...
        
        
# Implementation of Time Profiler
class TimeProfiler(TimeProfilerI):
    def __init__(self, profiling_timer: Callable):
        self.profilig_timer = profiling_timer
        
    @ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    def profile(self, func: BuiltinFunctionType | FunctionType, **kwargs) -> TimeProfilerResult:
        
        with TimeProfilerManager(profiling_timer=self.profilig_timer) as time_profiler_manager:
            profiling_result = func(**kwargs)
            
        return TimeProfilerResult(profiler=self,
                                  profiled_func=func,
                                  func_args=None,
                                  func_kwargs=kwargs,
                                  func_result=profiling_result if not time_profiler_manager.exception else None,
                                  func_execution_time=time_profiler_manager.func_execution_time,
                                  func_exception=time_profiler_manager.func_exception)
        
    def __repr__(self) -> str:
        return f'TimeProfiler(profiling_timer={self.profilig_timer})'
        
    
# Implementation of Thread Base Time Profiler
class ThreadBasedTimeProfiler(TimeProfilerI):
    @classmethod
    @ValidateType(('func', (BuiltinFunctionType, FunctionType)))
    def profile(cls, func: BuiltinFunctionType | FunctionType, **kwargs) -> TimeProfilerResult:
        
        with TimeProfilerManager(profiling_timer=time.time) as time_profiler_manager:
            thread = threading.Thread(target=func, kwargs=kwargs)
            thread.start()
            thread.join()
            
        return TimeProfilerResult(profiler=cls,
                                  profiled_func=func,
                                  func_args=None,
                                  func_kwargs=kwargs,
                                  func_result=None,
                                  func_execution_time=time_profiler_manager.func_execution_time,
                                  func_exception=time_profiler_manager.func_exception)