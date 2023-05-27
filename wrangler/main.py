import glob
from pathlib import Path
from lua_api import get_all_modules_versions


def module_files_list(pattern):
    return [Path(x) for x in glob.glob(pattern)]


def main():
    """main execution"""
    lines = []
    for x in module_files_list("/home/rlong/apps/global-workflow/modulefiles/*lua"):
        with open(x, "r") as _file:
            for y in _file:
                lines.append(y.strip().replace("\n", ""))
    print(get_all_modules_versions(lines))


if __name__ == "__main__":
    main()
