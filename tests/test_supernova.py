import os


from supernova import config, supernova


class TestSuperNova(object):

    def test_for_bypass_url(self):
        raw_creds = {
            "BYPASS_URL": 'some_url'
        }
        nova_args = []
        result = supernova.check_for_bypass_url(raw_creds, nova_args)
        assert result == ['--bypass-url', 'some_url']

    def test_for_no_bypass_url(self):
        raw_creds = {
            "NO_BYPASS_URL_HERE": 'some_url'
        }
        nova_args = []
        result = supernova.check_for_bypass_url(raw_creds, nova_args)
        assert result == []

    def test_for_executable_env_var(self):
        env_vars = {
            'OS_EXECUTABLE': 'glance'
        }
        supernova_args = {}
        supernova_args = supernova.check_for_executable(supernova_args,
                                                        env_vars)
        assert 'executable' in supernova_args
        assert supernova_args['executable'] == 'glance'

    def test_run_novaclient(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config(testcfg)
        supernova_args = {
            'debug': False,
            'executable': 'echo',
            'nova_env': 'dfw',
            'quiet': False,
        }
        result = supernova.run_command(nova_creds, ['list'], supernova_args)
        assert result == 0

    def test_run_novaclient_quiet(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config(testcfg)
        supernova_args = {
            'debug': False,
            'executable': 'echo',
            'nova_env': 'dfw',
            'quiet': True,
        }
        result = supernova.run_command(nova_creds, ['list'], supernova_args)
        assert result == 0

    def test_run_novaclient_with_debug(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config(testcfg)
        supernova_args = {
            'debug': True,
            'executable': 'echo',
            'nova_env': 'dfw',
            'quiet': False,
        }
        result = supernova.run_command(nova_creds, ['list'], supernova_args)
        assert result == 0

    def test_handle_stderr(self, tmpdir, capsys):
        p = tmpdir.mkdir("sub").join("stderr.txt")
        p.write("This would be in the stderr pipe")
        result = supernova.handle_stderr(p)
        out, err = capsys.readouterr()
        assert "stderr pipe" in out
        assert result
