-- Native energy/fuel/fluid/heat tests for all eighteen staged systems.
local E=require('shared.energy')
local P=require('scripts.power')
local X={}
local function create(surface,name,pos,extra)
  local spec=extra or {};spec.name=name;spec.position=pos;spec.force=game.forces.player
  return assert(surface.create_entity(spec),name)
end
function X.init(nauvis)
  local cases={};local stages={early=0,mid=0,late=0}
  for i,def in ipairs(E.plants) do
    local s,pos
    if def.passive=='geothermal' then s=nauvis;pos={x=-224-i*64,y=256}
    else
      s=game.create_surface('sn-stage-power-'..i,{width=64,height=64});pos={x=0,y=0}
      s.always_day=true;s.solar_power_multiplier=1;s.wind_speed=.015;s.set_property('pressure',1000)
    end
    s.request_to_generate_chunks(pos,2);s.force_generate_chunk_requests()
    for _,e in ipairs(s.find_entities_filtered({area={{pos.x-10,pos.y-10},{pos.x+10,pos.y+10}}})) do
      if e.type~='resource' then e.destroy() end
    end
    local tiles={}
    for x=pos.x-10,pos.x+10 do for y=pos.y-10,pos.y+10 do tiles[#tiles+1]={name='dirt-1',position={x,y}} end end
    if def.passive=='hydro' then
      for y=-1,2 do tiles[#tiles+1]={name='water',position={pos.x+3,pos.y+y}} end
    end
    s.set_tiles(tiles,true)
    local plant=create(s,'sn-'..def.name,pos);P.register(plant)
    local sink=create(s,'sn-engine-power-load',{pos.x+7,pos.y})
    create(s,'substation',{pos.x+3,pos.y+5})
    cases[#cases+1]={entity=plant,sink=sink,definition=def,peak_pollution=0,ash=0,hot=0}
    stages[def.stage]=stages[def.stage]+1
  end
  assert(stages.early==6 and stages.mid==6 and stages.late==6)
  storage.staged_power={cases=cases,start=game.tick}
end
function X.tick()
  local data=storage.staged_power;if not data or data.finished then return end
  local age=game.tick-data.start
  if age%60==0 then
    P.tick()
    for _,case in ipairs(data.cases) do
      local e,d=case.entity,case.definition
      if age>=120 then
        if d.kind=='burner-generator' then
          e.insert({name=d.fuel=='sn-grown-fuel' and 'sn-biopellet' or 'coal',count=50})
          if d.fuel=='sn-grown-fuel' then
            case.ash=case.ash+e.burner.burnt_result_inventory.get_item_count('sn-bio-ash')
            e.burner.burnt_result_inventory.clear()
          end
        elseif d.kind=='generator' then e.insert_fluid({name=d.fluid,amount=400,temperature=d.temperature})
        elseif d.kind=='reactor' then e.insert({name='uranium-fuel-cell',count=1})
        elseif d.kind=='fusion-generator' then
          e.insert_fluid({name='fusion-plasma',amount=10,temperature=1000000})
          case.hot=case.hot+e.remove_fluid({name='fluoroketone-hot',amount=1000})
        end
      end
      case.peak_pollution=math.max(case.peak_pollution,e.surface.get_pollution(e.position))
    end
  end
  if age<4800 then return end
  for _,case in ipairs(data.cases) do
    local e,d=case.entity,case.definition
    if d.kind=='reactor' then
      assert(e.temperature>100,'fission produced no real heat')
      assert(e.burner.currently_burning,'fission did not consume fuel')
    else
      local count=e.electric_network_statistics.get_input_count(e.name)
      assert(count>0,'no native electrical output: '..d.name)
      assert(count<=d.watts*age/60*1.02+d.watts*2,'power exceeded its declared energy envelope: '..d.name)
    end
    if d.pollution and d.pollution>0 then assert(case.peak_pollution>0,'no real emissions: '..d.name) end
    if d.name=='biopellet-engine' then assert(case.ash>0,'biomass engine produced no ash') end
    if d.kind=='fusion-generator' then assert(case.hot>0,'plasma generator did not return hot coolant') end
  end
  data.finished=true
  log('SECOND_NATURE_ENGINE_POWER_OPTIONS_OK')
  log('SECOND_NATURE_ENGINE_POWER_STAGES_OK')
end
return X
