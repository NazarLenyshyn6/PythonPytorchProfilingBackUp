"""Observers to save profiling results to multiple sources simultaneously."""

from typing_extensions import override
from dataclasses import dataclass
from abc import ABC, abstractmethod

from python_profiling import python_profiling_enums
from python_profiling import _base_profiling_result
from python_profiling import python_profiling_configs


class ProfilingObserverI(ABC):
    """Interface class for Profiling observers."""
    @abstractmethod
    def __init__(self, storagest: python_profiling_configs.StorageConfig):
        ...
        
    @abstractmethod
    def dump(self, result: _base_profiling_result.BaseProfilingResult) -> None:
        """Writes the profiling result to all configured storage sources.
        
        Args:
            result (BaseProfilingResult): The profiling result to persist.
            
        Returns: 
            None
        """

@dataclass
class ProfilingObserver(ProfilingObserverI):
    """Observer that stores configuration for saving profiling results to multiple sources.
    
    Attrigutes:
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
    """
    storages: python_profiling_configs.StorageConfig
    
    @override
    def dump(self, result: _base_profiling_result.BaseProfilingResult) -> None:
        for serializer_strategy, file_path, mode in zip(self.storages.serializers_strategies, 
                                                        self.storages.file_paths, 
                                                        self.storages.modes):
            result.dump(
                file_path=file_path, 
                mode=mode, 
                serializer_strategy=serializer_strategy
                )
                