-- REAL ENGINE smoke test. Packaged only by tools/headless.py, never with the mod.
require('util')
local K=require('__second-nature__/shared/catalog')
local C=require('__second-nature__/shared/constants')
local Probes=require('module_probes')
local function build(surface,name,pos)
  return assert(surface.create_entity({name=name,position=pos,force='player',raise_built=true}),name)
end
script.on_init(function()
  local force=game.forces.player
  force.research_all_technologies()
  storage.start_tick=game.tick
  storage.worlds={}
  for _,name in ipairs(C.planets) do
    local surface=game.planets[name].create_surface()
    surface.request_to_generate_chunks({0,0},2);surface.force_generate_chunk_requests()
    surface.peaceful_mode=true
    storage.worlds[name]=surface
    build(surface,'sn-ecology-monitor',{x=32,y=32})
    assert(surface.get_property('sn-restoration-domain')==1,name..' domain')
  end
  -- Instantiate every entity to exercise prototype/graphics/fluidbox initialization.
  for index,machine in ipairs(K.machines) do
    local surface=storage.worlds[machine.planet or 'nauvis']
    build(surface,'sn-'..machine.name,{x=-48+(index%8)*6,y=-48+math.floor(index/8)*6})
  end
  local surface=storage.worlds.nauvis
  Probes.run(surface,force)
  local a=build(surface,'sn-air-scrubber',{x=0,y=0})
  build(surface,'substation',{x=5,y=1})
  build(surface,'electric-energy-interface',{x=6,y=5})
  assert(a.insert({name='sn-filter-cartridge',count=1})==1)
  assert(a.insert_fluid({name='water',amount=25})==25)
  local idle=build(surface,'sn-air-scrubber',{x=0,y=7}) -- powered, no inputs
  local powerless=build(surface,'sn-air-scrubber',{x=96,y=0})
  powerless.insert({name='sn-filter-cartridge',count=1});powerless.insert_fluid({name='water',amount=25})
  surface.pollute({0,0},100)
  storage.machine,storage.idle,storage.powerless=a,idle,powerless
  storage.baseline=remote.call('second_nature','get_world','nauvis').cycles
  -- Physical transfer through diagonal custom vectors, not only setter acceptance.
  local arm=build(surface,'sn-vector-inserter',{x=80.5,y=44.5})
  arm.pickup_position={x=82.5,y=42.5};arm.drop_position={x=78.5,y=46.5}
  local source=build(surface,'iron-chest',{x=82.5,y=42.5})
  local destination=build(surface,'iron-chest',{x=78.5,y=46.5})
  assert(source.insert({name='iron-plate',count=4})==4)
  build(surface,'substation',{x=84,y=48});build(surface,'electric-energy-interface',{x=86,y=49})
  storage.transfer_source,storage.transfer_destination=source,destination
  -- New stable campaign prototypes and real inventory APIs.
  local ship=build(surface,'sn-lander',{x=64,y=64})
  for _,item in ipairs(C.landing_cargo) do assert(ship.insert({name=item[1],count=item[2]})==item[2],item[1]) end
  local friend=game.forces['sn-smoke-friendly'] or game.create_force('sn-smoke-friendly')
  assert(surface.create_entity({name='sn-bloomback',position={64,80},force=friend}))
  assert(surface.create_entity({name='sn-bloom-nest',position={72,80},force=friend}))
  rendering.draw_rectangle({surface=surface,left_top={60,60},right_bottom={92,92},color={0.2,0.8,0.4,0.15},filled=true,draw_on_ground=true,time_to_live=120})
  local absorptions=prototypes.entity['small-biter'].absorptions_to_join_attack
  assert(absorptions and absorptions.pollution>=1e29,'pollution recruitment cost: '..tostring(absorptions and absorptions.pollution))
  -- Save creation followed by benchmarking exercises storage LuaObject restoration.
  log('SECOND_NATURE_ENGINE_SMOKE_READY')
end)
script.on_nth_tick(60,function()
  if storage.finished or not storage.start_tick or game.tick-storage.start_tick<1800 then return end
  assert(storage.machine.valid,'tracked entity lost across save/load')
  assert(storage.machine.products_finished==1,'a single batch must increment products_finished by exactly one')
  assert(storage.idle.products_finished==0,'idle machine must not craft')
  assert(storage.powerless.products_finished==0,'unpowered machine must not craft')
  assert(storage.transfer_source.get_item_count('iron-plate')==0 and storage.transfer_destination.get_item_count('iron-plate')==4,'custom-vector inserter did not transfer its batch')
  local snapshot=remote.call('second_nature','get_world','nauvis')
  assert(snapshot.cycles==storage.baseline+1,'one actual completed cycle must earn one ecological cycle')
  assert(snapshot.values.atmosphere>C.profiles.nauvis.initial.atmosphere,'powered scrubber must improve atmosphere')
  assert(snapshot.removed_pollution>0,'pollution capture did not run')
  for _,name in ipairs(C.planets) do assert(remote.call('second_nature','get_world',name),'missing world '..name) end
  storage.machine.destroy({raise_destroy=true})
  storage.finished=true
  log('SECOND_NATURE_ENGINE_SMOKE_OK')
end)
