"""Read the single-source Lua catalog without running Factorio."""
from pathlib import Path
from lupa.lua52 import LuaRuntime
ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "second-nature"

def plain(value):
    if hasattr(value, "items"):
        pairs = list(value.items())
        if pairs and all(isinstance(k, (int, float)) for k, _ in pairs):
            return [plain(value[i]) for i in range(1, len(value) + 1)]
        return {k: plain(v) for k, v in pairs}
    return value

def load_catalog():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().package.path = str(MOD / "?.lua") + ";" + lua.globals().package.path
    return plain(lua.eval('require("shared.catalog")'))

def load_constants():
    return load_module("shared.constants")

def load_module(name):
    """Read any pure-data shared Lua module (no game globals) as plain Python."""
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().package.path = str(MOD / "?.lua") + ";" + lua.globals().package.path
    return plain(lua.eval(f'require("{name}")'))

if __name__ == "__main__":
    import json
    print(json.dumps(load_catalog(), indent=2, ensure_ascii=False))
