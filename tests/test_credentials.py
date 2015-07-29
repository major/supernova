import keyring.backend


import pytest


import six


from supernova import credentials, utils


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
        assert result[0] == 'prod:prodpass'
        if six.PY3:
            assert result[1] == b'password from TestKeyring'
        else:
            assert result[1] == 'password from TestKeyring'

    def test_get_user_password_failure(self, monkeypatch):
        def mockreturn(path):
            return False
        monkeypatch.setattr(credentials, "password_get", mockreturn)
        keyring.set_keyring(TestKeyring())
        result = credentials.get_user_password('prod', 'prodpass', force=True)
        assert not result

    def test_reject_confirmation(self, monkeypatch):
        def mockreturn(path):
            return False
        monkeypatch.setattr(utils, "confirm_credential_display", mockreturn)
        keyring.set_keyring(TestKeyring())
        result = credentials.get_user_password('prod', 'prodpass')
        assert result is None

    def test_password_get(self):
        keyring.set_keyring(TestKeyring())
        result = credentials.password_get('user')
        if six.PY3:
            assert result == b'password from TestKeyring'
        else:
            assert result == 'password from TestKeyring'

    def test_password_get_failure(self, monkeypatch):
        def mockreturn(self, username, password):
            return None
        monkeypatch.setattr(TestKeyring, "get_password", mockreturn)
        with pytest.raises(LookupError) as excinfo:
            credentials.password_get('global:something')
        assert "Couldn't find a credential" in str(excinfo.value)

    def test_password_set(self):
        keyring.set_keyring(TestKeyring())
        result = credentials.password_set('user', 'password')
        assert result

    def test_password_set_failure(self, monkeypatch):
        def mockreturn(system, username, password):
            return False
        monkeypatch.setattr(keyring, "set_password", mockreturn)
        keyring.set_keyring(TestKeyring())
        result = credentials.password_set('user', 'password')
        assert not result

    def test_invalid_environment(self):
        nova_env = "non-existent"
        nova_creds = {'dfw': None}
        with pytest.raises(KeyError) as excinfo:
            credentials.prep_nova_creds(nova_env, nova_creds)
        assert "was not found" in str(excinfo.value)

    def test_uppercase_credentials(self):
        nova_env = 'prod'
        nova_creds = {
            'prod': {
                'key': 'value'
            }
        }
        result = credentials.prep_nova_creds(nova_env, nova_creds)
        assert result[0][0] == 'KEY'

    def test_lowercase_credentials(self):
        nova_env = 'prod'
        nova_creds = {
            'prod': {
                'http_proxy': 'value'
            }
        }
        result = credentials.prep_nova_creds(nova_env, nova_creds)
        assert result[0][0] == 'http_proxy'

    def test_retrieve_values_from_keyring(self):
        nova_env = 'prod'
        nova_creds = {
            'prod': {
                'OS_PASSWORD': 'USE_KEYRING'
            }
        }
        result = credentials.prep_nova_creds(nova_env, nova_creds)
        if six.PY3:
            assert result[0][1] == b"password from TestKeyring"
        else:
            assert result[0][1] == "password from TestKeyring"

    def test_retrieve_values_from_keyring_failure(self, monkeypatch):
        def mockreturn(nova_env, param, value):
            return ('useername', False)
        monkeypatch.setattr(credentials, "pull_env_credential", mockreturn)
        nova_env = 'prod'
        nova_creds = {
            'prod': {
                'OS_PASSWORD': 'USE_KEYRING'
            }
        }
        with pytest.raises(LookupError) as excinfo:
            credentials.prep_nova_creds(nova_env, nova_creds)
        assert "No matching credentials" in str(excinfo.value)

    def test_pull_env_credential_global(self):
        keyring.set_keyring(TestKeyring())
        result = credentials.pull_env_credential('prod',
                                                 'OS_PASSWORD',
                                                 'USE_KEYRING["prodpass"]'
                                                 )
        assert isinstance(result, tuple)
        assert result[0] == 'global:prodpass'
        if six.PY3:
            assert result[1] == b'password from TestKeyring'
        else:
            assert result[1] == 'password from TestKeyring'

    def test_pull_env_credential_old_style(self):
        keyring.set_keyring(TestKeyring())
        result = credentials.pull_env_credential('prod',
                                                 'OS_PASSWORD',
                                                 'USE_KEYRING'
                                                 )
        assert isinstance(result, tuple)
        assert result[0] == 'prod:OS_PASSWORD'
        if six.PY3:
            assert result[1] == b'password from TestKeyring'
        else:
            assert result[1] == 'password from TestKeyring'

    def test_set_user_password(self):
        keyring.set_keyring(TestKeyring())
        environment = "prod"
        parameter = "prodpass"
        password = "supersecurepassword"
        result = credentials.set_user_password(environment, parameter,
                                               password)
        assert result
