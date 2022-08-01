
from typing import Any, Dict
from functools import lru_cache
import os
import pathlib
import yaml

KEYWORDS = ['tasks', 'edits', 'nodes','triggers', 'events']

ENV_TOKEN = "env."

class Config:
    """represents a yaml configuartion"""
    
    def __init__(self, data: Dict[Any, Any]):
        self._data = data
    
    def __getattr__(self, item: str):
        return self[item]

    def __getitem__(self, key: str):
        return self._data[key]
        # return get_environment_value(self._data[key])

    def __add__(self, other_config):
        return Config({**self._data, **other_config})
    
    @staticmethod
    def from_yaml(file_path: pathlib.Path) -> "Config":
        """instantiate Config with yaml file"""
        with open(file_path, "r", encoding="utf-8") as _file:
            return Config(yaml.safe_load(_file))

    
@lru_cache()
def get_environment_value(key, token=ENV_TOKEN) -> Any:
    """returns env value if it exists"""
    if token not in key:
        return key
    return os.environ[key.split(".", 1)[1]]
    

def add_externs(ecfconf, DEFS):
    if 'externs' in ecfconf.keys():
            for extern in ecfconf['externs']:
                DEFS.add_extern(extern)

class Node:

    def __init__(self, name, data, type = None):
        self.name = name
        self._data = data
        self._type = type

    def __str__(self):
        return f"<{self.type.capitalize()} {[self.name]}/>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.children)

    @property 
    def edits(self):
        """returns node edits"""
        return [] if 'edits' not in self._data else self._data['edits']
    
    @property 
    def nodes(self):
        """returns node edits"""
        return [] if 'nodes' not in self._data else self._data['nodes']
        
    @property
    def children(self):
        """returns children"""
        try:
            return [Node(k,v) for (k, v) in self._data.items()]
        except AttributeError:
            return []

    @property
    def type(self):
        if self._type is None:
            self._type = "family"
            if self.name.lower() in KEYWORDS:
                self._type = self.name
            if len(self.children) < 1:
                self._type = "node"
        return self._type


def get_suites(config: Config):
    return [Node(suite, config['suites'][suite], 'suite') for suite in config['suites']]

if __name__ == "__main__":
    config = Config.from_yaml(pathlib.Path("../prod.yml"))
    config = config + {}
    for suite in get_suites(config):
        print(suite)
        print(suite._type)
        for node in suite.children:
            print(node)
            print(node._type)
            for _node in node:
                print(_node)
                print(_node.type)
        # if "nodes" in config["suites"][suite]:
        #     for node in config["suites"][suite]["nodes"]:
        #         print(node)
                # print(node)
                # s.add_edit(f"{edit} {config['suites'][suite]['edits'][edit]}")
    # print(root.traverse_down())
    # for x in root:
    #     print(x.edits)
        



"""
self.args = args
self.env_configs = env_configs
self.suite_array = {}
self.DEFS = Defs()

# Load in the ecflow configurations
base_ecflowconfig = load_ecflow_config(f'{args.ecflow_config}')
self.ecfconf = update_ecflow_config(base_ecflowconfig, env_configs)

self.ecfhome = env_configs['base']['ECFgfs']

if 'scriptrepo' in self.ecfconf.keys():
    self.env_configs['base']['scriptrepo'] = self.ecfconf['scriptrepo']
elif 'scriptrepo' not in self.env_configs['base'].keys():
    self.env_configs['base']['scriptrepo'] = f"{self.ecfhome}/scripts"
self.scriptrepo = self.env_configs['base']['scriptrepo']
"""