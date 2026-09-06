local C = require("shared.constants")
local S = require("scripts.state")
local Model = require("shared.model")
local N = {}
function N.diplomacy()
  local force = game.forces["sn-symbiosis"]
  if not force then return end
  force.ai_controllable = false -- No expansion or combat groups; these are peaceful grazers.
  for _, other in pairs(game.forces) do
    if other.index ~= force.index then
      force.set_friend(other, true); other.set_friend(force, true)
      force.set_cease_fire(other, true); other.set_cease_fire(force, true)
    end
  end
end
local function friendly_force()
  local force = game.forces["sn-symbiosis"] or game.create_force("sn-symbiosis")
  N.diplomacy()
  return force
end
function N.available(world)
  return world and world.planet == "nauvis" and not world.native_outcome and Model.ready(world)
    and world.clean_since and game.tick - world.clean_since >= 2 * 60 * 60
end
function N.choose(world, mode, player)
  if mode ~= "symbiosis" and mode ~= "eradication" then return false end
  if player and game.is_multiplayer() and not player.admin then player.print({"sn-native.admin-only"}); return false end
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
  game.print({"sn-native.chosen-" .. mode}, {color = C.colors.biodiversity})
  return true
end
function N.tick(world)
  if world.planet ~= "nauvis" then return end
  if Model.ready(world) then world.clean_since = world.clean_since or game.tick else world.clean_since = nil end
  local setting = settings.global["sn-native-fate"].value
  if setting ~= "choose" and N.available(world) then N.choose(world, setting) end
end
function N.chunk(world, surface, chunk)
  if world.planet ~= "nauvis" or not world.native_outcome then return end
  local outcome = world.native_outcome
  local area = {{chunk.x * 32, chunk.y * 32}, {chunk.x * 32 + 32, chunk.y * 32 + 32}}
  -- Sweeps are bounded, repeatable and include mobile units, nests and worms.
  -- Future generated chunks go through the same permanent world policy.
  local enemies = surface.find_entities_filtered({area = area, name = C.native_names, force = "enemy", limit = 32})
  table.sort(enemies, function(a, b) return a.unit_number < b.unit_number end)
  local friend = outcome.mode == "symbiosis" and (game.forces["sn-symbiosis"] or friendly_force())
  for _, entity in ipairs(enemies) do
    if entity.valid then
      local replacement
      if outcome.mode == "symbiosis" then
        replacement = surface.create_entity({name = entity.type == "unit" and "sn-bloomback" or "sn-bloom-nest",
          position = entity.position, force = friend, raise_built = false})
      end
      if outcome.mode == "eradication" or replacement then
        entity.destroy({raise_destroy = true})
        outcome.processed = outcome.processed + 1
      end
    end
  end
  if world.air.cursor == #world.chunks then outcome.passes = outcome.passes + 1 end
end
return N
