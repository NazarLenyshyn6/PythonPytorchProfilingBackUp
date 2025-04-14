"""Enumerations for python profiling."""

from enum import Enum

class TimeProfilerStrategy(Enum):
    """Enumeration of valid strategies for TimeProfiler."""
    
    BASIC = 'basic'
    PRECISE = 'precise'
    CPU = 'cpu'
    THREAD_BASED = 'thread_based'
    MONOTONIC = 'monotonic'
    

class SerializerStrategy(Enum):
    """Enumeration of valid output formats for serialization."""
    
    JSON = 'json'
    TXT = 'txt'
    YAML = 'yaml'