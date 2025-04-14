import os
from functools import wraps
from Internals.logger import logger


def serialization_handler(file_extension: str):
    def decorator(func):
        @wraps(func)
        def wrapper(cls, data: dict, file_path: str, mode: str = 'w'):
            if not isinstance(file_path, str) or not file_path.endswith(file_extension):
                logger.info('Impossible to serialize data because %s has invalid extenstion, valid extension: %s', file_path, file_extension)
                return
            
            try:
                func(cls, data, file_path, mode)
                logger.info('Successfully serialized data to %s', file_path)
                
            except Exception as e:
                if os.path.exists(file_path) and not os.path.getsize(file_path):
                    os.remove(file_path)
                    
                logger.info('Impossigle to serialize data to %s because of following exception: %s', file_path, str(e))
                return
                
        return wrapper
    return decorator
