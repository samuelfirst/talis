import pytest
from configargparse import ArgParser

from talis.config import AppConfig


class TestAppConfig(object):
    def test_with_invalid_type(self):
        with pytest.raises(TypeError) as e_info:
            AppConfig([])

    def test_with_valid_type(self, cli_input):
        assert isinstance(AppConfig(cli_input).config_parse, ArgParser)

    def test_known_config(self, cli_input, default_env):
        cls = AppConfig(cli_input)
        for i in default_env:
            assert cls.get(i) == str(default_env.get(i))

    def test_unknown_config(self, cli_input, unknown_args):
        cls = AppConfig(cli_input)
        for i in unknown_args:
            unknown_arg = unknown_args.get(i)[1]
            assert cls.get(unknown_arg) == str(cls.get(unknown_args.get(i)[1]))
