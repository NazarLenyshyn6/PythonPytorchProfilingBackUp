"""Tools for visualization of call graph profiling."""

from abc import ABC, abstractmethod
import os
import subprocess
from typing_extensions import override

from Internals import checks
from Internals.logger import logger

class CallGraphVisualizerI(ABC):
    """Interface for call graph visualizer."""
    
    @abstractmethod
    def visualize(self, output_file: str):
        """Visualize call graph progiling.
        
        Args:
            output_file: file with call graph profiling result.
        """
    
class Gprof2dotVisualizer(CallGraphVisualizerI):
    
    @staticmethod
    @checks.ValidateType(('output_file', str))
    @override
    def visualize(output_file):
        if not output_file.endswith('.prof'):
            if os.path.exists(output_file):
                os.remove(output_file)
            raise ValueError('File path has to have  .prof extension')
        dot_file = output_file.replace('.prof', '.png')
        cmd = f"gprof2dot -f pstats {output_file} | dot -Tpng -o {dot_file}"
        subprocess.run(cmd, shell=True)
        logger.info('Visualization done successfuly.')
    
class SnakevizVisualizer(CallGraphVisualizerI):
    @staticmethod
    @checks.ValidateType(('output_file', str))
    @override
    def visualize(output_file):
        subprocess.run(f"snakeviz {output_file}", shell=True)
        logger.info('Visualization done successfuly.')