"""Observers to save profiling results to multiple sources simultaneously."""

from dataclasses import dataclass
from abc import ABC, abstractmethod

from python_profiling import python_profiling_enums
from python_profiling.time_profiling import time_profiling_results
from python_profiling import python_profiling_configs


class ProfilingObserverI(ABC):
    """Interface class for Profiling observers."""
    @abstractmethod
    def __init__(self, storagest: python_profiling_configs.StorageConfig):
        ...
        
    @abstractmethod
    def dump(self, result: time_profiling_results.BaseTimeProfilingResult) -> None:
        ...

@dataclass
class ProfilingObserver(ProfilingObserverI):
    """Observer that stores configuration for saving profiling results to multiple sources.
    
    Attrigutes:
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
    """
    storages: python_profiling_configs.StorageConfig
    
    def dump(self, result: time_profiling_results.BaseTimeProfilingResult) -> None:
        """Writes the profiling result to all configured storage sources.
        
        Args:
            result (BaseTimeProfilingResult): The profiling result to persist.
            
        Returns: 
            None
        """
        for serializer_strategy, file_path, mode in zip(self.storages.serializers_strategies, 
                                                        self.storages.file_paths, 
                                                        self.storages.modes):
            result.dump(
                file_path=file_path, 
                mode=mode, 
                serializer_strategy=serializer_strategy
                )
                