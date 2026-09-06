local C = require("shared.constants")
local K = require("shared.catalog")
local S = require("scripts.state")
local P = require("scripts.pollution")
local R = {}
local function calm(world, surface, position)
  return world.planet == "nauvis" and P.calm(surface, position) or 0
end
local function distance2(a, b) return (a.x - b.x)^2 + (a.y - b.y)^2 end
local function cleanup(world)
  for i = #world.groups, 1, -1 do
    local entry = world.groups[i]
    if not entry.group.valid or game.tick - entry.created > 15 * 60 * 60 then
      if entry.group.valid then entry.group.destroy() end -- Release survivors to normal AI; do not delete enemies.
      table.remove(world.groups, i)
    end
  end
end
local function target(world)
  local best, priority
  for id in pairs(world.machine_ids) do
    local rec = S.root().machines[id]
    if rec and rec.entity.valid and rec.last_effect and game.tick - rec.last_effect < 2 * 60 * 60 then
      local def = K.by_machine[rec.entity.name]
      if def.fixed and not def.dirty and def.name ~= "pheromone-dampener" and calm(world, rec.entity.surface, rec.entity.position) < 1 then
        local score = (def.name == "sanctuary" and 3 or (def.name == "seed-disperser" and 2 or 1))
        if not best or score > priority or (score == priority and id < best.id) then best, priority = rec, score end
      end
    end
  end
  return best
end
local function nest_for(world, surface, rec)
  local nests = surface.find_entities_filtered({position = rec.entity.position, radius = 512, type = "unit-spawner", force = "enemy", limit = 32})
  table.sort(nests, function(a, b)
    local da, db = distance2(a.position, rec.entity.position), distance2(b.position, rec.entity.position)
    if da == db then return a.unit_number < b.unit_number end
    return da < db
  end)
  for _, nest in ipairs(nests) do
    -- No enemies materializing inside the player's factory. A cleared perimeter is a valid defense.
    if distance2(nest.position, rec.entity.position) >= 96^2 and calm(world, surface, nest.position) < 1 then return nest end
  end
end
local function species(world, evolution, index)
  if world.planet == "gleba" then
    local size = evolution >= 0.65 and "big" or (evolution >= 0.3 and "medium" or "small")
    local role = index % 5 == 0 and "stomper" or (index % 3 == 0 and "strafer" or "wriggler")
    -- Wrigglers only have small/medium variants in some game versions.
    local name = size .. "-" .. role .. "-pentapod"
    if not prototypes.entity[name] then name = "small-wriggler-pentapod" end
    return name
  end
  if evolution < 0.2 then return index % 4 == 0 and "small-spitter" or "small-biter" end
  if index % 4 == 0 then return "sn-blight-spitter" end
  if evolution >= 0.55 then return "sn-canopy-breaker" end
  return "sn-rootbreaker"
end
local function dispatch(world, surface)
  local pending = world.warning
  world.warning = nil
  local rec = S.root().machines[pending.target]
  local nest = pending.nest
  if not (rec and rec.entity.valid and nest.valid and rec.entity.surface.index == surface.index
    and rec.entity.force.index == pending.force_index and nest.force.name == "enemy") then
    world.next_raid_check = game.tick + 2 * 60 * 60
    return
  end
  if rec.entity.force.get_cease_fire("enemy") or rec.entity.force.get_friend("enemy") then return end
  local sedation = math.max(calm(world, surface, nest.position), calm(world, surface, rec.entity.position))
  if sedation >= 1 then world.sedated_waves = (world.sedated_waves or 0) + 1; return end
  if not rec.last_effect or game.tick - rec.last_effect > 2 * 60 * 60 then return end
  local aggressive = settings.global["sn-native-resistance"].value == "relentless"
  local size = math.min(C.max_wave, math.floor(6 + world.pressure * (aggressive and 0.4 or 0.25) + world.stage * 2))
  size = math.max(1, math.floor(size * (1 - sedation)))
  -- Pentapods are substantially stronger than biters; count them conservatively.
  if world.planet == "gleba" then size = math.max(3, math.floor(size / 3)) end
  local group = surface.create_unit_group({position = nest.position, force = nest.force})
  if not group then return end
  local recruited = 0
  local units = surface.find_entities_filtered({position = nest.position, radius = 80, type = "unit", force = nest.force, limit = size})
  table.sort(units, function(a, b) return a.unit_number < b.unit_number end)
  for _, unit in ipairs(units) do
    if unit.commandable and not unit.commandable.parent_group then group.add_member(unit); recruited = recruited + 1 end
  end
  local crowded = surface.count_entities_filtered({position = nest.position, radius = 128, type = "unit", force = nest.force, limit = 150}) >= 150
  local evolution = math.max(nest.force.get_evolution_factor(surface), world.stage * 0.12)
  if not crowded then
    for i = recruited + 1, size do
      local name = species(world, evolution, i)
      if prototypes.entity[name] then
        local position = surface.find_non_colliding_position(name, nest.position, 24, 1)
        if position and distance2(position, rec.entity.position) >= 64^2 then
          local unit = surface.create_entity({name = name, position = position, force = nest.force})
          if unit then group.add_member(unit); recruited = recruited + 1 end
        end
      end
    end
  end
  if recruited > 0 then
    group.set_command({type = defines.command.attack, target = rec.entity, distraction = defines.distraction.none})
    group.start_moving()
    world.groups[#world.groups + 1] = {group = group, created = game.tick, target = rec.id, nest_position = {x = nest.position.x, y = nest.position.y}}
    rec.entity.force.print({"sn-message.raid", {"space-location-name." .. world.planet}, recruited}, {color = C.colors.pressure})
  else group.destroy() end
  world.pressure = math.max(0, world.pressure - 22)
  world.last_raid = game.tick
  world.next_raid_check = game.tick + (aggressive and 4 or 8) * 60 * 60
end
function R.tick(world, surface)
  cleanup(world)
  if world.native_outcome then world.warning = nil; return end
  for _, entry in ipairs(world.groups) do
    local rec = entry.target and S.root().machines[entry.target]
    if not entry.retreated and rec and rec.entity.valid and entry.group.valid and entry.nest_position
      and calm(world, surface, rec.entity.position) >= 1 then
      entry.group.set_command({type = defines.command.go_to_location, destination = entry.nest_position, distraction = defines.distraction.none})
      entry.retreated = true
      world.sedated_waves = (world.sedated_waves or 0) + 1
    end
  end
  local mode = settings.global["sn-native-resistance"].value
  if not C.profiles[world.planet].native or mode == "off" or surface.peaceful_mode then world.warning = nil; return end
  if not world.first_operation or game.tick - world.first_operation < settings.global["sn-grace-minutes"].value * 60 * 60 then return end
  if world.warning then if game.tick >= world.warning.at then dispatch(world, surface) end; return end
  if game.tick < (world.next_raid_check or 0) or world.pressure < (mode == "relentless" and 20 or 30) or #world.groups >= C.max_active_groups then return end
  world.next_raid_check = game.tick + 30 * 60
  local rec = target(world)
  if not rec then return end
  -- Respect scenario diplomacy and other forces, rather than turning this into a PvP grief mechanic.
  if rec.entity.force.get_cease_fire("enemy") or rec.entity.force.get_friend("enemy") then return end
  local nest = nest_for(world, surface, rec)
  if not nest then return end
  local effective = world.pressure * (1 - math.max(calm(world, surface, rec.entity.position), calm(world, surface, nest.position)))
  if effective < (mode == "relentless" and 20 or 30) then return end
  world.warning = {at = game.tick + C.warning_ticks, target = rec.id, nest = nest, force_index = rec.entity.force.index}
  local p = rec.entity.position
  rec.entity.force.print({"sn-message.raid-warning", {"space-location-name." .. world.planet}, 45,
    "[gps=" .. math.floor(p.x) .. "," .. math.floor(p.y) .. "," .. surface.name .. "]"}, {color = C.colors.pressure})
end
return R
