"""
Abstracts the configuration and environment from ECF
"""

import logging
from collections.abc import Mapping
import os
import pathlib
from typing import Any, Dict, List, Union
import os
import yaml

import stubs


log = logging.getLogger(__name__)

KEYWORDS = ["tasks", "edits", "nodes", "triggers", "events"]
DEFAULT_ENCODING = "utf-8"
ENV_TOKEN = "env."

NODE_TYPES = {"suite": stubs.Suite, "family": stubs.Family, "task": stubs.Task}


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
        log.warning("environment variable not found: [%s]", value.split(".", 1)[1])
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

    def __init__(self, name: str, data: Any, parent: Union["Node", None]):
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
                self._ecf_instance = NODE_TYPES[self.type.lower()](self.name)
            except KeyError:
                return None
        return self._ecf_instance

    def __str__(self):
        return f"<{self.type.capitalize()} {[self.name]} {['None' if self.parent is None else self.parent.name]}/>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.children)

    @property
    def children(self):
        """returns children"""
        try:
            return [Node(k, v, self) for (k, v) in self._data.items()]
        except AttributeError:
            return []

    def __fetch(self, key):
        print(key)
        return (
            {}
            if key not in self._data
            else {x: self._data[key][x] for x in self._data[key]}
        )

    @property
    def nodes(self):
        """returns nodes"""
        return [Node(x, self._data["nodes"][x], self) for x in self._data["nodes"]]

    @property
    def edits(self):
        """returns edits"""
        return (
            {}
            if "edits" not in self._data
            else {x: self._data["edits"][x] for x in self._data["edits"]}
        )

    def add_edits(self, node=None):
        for k, v in self.edits.items():
            self.ecf_instance.add(stubs.Edit(**self.edits))

    @property
    def triggers(self):
        """returns triggers"""
        try:
            return (
                []
                if "triggers" not in self._data
                else [dict(x) for x in self._data["triggers"]]
            )
        except TypeError:
            return []

    def add_triggers(self):
        """adds triggers to the node"""
        self.ecf_instance.add(stubs.Trigger(*self.triggers))

    @property
    def tasks(self):
        """returns tasks"""
        return (
            {}
            if "tasks" not in self._data
            else {x: self._data["tasks"][x] for x in self._data["tasks"]}
        )

    def add_tasks(self):
        """TODO"""

    @property
    def events(self):
        """returns tasks"""
        return (
            {}
            if "events" not in self._data
            else {x: self._data["events"][x] for x in self._data["events"]}
        )

    def add_events(self):
        """TODO"""

    @property
    def template(self):
        """returns tasks"""
        return None if "template" not in self._data else self._data["template"]

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
    SKIP = ["suite", "node", "nodes"]

    root = pathlib.Path(".")
    config = Config.from_yaml(pathlib.Path("../ecflow_build.yml"))
    config = config + {}
    defs = stubs.Defs()
    for suite in config.suites:
        defs.add_suite(suite.ecf_instance)
        for (k, v) in suite.edits.items():
            pass
            # suite.ecf_instance.edit(k, v) #TODO?
        for node in suite.nodes:
            if node.type == "family":
                print(node.edits)
            print(node)
            print("****************")
            print(node.traverse_down())
            print("\n")

        # defs.add_suite(suite.ecf_instance)
        # for x in suite.children:
        #     print(x)

        #     print(node)
        #     if node.parent is None or node.type in SKIP:
        #         continue
        #     if node.type == 'family':
        #         print("Adding family")
        #         print(node.type)
        #         print(node.parent)
        #         node.parent.ecf_instance.add_family(node, node.name)
        #     if node.type == 'edits':
        #         print("**********")
        #         for edit in node.edits:
        #             print(edit)
        #             # node.parent.ecf_instance.edit()
        #         print("**********")

        #     #     print("Adding family to suite")
        #     # if node.type == 'tasks':
        #         print(node)
        #     # print(node.ecf_instance)
        #     # print(pathlib.Path(root / node.local_path)) #1
        # exit()


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
