
from typing import Any
from ecflow_definitions_v2 import Suite
import collections
from functools import lru_cache
import os
import pathlib
import yaml


ENV_TOKEN = "env."

class Config(collections.UserDict):
    """represents a yaml configuartion"""
    
    def __getattribute__(self, item: str):
        return self[item]

    def __getitem__(self, key: str):
        return get_environment_value(self[key])

    def __add__(self, other_config):
        return Config({**self, **other_config})
    
    @staticmethod
    def from_yaml(file_path: pathlib.Path) -> "Config":
        """instantiate Config with yaml file"""
        with open(file_path, "r", encoding="utf-8") as _file:
            return Config(yaml.safe_load(_file))

    
@lru_cache
def get_environment_value(key, token=ENV_TOKEN) -> Any:
    """returns env value if it exists"""
    if token not in key:
        return key
    return os.environ[key.split(".", 1)[1]]
    


    


if __name__ == "__main__":
    root = Suite("root", None)
    config = Config.from_yaml(pathlib.Path("../prod.yml"))
    config = config + {}
    for suite in config.suites:
        s = Suite(suite, root)
        for edit in config["suites"][suite]["edits"]:
            s.add_edit(f"{edit} {config['suites'][suite]['edits'][edit]}")
        print(s.edits)
