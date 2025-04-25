"""Data Transfer Objects for Python profiling."""

import pydantic

from python_profiling import python_profiling_enums
from python_profiling.time_profiling import (
    time_profiler, 
    timeit_profiler, 
    line_time_profiler, 
    call_graph_time_profiler
    )
from python_profiling.memory_profiling import (
    peak_memory_profiler,
    object_allocation_profiler,
    line_memory_profiler
    )
from python_profiling.call_graph_profiling import call_graph_profiler
from Internals import checks
from Internals import execution_guards
from Internals.logger import logger


class StorageConfig(pydantic.BaseModel):
    """Configuration for storing profiling results.
    
    Attributes:
        serializers_strategies (list[SerializerStrategy]): List of serializers to use
            for saving profiling results. Defaults to an empty list.
        file_path (list[str]): List of file paths where results will be saved.
            Defaults to an empty list.
        modes(list[str]):  List of file write modes. If not provided,
            defaults to ['w'] for each serializer.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    
    serializers_strategies: list[python_profiling_enums.SerializerStrategy] = pydantic.Field(default_factory=list)
    file_paths: list[str] = pydantic.Field(default_factory=list)
    modes: list[str] | None = pydantic.Field(default=None)
    
    def model_post_init(self, __context):
        """Assign default write mode 'w' to each file if none is provided."""
        if not self.modes:
            self.modes = ['w' for _ in range(len(self.serializers_strategies))]
            
    @pydantic.model_validator(mode='after')
    def validate_lenghts_match(self) -> 'StorageConfig':
        """Validate that all configuration lists are of equal length.
        
        Returns:
            StorageConfig: Validated instance.
        
        Raises:
            ValueError: If `serializers_strategies`, `file_paths`, and `modes`
                do not have the same length.
        """
        serializers_lenght = len(self.serializers_strategies)
        file_paths_lenght = len(self.file_paths)
        modes_lenght = len(self.modes)
        
        if not (serializers_lenght == file_paths_lenght == modes_lenght == modes_lenght):
            raise ValueError(
                f'Amount of serializers, file_paths and modes has to be equal'
                f'got istead: {serializers_lenght, file_paths_lenght, modes_lenght}'
                )
        return self
    
class ComposedProfilingConfig:
    """Configuration for storing profiling results.
    
    Attributes:
        time_profiler (object): Initialized time profiler instance.
        memory_profiler (object): Initialized memory profiler instance.
    """
    _available_profilers = {
        python_profiling_enums.ProfilingType.TIME_PROFILING: {
            python_profiling_enums.TimeProfilingStrategy.TIME_PROFILER: time_profiler.TimeProfiler, 
            python_profiling_enums.TimeProfilingStrategy.TIMEIT_PROFILER: timeit_profiler.TimeItProfiler,
            python_profiling_enums.TimeProfilingStrategy.LINE_TIME_PROFILER: line_time_profiler.LineTimeProfiler,
            python_profiling_enums.TimeProfilingStrategy.CALL_GRAPH_TIME_PROFILER: call_graph_time_profiler.CallGraphTimeProfiler,
            }, 
        python_profiling_enums.ProfilingType.MEMORY_PROFILING: {
            python_profiling_enums.MemoryProfilingStrategy.PEAK_MEMORY_PROFILER: peak_memory_profiler.PeakMemoryProfiler, 
            python_profiling_enums.MemoryProfilingStrategy.OBJECT_ALLOCATION_PROFILER: object_allocation_profiler.ObjectAllocationProfiler,
            python_profiling_enums.MemoryProfilingStrategy.LINE_MEMORY_PROFILER: line_memory_profiler.LineMemoryProfiler
            },
        python_profiling_enums.ProfilingType.CALL_GRAPH_PROFILING: {
            python_profiling_enums.CallGraphProfilingStrategy.CALL_GRAPH_PROFILER: call_graph_profiler.CallGraphProfiler, 
            }
        }
    @checks.ValidateType([
        ('time_profiling_strategy', python_profiling_enums.TimeProfilingStrategy),
        ('memory_profiling_strategy', python_profiling_enums.MemoryProfilingStrategy),
        ('call_graph_profiling_strategy',  python_profiling_enums.CallGraphProfilingStrategy)
    ])
    def __init__(
        self, 
        time_profiling_strategy: python_profiling_enums.TimeProfilingStrategy,
        memory_profiling_strategy: python_profiling_enums.MemoryProfilingStrategy,
        call_graph_profiling_strategy: python_profiling_enums.CallGraphProfilingStrategy,
        time_profiling_strategy_params: dict = None,
        memory_profiling_strategy_params: dict = None,
        call_graph_profiling_strategy_params: dict = None
        ):
        """Initializes the composed profiling configuration.

        Args:
            time_profiling_strategy: Strategy for time profiling.
            memory_profiling_strategy: Strategy for memory profiling.
            call_graph_profiling_strategy: Strategy for call graph profiling.
            time_profiling_strategy_params: Parameters to initialize time profiler.
            memory_profiling_strategy_params: Parameters to initialize memory profiler.
            call_graph_profiling_strategy_params: Parameters to initialize call graph profiler.
        """
    
        def _initialize_profiler(profiler, profiler_params):
            if not profiler_params:
                return profiler()
            return profiler(**profiler_params)
        
        try:
            self.time_profiler = _initialize_profiler(
                self.get_profiler(
                    python_profiling_enums.ProfilingType.TIME_PROFILING,
                    time_profiling_strategy
                    ),
                time_profiling_strategy_params)
            self.memory_profiler = _initialize_profiler(
                self.get_profiler(
                    python_profiling_enums.ProfilingType.MEMORY_PROFILING,
                    memory_profiling_strategy
                ),
                memory_profiling_strategy_params)
            self.call_graph_profiler = _initialize_profiler(
                self.get_profiler(
                    python_profiling_enums.ProfilingType.CALL_GRAPH_PROFILING,
                    call_graph_profiling_strategy),
                call_graph_profiling_strategy_params)
            
        except Exception as e:
            logger.info(
                'Failed to initialize ComposedProfilingConfig: %s',
                str(e)
                )
    
    def __iter__(self):
        return iter((
            self.time_profiler,
            self.memory_profiler,
            self.call_graph_profiler
        ))
        
    def get_profiler(
        self, 
        profiling_type: python_profiling_enums.ProfilingType, 
        profiling_strategy: python_profiling_enums.TimeProfilingStrategy | python_profiling_enums.MemoryProfilingStrategy
        ):
        """Retrieves the profiler class for the given strategy.

        Args:
            profiling_type: The type of profiling (e.g., TIME_PROFILING).
            profiling_strategy: The strategy for the given profiling type.

        Returns:
            A profiler class corresponding to the provided strategy.

        Raises:
            TypeError: If profiling_type or strategy is invalid.
        """
        
        if not profiling_type in self._available_profilers:
            raise TypeError(
                "Invalid Profiling Type. Valid options: TIME_PROFILING, MEMORY_PROFILING."
            )
        profilers = self._available_profilers[profiling_type]
        if not profiling_strategy in profilers:
            raise TypeError("Invalid Profiling Strategy for given profiling type.")
        profiler = profilers[profiling_strategy]
        return profiler
    
    def _add_profiler(
        self, 
        profiling_type: python_profiling_enums.ProfilingType, 
        profiling_strategy: python_profiling_enums.TimeProfilingStrategy | python_profiling_enums.MemoryProfilingStrategy,
        profiler
        ):
        """Registers a new profiler class.

        Args:
            profiling_type: The profiling category (e.g., TIME_PROFILING).
            profiling_strategy: Strategy identifier.
            profiler: The profiler class to register.

        Raises:
            TypeError: If profiling_type is invalid.
        """
        if not profiling_type in self._available_profilers:
            raise TypeError("Invalid profiling type provided.")
        self._available_profilers[profiling_type][profiling_strategy] = profiler
        
    @classmethod
    def avaliable_profilers(cls):
        """Returns all currently available profilers."""
        for profiling_type in cls._available_profilers:
            print(f'Profiling type: {profiling_type}')
            for profiler in cls._available_profilers[profiling_type]:
                print(f'    Profiler: {profiler}')
            print()
        
    def __repr__(self) -> str:
        return (
            f"ComposedProfilingConfig("
            f"time_profiler={self.time_profiler}, "
            f"memory_profiler={self.memory_profiler})"
            f"call_graph_profiler={self.call_graph_profiler}"
        )