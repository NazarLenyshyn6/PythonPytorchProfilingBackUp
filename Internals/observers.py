"""Observers to save profiling results to multiple sources simultaneously."""

from dataclasses import dataclass
from abc import ABC, abstractmethod

from python_profiling.enums import SerializerStrategy
from python_profiling.time_profiling.time_profiling_results import BaseTimeProfilingResult
from python_profiling.configs import StorageConfig


@dataclass
class ProfilingObserver:
    """Observer that stores configuration for saving profiling results to multiple sources.
    
    Attrigutes:
        storages (StorageConfig): Data Transfer Object that contains all configured output destinations.
    """
    storages: StorageConfig
    
    def dump(self, result: BaseTimeProfilingResult) -> None:
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
                