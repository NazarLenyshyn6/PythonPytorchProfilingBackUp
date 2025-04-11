from dataclasses import dataclass
from typing import Any, Type
from types import BuiltinFunctionType, FunctionType
from Internals.checks import ValidateType
from Internals.serialization import SerializationHandler
from python_profiling.enums import SerializerStrategy

# Implementation of Basic Time Profiling Result
class BaseTimeProfilingResult:
    @property
    def profiling_data(self):
        return self.__dict__
    
    
    @property
    def profiling_data_str(self):
        return {key: f'{value}' for key, value in self.profiling_data.items()}
    
    
    @ValidateType(('context', dict))
    def add_context(self, context: dict):
        self.__dict__.update(context)
    
    
    def remove_context(self, context_element: Any):
        if context_element in self.__dict__:
            del self.__dict__[context_element]
            
            
    def dump(self, 
             file_path: str, 
             mode: str = 'w', 
             serializer_strategy:SerializerStrategy = SerializerStrategy.TXT):
        
        SerializationHandler.dump(data=self.profiling_data_str,
                                  file_path=file_path,
                                  mode=mode,
                                  serializer_strategy=serializer_strategy)
    
    
# Implementation of result provided by time profiler
@dataclass
class TimeProfilerResult(BaseTimeProfilingResult):
    profiler: Type
    profiled_func: BuiltinFunctionType | FunctionType
    func_args: tuple
    func_kwargs: dict
    func_result: Any
    func_execution_time: int | float
    func_exception: str | None = None
    
    
    def __str__(self) -> str:
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Args: {self.func_args}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Function Executions Time: {self.func_execution_time:.6f} seconds\n"
                f"Function Exception: {self.func_exception or 'None'}")
        
        
    def __repr__(self) -> str:
        return f'TimeProfilerResult(profiler={self.profiler.__class__.__name__}, profiled_func={self.profiled_func.__name__})'
        
        
@dataclass
class TimeItProfilerResult(BaseTimeProfilingResult):
    profiler: Type
    profiled_func: BuiltinFunctionType | FunctionType
    func_kwargs: dict
    func_result: Any
    repeats: int
    min_func_execution_time: int | float
    avg_func_execution_time: int | float
    max_func_execution_time: int | float
    func_exception: str | None = None
    
    
    def __str__(self) -> str:
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Function Min Executions Time: {self.min_func_execution_time:.6f} seconds\n"
                f"Function Avg of {self.repeats} Executions Time: {self.avg_func_execution_time:.6f} seconds\n"
                f"Function Max Executions Time: {self.max_func_execution_time:.6f} seconds\n"
                f"Function Exception: {self.func_exception or 'None'}")
        
        
    def __repr__(self) -> str:
        return f'TimeItProfilerResult(profiler={self.profiler.__class__.__name__}, profiled_func={self.profiled_func})'