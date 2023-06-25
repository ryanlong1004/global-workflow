import archive.lua_api as api


def test_read_load_module():
    expected = ("hpc", "1.1.0")
    actual = api.read_load_module('load(pathJoin("hpc", "1.1.0"))')
    assert expected == actual

    expected = ("rocoto", None)
    actual = api.read_load_module('load(pathJoin("rocoto"))')
    assert expected == actual

    expected = ("hpss", None)
    actual = api.read_load_module('load("hpss")')
    assert expected == actual


def test_read_prepend_path():
    expected = "/scratch2/NCEPDEV/nwprod/hpc-stack/libs/hpc-stack/modulefiles/stack"

    actual = api.read_prepend_path(
        'prepend_path("MODULEPATH", "/scratch2/NCEPDEV/nwprod/hpc-stack/libs/hpc-stack/modulefiles/stack")'
    )
    assert expected == actual


def test_read_whatis():
    expected = "Description: GFS run environment"
    actual = api.read_whatis('whatis("Description: GFS run environment")')
    assert expected == actual


def test_read_setenv():
    expected = ("WGRIB2", "wgrib2")
    actual = api.read_setenv('setenv("WGRIB2","wgrib2")')
    assert expected == actual
