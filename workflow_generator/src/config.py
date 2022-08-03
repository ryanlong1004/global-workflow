"""
Abstracts the configuration and environment from ECF
"""

import logging
from collections.abc import Mapping
from typing import Any, Dict, List
import os
import pathlib
import yaml
import stubs

log = logging.getLogger(__name__)

KEYWORDS = ["tasks", "edits", "nodes", "triggers", "events"]
DEFAULT_ENCODING = "utf-8"
ENV_TOKEN = "env."


class Config:
    """represents a yaml configuartion"""

    def __init__(self, data: Dict[Any, Any]):
        self._data = data

    def __getattr__(self, item: str):
        return self[item]

    def __getitem__(self, key: str):
        return self._data[key]

    def __add__(self, other_config):
        return Config({**self._data, **other_config})

    @property
    def suites(self):
        """returns top level suites"""
        return [
            Node(suite, config["suites"][suite], None) for suite in config["suites"]
        ]

    @staticmethod
    def from_yaml(file_path: pathlib.Path) -> "Config":
        """instantiate Config with yaml file"""
        with open(file_path, "r", encoding=DEFAULT_ENCODING) as _file:
            return Config(yaml.safe_load(_file))


def get_environment_value(value, indicator_token=ENV_TOKEN) -> Any:
    """returns env value if it exists"""
    if value is None or indicator_token not in value:
        return value
    try:
        return os.environ[value.split(".", 1)[1]]
    except KeyError:
        pass  # TODO remove
        # log.warning("environment variable not found: [%s]", value.split(".", 1)[1])
    return value


def sub_env_values(data: Dict[Any, Any]):
    """replaces all dict values with env variables if indicated"""
    if data is None:
        return data

    if not isinstance(data, Mapping):
        return get_environment_value(data)

    for item in data.keys():
        data[item] = get_environment_value(data[item])

    return data


def get_home(env_configs) -> pathlib.Path:
    """returns ECF gfs home?"""
    return pathlib.Path(env_configs["base"]["ECFgfs"])


def get_script_repo(env_configs):
    """returns script repo path from config or default"""
    return (
        pathlib.Path(get_home(env_configs) / "scripts")
        if "scriptrepo" not in env_configs
        else env_configs["scriptrepo"]
    )


def add_externs(env_configs, DEFS):
    """TODO"""
    if "externs" in env_configs:
        for extern in env_configs["externs"]:
            DEFS.add_extern(extern)


class Node:
    """encapsulates every type of Node"""

    def __init__(self, name, data, parent):
        self.name = name
        self.parent = parent
        self._data = sub_env_values(data)
        self._type = ""
        self._ecf_instance = None

    @property
    def ecf_instance(self):
        """returns the ecf class equivalent based on type"""
        if self._ecf_instance is None:
            try:
                clz = getattr(stubs, self.type.capitalize())
                self._ecf_instance = clz(self.name)
            except AttributeError:
                pass
            except TypeError:
                pass
        return self._ecf_instance

    def __str__(self):
        return f"<{self.type.capitalize()} {[self.name]} {['None' if self.parent is None else self.parent.name]}/>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.children)

    @property
    def edits(self):
        """returns edits"""
        return [] if "edits" not in self._data else self._data["edits"]

    @property
    def nodes(self):
        """returns nodes"""
        return [] if "nodes" not in self._data else self._data["nodes"]

    @property
    def triggers(self):
        """returns triggers"""
        return [] if "nodes" not in self._data else self._data["triggers"]

    @property
    def tasks(self):
        """returns tasks"""
        return [] if "nodes" not in self._data else self._data["tasks"]

    @property
    def children(self):
        """returns children"""
        try:
            return [Node(k, v, self) for (k, v) in self._data.items()]
        except AttributeError:
            return []

    @property
    def type(self) -> str:
        """returns the type of Node"""
        if self._type == "":
            self._type = "family"
            if self.parent is None:
                self._type = "suite"
            if self.name.lower() in KEYWORDS:
                self._type = self.name
            if len(self.children) < 1:
                self._type = "node"
        return self._type

    @property
    def local_path(self) -> str:
        """returns a / delimited string of paths based off of node names"""

        return "/".join(
            reversed(
                [
                    x.name
                    for x in self.traverse_up()
                    if x.type.lower() not in KEYWORDS and x.type.lower() not in ["node"]
                ]
            )
        )

    def traverse_up(self, accum=None) -> List["Node"]:
        """returns recursive list of parent nodes"""
        accum = [] if accum is None else accum
        accum.append(self)
        if self.parent is not None:
            self.parent.traverse_up(accum)
        return accum

    def traverse_down(self, accum=None) -> List["Node"]:
        """returns recursive list of child nodes"""
        accum = [] if accum is None else accum
        accum.append(self)
        for child in self.children:
            child.traverse_down(accum)
        return accum

    @property
    def root(self):
        """returns the root node regardless of caller"""
        return self.traverse_up()[-1]


if __name__ == "__main__":
    root = pathlib.Path(".")
    config = Config.from_yaml(pathlib.Path("../ecflow_build.yml"))
    config = config + {}
    for suite in config.suites:
        for node in suite.traverse_down():
            print(node)
            # print(node.ecf_instance)
            # print(pathlib.Path(root / node.local_path)) #1
            print(type(node.ecf_instance))
    #         print(node._data)
    # print("*" * 8)

    # if "nodes" in config["suites"][suite]:
    #     for node in config["suites"][suite]["nodes"]:
    #         print(node)
    # print(node)
    # s.add_edit(f"{edit} {config['suites'][suite]['edits'][edit]}")
    # print(root.traverse_down())
    # for x in root:
    #     print(x.edits)


"""
#1 https://stackoverflow.com/questions/48190959/how-do-i-append-a-string-to-a-path-in-python

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
