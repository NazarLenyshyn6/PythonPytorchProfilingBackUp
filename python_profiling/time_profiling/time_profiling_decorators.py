"""Time profiling decorators."""

from abc import ABC, abstractmethod
from functools import wraps
from enum import Enum
from typing import Type

from pydantic import BaseModel, ConfigDict, Field

from python_profiling.enums import TimeProfilerStrategy, SerializerStrategy
from python_profiling.configs import StorageConfig
from python_profiling.time_profiling.time_profiler import *
from python_profiling.time_profiling.timeit_profiler import TimeItProfiler
from typing import ClassVar, Callable

from Internals.checks import ValidateType
from Internals.observers import ProfilingObserver
from Internals.logger import logger


class TimeProfilingDecoratorI(ABC):
    """Interface for time profiling decorators.
    
    Args:
        _avaliable_time_profilers (ClassVar[dict]): .
    """
    
    _avaliable_time_profilers: ClassVar[dict] = {}
    
    @abstractmethod
    def __call__(self, func: Callable) -> Callable:
        ...
        
    @abstractmethod
    def _add_profiler(self, profiler_name: Enum, profiler: Type):
        ...
       
    @abstractmethod
    def change_profiler(self, profiler_name: Enum) -> None:
        ...
        
    @classmethod
    def avaliable_profilers(cls):
        return cls._avaliable_time_profilers
    
    @classmethod
    def _remove_profiler(cls, profiler_name: Enum):
        if profiler_name in cls._avaliable_time_profilers:
            del cls._avaliable_time_profilers[profiler_name]
            logger.info('%s has been removed', profiler_name)
    
class TimeProfilerDecorator(BaseModel, TimeProfilingDecoratorI):
    """Decorator for time profilin with time module"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    _avaliable_time_profilers: ClassVar[dict[TimeProfilerStrategy, TimeProfilerI]] = {
        TimeProfilerStrategy.BASIC: TimeProfiler(profiling_timer=time.time),
        TimeProfilerStrategy.PRECISE: TimeProfiler(profiling_timer=time.perf_counter),
        TimeProfilerStrategy.CPU: TimeProfiler(profiling_timer=time.process_time),
        TimeProfilerStrategy.THREAD_BASED: ThreadBasedTimeProfiler,
        TimeProfilerStrategy.MONOTONIC: TimeProfiler(profiling_timer=time.monotonic)
    }
    
    time_profiler_strategy: TimeProfilerStrategy = Field(default=TimeProfilerStrategy.BASIC)
    storages: StorageConfig = Field(default_factory=StorageConfig)
    time_profiler: TimeProfilerI = Field(init=False, default=None)
    observer: ProfilingObserver = Field(init=False, default=None)
    
    
    def model_post_init(self, __context):
        self.time_profiler = self._avaliable_time_profilers[self.time_profiler_strategy]
        self.observer = ProfilingObserver(storages=self.storages)
        
    
    @classmethod
    @ValidateType([('profiler_name', TimeProfilerStrategy), ('profiler', TimeProfilerI)])
    def _add_profiler(cls, profiler_name: TimeProfilerStrategy, profiler: TimeProfilerI):
        cls._avaliable_time_profilers[profiler_name] = profiler
        logger.info('%s has been added as %s', profiler, profiler_name)
        
        
    @ValidateType(('profiler_name', TimeProfilerStrategy))
    def change_profiler(self, profiler_name):
        self.time_profiler = self._avaliable_time_profilers[profiler_name]
        
        
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(**kwargs):
            result = self.time_profiler.profile(func=func, **kwargs)
            self.observer.dump(result)
            return result
        return wrapper
    
    
    
class TimeItProfilerDecorator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    timer: FunctionType | BuiltinFunctionType = Field(default=time.perf_counter)
    number: int = Field(default=10000)
    repeat: int = Field(default=1)
    storages: StorageConfig = Field(default_factory=StorageConfig)
    time_profiler: TimeItProfiler = Field(init=False, default=None)
    observer: ProfilingObserver = Field(init=False, default=None)
    
    
    def model_post_init(self, __context):
        self.time_profiler = TimeItProfiler(timer=self.timer,
                                            number=self.number,
                                            repeat=self.repeat)
        
        self.observer = ProfilingObserver(storages=self.storages)
    
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(**kwargs):
            result = self.time_profiler.profile(func=func, **kwargs)
            self.observer.dump(result)
            return result
        return wrapper