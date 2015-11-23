import sys
orig_import = __import__


class MockGi(object):
    called = 0

    @classmethod
    def require_version(cls, keyring, version):
        cls.called += 1
        return True

if getattr(sys.version_info, 'major', 2) == 3:
    import builtins

    class TestSupernovaImport(object):
        def test_import_gi(self):
            def import_mock(name, *args, **kwargs):
                if name == 'gi.require_version':
                    return MockGi
                return orig_import(name, *args, **kwargs)

            mods = sys.modules.copy()
            tmpmod = {}
            loading = []
            for mod in mods:
                if mod.startswith('supernova'):
                    if mod.startswith('supernova'):
                        loading.append(mod.split('.')[-1])
                    tmpmod[mod] = sys.modules[mod]
                    del sys.modules[mod]
            builtins.__import__ = import_mock
            __import__('supernova', fromlist=loading)
            sys.modules.update(tmpmod)
            assert MockGi.called == 1
            builtins.__import__ = orig_import
else:
    import __builtin__

    class TestSupernovaImport(object):
        def test_import_supernova_exception(self):
            def import_mock(name, *args, **kwargs):
                if name == 'gi.require_version':
                    return MockGi
                return orig_import(name, *args, **kwargs)
            mods = sys.modules.copy()
            loading = []
            tmpmod = {}
            for mod in mods:
                if mod.startswith('supernova'):
                    loading.append(mod.split('.')[-1])
                    tmpmod[mod] = sys.modules[mod]
                    del sys.modules[mod]
            __builtin__.__import__ = import_mock
            __import__('supernova', fromlist=loading)
            sys.modules.update(tmpmod)
            assert MockGi.called == 1
            __builtin__.__import__ = orig_import
