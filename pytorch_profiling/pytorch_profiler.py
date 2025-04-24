"""Pytorch  profiling"""

import os
from abc import ABC, abstractmethod
import time
from typing import Any

import torch
import torch.profiler
import pydantic

from python_profiling import python_profiling_configs
from python_profiling import python_profiling_enums
from pytorch_profiling import pytorch_profiling_results
from Internals import checks
from Internals import observers

class PyTorchProfilerI(ABC):
    """Interface class for PyTorch profiling."""
    
    @abstractmethod
    def __enter__(self):
        ...
        
    @abstractmethod
    def __exit__(self, exc_type, exc_val, traceback):
        ...
        
    @abstractmethod
    def record_function(self, name, func):
        ...
       
    @property 
    @abstractmethod
    def profiling_summary(self):
        ...
    
class PyTorchProfiler(PyTorchProfilerI, pydantic.BaseModel):
    """Concrete implementatino of PyTorch profiling."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    
    trace_name: str = pydantic.Field(default='default_trace')
    output_dir: str = pydantic.Field(default='pytorch_profiling_result_folder')
    activities: list | None = pydantic.Field(default=None)
    profile_memory: bool = pydantic.Field(default=True)
    record_shapes: bool = pydantic.Field(default=True)
    with_stack: bool = pydantic.Field(default=True)
    storages: python_profiling_configs.StorageConfig = pydantic.Field(default=python_profiling_configs.StorageConfig())
    observer: observers.ProfilingObserverI = pydantic.Field(default=observers.ProfilingObserver)
    profiler: Any  = pydantic.Field(init=False, default=None)
    start_time: Any = pydantic.Field(init=False, default=None)
    end_time: Any = pydantic.Field(init=False, default=None)
    
    def model_post_init(self, __context):
        if self.activities is None:
            self.activities = [torch.profiler.ProfilerActivity.CPU]  # Default to CPU for macOS
            
        self.profiler = None
        self.start_time = None
        self.end_time = None
        self._create_output_dir()
 
        
    def _create_output_dir(self):
        """Ensure the output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def __enter__(self):
        self.start_time = time.time()
        self.profiler = torch.profiler.profile(
            activities=self.activities,
            on_trace_ready=torch.profiler.tensorboard_trace_handler(self.output_dir),
            record_shapes=self.record_shapes,
            profile_memory=self.profile_memory,
            with_stack=self.with_stack
            )
        self.profiler.__enter__()
        return self
        
    def __exit__(self, exc_type, exc_val, traceback):
        self.end_time = time.time()
        self.profiler.__exit__(None, None, None)
        
    def record_function(self, name, func):
        """Wrap a function with profiling."""
        with torch.profiler.record_function(name):
            func()
        
    @property
    def profiling_summary(self):
        return pytorch_profiling_results.PyTorchProfilingResult(
            trace_name=self.trace_name,
            duration=self.end_time - self.start_time,
            output_dir=self.output_dir
            )