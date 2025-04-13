import timeit
from functools import wraps
from dataclasses import dataclass
from typing import Callable


class BaseManager:
    @staticmethod
    def handle_exception(self, exc_type, exc_value):
        self.exception = True if exc_type else False
        self.func_exception = exc_type if exc_type else None
            

# Implementation of context manager for Time Profiler
class TimeProfilerManager:
    def __init__(self, profiling_timer):
        self.profiling_timer = profiling_timer
    
    def __enter__(self) -> 'TimeProfilerManager':
        self.profiling_start = self.profiling_timer()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.profiling_stop = self.profiling_timer()
        self.func_execution_time = self.profiling_stop - self.profiling_start
        BaseManager.handle_exception(self, exc_type, exc_value)
        
        return True
    
    def __repr__(self) -> str:
        return f'fTimeProfilingManager(profiling_timer={self.profiling_timer})'
    
    
# Implementation of context manager for TimeIt Profiler
class TimeItProfilerManager:        
    def __enter__(self) -> 'TimeItProfilerManager':
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        BaseManager.handle_exception(self, exc_type, exc_value)
    
        return True