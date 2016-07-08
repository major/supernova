import webbrowser

from click.testing import CliRunner


from supernova import credentials, executable, supernova


class TestExecutable(object):

    def test_version_output(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova, ['--version'])
        assert result.exit_code == 0
        assert "supernova, version" in result.output

    def test_list_output(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova, ['--list'])
        assert result.exit_code == 0
        assert "dfw" in result.output

    def test_list_specify_config_file(self):
        runner = CliRunner()
        command = ['-c', 'tests/configs/test_list_specify_config_file',
                   '--list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code == 0
        assert "test_list_specify_config_file" in result.output

    def test_list_broken_configuration_file(self):
        runner = CliRunner()
        command = ['-c', 'tests/configs/rax_without_keyring_malformed',
                   '--list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code != 0
        assert "There's an error in your configuration file" in result.output

    def test_shortlist_output(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova, ['--shortlist'])
        assert result.exit_code == 0
        assert "dfw" in result.output

    def test_shortlist_specify_config_file(self):
        runner = CliRunner()
        command = ['-c', 'tests/configs/test_list_specify_config_file',
                   '--shortlist']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code == 0
        assert "test_list_specify_config_file" in result.output

    def test_shortlist_broken_configuration_file(self):
        runner = CliRunner()
        command = ['-c', 'tests/configs/rax_without_keyring_malformed',
                   '--shortlist']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code != 0
        assert "There's an error in your configuration file" in result.output

    def test_get_credential_success(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova_keyring,
                               ['-g', 'test', 'test'], input="y\n")

        assert result.exit_code == 0
        assert "password from TestKeyring" in result.output

    def test_missing_command(self):
        runner = CliRunner()
        command = ['dfw']
        result = runner.invoke(executable.run_supernova, command)
        from pprint import pprint
        pprint(result)
        assert result.exit_code == 1
        assert "Missing arguments" in result.output

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

    def test_valid_environment_list(self, monkeypatch):
        def mockreturn(nova_creds, nova_args, supernova_args):
            return 0
        monkeypatch.setattr(supernova, "run_command", mockreturn)
        runner = CliRunner()
        command = ['dfw,ord', 'list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code == 0

    def test_valid_environment_list_with_group(self, monkeypatch):
        def mockreturn(nova_creds, nova_args, supernova_args):
            return 0
        monkeypatch.setattr(supernova, "run_command", mockreturn)
        runner = CliRunner()
        command = ['dfw,raxusa', 'list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code == 0

    def test_env_regex(self, monkeypatch):
        envs = []

        def mockreturn(nova_creds, nova_args, supernova_args):
            envs.append(supernova_args['nova_env'])
            return 0
        monkeypatch.setattr(supernova, "run_command", mockreturn)
        runner = CliRunner()
        command = ['/^s/', 'list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code == 0
        assert envs == ['syd', 'someinova']

    def test_broken_configuration_file(self):
        runner = CliRunner()
        command = ['-c', 'tests/configs/rax_without_keyring_malformed', 'dfw',
                   'list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code != 0
        assert "There's an error in your configuration file" in result.output

    def test_broken_configuration_directory(self):
        runner = CliRunner()
        command = ['-c', 'tests/configs/', 'dfw',
                   'list']
        result = runner.invoke(executable.run_supernova, command)
        assert "Skipping 'tests/configs/rax_without_keyring_malformed', "
        "Parsing Error." in result.output

    def test_dashboard(self, monkeypatch):
        def mockreturn(url):
            return False
        monkeypatch.setattr(webbrowser, "open", mockreturn)
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova,
                               ['--dashboard', 'dfw'])
        assert result.exit_code == 0

    def test_dashboard_group(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova,
                               ['--dashboard', 'raxusa'])
        assert result.exit_code == 1
        assert 'group of environments' in result.output

    def test_dashboard_no_url(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova,
                               ['--dashboard', 'hkg'])
        assert result.exit_code == 1
        assert 'No SUPERNOVA_DASHBOARD_URL' in result.output

    def test_echo(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova, ['--echo', 'hkg'])
        assert result.exit_code == 0
        assert len(result.output.split('\n')) == 10
        assert 'OS_REGION_NAME=HKG' in result.output

    def test_echo_group(self):
        runner = CliRunner()
        result = runner.invoke(executable.run_supernova, ['--echo', 'raxusa'])
        assert result.exit_code == 1
        assert 'group of environments' in result.output

    def test_missing_configuration_file(self):
        runner = CliRunner()
        command = ['-c', 'asdfasdfasdfasdfasdfasdfasdf', 'dfw',
                   'list']
        result = runner.invoke(executable.run_supernova, command)
        assert result.exit_code != 0
        assert "Couldn't find a valid configuration file" in result.output
