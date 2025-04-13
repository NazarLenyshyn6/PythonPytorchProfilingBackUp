from enum import Enum

class FilePath(Enum):
    JSON = 'json'
    TXT = 'txt'
    YAML = 'yaml'
    
    
class FileExtension(Enum):
    JSON = '.json'
    TXT = '.txt'
    YAML = '.yaml'