import os


import pytest


from supernova import config


class TestConfig(object):

    def test_run_config(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        result = config.run_config(testcfg)
        assert result is not None
        assert len(result.keys()) == 5
        assert 'dfw' in result.keys()

    # NOTE: This test uses the .supernova testing config file in the root
    # of the repository.  It's hacky but it's what I've got. :/
    def test_get_config_file(self):
        result = config.get_config_file()
        assert result is not None
        assert result == '.supernova'

    def test_read_valid_configuration(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        result = config.load_config(config_file_override=testcfg)
        assert result is not None
        assert len(result.keys()) == 5
        assert 'dfw' in result.keys()

    def test_read_missing_configuration(self):
        testcfg = "/tmp/invalid_file"
        result = None
        with pytest.raises(Exception) as excinfo:
            result = config.load_config(config_file_override=testcfg)
        assert result is None
        assert "Couldn't find" in str(excinfo.value)

    def test_override_with_non_string(self):
        testcfg = "/tmp/invalid_file"
        result = None
        with pytest.raises(Exception) as excinfo:
            result = config.load_config(config_file_override=[testcfg])
        assert result is None
        assert "must be a string" in str(excinfo.value)
