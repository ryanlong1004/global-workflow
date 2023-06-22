"""Convert yaml config files to LUA scripts"""
import json
import os
from collections import UserDict, namedtuple
from typing import Any
from pathlib import Path

import yaml


def environment(values) -> list[tuple]:
    """returns list of EnvVariables"""
    _EnvVariable = namedtuple("EnvVariable", ["key", "value"])
    return [_EnvVariable(list(x.keys())[0], list(x.values())[0]) for x in values]


def modules(values) -> list[tuple]:
    """returns list of Modules"""
    _Module = namedtuple("Module", ["name", "version"])
    return [
        _Module(x[0], os.environ.get(x[1])) for x in [x.split("/", 1) for x in values]
    ]


def module_paths(values) -> list[Path]:
    """returns list of PosixPaths"""
    return [Path(x) for x in values]


def what_is(values) -> list[tuple]:
    """returns list of WhatIs"""
    WhatIs = namedtuple("WhatIs", ["value"])
    return [WhatIs(x) for x in values]


def _help(values) -> list[tuple]:
    """returns list of Help"""
    Help = namedtuple("Help", ["value"])
    return [Help(x) for x in values]


def extra(values) -> list["Script"]:
    """returns list of Script dicts"""
    return [Script(x, y) for (x, y) in values.items()]


mapper_props = {
    "modules": modules,
    "modulepaths": module_paths,
    "environment": environment,
    "whatis": what_is,
    "help": _help,
    "extra": extra,
}

mapper_lua = {
    "Module": lambda _module, version: f'load(pathJoin("{_module}", "{version}"))',
    "PosixPath": lambda _path: f'prepend_path("MODULEPATH", pathJoin("{_path}"))',
    "EnvVariable": lambda key, value: f'setenv("{key}", "{value}")',
    "whatis": lambda value: f'whatis("{value}")',
    "help": lambda value: f"help([[{value}]])",
    "extra": extra,
}


class Script:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return json.dumps(self.data, indent=4)

    def __getattr__(self, name):
        if name in self.data:
            return mapper_props[name](
                [self.data[name]]
                if isinstance(self.data[name], str)
                else self.data[name]
            )
        return None


def to_Lua(scripts: list[Script], path):
    with open(path, "w", encoding="utf-8") as _output:
        for script in scripts:
            # print(script)
            pass
        exit()


if __name__ == "__main__":
    with open("./test.yaml", "r") as _file:
        result = yaml.safe_load(_file)
        new_result = {Script(x, y) for (x, y) in result.items()}
        for x in new_result:
            print(x.extra)
        to_Lua(new_result, "./test.txt")
