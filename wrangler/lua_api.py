import re

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
    result = PATTERNS["load_module"].findall(value)
    assert result is not None
    try:
        return {"module": result[0][1:-1], "version": result[1][1:-1]}
    except IndexError:
        return {"module": result[0][1:-1], "version": None }


def read_prepend_path(value):
    result = PATTERNS["prepend_path"].match(value)
    assert result is not None
    return {"module_path": result.group(1)}


def read_whatis(value):
    result = PATTERNS["whatis"].match(value)
    assert result is not None
    return {"whatis": result.group(1)}


def read_setenv(value):
    result = PATTERNS["setenv"].match(value)
    assert result is not None
    return {"name": result.group(1), "value": result.group(2)}


def get_command_type(value):
    test = value.split("(", 1)[0]
    if test in COMMAND_TYPES:
        return test
    return False


def get_all_modules_versions(data):
    for x in data:
        if get_command_type(x) == "load":
            print(read_load_module(x))
    # return [read_load_module(x) for x in data if get_command_type(x) == "load"]
