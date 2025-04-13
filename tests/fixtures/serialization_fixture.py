import pytest
from copy import deepcopy
from Internals.serialization import SerializationHandler, TXTSerializer, YAMLSerializer
from python_profiling.enums import SerializerStrategy
from Internals.logger import logger


@pytest.fixture(scope='module')
def reset_serializers():
    original_serializers = deepcopy(SerializationHandler._avaliable_serializers)
    SerializationHandler._avaliable_serializers = {SerializerStrategy.TXT: TXTSerializer}
    logger.info('SerializationHandler avaliable serializers has been mocked')
    yield
    SerializationHandler._avaliable_serializers = original_serializers
    logger.info('SerializationHandler avaliable serializers has been restored to original ones')