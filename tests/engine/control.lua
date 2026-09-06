-- Optional REAL ENGINE smoke test. Packaged only by tools/headless.py, never with the mod.
local K=require('__second-nature__/shared/catalog')
local C=require('__second-nature__/shared/constants')
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
  -- Save creation followed by benchmarking exercises storage LuaObject restoration.
  log('SECOND_NATURE_ENGINE_SMOKE_READY')
end)
script.on_nth_tick(60,function()
  if storage.finished or not storage.start_tick or game.tick-storage.start_tick<1800 then return end
  assert(storage.machine.valid,'tracked entity lost across save/load')
  assert(storage.machine.products_finished==1,'a single batch must increment products_finished by exactly one')
  assert(storage.idle.products_finished==0,'idle machine must not craft')
  assert(storage.powerless.products_finished==0,'unpowered machine must not craft')
  local snapshot=remote.call('second_nature','get_world','nauvis')
  assert(snapshot.cycles==storage.baseline+1,'one actual completed cycle must earn one ecological cycle')
  assert(snapshot.values.atmosphere>35,'powered scrubber must improve atmosphere')
  assert(snapshot.removed_pollution>0,'pollution capture did not run')
  for _,name in ipairs(C.planets) do assert(remote.call('second_nature','get_world',name),'missing world '..name) end
  storage.machine.destroy({raise_destroy=true})
  storage.finished=true
  log('SECOND_NATURE_ENGINE_SMOKE_OK')
end)
