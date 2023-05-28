"""Main execution"""
import glob
from pathlib import Path
from lua_api import unique_module_names, unique_module_permutations
from file_operations import write_to_csv
import csv
import logging


def module_files_list(pattern):
    return [Path(x) for x in glob.glob(pattern)]


def find_errors():
    pass


def main():
    """main execution"""

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="wrangler.log",
    )

    lines = []
    for x in module_files_list("/home/rlong/apps/global-workflow/modulefiles/*lua"):
        with open(x, "r") as _file:
            for y in _file:
                lines.append(y.strip().replace("\n", ""))


if __name__ == "__main__":
    main()
