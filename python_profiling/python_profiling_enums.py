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