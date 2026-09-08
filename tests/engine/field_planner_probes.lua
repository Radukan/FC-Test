-- Real engine mining/upgrades, including inventory contents, quality, custom
-- inserter vectors and both ends of an underground pair. No fake job execution.
local D=require('scripts.field_drones')
local S=require('scripts.state')
local C=require('shared.field_drones')
local P={}
local function operator(c)
  return {index=1101,valid=true,connected=true,controller_type=defines.controllers.character,
    character=c,force=c.force,print=function() end,set_shortcut_toggled=function() end}
end
function P.init(surface,force)
  -- Isolate deterministic API probes from Nauvis wildlife/terrain succession.
  surface=game.create_surface('sn-isolated-field-planners',{width=512,height=512,seed=8123,
    default_enable_all_autoplace_controls=false,
    autoplace_settings={entity={treat_missing_as_default=false,settings={}},decorative={treat_missing_as_default=false,settings={}}}})
  surface.peaceful_mode=true
  surface.request_to_generate_chunks({220,170},2);surface.force_generate_chunk_requests()
  for _,e in ipairs(surface.find_entities_filtered({area={{216,166},{236,186}},type={'tree','simple-entity','cliff'}})) do e.destroy() end
  local tiles={};for x=216,235 do for y=166,185 do tiles[#tiles+1]={name='dirt-1',position={x,y}} end end
  surface.set_tiles(tiles,true)
  local function entity(name,pos,extra)
    local spec=extra or {};spec.name=name;spec.position=pos;spec.force=force
    return assert(surface.create_entity(spec),name)
  end
  local character=entity('character',{220,170});local inv=character.get_main_inventory()
  for name,count in pairs({[C.item]=12,[C.controller]=1,['fast-transport-belt']=1,['fast-underground-belt']=2}) do assert(inv.insert({name=name,count=count})==count) end
  assert(inv.insert({name='fast-inserter',quality='rare',count=1})==1)
  local chest=entity('iron-chest',{224.5,172.5})
  assert(chest.insert({name='iron-plate',count=17})==17)
  assert(chest.insert({name='electronic-circuit',quality='rare',count=5})==5)
  assert(chest.order_deconstruction(force))
  local belt=entity('transport-belt',{226.5,171.5},{direction=defines.direction.east})
  assert(belt.order_upgrade({force=force,target={name='fast-transport-belt',quality='normal'}}))
  local arm=entity('inserter',{225.5,175.5})
  arm.pickup_position={223.5,173.5};arm.drop_position={227.5,177.5}
  assert(arm.order_upgrade({force=force,target={name='fast-inserter',quality='rare'}}))
  local a=entity('underground-belt',{224.5,179.5},{direction=defines.direction.east,type='input'})
  local b=entity('underground-belt',{228.5,179.5},{direction=defines.direction.east,type='output'})
  assert(a.neighbours==b,'underground test pair did not connect')
  assert(a.order_upgrade({force=force,target={name='fast-underground-belt',quality='normal'}}))
  if not b.to_be_upgraded() then assert(b.order_upgrade({force=force,target={name='fast-underground-belt',quality='normal'}})) end
  local op=operator(character);assert(D.set_enabled(op,true));S.root().field_drones.owners[1101].cell=10
  storage.field_planner_probe={character=character,surface=surface,chest=chest,belt=belt,arm=arm,a=a,b=b,start=game.tick}
  D.step_player(op)
  assert(S.root().field_drones.owners[1101].active>=3,'planner targets did not dispatch')
end
function P.tick()
  local p=storage.field_planner_probe
  if not p or p.finished then return end
  local op=operator(p.character);D.step_player(op)
  if game.tick-p.start<1800 then return end
  local inv=p.character.get_main_inventory()
  assert(not p.chest.valid,'deconstruction did not remove the chest')
  assert(inv.get_item_count('iron-chest')==1 and inv.get_item_count('iron-plate')==17,'deconstruction lost chest or contents')
  assert(inv.get_item_count({name='electronic-circuit',quality='rare'})==5,'deconstruction lost item quality')
  local function at(name,pos) return assert(p.surface.find_entities_filtered({name=name,position=pos})[1],name) end
  local belt=at('fast-transport-belt',{226.5,171.5});assert(belt.direction==defines.direction.east)
  local arm=at('fast-inserter',{225.5,175.5})
  assert(arm.quality.name=='rare' and arm.pickup_position.x==223.5 and arm.drop_position.x==227.5,'upgrade lost quality or custom vectors')
  local a=at('fast-underground-belt',{224.5,179.5});local b=at('fast-underground-belt',{228.5,179.5})
  assert(a.neighbours==b,'upgraded underground pair is disconnected')
  for _,name in ipairs({'fast-transport-belt','fast-underground-belt'}) do assert(inv.get_item_count(name)==0,'new upgrade material was not consumed: '..name) end
  assert(inv.get_item_count({name='fast-inserter',quality='rare'})==0)
  assert(inv.get_item_count('transport-belt')==1 and inv.get_item_count('inserter')==1 and inv.get_item_count('underground-belt')==2,'old upgrade items not returned exactly once')
  assert(inv.get_item_count(C.item)==12,'planner work lost or duplicated reusable drones')
  assert(S.root().field_drones.owners[1101].active==0,'planner workers did not return')
  D.set_enabled(op,false);p.finished=true
  log('SECOND_NATURE_ENGINE_FIELD_PLANNERS_OK')
end
return P
