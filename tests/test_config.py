import os


import pytest


from supernova import config


class TestConfig(object):

    def test_run_config(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        result = config.run_config(testcfg)
        assert result is not None
        assert len(result.keys()) == 7
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
        assert len(result.keys()) == 7
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


class TestDynamicConfig(object):

    def test_bad_config_arg(self):
        result = None
        with pytest.raises(ValueError) as val_error:
            result = config.create_dynamic_configs('bad_arg')
        assert result is None
        assert "config should be ConfigObj" in str(val_error)

    def test_dynamic_sections_without_default(self):
        result = config.load_config()
        result['dynamic-section'] = {'OS_REGION_NAME': "DFW;ORD"}
        config.create_dynamic_configs(result)
        # The new sections exist
        assert 'dynamic-section-ORD' in result.sections
        assert 'dynamic-section-DFW' in result.sections

        # The default section is no longer provided
        assert 'dynamic-section' not in result.sections

        # The super group is set up correctly
        assert 'dynamic-section' in \
               result['dynamic-section-ORD'].get('SUPERNOVA_GROUP')
        assert 'dynamic-section' == \
               result['dynamic-section-DFW'].get('SUPERNOVA_GROUP')

        # The regions are correct
        assert 'ORD' == \
               result['dynamic-section-ORD'].get('OS_REGION_NAME')
        assert 'DFW' == \
               result['dynamic-section-DFW'].get('OS_REGION_NAME')
