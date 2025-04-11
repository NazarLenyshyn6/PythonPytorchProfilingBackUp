import os
from functools import wraps


def serialization_handler(file_extension: str):
    def decorator(func):
        @wraps(func)
        def wrapper(cls, data: dict, file_path: str, mode: str = 'w'):
            if not isinstance(file_path, str) or not file_path.endswith(file_extension):
                print(f'Impossible to serialize data because {file_path} has invalid extension, valid extension: {file_extension}')
                return
            
            try:
                func(cls, data, file_path, mode)
                
            except Exception as e:
                if os.path.exists(file_path) and not os.path.getsize(file_path):
                    os.remove(file_path)
                    
                print(f'Impossible to serialize data because to {file_path} of following exeption: {str(e)}')
                
        return wrapper
    return decorator
