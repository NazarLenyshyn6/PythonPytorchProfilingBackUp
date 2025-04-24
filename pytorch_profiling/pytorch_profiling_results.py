from dataclasses import dataclass
import datetime

from python_profiling import _base_profiling_result

@dataclass
class PyTorchProfilingResult(_base_profiling_result.BaseProfilingResult):
    trace_name: str
    duration: int | float
    output_dir: str
    
    def __str__(self) -> str:
        summary = self.profiling_data
        return f"""PyTorch Profiling Result.

Trace Name: `{summary['trace_name']}`  
Total Duration: `{summary['duration']:.4f} seconds`  
Output Directory: `{summary['output_dir']}`  

- How to View:
    1. Run this in your terminal: tensorboard --logdir={summary['output_dir']}
    2. Then open [http://localhost:6006](http://localhost:6006)

- Notes:
    1. CPU-only profiling (macOS doesn't support CUDA)
    2. View the *"Profiler"* tab in TensorBoard
"""
        
    def __repr__(self) -> str:
        return f'PyTorchProfilingResult(output_dir={self.output_dir})'