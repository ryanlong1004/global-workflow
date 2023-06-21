"""Convert yaml config files to LUA scripts"""
import json
import os
from collections import UserDict
from typing import Any

import yaml


class Module:
    """represents a load module"""

    def __init__(self, value: str):
        self.module, self.version_var = value.split("/", 1)
        self.version = os.environ.get(self.version_var)

    def __str__(self):
        return f'load(pathJoin("{self.module}", "{self.version}"))'


class EnvVariable:
    """represents an environment variable"""

    def __init__(self, key, value):
        self.key, self.value = key, value

    def __str__(self) -> str:
        return f'setenv("{self.key}", "{self.value}")'


class Config(UserDict):
    """represents a yaml config file"""

    def __str__(self) -> str:
        return json.dumps(self.data, indent=4)

    @property
    def common(self) -> "Script":
        """returns common script"""
        return [Script({x: y}) for (x, y) in self.data.items() if x == "common"][0]

    @property
    def scripts(self) -> list["Script"]:
        """returns scripts"""
        return [Script({x: y}) for (x, y) in self.data.items() if x != "common"]


class Script(UserDict):
    """represents a lua script as a python dict"""

    def __init__(self, val=None):
        if val is None:
            val = {}
        super().__init__(val)
        self.changed = False

    def __str__(self) -> str:
        return json.dumps(self.data, indent=4)

    @property
    def name(self) -> str:
        """returns the script name"""
        return list(self.data.keys())[0]

    @property
    def content(self) -> dict[str, Any]:
        """returns the script content as dict"""
        return self.data.get(self.name)

    @property
    def modules(self):
        """returns modules"""
        modules = self.content.get("modules")
        if modules is None:
            return []
        return [Module(x) for x in modules]

    @property
    def module_paths(self):
        """returns module path"""
        module_paths = self.content.get("modulepaths")
        if module_paths is None:
            return ""
        return [f'prepend_path("MODULEPATH". pathJoin("{x}"))' for x in module_paths]

    @property
    def env_variables(self) -> list[EnvVariable]:
        """returns environment variables"""
        environment = self.content.get("environment")
        if environment is None:
            return []
        _result = []
        for item in environment:
            for key, value in item.items():
                _result.append(EnvVariable(key, value))
        return _result

    @property
    def help(self):
        """returns help"""
        _help = self.content.get("help")
        if _help is None:
            return ""
        return f"help([[{_help}]])"

    @property
    def what_is(self):
        """returns what is"""
        what_is = self.content.get("whatis")
        if what_is is None:
            return ""
        return f'whatis("{what_is}")'


def to_Lua(scripts: list[Script], path):
    with open(path, "w") as _output:
        for script in scripts:
            _output.write(f"{script.help}\n")
            for module_path in script.module_paths:
                _output.write(f"{module_path}\n")
            for module in script.modules:
                _output.write(f"{module}\n")
            for env in script.env_variables:
                _output.write(f"{env}\n")
            _output.write(f"{script.what_is}\n")


if __name__ == "__main__":
    with open("./test.yaml", "r") as _file:
        result = yaml.safe_load(_file)
        config = Config(result)
        for x in config.scripts:
            to_Lua([config.common, x], f"./{x.name}.lua")
