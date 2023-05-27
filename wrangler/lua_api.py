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
    result = PATTERNS["prepend_path"].match(value)
    assert result is not None
    return result.group(1)


def read_whatis(value):
    result = PATTERNS["whatis"].match(value)
    assert result is not None
    return result.group(1)


def read_setenv(value):
    result = PATTERNS["setenv"].match(value)
    assert result is not None
    return (result.group(1), result.group(2))


def get_command_type(value):
    test = value.split("(", 1)[0]
    if test in COMMAND_TYPES:
        return test
    return False


def get_all_modules_versions(data):
    return [read_load_module(x) for x in data if get_command_type(x) == "load"]
