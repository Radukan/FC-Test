#!/usr/bin/env python3
"""Run Wube's actual data-stage Lua in Lua 5.2, then load Second Nature.

This is NOT the Factorio engine. It validates executable data scripts and their
resulting graph. Engine-generated enums are supplied; absent proprietary sprite
metadata is represented by placeholders. C++ prototype/graphics validation and
runtime integration still require the headless/graphical game (see headless.py).
"""
from pathlib import Path
import json, re, sys
from lupa.lua52 import LuaRuntime
from catalog import ROOT, MOD

class DataStage:
    def __init__(self, upstream: Path, overhaul=True, startup_overrides=None):
        self.upstream=Path(upstream).resolve();self.lua=LuaRuntime(unpack_returned_tuples=True)
        self.cache={};self.context='core';self.stubbed_sprites=set()
        self.version=json.loads((self.upstream/'base/info.json').read_text())['version']
        self.lua.execute('''
          function table_size(t) local n=0; for _ in pairs(t) do n=n+1 end; return n end
          log=function() end; serpent={block=function(x) return tostring(x) end, line=function(x) return tostring(x) end}
          kg=1000; tons=1000000; minute=3600; second=60; hour=216000
          feature_flags={quality=true,rail_bridges=true,space_travel=true,spoiling=true,freezing=true,segmented_units=true,expansion_shaders=true}
          settings={startup={['sn-overhaul-progression']={value=true}}}
          defines={default_icon_size=64,direction={north=0,northnortheast=1,northeast=2,eastnortheast=3,east=4,eastsoutheast=5,southeast=6,southsoutheast=7,south=8,southsouthwest=9,southwest=10,westsouthwest=11,west=12,westnorthwest=13,northwest=14,northnorthwest=15},constant={default_icon_size=64}}
          math.clamp=function(x,a,b) return math.max(a, math.min(b,x)) end
          math.round=function(x) return math.floor(x+0.5) end
        ''')
        self.lua.globals().settings.startup['sn-overhaul-progression'].value=overhaul
        for name, value in ({'sn-expedition-character':True,'sn-desolate-start':True,'sn-legacy-smog':80,'sn-biter-metabolism':True,'sn-menu-background':True} | (startup_overrides or {})).items():
            self.lua.globals().settings.startup[name] = self.lua.table_from({'value':value})
        self.lua.globals().require=self.require
        # Only enums used by upstream's data stage; no permissive missing-property metatable.
        enums=set()
        for mod in ('core','base','elevated-rails','quality','recycler','space-age'):
            for path in (self.upstream/mod).rglob('*.lua'):
                enums.update(re.findall(r'defines\.([\w]+)\.([\w]+)',path.read_text(errors='replace')))
        for index,(group,key) in enumerate(sorted(enums),1):
            if group in ('prototypes','direction','constant'):continue
            if self.lua.globals().defines[group] is None:self.lua.globals().defines[group]=self.lua.table()
            self.lua.globals().defines[group][key]=index
        hierarchy=self.upstream/'core/lualib/prototype-hierarchy.lua'
        if hierarchy.exists():
            self.lua.globals()._hierarchy=self.execute(hierarchy,'core')
            self.lua.execute('''
              defines.prototypes={}
              local function flatten(name, node, output)
                if not node._abstract then output[name]=true end
                for key, child in pairs(node) do if key~='_abstract' then flatten(key,child,output) end end
              end
              for name,node in pairs(_hierarchy) do local out={};defines.prototypes[name]=out;flatten(name,node,out) end
            ''')
        else:
            self.lua.execute('''defines.prototypes={item={}}; for _,name in ipairs({'item','tool','ammo','armor','capsule','gun','module','rail-planner','repair-tool','item-with-entity-data','item-with-inventory','item-with-label','item-with-tags','selection-tool','copy-paste-tool','blueprint','blueprint-book','deconstruction-item','upgrade-item','space-platform-starter-pack'}) do defines.prototypes.item[name]=true end''')
        mods=['core','base','elevated-rails']
        if (self.upstream/'recycler').exists():mods.append('recycler')
        mods+=['quality','space-age','second-nature'];self.mods=mods
        self.lua.globals().mods=self.lua.table_from({m: self.version if m!='second-nature' else json.loads((MOD/'info.json').read_text())['version'] for m in mods})
        self.require('dataloader')
        for stage in ('data.lua','data-updates.lua','data-final-fixes.lua'):
            if stage == 'data-updates.lua' and not hierarchy.exists():
                self.lua.execute('''
                  defines.prototypes.entity={}; defines.prototypes.equipment={}
                  for kind,collection in pairs(data.raw) do
                    for _,p in pairs(collection) do
                      if p.collision_box or p.selection_box then defines.prototypes.entity[kind]=true end
                      if kind:match('%-equipment$') then defines.prototypes.equipment[kind]=true end
                    end
                  end
                ''')
            for mod in mods:
                folder=MOD if mod=='second-nature' else self.upstream/mod
                path=folder/stage
                if path.exists():self.execute(path,mod)
        self.raw=self.lua.globals().data.raw

    def execute(self,path,context):
        previous=self.context;self.context=context
        try:return self.lua.execute(Path(path).read_text(encoding='utf-8'),name='@'+str(path))
        finally:self.context=previous

    def require(self,name):
        name=str(name)
        explicit=re.match(r'^__([^_]+(?:-[^_]+)?)__[./](.*)$',name)
        if explicit:
            context,relative=explicit.groups()
        else:context,relative=self.context,name
        relative=relative.replace('.','/') if '/' not in relative else relative
        folder=MOD if context=='second-nature' else self.upstream/context
        candidates=[folder/(relative+'.lua')]
        if not explicit:
            candidates += [self.upstream/'core/lualib'/(relative+'.lua'), folder/'lualib'/(relative+'.lua')]
        path=next((p for p in candidates if p.exists()),None)
        if path is None:
            if relative.startswith("sound/ambient/"):
                return self.lua.table_from({"type":"ambient-sound", "name":"unavailable-"+relative})
            if relative.startswith("menu-simulations/"):
                return self.lua.table()  # Promotional saved simulations are not prototype definitions.
            if '/graphics/' in '/'+relative or name.startswith('__') and '/graphics/' in name:
                self.stubbed_sprites.add(name)
                return self.lua.table_from({'width':256,'height':256,'line_length':1,'shift':self.lua.table_from([0,0])})
            raise FileNotFoundError(f'Module {name!r} from {self.context}; searched {candidates}')
        key=str(path.resolve())
        if key not in self.cache:
            result=self.execute(path,context)
            self.cache[key]=True if result is None else result
        return self.cache[key]

if __name__=='__main__':
    upstream=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'.cache/factorio-data'
    stage=DataStage(upstream)
    count=sum(len(list(table.keys())) for _,table in stage.raw.items())
    custom=sum(sum(name.startswith('sn-') for name in table.keys()) for _,table in stage.raw.items())
    print(f'Factorio {stage.version}: executed all data stages; {count} prototypes; {custom} Second Nature prototypes.')
    print(f'{len(stage.stubbed_sprites)} unavailable upstream sprite metadata files stubbed. This is not engine validation.')
