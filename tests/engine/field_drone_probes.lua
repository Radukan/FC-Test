-- Unmodified production drone modules, isolated companion storage, real engine
-- characters/inventories/ghosts/render objects. The LuaPlayer-facing shell below
-- is a fixture: headless has no interactive GUI/player to drive the shortcut.
local S=require('scripts.state')
local D=require('scripts.field_drones')
local C=require('shared.field_drones')
local P={}
local function operator(index,character)
  return {index=index,valid=true,connected=true,controller_type=defines.controllers.character,
    character=character,force=character.force,
    print=function() end,set_shortcut_toggled=function() end}
end
local function total(inventories,name,quality)
  local n=0
  for _,inv in ipairs(inventories) do n=n+inv.get_item_count({name=name,quality=quality or 'normal'}) end
  return n
end
function P.init(surface,force)
  -- Isolate deterministic API probes from Nauvis wildlife/terrain succession.
  surface=game.create_surface('sn-isolated-field-crew',{width=512,height=512,seed=8123,
    default_enable_all_autoplace_controls=false,
    autoplace_settings={entity={treat_missing_as_default=false,settings={}},decorative={treat_missing_as_default=false,settings={}}}})
  surface.peaceful_mode=true
  D.init()
  surface.request_to_generate_chunks({120,150},2);surface.force_generate_chunk_requests()
  for _,entity in ipairs(surface.find_entities_filtered({area={{116,146},{151,161}},type={'tree','simple-entity','cliff'}})) do entity.destroy() end
  local tiles={}
  for x=116,150 do for y=146,160 do tiles[#tiles+1]={name='dirt-1',position={x,y}} end end
  surface.set_tiles(tiles,true)
  local a=assert(surface.create_entity({name='character',position={120,150},force=force}))
  local b=assert(surface.create_entity({name='character',position={121,150},force=force}))
  local ai,bi=a.get_main_inventory(),b.get_main_inventory()
  assert(ai.insert({name=C.controller,count=1})==1 and bi.insert({name=C.controller,count=1})==1)
  assert(ai.insert({name=C.item,count=12})==12 and bi.insert({name=C.item,count=2})==2)
  assert(ai.insert({name='stone-wall',count=10})==10 and bi.insert({name='stone-wall',count=3})==3)
  assert(ai.insert({name='stone-brick',count=1})==1)
  assert(ai.insert({name='iron-chest',quality='rare',count=1})==1)
  local function ghost(name,pos,q,tile)
    return assert(surface.create_entity({name=tile and 'tile-ghost' or 'entity-ghost',inner_name=name,
      position=pos,force=force,quality=q or 'normal',expires=false}))
  end
  local normal=ghost('stone-wall',{126.5,152.5})
  local rare=ghost('iron-chest',{127.5,154.5},'rare')
  local tile=ghost('stone-path',{123.5,153.5},nil,true)
  local cancelled=ghost('stone-wall',{128.5,151.5})
  local loose=ghost('stone-wall',{127.5,156.5})
  local item=assert(surface.create_entity({name='item-on-ground',position={127.5,156.5},stack={name='copper-plate',count=5}}))
  local port=assert(surface.create_entity({name='roboport',position={137,150},force=force}))
  assert(surface.create_entity({name='substation',position={143,151},force=force}))
  assert(surface.create_entity({name='electric-energy-interface',position={146,155},force=force}))
  assert(port.get_inventory(defines.inventory.roboport_robot).insert({name=C.item,count=1})==0,'field drones can dock in a native roboport')
  local pa,pb=operator(1001,a),operator(1002,b)
  assert(D.set_enabled(pa,true) and D.set_enabled(pb,true))
  S.root().field_drones.owners[1001].cell=10;S.root().field_drones.owners[1002].cell=10
  D.step_player(pa);D.step_player(pb)
  assert(S.root().field_drones.active==4,'native dispatch/loose-item guard: '..S.root().field_drones.active)
  assert(normal.valid and rare.valid and tile.valid,'a dispatch instantly constructed a ghost')
  assert(total({ai,bi},C.item)==10,'four field drone items were not reserved')
  for _,rec in pairs(S.root().field_drones.workers) do
    assert(rec.entity.type=='simple-entity-with-owner' and rec.entity.logistic_network==nil)
    assert(rec.cargo.valid and rec.visual.valid and rec.shadow.valid,'native escrow/render creation failed')
  end
  cancelled.destroy()
  storage.drone_probe={characters={a,b},normal=normal,rare=rare,tile=tile,loose=loose,item=item,port=port,
    surface=surface,network_checked=false,finished=false}
  -- Save creation ends immediately after initialization. The benchmark must
  -- restore the in-flight LuaInventory, LuaEntity and LuaRenderObject references.
  log('SECOND_NATURE_ENGINE_FIELD_DRONES_READY')
end
function P.tick()
  local p=storage.drone_probe
  if not p or p.finished then return end
  local pa,pb=operator(1001,p.characters[1]),operator(1002,p.characters[2])
  D.step_player(pa);D.step_player(pb)
  if game.tick>=60 and not p.network_checked then
    assert(p.port.logistic_network and p.port.energy>0,'native reference roboport is not powered/networked')
    for _,rec in pairs(S.root().field_drones.workers) do
      assert(rec.entity.logistic_network==nil,'field drone joined the nearby network')
      assert(rec.entity.position.x>120 or rec.stage=='returning','drone did not physically travel')
    end
    p.network_checked=true
  end
  if game.tick<1200 then return end
  local ai,bi=p.characters[1].get_main_inventory(),p.characters[2].get_main_inventory()
  assert(not p.normal.valid and not p.rare.valid and not p.tile.valid,'real ghosts incomplete: normal='..tostring(p.normal.valid)..' rare='..tostring(p.rare.valid)..' tile='..tostring(p.tile.valid)..' active='..S.root().field_drones.active)
  assert(p.surface.get_tile({123.5,153.5}).name=='stone-path','tile revival did not place the requested tile')
  local rare=p.surface.find_entities_filtered({position={127.5,154.5},name='iron-chest',quality='rare'})
  assert(#rare==1,'revival lost the requested quality')
  assert(total({ai,bi},'stone-wall')==12,'construction/cancellation changed wall-item conservation')
  assert(total({ai,bi},'stone-brick')==0 and total({ai,bi},'iron-chest','rare')==0,'native building material was not consumed exactly once')
  assert(total({ai,bi},C.item)==14,'a successful or cancelled sortie lost/duplicated a drone')
  assert(p.loose.valid and p.item.valid and p.item.stack.count==5,'field drones moved or deleted loose cargo')
  assert(S.root().field_drones.active==0,'in-flight state did not drain')
  assert(S.root().field_drones.owners[1001].built+S.root().field_drones.owners[1002].built==3,'two operators duplicated a task')
  D.set_enabled(pa,false);D.set_enabled(pb,false)
  p.finished=true
  log('SECOND_NATURE_ENGINE_FIELD_DRONES_OK')
end
return P
