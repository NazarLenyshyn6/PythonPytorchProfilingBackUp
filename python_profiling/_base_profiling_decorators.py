"""Functionality that is common for all profiling decorators"""

from typing import Callable
import functools

from python_profiling import python_profiling_configs
from Internals import checks
from Internals import observers


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