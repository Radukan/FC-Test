#!/usr/bin/env python3
"""Run the real pure-Lua ecology model with a fully supplied reference kit.
This is a balance test, not an engine or logistics playthrough.
"""
from lupa.lua52 import LuaRuntime
from catalog import MOD,plain
import json

def simulate():
    lua=LuaRuntime(unpack_returned_tuples=True);lua.globals().package.path=str(MOD/'?.lua')+';'+lua.globals().package.path
    return plain(lua.execute('''
      local C=require('shared.constants');local K=require('shared.catalog');local M=require('shared.model')
      local results={}
      for _,planet in ipairs(C.planets) do
        local s=M.new(planet);s.first_operation=1
        local names={'sn-air-scrubbing','sn-thermal-balancing','sn-watershed-restoration','sn-soil-restoration','sn-pioneer-reseeding','sn-mineral-detoxification','sn-habitat-restoration'}
        local kit={4,4,3,3,3,2,1}
        for _,machine in ipairs(K.machines) do if machine.planet==planet then names[#names+1]='sn-'..machine.fixed;kit[#kit+1]=2 end end
        local milestones={};local previous=s.stage
        for minute=1,180 do
          for i,name in ipairs(names) do local r=K.by_recipe[name]
            if not r.stage or s.stage>=r.stage then M.apply(s,r.effects,60/r.seconds*kit[i],1) end
          end
          M.advance(s,60,1)
          if s.stage>previous then for stage=previous+1,s.stage do milestones[stage]=minute end;previous=s.stage end
          if M.ready(s) then results[#results+1]={planet=planet,minutes=minute,values=s.values,toxicity=s.toxicity,milestones=milestones};break end
        end
        assert(M.ready(s),'Reference kit failed to converge on '..planet)
      end
      return results
    '''))
if __name__=='__main__':print(json.dumps(simulate(),indent=2,sort_keys=True))
