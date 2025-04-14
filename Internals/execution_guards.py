"""Helper functions that encapsulate logic of expection handling to guarantee safe function execution."""

import os
from functools import wraps
from Internals.logger import logger
from typing import Callable


def serialization_handler(file_extension: str):
    '''Decorator Factory which handle excaptions that occurs during serialization process.
    
    Args:
        file_extenstion (str): Required extenstion for file path.
        
    Returns:
        Callable: Decorator which handle exceptions that occurs during serialization process.
    '''
    def decorator(func: Callable) -> Callable:
        """Decorator which handle excaptions that occurs during serialization process.
        
        Args:
            func (Callable): The function that performs serializatoin.
            
        Returns:
            Callable: Wrapped function that performs serialization.
        """
        @wraps(func)
        def wrapper(cls, data: dict, file_path: str, mode: str = 'w'):
            '''Wrapped function that validates path and handles serialization exceptions.
            
            Args:
                cls: Class instance or class object using the decorator.
                data (data): Data to serialize.
                file_path (str): Output file path.
                mode (str): File mode, default is 'w' (write).
                
            Returns:
                None: return no value, log result of serializaton process.
            '''
            if not isinstance(file_path, str) or not file_path.endswith(file_extension):
                logger.info(
                    'Impossible to serialize data because %s has invalid extenstion, valid extension: %s', 
                    file_path, 
                    file_extension
                    )
                return
            
            try:
                func(cls, data, file_path, mode)
                logger.info(
                    'Successfully serialized data to %s', 
                    file_path
                    )    
            except Exception as e:
                if os.path.exists(file_path) and not os.path.getsize(file_path):
                    os.remove(file_path)
                    
                logger.info(
                    'Impossigle to serialize data to %s because of following exception: %s', 
                    file_path, 
                    str(e)
                    )
                return   
        return wrapper
    return decorator
