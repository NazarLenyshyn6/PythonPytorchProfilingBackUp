import pytest, time, os
from python_profiling.time_profiling.time_profiling_decorators import *
from python_profiling.time_profiling.time_profiling_results import *
from python_profiling.enums import TimeProfilerStrategy
from contextlib import nullcontext
from python_profiling.configs import StorageConfig
from pydantic import ValidationError


@pytest.mark.parametrize(
    "decorator, decorator_kwargs, func, func_kwargs, raised_exception_ctx, expected_result_class",
    [
        (
            TimeProfilerDecorator,
            {'time_profiler_strategy': TimeProfilerStrategy.BASIC, 'storages': 'common_storage'},
            lambda x: x + 1,
            {'x': 1},
            nullcontext(),
            TimeProfilerResult
        ),
        (
            TimeProfilerDecorator,
            {'time_profiler_strategy': TimeProfilerStrategy.PRECISE, 'storages': 'common_storage'},
            lambda x: x + 1,
            {'x': 1},
            nullcontext(),
            TimeProfilerResult
        ),
        (
            TimeProfilerDecorator,
            {'time_profiler_strategy': TimeProfilerStrategy.CPU, 'storages': 'common_storage'},
            lambda x: x + 1,
            {'x': 1},
            nullcontext(),
            TimeProfilerResult
        ),
        (
            TimeProfilerDecorator,
            {'time_profiler_strategy': TimeProfilerStrategy.THREAD_BASED, 'storages': 'common_storage'},
            lambda x: x + 1,
            {'x': 1},
            nullcontext(),
            TimeProfilerResult
        ),
        (
            TimeProfilerDecorator,
            {'time_profiler_strategy': TimeProfilerStrategy.MONOTONIC, 'storages': 'common_storage'},
            lambda x: x + 1,
            {'x': 1},
            nullcontext(),
            TimeProfilerResult
        ),
        (
            TimeItProfilerDecorator,
            {'timer': time.perf_counter, 'number': 10000, 'repeat': 3, 'storages': 'common_storage'},
            lambda x: x + 1,
            {'x': 1},
            nullcontext(),
            TimeItProfilerResult
        ),
        (
            TimeProfilerDecorator,
            {'time_profiler_strategy': 'invalid_strategy', 'storages': 'common_storage'},
            lambda x: x + 1,
            {'x': 1},
            pytest.raises(ValidationError),
            None  
        ),
        (
            TimeItProfilerDecorator,
            {'timer': 11, 'number': 10000, 'repeat': 3, 'storages': 'common_storage'},
            lambda x: x + 1,
            {'x': 1},
            pytest.raises(ValidationError),
            TimeItProfilerResult
        ),
        (
            TimeProfilerDecorator,
            {'time_profiler_strategy': TimeProfilerStrategy.BASIC, 'storages': {'common_storage'}},
            lambda x: x + 1,
            {'x': 1},
            pytest.raises(ValidationError),
            TimeProfilerResult
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
    with raised_exception_ctx:        
        if decorator_kwargs['storages']  == 'common_storage':
            decorator_kwargs['storages'] = common_storage
            
        decorated_func = decorator(**decorator_kwargs)(func)
        profiling_result = decorated_func(**func_kwargs)
        assert isinstance(profiling_result,expected_result_class)
        
        for file_path in decorator_kwargs['storages'].file_paths: 
            assert os.path.exists(file_path)
            remove_dummy_file(file_path)

            
        
        
        
    