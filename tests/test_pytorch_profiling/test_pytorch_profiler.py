import contextlib

import pytest
import pydantic

from pytorch_profiling import pytorch_profiler
from pytorch_profiling import pytorch_profiling_results

pytorch_profiler.PyTorchProfiler

@pytest.mark.parametrize(
    'profiler_params, raised_exception_ctx', 
    [
        ({'trace_name': 'test_trace', 'output_dir': 'test_dir'}, contextlib.nullcontext()),
        ({'output_dir': 1}, pytest.raises(pydantic.ValidationError))
        ]
    )
def test_PyTorchProfiler(
    profiler_params, 
    raised_exception_ctx,
    pytorch_profiling_setup,
    remove_profiling_dir
    ):
    model = pytorch_profiling_setup.model
    optimizer = pytorch_profiling_setup.optimizer
    loss_fn = pytorch_profiling_setup.loss_fn
    data = pytorch_profiling_setup.data
    target = pytorch_profiling_setup.target
    
    with raised_exception_ctx:
    	with pytorch_profiler.PyTorchProfiler(**profiler_params) as profiler:
         for epoch in range(3):
            profiler.record_function("forward", lambda: model(data))
            output = model(data)
            
            profiler.record_function("loss", lambda: loss_fn(output, target))
            loss = loss_fn(output, target)
            
            profiler.record_function("backward", lambda: loss.backward(retain_graph=True))
            loss.backward(retain_graph=True)
            
            profiler.record_function("optimizer_step", lambda: optimizer.step())
            optimizer.step()
            optimizer.zero_grad()
            
            result = profiler.profiling_summary
            assert isinstance(result, pytorch_profiling_results.PyTorchProfilingResult)
            
    if 'output_dir' in profiler_params:
        remove_profiling_dir(profiler_params['output_dir'])