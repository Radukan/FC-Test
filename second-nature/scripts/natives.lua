local C = require("shared.constants")
local S = require("scripts.state")
local Model = require("shared.model")
local Pollution = require("scripts.pollution")
local Achievements = require("scripts.achievements")
local N = {}
local native = {}
for _, name in ipairs(C.native_names) do native[name] = true end
function N.diplomacy()
  local force = game.forces["sn-symbiosis"]
  if not force then return end
  force.ai_controllable = false
  for _, other in pairs(game.forces) do
    if other.index ~= force.index then
      force.set_friend(other, true); other.set_friend(force, true)
      force.set_cease_fire(other, true); other.set_cease_fire(force, true)
    end
  end
end
local function friendly_force()
  local force = game.forces["sn-symbiosis"]
  if not force then force = game.create_force("sn-symbiosis"); N.diplomacy() end
  return force
end
local function transform(world, surface, entity)
  if not (entity and entity.valid and entity.surface.index == surface.index and entity.force.name == "enemy" and native[entity.name]) then return end
  local outcome, replacement = world.native_outcome
  if outcome.mode == "symbiosis" then
    replacement = surface.create_entity({name = entity.type == "unit" and "sn-bloomback" or "sn-bloom-nest",
      position = entity.position, force = friendly_force(), raise_built = false})
  end
  -- Do not silently eradicate an organism if creation of its friendly form failed.
  if outcome.mode == "eradication" or replacement then
    entity.destroy({raise_destroy = true})
    outcome.processed = outcome.processed + 1
  end
end
function N.available(world)
  return world and world.planet == "nauvis" and not world.native_outcome and Model.ready(world)
    and world.clean_since and game.tick - world.clean_since >= 2 * 60 * 60
end
function N.choose(world, mode, player)
  if mode ~= "symbiosis" and mode ~= "eradication" then return false end
  if player and game.is_multiplayer() and not player.admin then player.print({"sn-native.admin-only"}); return false end
  local surface = world and game.surfaces[world.surface_index]
  if surface then Pollution.sample(world, surface) end -- Fresh total at the irreversible decision.
  if not N.available(world) then if player then player.print({"sn-native.not-ready"}) end; return false end
  world.native_outcome = {mode = mode, at = game.tick, processed = 0, passes = 0, by = player and player.index or 0}
  world.warning = nil
  for _, entry in ipairs(world.groups) do
    if entry.group.valid then
      entry.group.set_command({type = defines.command.stop, distraction = defines.distraction.none})
      entry.group.destroy()
    end
  end
  world.groups = {}
  if mode == "symbiosis" then friendly_force() end
  -- A single decision-time index guarantees that mobile natives cannot outrun
  -- the terrain survey. LuaEntity references are save-safe and kept OUT of snapshots.
  world.native_queue = surface.find_entities_filtered({name = C.native_names, force = "enemy"})
  table.sort(world.native_queue, function(a, b) return a.unit_number > b.unit_number end)
  world.native_outcome.pending = #world.native_queue
  -- A planetary decision, credited to everyone who worked toward it.
  Achievements.award_world(world, mode == "symbiosis" and "common-ground" or "quiet-eden")
  if player then Achievements.award(player.force, mode == "symbiosis" and "common-ground" or "quiet-eden") end
  game.print({"sn-native.chosen-" .. mode}, {color = C.colors.biodiversity})
  return true
end
function N.tick(world)
  if world.planet ~= "nauvis" then return end
  if Model.ready(world) then world.clean_since = world.clean_since or game.tick else world.clean_since = nil end
  local setting = settings.global["sn-native-fate"].value
  if setting ~= "choose" and N.available(world) then N.choose(world, setting) end
  if world.native_outcome and world.native_queue then
    local surface = game.surfaces[world.surface_index]
    for _ = 1, math.min(32, #world.native_queue) do transform(world, surface, table.remove(world.native_queue)) end
    world.native_outcome.pending = #world.native_queue
    if #world.native_queue == 0 then world.native_queue = nil end
  end
end
function N.chunk(world, surface, chunk)
  if world.planet ~= "nauvis" or not world.native_outcome then return end
  local area = {{chunk.x * 32, chunk.y * 32}, {chunk.x * 32 + 32, chunk.y * 32 + 32}}
  local enemies = surface.find_entities_filtered({area = area, name = C.native_names, force = "enemy", limit = 32})
  table.sort(enemies, function(a, b) return a.unit_number < b.unit_number end)
  for _, entity in ipairs(enemies) do transform(world, surface, entity) end
  if world.air.cursor == #world.chunks then world.native_outcome.passes = world.native_outcome.passes + 1 end
end
function N.spawned(event)
  local entity = event.entity
  if not (entity and entity.valid and native[entity.name]) then return end
  local world = S.by_planet("nauvis")
  if world and world.native_outcome and world.surface_index == entity.surface.index then transform(world, entity.surface, entity) end
end
return N
