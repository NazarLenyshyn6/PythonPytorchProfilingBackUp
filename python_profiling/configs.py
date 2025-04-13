from pydantic import BaseModel, ConfigDict, Field, model_validator
from python_profiling.enums import SerializerStrategy


class StorageConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    serializers_strategies: list[SerializerStrategy] = Field(default_factory=list)
    file_paths: list[str] = Field(default_factory=list)
    modes: list[str] | None = Field(default=None)
    
    
    def model_post_init(self, __context):
        if not self.modes:
            self.modes = ['w' for _ in range(len(self.serializers_strategies))]
            
    
    @model_validator(mode='after')
    def validate_lenghts_match(self) -> 'StorageConfig':
        serializers_lenght = len(self.serializers_strategies)
        file_paths_lenght = len(self.file_paths)
        modes_lenght = len(self.modes)
        
        if not (serializers_lenght == file_paths_lenght == modes_lenght == modes_lenght):
            raise ValueError(f'Amount of serializers, file_paths and modes has to be equal, got istead: {serializers_lenght, file_paths_lenght, modes_lenght}')
        
        return self