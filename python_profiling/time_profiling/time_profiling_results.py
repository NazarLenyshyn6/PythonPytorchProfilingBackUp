"""Structured time profiling results."""

from dataclasses import dataclass
from typing import Any, Type
from types import BuiltinFunctionType, FunctionType

from Internals.checks import ValidateType
from Internals.serialization import SerializationHandler
from python_profiling.enums import SerializerStrategy
from Internals.logger import logger


class BaseTimeProfilingResult:
    """Defines functionality that is common across all time profilers."""
    
    @property
    def profiling_data(self):
        """Returns profiling data as a dictionary.
        
        Returns:
            dict: Dictionary containing all profiling data.
        """
        return self.__dict__
    
    @property
    def profiling_data_str(self):
        """Returns profiling data with all values as strings.
        
        Returns:
            dict: Dictionary with all profiling data as strings.
        """
        return {key: f'{value}' for key, value in self.profiling_data.items()}
    
    @ValidateType(('context', dict))
    def add_context(self, context: dict) -> None:
        """Adds additional metadata to profiling result.
        
        Args:
            context (dict): Dictionary with extra profiling information.
        
        Returns:
            None
            
        Raises:
            InvalidInputTypeError: if provided content is not a dictionary.
        """
        self.__dict__.update(context)
        logger.info(
            'profiling data has been extended with context %s successfully', 
            context
            ) # might be removed
     
    
    def remove_context(self, context_element: Any) -> None:
        """Removes a key from the profiling context.
        
        Args:
            context_element: Key to remove from profiling data.
        
        Returns:
            None
        """
        if context_element in self.__dict__:
            del self.__dict__[context_element]
            logger.info('context %s has been removed from profiling data', context_element)
            
            
    def dump(
        self, 
        file_path: str, 
        mode: str = 'w', 
        serializer_strategy:SerializerStrategy = SerializerStrategy.TXT
        ) -> None:
        """Serializes data to a file using the chosen serialization strategy.
        
        Args:
            data (dict): Data to serialize.
            file_path (str): Output file path.
            mode (str):  File mode, default is 'w' (write).
            serializer_strategy (SerializerStrategy): Serializer to perform serializaton.
            
        Returns:
            None
            
        Raises:
            InvalidInputTypeError: If the provided serializer strategy is invalid.
            MissingArgumentError: If a required argument is missing.
        """
        
        SerializationHandler.dump(data=self.profiling_data_str,
                                  file_path=file_path,
                                  mode=mode,
                                  serializer_strategy=serializer_strategy)
    
    
# Implementation of result provided by time profiler
@dataclass
class TimeProfilerResult(BaseTimeProfilingResult):
    """Structured profiling result for time profiling with time module.
    
    Args:
        profiler: A class implementing TimeProfilerI.
        profiled_func: Profiled function.
        func_args: Arguments of profiled function.
        func_kwargs: Keyword arguments of profiled funciton.
        func_result: Profiled function result.
        func_execution_time: Profiled function execution time.
        func_exception: Exception raised during execution, if any.
    """
    
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
    """Structured profiling result for time profiling with timeit module.
    
    Args:
        profiler: An instance of TimeItProfiler.
        profiled_func: Profiled function.
        func_kwargs: Keyword arguments of profiled funciton.
        func_result: Profiled function result.
        repeat: Number of repetitions in the timeit loop.
        min_func_execution_time: Minimum execution time.
        avg_func_execution_time: Average execution time.
        max_func_execution_time:  Maximum execution time.
        func_exception: Exception raised during execution, if any.
    """
    
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