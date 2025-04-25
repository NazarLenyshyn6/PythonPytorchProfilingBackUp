"""Memory profiling decorators."""

from typing import Callable, Literal

from python_profiling.memory_profiling import peak_memory_profiler
from python_profiling.memory_profiling import object_allocation_profiler
from python_profiling.memory_profiling import line_memory_profiler
from python_profiling import _base_profiling_decorators
from python_profiling import python_profiling_configs
from Internals import observers

class PeakMemoryProfilerDecorator(_base_profiling_decorators.BaseProfilingDecorator):
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
        
class LineMemoryProfilerDecorator(_base_profiling_decorators.BaseProfilingDecorator):
    """Decorator for memory profiling with memory_profiler module.
    
    Attributes:
        interval: The time interval (in seconds) between consecutive memory measurements.
        timeout: Specifies the maximum duration (in seconds) to collect memory measurements. 
            If exceeded, measurement is terminated.
        backed: Etermines the backend method for acquiring memory usage data.
        include_children: If True, includes memory usage of all child processes 
            spawned by the target process or callable.
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
        obaserver (ProfilingObserver): A class that responsible for storing profiling result to.
        
    Raises:
        ValidationError: If sort_key, func_filter, top_n has incorrect type.
        InvalidInputError: If storages or observer has incorrect type.
    """
    def __init__(
        self, 
        interval: int | float = 0.2, 
        timeout: int = 5,
        backed: Literal['psutil', 'ps'] = 'psutil',
        include_children: bool = True,
        storages: python_profiling_configs.StorageConfig = python_profiling_configs.StorageConfig(), 
        observer: observers.ProfilingObserverI = observers.ProfilingObserver
        ):
        """Initialize LineMemoryProfiler, observer with provided parametrs and storages."""
        self.memory_profiler = line_memory_profiler.LineMemoryProfiler(
            interval=interval,
            timeout=timeout,
            backed=backed,
            include_children=include_children
            )
        self._init_observer(storages=storages, observer=observer)
        
    def __call__(self, func: Callable):
        return self.base_profiling__call__(
            func=func,
            profiling_func=self.memory_profiler.profile,
            observing_func=self.observer.dump
            )
