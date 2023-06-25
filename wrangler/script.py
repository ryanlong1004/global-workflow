"""Convert yaml config files to LUA scripts"""
import json
import os
from typing import Any
from pathlib import Path
import yaml


def ensure_list(value):
    """ensures a value is a list or coerces to list of len 1"""
    return value if isinstance(value, list) else [value]


def environment(values: list[dict[str, Any]]) -> list[str]:
    """returns list of EnvVariables"""
    results = []
    for value in ensure_list(values):
        for key, value in value.items():
            results.append(f'setenv("{key}", "{value}")\n')
    return results


def modules(values: list[str]) -> list[str]:
    """returns list of Modules"""
    results = []
    for value in ensure_list(values):
        key, _value = value.split("/")
        results.append(f'load(pathJoin("{key}", "{os.environ.get(_value)}"))\n')
    return results


def module_paths(values) -> list[str]:
    """returns list of PosixPaths"""
    return [f'prepend_path("MODULEPATH", pathJoin("{_path}"))\n' for _path in values]


def what_is(values) -> list[str]:
    """returns list of WhatIs"""
    return [f'whatis("{value}")\n' for value in ensure_list(values)]


def _help(values) -> list[str]:
    """returns list of Help"""
    return [f"help([[{value}]])\n" for value in ensure_list(values)]


def extra(values) -> list[str]:
    """returns list of Script dicts"""
    results = []
    for value in ensure_list(values):
        for key, _values in value.items():
            results.append(*mapper_props[key](_values))
    return results


mapper_props = {
    "modules": modules,
    "modulepaths": module_paths,
    "environment": environment,
    "whatis": what_is,
    "help": _help,
    "extra": extra,
}


class Script:
    """represents a dynamic lua script from yaml file"""

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return json.dumps(self.data, indent=4)

    def __iter__(self):
        return (x for x in self.data.items())

    def __getattr__(self, name):
        print(name)
        if name in self.data:
            return mapper_props[name](
                [self.data[name]]
                if isinstance(self.data[name], str)
                else self.data[name]
            )
        return None

    def __getitem__(self, key):
        return self.data.get(key, None)

    def get(self, key, default=None) -> Any:
        """attempts to get value from instance or returns default"""
        if key in self.data:
            return self.data[key]
        return default


def to_lua(_script: Script) -> list[str]:
    """converts a Script instance to a lua script"""
    order = ["help", "modulepaths", "environment", "modules", "whatis", "extra"]
    results = []
    for key in order:
        for _line in mapper_props[key](_script.get(key, [])):
            results.append(_line)
    return results


def get_common(scripts: list[Script]) -> Script:
    """returns common script if it exists"""
    return list(filter(lambda x: x.name == "common", scripts))[0]
