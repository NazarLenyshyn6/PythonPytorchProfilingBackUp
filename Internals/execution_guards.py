import os
from functools import wraps
from Internals.logger import logger


def serialization_handler(file_extension: str):
    def decorator(func):
        @wraps(func)
        def wrapper(cls, data: dict, file_path: str, mode: str = 'w'):
            if not isinstance(file_path, str) or not file_path.endswith(file_extension):
                return f'Impossible to serialize data because {file_path} has invalid extension, valid extension: {file_extension}'
            
            try:
                func(cls, data, file_path, mode)
                logger.info('Successfully serialized data to %s', file_path)
                
            except Exception as e:
                if os.path.exists(file_path) and not os.path.getsize(file_path):
                    os.remove(file_path)
                    
                return f'Impossible to serialize data because to {file_path} of following exeption: {str(e)}'
                
        return wrapper
    return decorator
