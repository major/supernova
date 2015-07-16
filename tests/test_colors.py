from supernova import colors


class TestColors(object):

    def test_gwrap(self):
        output = colors.gwrap("TEST")
        assert output == "\x1b[92mTEST\x1b[0m"

    def test_rwrap(self):
        output = colors.rwrap("TEST")
        assert output == "\x1b[91mTEST\x1b[0m"
