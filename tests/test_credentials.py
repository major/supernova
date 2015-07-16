import keyring.backend


from supernova import credentials


class TestKeyring(keyring.backend.KeyringBackend):
    """A test keyring which always outputs same password
    """
    priority = 1

    def set_password(self, servicename, username, password):
        pass

    def get_password(self, servicename, username):
        return "password from TestKeyring"

    def delete_password(self, servicename, username, password):
        pass


class TestCredentials(object):

    def test_get_user_password(self):
        keyring.set_keyring(TestKeyring())
        result = credentials.get_user_password('prod', 'prodpass', force=True)
        assert result is None

    def test_pull_env_credential(self):
        keyring.set_keyring(TestKeyring())
        result = credentials.pull_env_credential('prod',
                                                 'OS_PASSWORD',
                                                 'USE_KEYRING["prodpass"]'
                                                 )
        assert isinstance(result, tuple)
        assert result[0] == 'global:prodpass'
        assert result[1] == 'password from TestKeyring'
