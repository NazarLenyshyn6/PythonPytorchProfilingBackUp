"""Serializers to write profiling results to various sources in different formats."""

from abc import ABC, abstractmethod
import inspect
import json

import yaml

from python_profiling.enums import SerializerStrategy
from Internals.checks import ValidateType
from Internals.execution_guards import serialization_handler
from Internals.logger import logger


class SerializerI(ABC):
    """Defines common interface for all data serializers."""
    
    @classmethod
    @abstractmethod
    def dump(cls, data: dict, file_path: str, mode: str):
        ...
        
        
class JSONSerializer(SerializerI):
    """Serialize data in JSON format."""
    
    @classmethod
    @serialization_handler('.json')
    def dump(cls, data: dict, file_path: str, mode: str) -> None:
        """Serializes the data to a file using JSON format.
        
        Args:
            data (dict): Data to serialize.
            file_path (str): Output file path.
            mode (str):  File mode, default is 'w' (write).
            
        Returns:
            None
        """
        with open(file_path, mode=mode) as f:
            json.dump(data, f, indent=4)
            
            
class TXTSerializer(SerializerI):
    """Serializes data in plain text format."""
    
    @classmethod
    @serialization_handler('.txt')
    def dump(cls, data: dict, file_path: str, mode: str):
        """Serializes the data to a file using plain text format.
        
        Args:
            data (dict): Data to serialize.
            file_path (str): Output file path.
            mode (str):  File mode, default is 'w' (write).
            
        Returns:
            None
        """
        with open(file_path, mode=mode) as f:
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
                
                
class YAMLSerializer(SerializerI):
    """Serializes data in YAML format."""
    
    @classmethod
    @serialization_handler('.yaml')
    def dump(cls, data: dict, file_path: str, mode: str):
        """Serializes the data to a file using YAML format.
        
        Args:
            data (dict): Data to serialize.
            file_path (str): Output file path.
            mode (str):  File mode, default is 'w' (write).
            
        Returns:
            None
        """
        with open(file_path, mode=mode) as f:
            yaml.safe_dump(data, f)    
      
                
class SerializationHandler:
    """Handles registration and execution of serializers for various formats.
    
    Attributes:
        _avaliable_serializers (dict[SerializerStrategy, SerializerI]): A registry
            of available serializers mapped by their respective strategy.
    """
    _avaliable_serializers = {SerializerStrategy.JSON: JSONSerializer,
                             SerializerStrategy.TXT: TXTSerializer,
                             SerializerStrategy.YAML: YAMLSerializer}  
    
    @classmethod
    @ValidateType([('serializer', SerializerI), ('serializer_name', SerializerStrategy)]) # probably will be removedd
    def _add_serializer(cls, serializer: SerializerI, serializer_name: SerializerStrategy) -> None:
        """Registers a new serializer into the available serializers registry.
        
        Args:
            serializer (SerializerI): A class that inherits from `SerializerI` and provides
                                    a concrete implementation for data serialization.
            serializer_name (SerializerStrategy): Name to register serializer under.
            
        Returns:
            None
            
        Raises:
            InvalidInputTypeError: If serializer or serializer_name are of incorrect types.
            MissingArgumentError: If any required argument is missing.
        """
        cls._avaliable_serializers[serializer_name] = serializer
        logger.info('%s has been added as %s', serializer, serializer_name)
        
        
    @classmethod
    def _remove_serializer(cls, serializer_name: SerializerStrategy) -> None:
        """Removes a serializer from the registry.

        Args:
            serializer_name (SerializerStrategy): The serializer name to remove.

        Returns:
            None
        """
        if serializer_name in cls._avaliable_serializers:
            del cls._avaliable_serializers[serializer_name]
            logger.info('%s has been removed', serializer_name)
        
        
    @classmethod
    def avaliable_serializers(cls):
        """Returns the currently registered serializers.

        Returns:
            dict: Dictionary of all available serializers.
        """
        return cls._avaliable_serializers
        
        
    @classmethod
    @ValidateType(('serializer_strategy', SerializerStrategy)) # probably will be removed
    def dump(cls, 
             data: dict, 
             file_path: str,
             mode: str = 'w', 
             serializer_strategy: SerializerStrategy = SerializerStrategy.TXT
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
        
        cls._avaliable_serializers[serializer_strategy].dump(data=data,
                                                             file_path=file_path,
                                                             mode=mode)
                
                
                