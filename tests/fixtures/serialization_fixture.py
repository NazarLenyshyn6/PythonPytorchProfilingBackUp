"""Fixtures for serialization setups and tear dows."""

import copy

import pytest

from python_profiling import python_profiling_enums
from Internals import serialization
from Internals.logger import logger


@pytest.fixture(scope='module')
def reset_serializers():
    """Mocks avaliable serializers for test and than restore to original state."""
    original_serializers = copy.deepcopy(serialization.SerializationHandler._avaliable_serializers)
    serialization.SerializationHandler._avaliable_serializers = {
        python_profiling_enums.SerializerStrategy.TXT: serialization.TXTSerializer
        }
    logger.info('SerializationHandler avaliable serializers has been mocked.')
    yield
    serialization.SerializationHandler._avaliable_serializers = original_serializers
    logger.info('SerializationHandler avaliable serializers has been restored to original ones.')