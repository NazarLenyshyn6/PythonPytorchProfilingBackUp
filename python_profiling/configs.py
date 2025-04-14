"""Data Transfer Objects for Python profiling."""

from pydantic import BaseModel, ConfigDict, Field, model_validator
from python_profiling.enums import SerializerStrategy


class StorageConfig(BaseModel):
    """Configuration for storing profiling results.
    
    Attributes:
        serializers_strategies (list[SerializerStrategy]): List of serializers to use
            for saving profiling results. Defaults to an empty list.
        file_path (list[str]): List of file paths where results will be saved.
            Defaults to an empty list.
        modes(list[str]):  List of file write modes. If not provided,
            defaults to ['w'] for each serializer.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    serializers_strategies: list[SerializerStrategy] = Field(default_factory=list)
    file_paths: list[str] = Field(default_factory=list)
    modes: list[str] | None = Field(default=None)
    
    def model_post_init(self, __context):
        """Assign default write mode 'w' to each file if none is provided."""
        if not self.modes:
            self.modes = ['w' for _ in range(len(self.serializers_strategies))]
            
    @model_validator(mode='after')
    def validate_lenghts_match(self) -> 'StorageConfig':
        """Validate that all configuration lists are of equal length.
        
        Returns:
            StorageConfig: Validated instance.
        
        Raises:
            ValueError: If `serializers_strategies`, `file_paths`, and `modes`
                do not have the same length.
        """
        serializers_lenght = len(self.serializers_strategies)
        file_paths_lenght = len(self.file_paths)
        modes_lenght = len(self.modes)
        
        if not (serializers_lenght == file_paths_lenght == modes_lenght == modes_lenght):
            raise ValueError(
                f'Amount of serializers, file_paths and modes has to be equal'
                f'got istead: {serializers_lenght, file_paths_lenght, modes_lenght}'
                )
        return self