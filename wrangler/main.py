import re

PATTERNS = {
    "load_module": re.compile(r"^load\(pathJoin\(\"(.*)\",\s\"(.*)\"\)\)$"),
    "prepend_path": re.compile(r"^prepend_path\(.*\"(\/.*)\".*$"),
    "what_is": re.compile(r"^whatis\(\"(.*)\"\)$"),
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


if __name__ == "__main__":
    print(read_load_module('load(pathJoin("hpc", "1.1.0"))'))
    print(
        read_prepend_path(
            'prepend_path("MODULEPATH", "/scratch2/NCEPDEV/nwprod/hpc-stack/libs/hpc-stack/modulefiles/stack")'
        )
    )
    print(
        read_prepend_path(
            'prepend_path("MODULEPATH", pathJoin("/scratch1/NCEPDEV/global/glopara/git/Fit2Obs/v1.0.0/modulefiles"))'
        )
    )
    print(read_what_is('whatis("Description: GFS run environment")'))
