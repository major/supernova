from supernova import supernova


class TestSuperNova(object):

    def test_init(self):
        obj =  supernova.SuperNova()
        assert obj is not None
