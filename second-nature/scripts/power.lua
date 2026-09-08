-- Weather, shoreline and geothermal output only. Native generators own all
-- fuel, steam, plasma and fission energy consumption/conversion.
local E=require("shared.energy")
local S=require("scripts.state")
local P={}
local function root() return S.root().power_sources end
local function clamp(n,a,b) return math.max(a,math.min(b,n)) end
local function region(entity,def)
  local size=def.region_size or 32
  return entity.surface.index..":"..math.floor(entity.position.x/size)..":"..math.floor(entity.position.y/size)
end
local function region_budgets()
  local result={}
  for _,entity in pairs(root().entities) do
    if entity and entity.valid and entity.active~=false then
      local def=E.by_plant[entity.name]
      if def and def.passive=="geothermal" then
        local key=region(entity,def);local r=result[key] or {weight=0,budget=0,legacy_floor=0}
        r.weight=r.weight+def.watts;r.budget=math.max(r.budget,def.watts)
        if root().legacy and root().legacy[entity.unit_number] then r.legacy_floor=r.legacy_floor+1500000 end
        result[key]=r
      end
    end
  end
  root().regions=result
end
function P.output(entity,tick)
  local def=E.by_plant[entity.name]
  if not (def and def.passive and entity.active~=false) then return 0 end
  local surface=entity.surface
  if surface.platform then return 0 end
  if def.passive=="wind" then
    local pressure=surface.get_property("pressure") or 0
    if pressure<300 then return 0 end
    local wind=clamp(math.abs(surface.wind_speed or 0)/.015,0,1)
    local phase=surface.index*.7+math.floor(entity.position.x/256)*.11+math.floor(entity.position.y/256)*.17
    local gust=clamp(.45+.4*math.sin(tick/900+phase)+.2*math.sin(tick/257+phase),0,1)
    return def.watts*wind*gust*clamp(pressure/1000,0,1)
  elseif def.passive=="hydro" then
    local tiles=surface.find_tiles_filtered({position=entity.position,radius=4,
      name={"water","deepwater","water-green","deepwater-green"},limit=4})
    return #tiles>=4 and def.watts or 0
  end
  local factors={nauvis=.8,gleba=.65,fulgora=.55,vulcanus=1,aquilo=.3}
  local planet=surface.planet and surface.planet.name
  local budget=root() and root().regions and root().regions[region(entity,def)]
  local watts=def.watts
  if budget and budget.weight>0 then
    local floor=(root().legacy and root().legacy[entity.unit_number]) and 1500000 or 0
    watts=floor+math.max(0,budget.budget-budget.legacy_floor)*def.watts/budget.weight
  end
  return watts*(factors[planet] or 0)
end
function P.register(entity,defer)
  if not (entity and entity.valid and entity.unit_number) then return end
  local def=E.by_plant[entity.name]
  if def and def.passive then
    root().entities[entity.unit_number]=entity
    if not defer then
      if def.passive=="geothermal" then
        region_budgets();local key=region(entity,def)
        for _,other in pairs(root().entities) do
          local d=other.valid and E.by_plant[other.name]
          if d and d.passive=="geothermal" and region(other,d)==key then other.power_production=P.output(other,game.tick)/60 end
        end
      else entity.power_production=P.output(entity,game.tick)/60 end
    end
  end
end
function P.init()
  local state=S.root();local previous=state.power_sources
  state.power_sources=state.power_sources or {entities={},version=2,legacy={}}
  if previous and not previous.version then
    previous.legacy={}
    for id,entity in pairs(previous.entities) do
      if entity and entity.valid and entity.name=="sn-geothermal-bore" then previous.legacy[id]=true end
    end
    previous.version=2
  end
  local names={};for name,def in pairs(E.by_plant) do if def.passive then names[#names+1]=name end end;table.sort(names)
  for _,surface in pairs(game.surfaces) do
    for _,entity in ipairs(surface.find_entities_filtered({name=names})) do P.register(entity,true) end
  end
  P.tick()
end
function P.tick()
  if not root() then return end
  local remove={}
  for id,entity in pairs(root().entities) do if not (entity and entity.valid) then remove[#remove+1]=id end end
  for _,id in ipairs(remove) do root().entities[id]=nil;if root().legacy then root().legacy[id]=nil end end
  region_budgets()
  for _,entity in pairs(root().entities) do entity.power_production=P.output(entity,game.tick)/60 end
end
return P
