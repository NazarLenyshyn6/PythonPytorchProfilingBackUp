"""."""

import os
import pytest

from Internals.logger import logger

pytest_plugins = [
    "tests.fixtures.configs_fixtures",
    "tests.fixtures.file_fixtures",
    "tests.fixtures.profiling_results_fixtures",
    "tests.fixtures.serialization_fixture",
    "tests.fixtures.time_profiler_fixtures"
]


@pytest.fixture
def remove_dummy_file():
    """Removes files created during testing."""
    def cleanup(file_path: str):
        if not os.path.exists(file_path):
            logger.info('File %s not found. Skipping removal', file_path)
            return
        try:
            os.remove(file_path)
            logger.info(f"Successfully removed file: %s", file_path)
        except Exception as e:
            logger.info('Impossible to remove %s because of : %s', file_path, str(e))
    return cleanup