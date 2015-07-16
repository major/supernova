from click.testing import CliRunner


import pkg_resources


from supernova import executable


class TestSuperNova(object):

    def test_version_output(self):
        # Get the current version number using setuptools
        version = pkg_resources.require("supernova")[0].version

        runner = CliRunner()
        result = runner.invoke(executable.run_supernova, ['--version'])
        assert result.exit_code == 0
        assert result.output == "supernova, version {0}\n".format(version)
