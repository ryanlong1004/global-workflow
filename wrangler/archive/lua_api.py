"""abstracts interface to Lua scripts"""
import glob
import json
from pathlib import Path
import re

import collections

PATTERNS = {
    "load_module": re.compile(r"[\"\']\S*[\"\']"),
    "prepend_path": re.compile(r"^prepend_path\(.*\"(\/.*)\".*$"),
    "whatis": re.compile(r"^whatis\(\"(.*)\"\)$"),
    "setenv": re.compile(r"^setenv\(\"(.*)\",\"(.*)\"\)$"),
}

COMMAND_TYPES = ["help", "whatis", "load", "setenv"]


def write_load_module(module_name, module_version):
    return f"load(pathjoin({module_name}, {module_version}))"


def write_prepend_path(module_path, path):
    return f"prepend_path('{module_path}', '{path}')"


def write_whatis(description):
    return f"whatis('{description}')"


def read_load_module(value):
    """extracts the module and version from a 'load' command

    The value.replace is to normalize the use of spaces and
    commas.
    """
    result = PATTERNS["load_module"].findall(value.replace(",", ", "))
    assert result is not None
    try:
        return (result[0][1:-1], result[1][1:-1])
    except IndexError:
        return (result[0][1:-1], None)


def read_prepend_path(value):
    """extracts path from prepend_path command"""
    result = PATTERNS["prepend_path"].match(value)
    assert result is not None
    return result.group(1)


def read_whatis(value):
    """extracts 'whatis' value from command"""
    result = PATTERNS["whatis"].match(value)
    assert result is not None
    return result.group(1)


def read_setenv(value):
    """extracts env name and value from setenv command"""
    result = PATTERNS["setenv"].match(value)
    assert result is not None
    return (result.group(1), result.group(2))


def get_command_type(value):
    """returns value if known command type, otherwise false"""
    test = value.split("(", 1)[0]
    if test in COMMAND_TYPES:
        return test
    return False


def unique_module_permutations(data):
    """returns all unique modules name/version combinations from each load command"""
    return set([read_load_module(x) for x in data if get_command_type(x) == "load"])


def unique_module_names(data):
    """returns all unique module names from each load command"""
    return set([read_load_module(x)[0] for x in data if get_command_type(x) == "load"])


def unique_job_names(data):
    return set([read_load_module(x)[0] for x in data if get_command_type(x) == "load"])


def modules_and_versions_dict(data):
    module_names = unique_module_names(data)
    versions = unique_module_permutations(data)
    output = {}
    for x in module_names:
        output[x] = []
        for y in versions:
            if x == y[0]:
                output[x].append(y[1])
    return json.dumps(
        collections.OrderedDict(sorted([item for item in output.items()]))
    )


def module_files_list(pattern):
    return [Path(x) for x in glob.glob(pattern)]


if __name__ == "__main__":
    lines = []
    for x in module_files_list("/home/rlong/apps/global-workflow/modulefiles/*lua"):
        with open(x, "r") as _file:
            for y in _file:
                lines.append(y.strip().replace("\n", ""))
    print(modules_and_versions_dict(lines))
