import contextlib

import pytest

from python_profiling.call_graph_profiling import call_graph_profiler
from python_profiling import python_profiling_enums


@pytest.mark.parametrize(
    '''
    output_file, 
    file_to_remove, 
    visualizer_strategy, 
    func, 
    func_kwargs,
    func_result,
    func_exception, 
    raised_exception_ctx
    ''', 
    [
        (
            'call_graph_profiling_result.prof', 
            'call_graph_profiling_result.png',
            python_profiling_enums.CallGraphVisualizers.GPROF2DOT,
            lambda x: x + 1, 
            {'x': 1}, 
            2,
            None,
            contextlib.nullcontext()
            ), 
        (
            'call_graph_profiling_result.prof', 
            'call_graph_profiling_result.png',
            python_profiling_enums.CallGraphVisualizers.GPROF2DOT,
            lambda x: 1 / x, 
            {'x': 0}, 
            None,
            ZeroDivisionError,
            contextlib.nullcontext()
            ), 
        (
            'call_graph_profiling_result.txt', 
            'call_graph_profiling_result.png',
            python_profiling_enums.CallGraphVisualizers.GPROF2DOT,
            lambda x: 1 / x, 
            {'x': 0}, 
            None,
            ZeroDivisionError,
            pytest.raises(ValueError)
            ), 
        ]
    )
def test_CallGraphProfiler(
    output_file, 
    file_to_remove,
    visualizer_strategy, 
    func, 
    func_kwargs,
    func_result,
    func_exception,
    raised_exception_ctx,
    remove_dummy_file
    ):
    with raised_exception_ctx:
        profiler = call_graph_profiler.CallGraphProfiler(
            output_file=output_file,
            visualizer_strategy=visualizer_strategy
            )
        result = profiler.profile(func=func, **func_kwargs)
        remove_dummy_file(file_to_remove)
        assert result.profiler == call_graph_profiler.CallGraphProfiler
        assert result.profiled_func == func
        assert result.func_kwargs == func_kwargs
        assert result.func_result == func_result
        assert result.output_file == output_file
        assert result.func_exception == func_exception
        