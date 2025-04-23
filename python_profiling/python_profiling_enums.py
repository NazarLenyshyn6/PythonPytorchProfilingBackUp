"""Enumerations for Python profiling."""

import enum

class TimeProfilerStrategy(enum.Enum):
    """Enumeration of valid strategies for TimeProfiler."""
    
    BASIC = 'basic'
    PRECISE = 'precise'
    CPU = 'cpu'
    THREAD_BASED = 'thread_based'
    MONOTONIC = 'monotonic'
    

class SerializerStrategy(enum.Enum):
    """Enumeration of valid output formats for serialization."""
    
    JSON = 'json'
    TXT = 'txt'
    YAML = 'yaml'
    
    
class ProfilingType(enum.Enum):
    """Enumeration of existing profiling types"""
    
    TIME_PROFILING = 'time_profiling'
    MEMORY_PROFILING = 'memory_profiling'
    CALL_GRAPH_PROFILING = 'call_graph_profiling'
    
    
class TimeProfilingStrategy(enum.Enum):
    """Enumeration of existing time profiling options."""
    
    TIME_PROFILER = 'time_profiler'
    TIMEIT_PROFILER = 'timeit_profiler'
    LINE_TIME_PROFILER = 'line_time_profiler'
    CALL_GRAPH_TIME_PROFILER = 'call_graph_time_profiler'
    
    
class MemoryProfilingStrategy(enum.Enum):
    """Enumeration of existing memory profiling options."""
    
    PEAK_MEMORY_PROFILER = 'peak_memory_profiler'
    OBJECT_ALLOCATION_PROFILER = 'object_allocation_profiler'
    LINE_MEMORY_PROFILER = 'line_memory_profiler'
    