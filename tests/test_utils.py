import os


from supernova import config, utils


class TestUtils(object):

    def test_get_envs_in_group(self):
        testcfg = "{0}/tests/configs/rax_without_keyring".format(os.getcwd())
        nova_creds = config.load_config([testcfg])
        result = utils.get_envs_in_group('raxusa', nova_creds)
        assert len(result) == 3
        assert 'dfw' in result
