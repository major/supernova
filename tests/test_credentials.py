import keyring.backend


import six


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

    def test_password_get(self):
        keyring.set_keyring(TestKeyring())
        result = credentials.password_get('user')
        if six.PY3:
            assert result == 'password from TestKeyring'
        else:
            assert result == b'password from TestKeyring'

    def test_pull_env_credential(self):
        keyring.set_keyring(TestKeyring())
        result = credentials.pull_env_credential('prod',
                                                 'OS_PASSWORD',
                                                 'USE_KEYRING["prodpass"]'
                                                 )
        assert isinstance(result, tuple)
        assert result[0] == 'global:prodpass'
        assert 'TestKeyring' in result[1]
        if six.PY3:
            assert result[1] == 'password from TestKeyring'
        else:
            assert result[1] == b'password from TestKeyring'
