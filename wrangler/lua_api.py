import re

PATTERNS = {
    "load_module": re.compile(r"^load\(pathJoin\(\"(.*)\",\s\"(.*)\"\)\)$"),
    "prepend_path": re.compile(r"^prepend_path\(.*\"(\/.*)\".*$"),
    "what_is": re.compile(r"^whatis\(\"(.*)\"\)$"),
    "setenv": re.compile(r"^setenv\(\"(.*)\",\"(.*)\"\)$"),
}


def write_load_module(module_name, module_version):
    return f"load(pathjoin({module_name}, {module_version}))"


def write_prepend_path(module_path, path):
    return f"prepend_path('{module_path}', '{path}')"


def write_what_is(description):
    return f"whatis('{description}')"


def read_load_module(value):
    result = PATTERNS["load_module"].match(value)
    assert result is not None
    return {"module": result.group(1), "version": result.group(2)}


def read_prepend_path(value):
    result = PATTERNS["prepend_path"].match(value)
    assert result is not None
    return {"module_path": result.group(1)}


def read_what_is(value):
    result = PATTERNS["what_is"].match(value)
    assert result is not None
    return {"what_is": result.group(1)}


def read_setenv(value):
    result = PATTERNS["setenv"].match(value)
    assert result is not None
    return {"name": result.group(1), "value": result.group(2)}
