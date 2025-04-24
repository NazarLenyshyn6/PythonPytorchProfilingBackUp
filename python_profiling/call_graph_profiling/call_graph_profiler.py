""""""

import os
from abc import ABC, abstractmethod
from typing import Callable
from typing_extensions import override

from python_profiling import python_profiling_enums
from python_profiling.call_graph_profiling import call_graph_visualization
from python_profiling.call_graph_profiling import call_graph_profiling_results
from Internals import context_managers

class CallGraphProfilerI(ABC):
    """Interface for call graph profilers using different visualization strategies."""
    _avaliable_visualizers = {
        python_profiling_enums.CallGraphVisualizers.GPROF2DOT: call_graph_visualization.Gprof2dotVisualizer,
        python_profiling_enums.CallGraphVisualizers.SNAKEVIZ: call_graph_visualization.SnakevizVisualizer
        }
    
    def __init__(
        self, 
        output_file: str = 'call_graph_profiling_result.prof', 
        visualizer_strategy: python_profiling_enums.CallGraphVisualizers = 
            python_profiling_enums.CallGraphVisualizers.GPROF2DOT
        ):
        self.output_file = output_file
        if not visualizer_strategy in self._avaliable_visualizers:
            raise KeyError('Invalid visualizer strategy.')
        self.visualizer = self._avaliable_visualizers[visualizer_strategy]
        """Initializes the call graph profiler interface.

        Args:
            output_file: The path to save the profiling result.
            visualizer_strategy: The strategy used to visualize the profiling result.

        Raises:
            KeyError: If the given visualizer strategy is invalid.
        """
        
    @abstractmethod
    def profile(self, func: Callable, **kwargs):
        """Profiles the given function and visualizes the call graph.

        Args:
            func: The function to be profiled.
            **kwargs: Arguments to be passed to the function.
        """
        ...
    
    @abstractmethod
    def __call__(self, func: Callable):
        """Allows the profiler instance to be used as a decorator.

        Args:
            func: The function to be wrapped and profiled.

        Returns:
            Callable: The wrapped function.
        """
        ...
        
class CallGraphProfiler(CallGraphProfilerI):
    """Concrete implementation of the call graph profiler."""
    
    def __repr__(self) -> str:
        return f'CallGraphProfiler(visualizer={self.visualizer})'
    
    @override
    def profile(self, func, **kwargs):
        with context_managers.CallGraphTimeProfilerManager(self.output_file) as call_graph_profiling_manager:
            result = func(**kwargs)
        self.visualizer.visualize(output_file=self.output_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        return call_graph_profiling_results.CallGraphProfilerResult(
            profiler=CallGraphProfiler,
            profiled_func=func,
            func_kwargs=kwargs,
            func_result=result if not call_graph_profiling_manager.exception else None,
            output_file=self.output_file,
            func_exception=call_graph_profiling_manager.func_exception
            )
            
    @override
    def __call__(self, func: Callable):
        def wrapper(**kwargs):
            return self.profile(func=func, **kwargs)
        return wrapper
        
        
        
    
    