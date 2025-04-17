"""Time profiling decorators."""

from abc import ABC, abstractmethod
import functools
import enum
from typing import Type, ClassVar, Callable
import time
from types import BuiltinFunctionType, FunctionType

import pydantic

from python_profiling import python_profiling_enums
from python_profiling import python_profiling_configs
from python_profiling.time_profiling import time_profiler as time_profiler_
from python_profiling.time_profiling import timeit_profiler
from python_profiling.time_profiling import time_profiling_results
from python_profiling.time_profiling import line_time_profiler
from python_profiling.time_profiling import call_graph_time_profiler
from Internals import checks
from Internals import observers
from Internals.logger import logger


class BaseProfilingDecorator:
    """Provides shared functionality for all profiling decorators."""
    
    @checks.ValidateType(
        [
            ('storages', python_profiling_configs.StorageConfig), 
            ('observer', observers.ProfilingObserverI)
            ]
        )
    def _init_observer(
        self, 
        storages: python_profiling_configs.StorageConfig, 
        observer:  observers.ProfilingObserverI
        ):
        """Validate storagest, observer types, if correct initialize observer instance.
        
        Raises:
            InvalidInputType: If storages or observer of incorrect type.
        """
        self.observer = observer(storages=storages)
    
    @staticmethod
    def base_profiling__call__(func: Callable, profiling_func: Callable, observing_func: Callable):
        """Decorator for profiling and storing profiling results.
        
        Args:
            func (Callable): The original function to decorate.
            profiling_func (Callable): A profiling function that wraps the target function.
             observing_func (Callable): A function that handles storing of profiling result.
             
        Returns:
            Callable: A wrapped function that runs profiling and stores the result.
        """
        @functools.wraps(func)
        def wrapper(**kwargs) -> Callable:
            """Profile provided function and stores profiling result.
            
            Args:
            **kwargs: Keyword arguments to pass to the function.
            
            Returns:
                object: Structured profiling result returned by the profiling function.
            """
            result = profiling_func(func=func, **kwargs)
            observing_func(result)
            return result
        return wrapper


class TimeProfilingDecoratorI(ABC):
    """Interface for time profiling decorators."""
    
    _avaliable_time_profilers: ClassVar[dict] = {}
    
    @abstractmethod
    def __call__(self, func: Callable) -> Callable:
        ...
        
    @abstractmethod
    def _add_profiler(self, profiler_name: enum.Enum, profiler: Type):
        ...
       
    @abstractmethod
    def change_profiler(self, profiler_name: enum.Enum) -> None:
        ...
        
    @classmethod
    def avaliable_profilers(cls):
        """Returns the currently registered time profilers."""
        return cls._avaliable_time_profilers
    
    @classmethod
    def _remove_profiler(cls, profiler_name: python_profiling_enums.TimeProfilerStrategy) -> None:
        """Removes time profiler from the registry."""
        if profiler_name in cls._avaliable_time_profilers:
            del cls._avaliable_time_profilers[profiler_name]
            logger.info('%s has been removed', profiler_name)
    
class TimeProfilerDecorator(pydantic.BaseModel, TimeProfilingDecoratorI, BaseProfilingDecorator):
    """Decorator for time profiling with time module.
    
    Attributes:
        time_profiler_strategy (TimeProfilerStrategy): Time profiling strategy to perform profilng.
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
        time_profiler (TimeProfilerI): Time profiler based on time module.
        obaserver (ProfilingObserver): A class that responsible for storing profiling result to 
        multiple sources.
    """
    
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    
    _avaliable_time_profilers: ClassVar[dict[python_profiling_enums.TimeProfilerStrategy, time_profiler_.TimeProfilerI]] = {
        python_profiling_enums.TimeProfilerStrategy.BASIC: time_profiler_.TimeProfiler(profiling_timer=time.time),
        python_profiling_enums.TimeProfilerStrategy.PRECISE: time_profiler_.TimeProfiler(profiling_timer=time.perf_counter),
        python_profiling_enums.TimeProfilerStrategy.CPU: time_profiler_.TimeProfiler(profiling_timer=time.process_time),
        python_profiling_enums.TimeProfilerStrategy.THREAD_BASED: time_profiler_.ThreadBasedTimeProfiler,
        python_profiling_enums.TimeProfilerStrategy.MONOTONIC: time_profiler_.TimeProfiler(profiling_timer=time.monotonic)
    }
    
    time_profiler_strategy: python_profiling_enums.TimeProfilerStrategy = pydantic.Field(default=python_profiling_enums.TimeProfilerStrategy.BASIC)
    storages: python_profiling_configs.StorageConfig = pydantic.Field(default_factory=python_profiling_configs.StorageConfig)
    time_profiler: time_profiler_.TimeProfilerI = pydantic.Field(init=False, default=None)
    observer: observers.ProfilingObserverI = pydantic.Field(init=False, default=None)
    
    def model_post_init(self, __context):
        """Setup time profiler and observer based on provided profiling stragedy and storages."""
        self.time_profiler = self._avaliable_time_profilers[self.time_profiler_strategy]
        self.observer = observers.ProfilingObserver(storages=self.storages)
        
    @classmethod
    @checks.ValidateType(
        [
            ('profiler_name', python_profiling_enums.TimeProfilerStrategy), 
            ('profiler', time_profiler_.TimeProfilerI)
            ]
        )
    def _add_profiler(cls, profiler_name: python_profiling_enums.TimeProfilerStrategy, profiler: time_profiler_.TimeProfilerI):
        """Registers a new time profiler into the available time profilers registry.
        
        Args:
            profiler (TimeProfilerI): A class that inherits from `TimeProfilerI` and provides
                                    a concrete implementation for time profiling.
            profiler_name (python_profiling_enums.TimeProfilerStrategy): Name to register time profiler under.
            
        Returns:
            None
            
        Raises:
            InvalidInputTypeError: If profiler or profiler are of incorrect types.
            MissingArgumentError: If any required argument is missing.
        """
        cls._avaliable_time_profilers[profiler_name] = profiler
        logger.info('%s has been added as %s', profiler, profiler_name)
        
    @checks.ValidateType(('profiler_name', python_profiling_enums.TimeProfilerStrategy))
    def change_profiler(self, profiler_name: python_profiling_enums.TimeProfilerStrategy) -> None:
        """Change time profiling strategy."""
        self.time_profiler = self._avaliable_time_profilers[profiler_name]
        
    def __call__(self, func: Callable) -> Callable:
        return self.base_profiling__call__(
            func=func,
            profiling_func=self.time_profiler.profile,
            observing_func=self.observer.dump
            )
        
class TimeItProfilerDecorator(BaseProfilingDecorator):
    """Decorator for time profiling with timeit module.
    
    Attributes:            
        timer (FunctionType | BuiltinFunctionType): Timer function used for profiling.
        number (int): Number of times to execute the function per repeat.
        repeat (int): Number of repetitions to run.
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
        time_profiler (TimeProfilerI): Time profiler based on time module.
        obaserver (ProfilingObserver): A class that responsible for storing profiling result to.
        multiple sources.
    """
    
    def __init__(
        self, 
        timer: FunctionType | BuiltinFunctionType = time.perf_counter,
        number: int = 10000,
        repeat: int = 1,
        storages: python_profiling_configs.StorageConfig = python_profiling_configs.StorageConfig,
        observer: observers.ProfilingObserverI = observers.ProfilingObserver
        ):
        self.time_profiler = timeit_profiler.TimeItProfiler(timer=timer,
                                                            number=number,
                                                            repeat=repeat)
        self._init_observer(storages=storages, observer=observer)
        
    def __call__(self, func: Callable) -> Callable:
        return self.base_profiling__call__(
            func=func,
            profiling_func=self.time_profiler.profile,
            observing_func=self.observer.dump
            )
        
class LineTimeProfilerDecorator(BaseProfilingDecorator):
    """Decorator for time profiling with line_profiler module.
    
    Attributes:
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
        obaserver (ProfilingObserver): A class that responsible for storing profiling result to.

    """
    def __init__(
        self, 
        storages: python_profiling_configs.StorageConfig = python_profiling_configs.StorageConfig, 
        observer: observers.ProfilingObserverI = observers.ProfilingObserver
        ):
        self._init_observer(storages=storages,observer=observer)
        
    def __call__(self, func: Callable) -> Callable:
        return self.base_profiling__call__(
            func=func,
            profiling_func=line_time_profiler.LineTimeProfiler.profile,
            observing_func=self.observer.dump
        )
        
class CallGraphTimeProfilerDecorator(BaseProfilingDecorator):
    """Decorator for time profiling with line_profiler module.
    
    Attributes:
        sort_key (str): Metric to sort by (e.g., 'cumulative', 'time', etc.).
        func_filter (str | None): Optional function name to filter profiling output.
        top_n (int): Number of top entries to show in the profiling output.
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
        obaserver (ProfilingObserver): A class that responsible for storing profiling result to.
        
    Raises:
        ValidationError: If sort_key, func_filter, top_n has incorrect type.
        InvalidInputError: If storages or observer has incorrect type.
    """
    def __init__(
        self, 
        sort_key: str = 'cumulative', 
        func_filter: str = '', 
        top_n: int = 10,
        storages: python_profiling_configs.StorageConfig = python_profiling_configs.StorageConfig(),
        observer:  observers.ProfilingObserverI =  observers.ProfilingObserver
        ):
        self.sort_key = sort_key
        self.func_filter = func_filter
        self.top_n = top_n
        self._init_observer(storages=storages, observer=observer)
        self.profiler = call_graph_time_profiler.CallGraphTimeProfiler(sort_key=self.sort_key,
                                                                       func_filter=self.func_filter,
                                                                       top_n=self.top_n)
        
    def __call__(self, func: Callable) -> Callable:
        return self.base_profiling__call__(
            func=func,
            profiling_func=self.profiler.profile,
            observing_func=self.observer.dump
        )
        
    
    
    