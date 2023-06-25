"""main execution"""

import logging
from pathlib import Path

import yaml

from script import Script, get_common, to_lua


def load_scripts_from_yamls(_paths: list[Path]) -> list[Script]:
    results = []
    for _path in _paths:
        logging.info('extracting scripts from %s', _path)
        with open(_path, "r", encoding="utf-8") as _file:
            results.extend([Script(name, data) for (name, data) in yaml.safe_load(_file).items()])
    return results

def write_scripts_to_lua(output_path: Path, scripts: list[Script]) -> None:
    for script in scripts:
        with open(Path(output_path / f"{script.name}.lua"), "w", encoding="utf-8") as _output:
            _output.writelines(to_lua(get_common(scripts)))
            _output.writelines(to_lua(script))

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="wrangler.log",
    )

    _input = "./test.yaml"
    
    scripts = load_scripts_from_yamls([Path(_input)])
    write_scripts_to_lua(Path("./"), scripts)

if __name__ == "__main__":
    main()
