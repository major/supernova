import os


import click


from supernova import config, utils


class TestUtils(object):

    def test_assemble_username(self):
        result = utils.assemble_username('firstparam', 'secondparam')
        assert result == "firstparam:secondparam"

    def test_env_var_warning(self):
        os.environ["OS_LETS_CAUSE_A_WARNING"] = "BOOM"
        result = utils.check_environment_presets()
        assert not result

    def test_env_var_pass(self):
        os.environ = {"KEY": 'value'}
        result = utils.check_environment_presets()
        assert result

    def test_confirm_credential_display_forced(self):
        result = utils.confirm_credential_display(True)
        assert result

    def test_confirm_credential_display_not_forced(self, monkeypatch):
        # We have to patch the click.confirm() method since we can't use stdin
        # as a user would.
        def mockreturn(text):
            return True
        monkeypatch.setattr(click, "confirm", mockreturn)
        result = utils.confirm_credential_display()
        assert result

    def test_is_valid_environment_success(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config(testcfg)
        result = utils.is_valid_environment('dfw', nova_creds)
        assert result

    def test_is_valid_environment_failure(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config(testcfg)
        result = utils.is_valid_environment('non-existent', nova_creds)
        assert not result

    def test_is_valid_group_success(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config(testcfg)
        result = utils.is_valid_group('raxusa', nova_creds)
        assert result

    def test_is_valid_group_failure(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config(testcfg)
        result = utils.is_valid_group('non-existent', nova_creds)
        assert not result

    def test_get_envs_in_group(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config(testcfg)
        result = utils.get_envs_in_group('raxusa', nova_creds)
        assert len(result) == 3
        assert 'dfw' in result

    def test_rm_prefix(self):
        assert utils.rm_prefix('nova_variable') == 'variable'
        assert utils.rm_prefix('novaclient_variable') == 'variable'
        assert utils.rm_prefix('os_variable') == 'variable'
        assert utils.rm_prefix('bare_variable') == 'bare_variable'
