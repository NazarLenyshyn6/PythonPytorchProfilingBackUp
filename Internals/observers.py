from abc import ABC, abstractmethod
from python_profiling.enums import SerializerStrategy
from python_profiling.time_profiling.time_profiling_results import TimeProfilerResult
from python_profiling.configs import StorageConfig
from dataclasses import dataclass


@dataclass
class ProfilingObserver:
    storages: StorageConfig
    
    def dump(self, result: TimeProfilerResult):
        for serializer_strategy, file_path, mode in zip(self.storages.serializers, self.storages.file_paths, self.storages.modes):
            result.dump(file_path=file_path, mode=mode, serializer_strategy=serializer_strategy)
                