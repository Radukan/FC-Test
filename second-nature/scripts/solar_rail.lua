-- Solar-only traction adapter. Native roof equipment charges native batteries;
-- only withdrawn battery joules enter the locomotive's inaccessible burner.
local E=require("shared.energy")
local S=require("scripts.state")
local R={}
local FUEL="sn-solar-drive-charge"
local function root() return S.root().solar_rail end
local function components(entity,definition)
  local grid=entity.grid
  if not (grid and grid.valid) then return nil end
  local panel,battery
  for _,eq in pairs(grid.equipment) do
    if eq.name=="sn-solar-rail-panel-"..definition.tier and not panel then panel=eq
    elseif eq.name=="sn-solar-rail-battery-"..definition.tier and not battery then battery=eq
    else return nil end
  end
  if panel and battery then return panel,battery end
end
local function private_fuel(burner)
  local current=burner.currently_burning
  if not current then return false end
  local name=current.name
  if type(name)=="table" or type(name)=="userdata" then name=name.name end
  return name==FUEL
end
local function clear_motor(entity)
  local burner=entity.burner
  if burner then burner.heat=0;burner.currently_burning=nil end
end
local function twilight(surface)
  return math.max(0,math.min(1,((surface.darkness or 0)-.10)/.70))
end
function R.definition(entity) return entity and entity.valid and E.by_train[entity.name] end
function R.register(entity)
  local definition=R.definition(entity)
  if not definition or not entity.unit_number then return nil end
  local r=root();if r.locos[entity.unit_number] then return r.locos[entity.unit_number] end
  local grid=entity.grid
  if grid and grid.valid and #grid.equipment==0 then
    -- A newly crafted locomotive paid for these factory-fitted components.
    -- The locked grid cannot be emptied/re-fitted by normal player actions.
    grid.put({name="sn-solar-rail-panel-"..definition.tier,position={0,0}})
    local battery=grid.put({name="sn-solar-rail-battery-"..definition.tier,position={2,0}})
    if battery then battery.energy=0 end
  end
  clear_motor(entity)
  local rec={entity=entity,credit=0,consumed=0,unit_number=entity.unit_number}
  r.locos[entity.unit_number]=rec
  return rec
end
function R.init()
  local state=S.root();state.solar_rail=state.solar_rail or {locos={}}
  local names={};for name in pairs(E.by_train) do names[#names+1]=name end;table.sort(names)
  for _,surface in pairs(game.surfaces) do
    for _,entity in ipairs(surface.find_entities_filtered({name=names})) do R.register(entity) end
  end
  for id,rec in pairs(root().locos) do if not (rec.entity and rec.entity.valid) then root().locos[id]=nil end end
end
function R.flush(entity)
  if not root() or not (entity and entity.valid) then return end
  local rec=root().locos[entity.unit_number];if not rec then return end
  local def=E.by_train[entity.name];if not def then return end
  local _,battery=components(entity,def)
  local burner=entity.burner;local left=0
  if burner and private_fuel(burner) then left=math.min(rec.credit or 0,math.max(0,burner.remaining_burning_fuel+burner.heat)) end
  rec.consumed=(rec.consumed or 0)+math.max(0,(rec.credit or 0)-left)
  if battery and left>0 then battery.energy=math.min(battery.max_energy,battery.energy+left) end
  clear_motor(entity);rec.credit=0
end
local function fund(rec,def)
  local entity=rec.entity
  R.flush(entity)
  local _,battery=components(entity,def)
  if not battery then rec.invalid_grid=true;return end
  rec.invalid_grid=false
  local night=twilight(entity.surface)
  local allowed=def.watts*E.motor_interval/60*(1-night*(1-def.night_power))
  local joules=math.min(math.max(0,battery.energy),allowed)
  if joules<=.001 then return end
  battery.energy=battery.energy-joules
  entity.burner.currently_burning={name=FUEL,quality="normal"}
  entity.burner.remaining_burning_fuel=joules
  entity.burner.heat=0
  rec.credit=joules
end
function R.tick()
  if not root() then return end
  local limits={};local stale={}
  for id,rec in pairs(root().locos) do
    local entity=rec.entity
    if not (entity and entity.valid) then stale[#stale+1]=id
    else
      local def=E.by_train[entity.name]
      if not def then stale[#stale+1]=id
      else
        if game.tick%E.motor_interval==0 then fund(rec,def) end
        local train=entity.train
        if train and train.valid then
          local n=twilight(entity.surface)
          local cap=def.day_speed+(def.night_speed-def.day_speed)*n
          local old=limits[train.id]
          if not old or cap<old.cap then limits[train.id]={train=train,cap=cap} end
        end
      end
    end
  end
  for _,id in ipairs(stale) do root().locos[id]=nil end
  for _,entry in pairs(limits) do
    local train,speed=entry.train,entry.train.speed
    -- Never increase velocity, change manual mode or rewrite schedules. A
    -- consist containing solar locomotives obeys its lowest solar speed cap.
    if math.abs(speed)>entry.cap then train.speed=speed<0 and -entry.cap or entry.cap end
  end
end
function R.status(entity)
  local def=R.definition(entity);if not def then return nil end
  local panel,battery=components(entity,def)
  local rec=root() and root().locos[entity.unit_number]
  local night=twilight(entity.surface)
  return {energy=battery and battery.energy or 0,capacity=battery and battery.max_energy or def.battery_joules,
    solar_watts=def.solar_watts,cap=def.day_speed+(def.night_speed-def.day_speed)*night,
    mode=not panel and "invalid-grid" or (night>.8 and "night" or (night>.05 and "twilight" or "day")),
    consumed=rec and rec.consumed or 0}
end
return R
