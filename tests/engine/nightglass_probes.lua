-- Real native electricity, solar equipment, batteries, fuel rejection and rail
-- traction. Test energy seeds are isolated and labeled; sunlight drives the main cases.
local S=require('scripts.state')
local R=require('scripts.solar_rail')
local P=require('scripts.power')
local E=require('shared.energy')
local N={}
local function battery(loco)
  for _,eq in pairs(loco.grid.equipment) do if eq.name:find('sn%-solar%-rail%-battery') then return eq end end
end
local function entity(surface,name,pos,extra)
  local spec=extra or {};spec.name=name;spec.position=pos;spec.force=game.forces.player
  return assert(surface.create_entity(spec),name)
end
local function clear(surface,area)
  for _,e in ipairs(surface.find_entities_filtered({area=area,type={'tree','simple-entity','cliff','unit-spawner','turret'}})) do e.destroy() end
  local tiles={};for x=area[1][1],area[2][1] do for y=area[1][2],area[2][2] do tiles[#tiles+1]={name='dirt-1',position={x,y}} end end
  surface.set_tiles(tiles,true)
end
function N.init(nauvis)
  R.init();P.init()
  local surface=game.create_surface('sn-solar-rail-probe',{width=128,height=768})
  surface.request_to_generate_chunks({24,-80},10);surface.force_generate_chunk_requests()
  clear(surface,{{-4,-260},{54,28}})
  surface.always_day=false;surface.freeze_daytime=true;surface.daytime=.5;surface.solar_power_multiplier=1
  local case={surface=surface,locos={},rails={},start=game.tick,peaks={},phase='empty-night',plants={}}
  for i=1,4 do
    local x=(i-1)*16
    local ends={}
    for y=-256,24,2 do
      local rail=entity(surface,'straight-rail',{x,y},{direction=defines.direction.north})
      if y==-256 then ends.far=rail elseif y==20 then ends.home=rail end
    end
    local def=E.trains[math.min(i,3)]
    local loco=entity(surface,'sn-'..def.name,{x,20},{orientation=0})
    R.register(loco)
    assert(loco.insert({name='coal',count=1})==0,'solar locomotive accepted coal')
    assert(loco.insert({name='rocket-fuel',count=1})==0,'solar locomotive accepted rocket fuel')
    assert(loco.grid and #loco.grid.equipment==2 and battery(loco).energy==0,'new solar grid did not start empty')
    assert(loco.grid.max_solar_energy>0,'native roof panels are not a solar source')
    loco.train.manual_mode=true
    case.locos[i]=loco;case.rails[i]=ends;case.peaks[i]=0
  end
  -- A nearby ordinary grid must not charge the isolated locomotive grid.
  entity(surface,'electric-energy-interface',{7,12})
  entity(surface,'substation',{6,17})
  entity(surface,'accumulator',{9,19})
  -- Separate escrow seed proves non-zero native LuaBurner/LuaEquipment state
  -- survives creation/save/reload. It is not used to prove solar generation.
  battery(case.locos[4]).energy=12345
  R.tick()
  assert(battery(case.locos[4]).energy+case.locos[4].burner.remaining_burning_fuel<=12345.001)
  storage.nightglass=case
  -- Each power source has a native accumulator load. Dirty sources burn real
  -- fuel; the biomass unit must also produce its ash inventory.
  for index,def in ipairs(E.plants) do
    local ps
    if def.passive=='geothermal' then
      ps=nauvis;ps.request_to_generate_chunks({-180,240},2);ps.force_generate_chunk_requests();clear(ps,{{-188,232},{-172,248}})
    else
      ps=game.create_surface('sn-power-probe-'..index,{width=64,height=64})
      ps.request_to_generate_chunks({0,0},2);ps.force_generate_chunk_requests();clear(ps,{{-8,-8},{8,8}})
      ps.always_day=true;ps.solar_power_multiplier=1;ps.wind_speed=.015;ps.set_property('pressure',1000)
    end
    local pos=def.passive=='geothermal' and {x=-180,y=240} or {x=0,y=0}
    local plant=entity(ps,'sn-'..def.name,pos);P.register(plant)
    local load=entity(ps,'accumulator',{pos.x+5,pos.y})
    entity(ps,'accumulator',{pos.x+5,pos.y+3});entity(ps,'accumulator',{pos.x+5,pos.y-3})
    entity(ps,'substation',{pos.x+3,pos.y+4})
    if def.kind=='burner-generator' then
      local fuel=def.fuel=='sn-grown-fuel' and 'sn-biopellet' or 'coal'
      assert(plant.insert({name=fuel,count=20})==20)
    end
    case.plants[#case.plants+1]={entity=plant,load=load,definition=def,peak_pollution=0}
  end
  log('SECOND_NATURE_ENGINE_NIGHTGLASS_READY')
end
function N.tick()
  local c=storage.nightglass;if not c or c.finished then return end
  local age=game.tick-c.start
  R.tick();if game.tick%60==0 then P.tick() end
  if age==60 then
    local e=c.locos[4];local total=battery(e).energy+e.burner.remaining_burning_fuel+e.burner.heat
    assert(total>0 and total<=12345.01,'saved motor escrow minted or lost all test energy')
    R.flush(e);battery(e).energy=0
  end
  if age==300 then
    for i=1,3 do
      local e=c.locos[i]
      assert(battery(e).energy==0 and e.burner.remaining_burning_fuel==0,'night or ordinary grid charged a solar train')
    end
    c.surface.daytime=0;c.phase='solar-charge'
  elseif age==1200 then
    for i=1,3 do
      local e=c.locos[i]
      assert(battery(e).energy>1000000,'native panels did not charge the stopped train')
      c['charged-'..i]=battery(e).energy
      e.train.schedule={current=1,records={{rail=c.rails[i].far,temporary=true,wait_conditions={{type='time',ticks=600}}}}}
      e.train.manual_mode=false
    end
    c.phase='day-drive'
  elseif age==2100 then
    for i=1,3 do
      local e=c.locos[i];local def=E.trains[i]
      assert(e.position.y<10,'solar-only native traction did not move the locomotive')
      assert(c.peaks[i]>0 and c.peaks[i]<=def.day_speed+.01,'day speed exceeded the solar prototype limit')
      assert(S.root().solar_rail.locos[e.unit_number].consumed>0,'native motion consumed no battery credit')
      e.train.schedule={current=1,records={{rail=c.rails[i].home,temporary=true,wait_conditions={{type='time',ticks=600}}}}}
      e.train.manual_mode=false
      c['night-y-'..i]=e.position.y;c['night-used-'..i]=S.root().solar_rail.locos[e.unit_number].consumed
    end
    c.surface.daytime=.5;c.phase='night-drive';R.tick()
  elseif age==3300 then
    for i=1,3 do
      local e=c.locos[i]
      assert(math.abs(e.position.y-c['night-y-'..i])>1,'stored solar energy did not propel the train at night')
      assert(S.root().solar_rail.locos[e.unit_number].consumed>c['night-used-'..i],'night movement used no stored energy')
      R.flush(e);battery(e).energy=0
      c['spent-'..i]=S.root().solar_rail.locos[e.unit_number].consumed
    end
    c.phase='empty-coast'
  elseif age==4800 then
    for i=1,3 do
      local e=c.locos[i]
      assert(battery(e).energy==0 and e.burner.remaining_burning_fuel==0,'depleted solar train was refueled without sunlight')
      assert(S.root().solar_rail.locos[e.unit_number].consumed==c['spent-'..i],'empty train received hidden traction energy')
    end
    for _,p in ipairs(c.plants) do
      assert(p.load.energy>0,'native power source did not charge its accumulator: '..p.definition.name)
      if p.definition.pollution and p.definition.pollution>0 then assert(p.peak_pollution>0,'polluting generator emitted no real pollution') end
      if p.definition.kind=='burner-generator' then
        assert(p.entity.burner.currently_burning or p.entity.burner.inventory.get_item_count()<20,'fuel generator consumed no fuel')
      end
      if p.definition.name=='biopellet-engine' then
        assert(p.entity.burner.burnt_result_inventory.get_item_count('sn-bio-ash')>0,'biopellet engine produced no real ash')
      end
    end
    c.finished=true
    log('SECOND_NATURE_ENGINE_SOLAR_RAIL_OK')
    log('SECOND_NATURE_ENGINE_POWER_OPTIONS_OK')
  end
  if age%60==0 then for _,p in ipairs(c.plants) do p.peak_pollution=math.max(p.peak_pollution,p.entity.surface.get_pollution(p.entity.position)) end end
  for i=1,3 do
    local e=c.locos[i];local speed=math.abs(e.train.speed)
    if c.phase=='day-drive' then c.peaks[i]=math.max(c.peaks[i],speed) end
    if c.phase=='night-drive' or c.phase=='empty-coast' then
      assert(speed<=E.trains[i].night_speed+.01,'solar train exceeded its nighttime speed limit')
    end
  end
end
return N
