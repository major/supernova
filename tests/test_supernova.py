import os


from supernova import config, supernova


class TestSuperNova(object):

    def test_run_novaclient(self):
        # def mockreturn(commandline):
        #     return False
        # monkeypatch.setattr(supernova, "execute_executable", mockreturn)
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config([testcfg])
        supernova_args = {
            'debug': False,
            'executable': 'echo',
            'nova_env': 'dfw'
        }
        result = supernova.run_command(nova_creds, 'list', supernova_args)
        assert result == 0

    def test_run_novaclient_with_debug(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config([testcfg])
        supernova_args = {
            'debug': True,
            'executable': 'echo',
            'nova_env': 'dfw'
        }
        result = supernova.run_command(nova_creds, 'list', supernova_args)
        assert result == 0
