import os


def test_environment_variables(set_environment_variables):
    """ Tests if the required environment variables in order to correctly execute those tests are valid. """
    assert os.environ['STEAM_DATA_PATH'] == "temp", "Wrong Steam data directory path!"
    assert os.environ['PYTHON_VIRTUALENV_PATH'] == ".venv", "Wrong Python virtualenv path!"