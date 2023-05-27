import lua_api as api


def test_read_load_module():
    expected = {"module": "hpc", "version": "1.1.0"}
    actual = api.read_load_module('load(pathJoin("hpc", "1.1.0"))')
    assert expected == actual

    expected = {"module": "rocoto", "version": None}
    actual = api.read_load_module('load(pathJoin("rocoto"))')
    assert expected == actual

    expected = {"module": "hpss", "version": None}
    actual = api.read_load_module('load("hpss")')
    assert expected == actual


def test_read_prepend_path():
    expected = {
        "module_path": "/scratch2/NCEPDEV/nwprod/hpc-stack/libs/hpc-stack/modulefiles/stack"
    }
    actual = api.read_prepend_path(
        'prepend_path("MODULEPATH", "/scratch2/NCEPDEV/nwprod/hpc-stack/libs/hpc-stack/modulefiles/stack")'
    )
    assert expected == actual


def test_read_whatis():
    expected = {"whatis": "Description: GFS run environment"}
    actual = api.read_whatis('whatis("Description: GFS run environment")')
    assert expected == actual


def test_read_setenv():
    expected = {"name": "WGRIB2", "value": "wgrib2"}
    actual = api.read_setenv('setenv("WGRIB2","wgrib2")')
    assert expected == actual
