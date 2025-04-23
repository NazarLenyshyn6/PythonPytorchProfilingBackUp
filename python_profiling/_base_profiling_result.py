"""Functionality that is common accross all profiling result (time, memory, call graph)."""

from typing import Any


from python_profiling import python_profiling_enums
from Internals import serialization
from Internals import checks
from Internals.logger import logger


class BaseProfilingResult:
    """Defines functionality that is common across all profiling results."""
    
    @property
    def profiling_data(self):
        """Returns profiling data as a dictionary."""
        return self.__dict__
    
    @property
    def profiling_data_str(self):
        """Returns profiling data with all values as strings."""
        return {key: f'{value}' for key, value in self.profiling_data.items()}
    
    @checks.ValidateType(('context', dict))
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
        """Removes a key from the profiling context."""
        if context_element in self.__dict__:
            del self.__dict__[context_element]
            logger.info('context %s has been removed from profiling data', context_element)
            
    def dump(
        self, 
        file_path: str, 
        mode: str = 'w', 
        serializer_strategy: python_profiling_enums.SerializerStrategy = python_profiling_enums.SerializerStrategy.TXT
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
        
        serialization.SerializationHandler.dump(data=self.profiling_data_str,
                                                file_path=file_path,
                                                mode=mode,
                                                serializer_strategy=serializer_strategy)