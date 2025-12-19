import os
import pytest


@pytest.fixture
def set_steam_data_path():
    # We do not want to affect the actual Steam data directory
    os.environ['STEAM_DATA_PATH'] = "temp"


@pytest.fixture(scope="session")
def install_package_locally():
    # We want to run our tests on the latest development version
    os.system("pip install .")


@pytest.fixture
def set_environment_variables(set_steam_data_path, install_package_locally):
    # We do not want to test on the real installation but on this one
    os.environ['PYTHON_VIRTUALENV_PATH'] = ".venv"
