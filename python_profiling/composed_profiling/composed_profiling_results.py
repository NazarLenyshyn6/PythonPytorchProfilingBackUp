
from python_profiling import _base_profiling_result

class ComposedProfilerResult(_base_profiling_result.BaseProfilingResult):
    """Structured profiling result combining time and memory profiling results.

    Attributes:
        time_profiling_result (BaseProfilingResult): Structured time profiling result.
        memory_profiling_result (BaseProfilingResult): Structured memory profiling result.
    """
    
    def __init__(
        self, 
        time_profiling_result: _base_profiling_result.BaseProfilingResult, 
        memory_profiling_result: _base_profiling_result.BaseProfilingResult
        ):
        """Initializes a composed profiler result.

        Args:
            time_profiling_result: Structured time profiling result.
            memory_profiling_result: Structured memory profiling result.
        """
        self.time_profiling_result = time_profiling_result
        self.memory_profiling_result = memory_profiling_result
    
    def __str__(self) -> str:
        return (
            f"Time Profiling Result:\n{self.time_profiling_result}\n"
            f"Memory Profiling Result:\n{self.memory_profiling_result}"
        )
        
    def __repr__(self):
        return (
            f"ComposedProfilerResult("
            f"time_profiling_result={repr(self.time_profiling_result)}, "
            f"memory_profiling_result={repr(self.memory_profiling_result)})"
        )