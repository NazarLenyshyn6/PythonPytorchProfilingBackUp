"""Serializers to write profiling results to various sources in different formats."""

from abc import ABC, abstractmethod
import inspect
import json

import yaml
from typing_extensions import override

from python_profiling import python_profiling_enums
from Internals import checks
from Internals import execution_guards
from Internals.logger import logger
from Internals import serialization


class SerializerI(ABC):
    """Defines common interface for all data serializers."""
    
    @classmethod
    @abstractmethod
    def dump(cls, data: dict, file_path: str, mode: str):
        """Serializes the data to a file using specified format.
        
        Args:
            data (dict): Data to serialize.
            file_path (str): Output file path.
            mode (str): File mode, default is 'w' (write).
        """
        
        
class JSONSerializer(SerializerI):
    """Serialize data in JSON format."""
    
    @classmethod
    @execution_guards.serialization_handler('.json')
    @override
    def dump(cls, data: dict, file_path: str, mode: str) -> None:
        with open(file_path, mode=mode) as f:
            json.dump(data, f, indent=4)
            
            
class TXTSerializer(SerializerI):
    """Serializes data in plain text format."""
    
    @classmethod
    @execution_guards.serialization_handler('.txt')
    @override
    def dump(cls, data: dict, file_path: str, mode: str):
        with open(file_path, mode=mode) as f:
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
                
                
class YAMLSerializer(SerializerI):
    """Serializes data in YAML format."""
    
    @classmethod
    @execution_guards.serialization_handler('.yaml')
    @override
    def dump(cls, data: dict, file_path: str, mode: str):
        with open(file_path, mode=mode) as f:
            yaml.safe_dump(data, f)    
      
                
class SerializationHandler:
    """Handles registration and execution of serializers for various formats.
    
    Attributes:
        _avaliable_serializers (dict[SerializerStrategy, SerializerI]): A registry
            of available serializers mapped by their respective strategy.
    """
    _avaliable_serializers = {
        python_profiling_enums.SerializerStrategy.JSON: JSONSerializer,
        python_profiling_enums.SerializerStrategy.TXT: TXTSerializer,
        python_profiling_enums.SerializerStrategy.YAML: YAMLSerializer
        }  
    
    @classmethod
    @checks.ValidateType(
        [
            ('serializer', serialization.SerializerI), 
            ('serializer_name', python_profiling_enums.SerializerStrategy)
            ]
        ) 
    def _add_serializer(
        cls, 
        serializer: SerializerI, 
        serializer_name: python_profiling_enums.SerializerStrategy
        ) -> None:
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
    def _remove_serializer(cls, serializer_name: python_profiling_enums.SerializerStrategy) -> None:
        """Removes a serializer from the registry."""
        if serializer_name in cls._avaliable_serializers:
            del cls._avaliable_serializers[serializer_name]
            logger.info('%s has been removed', serializer_name)
        
        
    @classmethod
    def avaliable_serializers(cls):
        """Returns the currently registered serializers."""
        return cls._avaliable_serializers
        
        
    @classmethod
    @checks.ValidateType(('serializer_strategy', python_profiling_enums.SerializerStrategy)) # probably will be removed
    def dump(
        cls, 
        data: dict, 
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
        
        cls._avaliable_serializers[serializer_strategy].dump(data=data,
                                                             file_path=file_path,
                                                             mode=mode)
                
                
                