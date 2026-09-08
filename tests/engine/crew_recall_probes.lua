-- Real in-flight recall: toggle must not instantly delete/refund a distant bot.
local D=require('scripts.field_drones')
local S=require('scripts.state')
local X={}
local function player(c)
  return {index=1301,valid=true,connected=true,controller_type=defines.controllers.character,
    character=c,force=c.force,print=function() end}
end
function X.init(surface,force)
  local startup=game.create_force('sn-startup-sticks-probe')
  assert(startup.recipes['iron-stick'].enabled and startup.recipes['small-electric-pole'].enabled)
  assert(not startup.technologies['logistic-science-pack'].researched)
  surface.request_to_generate_chunks({320,180},2);surface.force_generate_chunk_requests()
  for _,e in ipairs(surface.find_entities_filtered({area={{315,175},{334,186}},type={'tree','simple-entity','cliff'}})) do e.destroy() end
  local tiles={};for x=315,334 do for y=175,186 do tiles[#tiles+1]={name='dirt-1',position={x,y}} end end;surface.set_tiles(tiles,true)
  local c=assert(surface.create_entity({name='character',position={320,180},force=force}))
  local inv=c.get_main_inventory()
  for _,name in ipairs({'sn-field-controller','sn-field-drone','stone-wall'}) do assert(inv.insert({name=name,count=1})==1) end
  local ghost=assert(surface.create_entity({name='entity-ghost',inner_name='stone-wall',position={330.5,181.5},force=force}))
  local p=player(c);D.set_enabled(p,true);S.root().field_drones.owners[1301].cell=10;D.step_player(p)
  local id=next(S.root().field_drones.owners[1301].workers)
  assert(id,'recall probe failed to launch')
  storage.recall_probe={character=c,ghost=ghost,id=id,start=game.tick}
end
function X.tick()
  local c=storage.recall_probe;if not c or c.finished then return end
  local age=game.tick-c.start;local p=player(c.character)
  D.step_player(p)
  if age==60 then
    local rec=S.root().field_drones.workers[c.id]
    assert(rec and rec.entity.valid and rec.entity.position.x>322)
    c.before=rec.entity.position.x;D.set_enabled(p,false)
    assert(rec.entity.valid and rec.entity.position.x==c.before and rec.cargo.valid and rec.stage=='returning')
    assert(c.character.get_main_inventory().get_item_count('sn-field-drone')==0)
  elseif age==75 then
    local rec=S.root().field_drones.workers[c.id]
    assert(rec and rec.entity.valid and rec.entity.position.x<c.before,'paused worker did not fly home')
    D.set_enabled(p,true);assert(rec.entity.valid and rec.stage=='returning')
    D.set_enabled(p,false)
  elseif age==300 then
    assert(not S.root().field_drones.workers[c.id])
    assert(c.ghost.valid,'paused construction was completed')
    local inv=c.character.get_main_inventory()
    assert(inv.get_item_count('sn-field-drone')==1 and inv.get_item_count('stone-wall')==1)
    c.finished=true
    log('SECOND_NATURE_ENGINE_CREW_RECALL_OK')
  end
end
return X
