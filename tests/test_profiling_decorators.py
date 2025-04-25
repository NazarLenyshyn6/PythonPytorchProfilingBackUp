import os
import time
import pytest
import contextlib

import pydantic

from python_profiling.time_profiling import time_profiling_decorators
from python_profiling.time_profiling import time_profiling_results
from python_profiling.memory_profiling import memory_profiling_decorators
from python_profiling.memory_profiling import memory_profiling_results
from python_profiling import python_profiling_enums
from python_profiling.composed_profiling import composed_profiler
from python_profiling.composed_profiling import composed_profiling_results

from python_profiling.python_profiling_configs import StorageConfig

COMMON_STORAGE = 'common_storage'
INVALID_STRATEGY = 'invalid_strategy'


@pytest.mark.parametrize(
    "decorator, decorator_kwargs, func, func_kwargs, raised_exception_ctx, expected_result_class",
    [
        (
            time_profiling_decorators.TimeProfilerDecorator,
            {
                'time_profiler_strategy': python_profiling_enums.TimeProfilerStrategy.BASIC, 
                'storages': COMMON_STORAGE
                },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            time_profiling_results.TimeProfilerResult
        ),
        (
            time_profiling_decorators.TimeProfilerDecorator,
            {
                'time_profiler_strategy': python_profiling_enums.TimeProfilerStrategy.PRECISE, 
                'storages': COMMON_STORAGE
                },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            time_profiling_results.TimeProfilerResult
        ),
        (
            time_profiling_decorators.TimeProfilerDecorator,
            {
                'time_profiler_strategy': python_profiling_enums.TimeProfilerStrategy.CPU, 
                'storages': COMMON_STORAGE
                },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            time_profiling_results.TimeProfilerResult
        ),
        (
            time_profiling_decorators.TimeProfilerDecorator,
            {
                'time_profiler_strategy': python_profiling_enums.TimeProfilerStrategy.THREAD_BASED, 
                'storages': COMMON_STORAGE
                },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            time_profiling_results.TimeProfilerResult
        ),
        (
            time_profiling_decorators.TimeProfilerDecorator,
            {
                'time_profiler_strategy': python_profiling_enums.TimeProfilerStrategy.MONOTONIC, 
                'storages': COMMON_STORAGE
                },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            time_profiling_results.TimeProfilerResult
        ),
        (
            time_profiling_decorators.TimeItProfilerDecorator,
            {'timer': time.perf_counter, 'number': 10000, 'repeat': 3, 'storages': COMMON_STORAGE},
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            time_profiling_results.TimeItProfilerResult
        ),
        (
            time_profiling_decorators.LineTimeProfilerDecorator,
            {'storages': COMMON_STORAGE},
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            time_profiling_results.LineTimeProfilerResult
        ),
        (
            time_profiling_decorators.CallGraphTimeProfilerDecorator,
            {'storages': COMMON_STORAGE},
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            time_profiling_results.CallGraphTimeProfilerResult
        ),
        (
            time_profiling_decorators.TimeProfilerDecorator,
            {'time_profiler_strategy': INVALID_STRATEGY, 'storages': COMMON_STORAGE},
            lambda x: x + 1,
            {'x': 1},
            pytest.raises(pydantic.ValidationError),
            None  
        ),
        (
            time_profiling_decorators.TimeItProfilerDecorator,
            {'timer': 11, 'number': 10000, 'repeat': 3, 'storages': COMMON_STORAGE},
            lambda x: x + 1,
            {'x': 1},
            pytest.raises(pydantic.ValidationError),
            time_profiling_results.TimeItProfilerResult
        ),
        (
            memory_profiling_decorators.PeakMemoryProfilerDecorator,
            {
                'nframes': 1,
                'key_type': 'lineno',
                'top_n': 5,
                'storages': COMMON_STORAGE
            },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            memory_profiling_results.PeakMemoryProfilerResult
        ),
        (
            memory_profiling_decorators.ObjectAllocationProfilerDecorator,
            {
                'storages': COMMON_STORAGE
            },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            memory_profiling_results.ObjectAllocationProfilerResult
        ),
        (
            memory_profiling_decorators.LineMemoryProfilerDecorator,
            {
                'storages': COMMON_STORAGE
            },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            memory_profiling_results.LineMemoryProfilerResult
        ),
        (
            composed_profiler.ComposedProfiler,
            {   
                'storages': COMMON_STORAGE
            },
            lambda x: x + 1,
            {'x': 1},
            contextlib.nullcontext(),
            composed_profiling_results.ComposedProfilerResult
        ),
    ]
)
def test_time_profiler_decorator(
    decorator,
    decorator_kwargs,
    func,
    func_kwargs,
    raised_exception_ctx,
    expected_result_class,
    common_storage,
    remove_dummy_file
):
    """Test if time profiler decorator correstly dump profiling result to specified sources."""
    with raised_exception_ctx:        
        # for testing valid (commo storage) and inlvalid storages cases
        if decorator_kwargs['storages']  == COMMON_STORAGE:
            decorator_kwargs['storages'] = common_storage
            
        decorated_func = decorator(**decorator_kwargs)(func)
        profiling_result = decorated_func(**func_kwargs)
        assert isinstance(profiling_result,expected_result_class)
        
        for file_path in decorator_kwargs['storages'].file_paths: 
            if os.path.exists(file_path):
                remove_dummy_file(file_path)

            
        
        
        
    