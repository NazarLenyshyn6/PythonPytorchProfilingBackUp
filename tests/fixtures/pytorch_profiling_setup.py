"""Fixtures for pytorch profiling setup."""

import os
import shutil

import pytest
import torch

from Internals.logger import logger

class PyTorchProfilingSetup:
    model = torch.nn.Linear(1000, 1000)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    loss_fn = torch.nn.MSELoss()
    data = torch.randn(20, 1000)
    target = torch.rand(20, 1000)
    
    
@pytest.fixture(scope='module')
def pytorch_profiling_setup():
    return PyTorchProfilingSetup

@pytest.fixture
def remove_profiling_dir():
    """Removes files created during testing."""
    def cleanup(output_dir: str):
        if not os.path.exists(output_dir):
            logger.info('Directory %s not found. Skipping removal', output_dir)
            return
        try:
            shutil.rmtree(output_dir, ignore_errors=True)
            logger.info(f"Successfully removed directory: %s", output_dir)
        except Exception as e:
            logger.info('Impossible to remove %s because of : %s', output_dir, str(e))
    return cleanup
        
        