"""Memory profiling decorators."""

from typing import Callable

from python_profiling.memory_profiling import peak_memory_profiler
from python_profiling.memory_profiling import object_allocation_profiler
from python_profiling import _base_profiling_decorators
from python_profiling import python_profiling_configs
from Internals import observers

class PeakMemoryProfilerResultDecorator(_base_profiling_decorators.BaseProfilingDecorator):
    """Decorator for memory profiling with tracemalloc module.
    
    Profile peak memory allocation during function execution.
    
    Attributes:
        nframes: Number of stack frames to include in each memory trace.
        key_type: Sorting method for snapshot comparisons.
        top_n: .
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
        obaserver (ProfilingObserver): A class that responsible for storing profiling result to.
        
    Raises:
        ValidationError: If sort_key, func_filter, top_n has incorrect type.
        InvalidInputError: If storages or observer has incorrect type.
    """
    def __init__(
        self, 
        nframes: int = 1,
        key_type: str = 'lineno',
        top_n: int = 5,
        storages: python_profiling_configs.StorageConfig = python_profiling_configs.StorageConfig(), 
        observer: observers.ProfilingObserverI = observers.ProfilingObserver
        ):
        self._init_observer(storages=storages, observer=observer)
        self.memory_profiler = peak_memory_profiler.PeakMemoryProfiler(nframes=nframes,
                                                                       key_type=key_type,
                                                                       top_n=top_n)
        
    def __call__(self, func: Callable):
        return self.base_profiling__call__(
            func=func,
            profiling_func=self.memory_profiler.profile,
            observing_func=self.observer.dump
            )
        
        
class ObjectAllocationProfilerDecorator(_base_profiling_decorators.BaseProfilingDecorator):
    """Decorator for memory profiling with pympler module.
    
    Tracks live object graphs, memory growth over time, and type-specific memory usage with pympler module.
    
    Attributes:
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
        obaserver (ProfilingObserver): A class that responsible for storing profiling result to.
        
    Raises:
        InvalidInputError: If storages or observer has incorrect type.
    """
    
    def __init__(
        self, 
        storages: python_profiling_configs.StorageConfig = python_profiling_configs.StorageConfig(), 
        observer: observers.ProfilingObserverI = observers.ProfilingObserver
        ):
        self._init_observer(storages=storages, observer=observer)
        
    def __call__(self, func: Callable):
        return self.base_profiling__call__(
            func=func,
            profiling_func=object_allocation_profiler.ObjectAllocationProfiler.profile,
            observing_func=self.observer.dump
            )
