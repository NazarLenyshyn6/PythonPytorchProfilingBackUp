"""Enumerations for tests."""

import enum

class FilePath(enum.Enum):
    """Enumeration of valid file formats."""
    
    JSON = 'json'
    TXT = 'txt'
    YAML = 'yaml'
    
    
class FileExtension(enum.Enum):
    """Enumeration of valid file extensions."""
    
    JSON = '.json'
    TXT = '.txt'
    YAML = '.yaml'