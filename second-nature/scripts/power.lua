-- Only weather/geothermal sources need runtime output. Fuel generators and
-- photovoltaic racks use native fuel/electricity/solar mechanics.
local E=require("shared.energy")
local S=require("scripts.state")
local P={}
local function root() return S.root().power_sources end
local function clamp(n,a,b) return math.max(a,math.min(b,n)) end
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
  end
  local factors={nauvis=.8,gleba=.65,fulgora=.55,vulcanus=1,aquilo=.3}
  local planet=surface.planet and surface.planet.name
  return def.watts*(factors[planet] or 0)
end
function P.register(entity)
  if not (entity and entity.valid and entity.unit_number) then return end
  local def=E.by_plant[entity.name]
  if def and def.passive then
    root().entities[entity.unit_number]=entity
    entity.power_production=P.output(entity,game.tick)/60 -- runtime API is joules/tick
  end
end
function P.init()
  local state=S.root();state.power_sources=state.power_sources or {entities={}}
  local names={};for name,def in pairs(E.by_plant) do if def.passive then names[#names+1]=name end end;table.sort(names)
  for _,surface in pairs(game.surfaces) do
    for _,entity in ipairs(surface.find_entities_filtered({name=names})) do P.register(entity) end
  end
end
function P.tick()
  if not root() then return end
  local remove={}
  for id,entity in pairs(root().entities) do
    if entity and entity.valid then entity.power_production=P.output(entity,game.tick)/60
    else remove[#remove+1]=id end
  end
  for _,id in ipairs(remove) do root().entities[id]=nil end
end
return P
