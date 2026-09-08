from pathlib import Path
import sys
import pytest
from lupa.lua52 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from catalog import MOD

@pytest.fixture
def lua():
    runtime=LuaRuntime(unpack_returned_tuples=True)
    runtime.globals().package.path=str(MOD/'?.lua')+';'+runtime.globals().package.path
    return runtime

@pytest.fixture
def game_lua(lua):
    lua.execute((ROOT/'tests/runtime_fixture.lua').read_text(),name='@runtime_fixture.lua')
    lua.globals().mock.gui_reserved=lua.execute((ROOT/'tests/gui_reserved.lua').read_text())
    lua.execute((MOD/'control.lua').read_text(),name='@control.lua')
    lua.execute('mock.init()')
    return lua
