"""Structured memory profiling results."""

from typing import Type, Any
from types import  BuiltinFunctionType, FunctionType
from dataclasses import dataclass
import tracemalloc

from python_profiling import _base_profiling_result

@dataclass
class PeakMemoryProfilerResult(_base_profiling_result.BaseProfilingResult):
    """Structured profiling result for memory profiling with tracemalloc module.
    
    Attributes:
        profiler: A class implementing TimeProfilerI.
        profiled_func: Profiled function.
        func_kwargs: Keyword arguments of profiled funciton.
        func_result: Profiled function result.
        current_memory: Current size of traced memory blocks.
        peak_memory: Peak size of traced memory blocks.
        snapshot_before: Captures memory allocations before function call.
        snapshot_after: Captures memory allocations after function call.
        func_exception: Exception raised during execution, if any.
    """
    top_n: int
    key_type: str
    profiler: Type
    profiled_func: BuiltinFunctionType | FunctionType
    func_kwargs: dict
    func_result: Any
    current_memory: float
    peak_memory: float
    allocation_before: tracemalloc.Snapshot
    allocation_after: tracemalloc.Snapshot
    func_exception: str | None = None
    
    def _top_memory_differences(self):
        """Compare allocations by specified sort key."""
        print(f"Top {self.top_n} memory differences by '{self.key_type}':")
        for stat in self.allocation_after.compare_to(self.allocation_before, self.key_type)[:self.top_n]:
            print(stat)
        print()
        
    def _top_memory_allocations(self):
        """Compare snapshots by 'traceback' and explore call stack."""
        print(f"Top {self.top_n} allocations by 'traceback':")
        for stat in self.allocation_after.statistics('traceback')[:self.top_n]:
            print(f"Memory block: {stat.size / 1024:.2f} KB in {stat.count} allocations")
            for line in stat.traceback.format():
                print("  -", line)
            print()
    
    def __str__(self) -> str:
        self._top_memory_differences()
        self._top_memory_allocations()
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Current memory: {self.current_memory:.6f} KB\n"
                f"Peak memory: {self.peak_memory:.6f} KB\n"
                f"Allocation before: {self.allocation_before}KB\n"
                f"Allocation after: {self.allocation_after}\n"
                f"Allocation after statictics: {self.allocation_after.statistics}\n"
                f"Function Exception: {self.func_exception or 'None'}")
        
    def __repr__(self) -> str:
        return f'PeakMemoryProfilerResult(profiler={self.profiler.__class__.__name__}, profiled_func={self.profiled_func.__name__})'
        
    

