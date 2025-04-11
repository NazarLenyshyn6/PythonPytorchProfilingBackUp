from enum import Enum

class TimeProfilerStrategy(Enum):
    BASIC = 'basic'
    PRECISE = 'precise'
    CPU = 'cpu'
    THREAD_BASED = 'thread_based'
    MONOTONIC = 'monotonic'
    

class SerializerStrategy(Enum):
    JSON = 'json'
    TXT = 'txt'
    YAML = 'yaml'