"""main execution"""

import logging
from pathlib import Path

import yaml

from script import Script, find_script, to_lua


def load_scripts_from_yamls(_paths: list[Path]) -> list[Script]:
    """instantiates Script instances from yaml files"""
    results = []
    for _path in _paths:
        logging.info("extracting scripts from %s", _path)
        with open(_path, "r", encoding="utf-8") as _file:
            results.extend(
                [Script(name, data) for (name, data) in yaml.safe_load(_file).items()]
            )
    return results


def write_scripts_to_lua(
    output_path: Path, scripts: list[Script], prepend_script_name=None
) -> None:
    """outputs lua scripts from Script instances to output_path"""
    prepend_script = (
        to_lua(find_script(prepend_script_name, scripts))
        if prepend_script_name is not None
        else None
    )
    for script in (x for x in scripts if x.name != prepend_script_name):
        with open(
            Path(output_path / f"{script.name}.lua"), "w", encoding="utf-8"
        ) as _output:
            if prepend_script:
                _output.writelines(prepend_script)
            _output.writelines(to_lua(script))


def main():
    """main execution"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="wrangler.log",
    )

    _input = [Path("./test.yaml"), Path("test copy.yaml")]

    scripts = load_scripts_from_yamls(_input)
    write_scripts_to_lua(Path("./"), scripts, "common")


if __name__ == "__main__":
    main()
