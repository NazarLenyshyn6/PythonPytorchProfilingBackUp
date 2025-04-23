"""Provide functionality for composite function profiling."""

from abc import ABC, abstractmethod
from types import BuiltinFunctionType, FunctionType
from typing_extensions import override

from python_profiling import python_profiling_enums
from python_profiling import python_profiling_configs
from python_profiling.composed_profiling import composed_profiling_results
from python_profiling import _base_profiling_decorators
from Internals import observers


class ComposedProfilerI(ABC, _base_profiling_decorators.BaseProfilingDecorator):
    """Interface for composed function profiling.

    Attributes:
        composed_profiling_config (ComposedProfilingConfig): Configuration specifying time and memory profilers.
        storages (StorageConfig): Data Transfer Object containing all output destinations.
        observer (ProfilingObserver): Responsible for storing profiling results.
    """
    def __init__(
        self, 
        composed_profiling_config: python_profiling_configs.ComposedProfilingConfig = 
        python_profiling_configs.ComposedProfilingConfig(
            time_profiling_strategy=python_profiling_enums.TimeProfilingStrategy.LINE_TIME_PROFILER,
            memory_profiling_strategy=python_profiling_enums.MemoryProfilingStrategy.OBJECT_ALLOCATION_PROFILER
            ),
        storages: python_profiling_configs.StorageConfig = python_profiling_configs.StorageConfig(),
        observer: observers.ProfilingObserverI = observers.ProfilingObserver
        ):
        self.composed_profiling_config = composed_profiling_config
        self._init_observer(storages=storages, observer=observer)

    @abstractmethod
    def profile(self, func: BuiltinFunctionType | FunctionType, **kwargs):
        """Perform profiling with specified profiling strategies.

        Args:
            func: The function to profile.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            ComposedProfilerResult: Structured profiling result.
        """
        
    @abstractmethod
    def __call__(self, func: BuiltinFunctionType | FunctionType):
        """Decorator for composed profiling.

        Args:
            func: Function to profile.

        Returns:
            Callable: A wrapped function with profiling logic.
        """
        
class ComposedProfiler(ComposedProfilerI):
    """Concrete implementation of a composed function profiler."""
    @override
    def __call__(self, func: BuiltinFunctionType | FunctionType):
        return self.base_profiling__call__(
            func=func,
            profiling_func=self.profile,
            observing_func=self.observer.dump
            )
    
    def __repr__(self) -> str:
        return f'ComposedProfiler(composed_profiling_config={self.composed_profiling_config})'
    
    @override
    def profile(self, func: BuiltinFunctionType | FunctionType, **kwargs):
        profiling_results = []
        for profiler in self.composed_profiling_config:
            profiling_results.append(profiler.profile(func=func, **kwargs))
        return composed_profiling_results.ComposedProfilerResult(*profiling_results)
        
