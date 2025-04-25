"""PyTorch profiling integration with structured configuration and result interface."""

import os
import time
from typing import Any

import torch
import torch.profiler
import pydantic
from abc import ABC, abstractmethod

from python_profiling import python_profiling_configs
from python_profiling import python_profiling_enums
from pytorch_profiling import pytorch_profiling_results
from Internals import checks
from Internals import observers


class PyTorchProfilerI(ABC):
    """Interface class for PyTorch profiling."""

    @abstractmethod
    def __enter__(self):
        """Start profiling session."""
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, traceback):
        """End profiling session."""
        ...

    @abstractmethod
    def record_function(self, name, func):
        """Wrap a block or function for profiling.

        Args:
            name (str): Name of the profiling section.
            func (Callable): The function to execute under the profiler.
        """
        ...

    @property
    @abstractmethod
    def profiling_summary(self):
        """Return structured profiling summary result."""
        ...


class PyTorchProfiler(PyTorchProfilerI, pydantic.BaseModel):
    """Concrete implementation of the PyTorch profiler interface."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    trace_name: str = pydantic.Field(default="default_trace")
    output_dir: str = pydantic.Field(default="pytorch_profiling_result_folder")
    activities: list | None = pydantic.Field(default=None)
    profile_memory: bool = pydantic.Field(default=True)
    record_shapes: bool = pydantic.Field(default=True)
    with_stack: bool = pydantic.Field(default=True)
    profiler: Any = pydantic.Field(init=False, default=None)
    start_time: Any = pydantic.Field(init=False, default=None)
    end_time: Any = pydantic.Field(init=False, default=None)

    def model_post_init(self, __context):
        """Initialize internal profiler settings."""
        if self.activities is None:
            self.activities = [torch.profiler.ProfilerActivity.CPU]  # macOS-safe: CPU only

        self._create_output_dir()

    def _create_output_dir(self):
        """Ensure the profiling output directory exists."""
        os.makedirs(self.output_dir, exist_ok=True)

    def __enter__(self):
        """Start the profiling session and initialize timing."""
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
        """Stop the profiling session and record end time."""
        self.end_time = time.time()
        self.profiler.__exit__(exc_type, exc_val, traceback)
        return True

    def record_function(self, name, func):
        """Wrap a function call under a named profiling scope.

        Args:
            name (str): The name of the recorded profiling block.
            func (Callable): The function to run inside the scope.
        """
        with torch.profiler.record_function(name):
            return func()

    @property
    def profiling_summary(self):
        """Structured summary result from profiling session.

        Returns:
            PyTorchProfilingResult: Result with trace name, duration, and output path.
        """
        return pytorch_profiling_results.PyTorchProfilingResult(
            trace_name=self.trace_name,
            duration=self.end_time - self.start_time,
            output_dir=self.output_dir
        )
