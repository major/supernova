from click.testing import CliRunner


import pkg_resources


from supernova import credentials, executable, supernova


class TestExecutable(object):

    def test_version_output(self):
        # Get the current version number using setuptools
        version = pkg_resources.require("supernova")[0].version

        runner = CliRunner()
        result = runner.invoke(executable.run_supernova, ['--version'])
        assert result.exit_code == 0
        assert result.output == "supernova, version {0}\n".format(version)

    def test_get_credential_success(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova_keyring,
                               ['-g', 'test', 'test'], input="y\n")

        assert result.exit_code == 0
        assert "password from TestKeyring" in result.output

    def test_missing_command(self):
        runner = CliRunner()
        command = ['environment']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code == 2
        assert "Usage" in result.output

    def test_invalid_env(self):
        runner = CliRunner()
        command = ['nonexistent', 'list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code == 1
        assert "Couldn't find an environment" in result.output

    def test_keyring_cant_get_password(self, monkeypatch):
        def mockreturn(env, param):
            return False
        monkeypatch.setattr(credentials, "get_user_password", mockreturn)
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova_keyring,
                               ['-g', 'test', 'test'], input="y\n")

        assert result.exit_code == 1
        assert "Unable to find a credential" in result.output

    def test_keyring_without_action(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova_keyring,
                               ['test', 'test'], input="y\n")

        assert result.exit_code == 0
        assert "must specify --get or --set" in result.output

    def test_set_credential_failure(self, monkeypatch):
        def mockreturn(environment, parameter, password):
            return False
        monkeypatch.setattr(credentials, "set_user_password", mockreturn)
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova_keyring,
                               ['-s', 'test', 'test'], input="test")
        assert result.exit_code == 1
        assert "Unable to store" in result.output

    def test_set_credential_failure_full(self, monkeypatch):
        def mockreturn(environment, parameter, password):
            return False
        monkeypatch.setattr(credentials, "set_user_password", mockreturn)
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova_keyring,
                               ['--set', 'test', 'test'], input="test")
        assert result.exit_code == 1
        assert "Unable to store" in result.output

    def test_set_credential_success(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova_keyring,
                               ['-s', 'test', 'test'], input="test")
        assert result.exit_code == 0
        assert "Successfully stored" in result.output

    def test_valid_group(self, monkeypatch):
        def mockreturn(nova_creds, nova_args, supernova_args):
            return 0
        monkeypatch.setattr(supernova, "run_command", mockreturn)
        runner = CliRunner()
        command = ['raxusa', 'list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code == 0
