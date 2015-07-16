import os


from supernova import config


class TestConfig(object):

    def test_env_var_warning(self):
        os.environ["OS_LETS_CAUSE_A_WARNING"] = "BOOM"
        result = config.check_environment_presets()
        assert not result

    def test_env_var_pass(self):
        os.environ = {"KEY": 'value'}
        result = config.check_environment_presets()
        assert result

    def test_read_configuration(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        result = config.load_supernova_config(config_file_override=testcfg)
        assert result is not None
        assert len(result.sections()) == 5
        assert 'dfw' in result.sections()
