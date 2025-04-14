import inspect, json, yaml
from abc import ABC, abstractmethod
from python_profiling.enums import SerializerStrategy
from Internals.checks import ValidateType
from Internals.execution_guards import serialization_handler
from Internals.logger import logger


class SerializerI(ABC):
    @classmethod
    @abstractmethod
    def dump(cls, data: dict, file_path: str, mode: str):
        ...
        
        
class JSONSerializer(SerializerI):
    @classmethod
    @serialization_handler('.json')
    def dump(cls, data: dict, file_path: str, mode: str):
        with open(file_path, mode=mode) as f:
            json.dump(data, f, indent=4)
            
            
class TXTSerializer(SerializerI):
    @classmethod
    @serialization_handler('.txt')
    def dump(cls, data: dict, file_path: str, mode: str):
        with open(file_path, mode=mode) as f:
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
                
                
class YAMLSerializer(SerializerI):
    @classmethod
    @serialization_handler('.yaml')
    def dump(cls, data: dict, file_path: str, mode: str):
        with open(file_path, mode=mode) as f:
            yaml.safe_dump(data, f)    
      
                
class SerializationHandler:
    _avaliable_serializers = {SerializerStrategy.JSON: JSONSerializer,
                             SerializerStrategy.TXT: TXTSerializer,
                             SerializerStrategy.YAML: YAMLSerializer}  
    
    @classmethod
    @ValidateType([('serializer', SerializerI), ('serializer_name', SerializerStrategy)]) # probably will be removedd
    def _add_serializer(cls, serializer: SerializerI, serializer_name: SerializerStrategy):
        cls._avaliable_serializers[serializer_name] = serializer
        logger.info('%s has been added as %s', serializer, serializer_name)
        
        
    @classmethod
    def _remove_serializer(cls, serializer_name: SerializerStrategy):
        if serializer_name in cls._avaliable_serializers:
            del cls._avaliable_serializers[serializer_name]
            logger.info('%s has been removed', serializer_name)
        
        
    @classmethod
    def avaliable_serializers(cls):
        return cls._avaliable_serializers
        
        
    @classmethod
    @ValidateType(('serializer_strategy', SerializerStrategy)) # probably will be removed
    def dump(cls, 
             data: dict, 
             file_path: str,
             mode: str = 'w', 
             serializer_strategy: SerializerStrategy = SerializerStrategy.TXT):
        
        cls._avaliable_serializers[serializer_strategy].dump(data=data,
                                                             file_path=file_path,
                                                             mode=mode)
                
                
                