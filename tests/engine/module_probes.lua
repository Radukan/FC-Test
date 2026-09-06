-- Unmodified runtime module copies run in THIS test mod's isolated storage,
-- against real engine surfaces/entities. No debug/mutation API ships in Second Nature.
local C = require("shared.constants")
local S = require("scripts.state")
local Campaign = require("scripts.campaign")
local Pollution = require("scripts.pollution")
local Model = require("shared.model")
local Natives = require("scripts.natives")
local Resistance = require("scripts.resistance")
local Probe = {}
function Probe.run(surface, force)
  S.init()
  Campaign.init(true)
  assert(S.root().campaign.active, "new freeplay landing was not enabled")
  local world = S.world(surface)
  Pollution.index(world, surface)
  assert(#world.chunks > 0 and world.air.measured, "real chunk/pollution survey did not initialize")
  assert(surface.count_entities_filtered({type = {"tree", "fish"}}) == 0, "desolate Nauvis contains generated trees/fish")
  local camp = assert(Campaign.land(force, surface), "real lander placement failed")
  assert(not camp.ship.minable and not camp.ship.destructible)
  assert(camp.ship.get_item_count("iron-plate") == 200, "lander inventory grant")
  assert(Campaign.land(force, surface).ship == camp.ship, "landing is not idempotent")
  local turrets = surface.find_entities_filtered({name = "gun-turret", force = force})
  assert(#turrets == 2, "deployed starter turrets")
  for _, turret in ipairs(turrets) do assert(turret.get_item_count("firearm-magazine") == 75) end
  Campaign.init(false)
  assert(Campaign.land(force, surface).ship == camp.ship, "configuration changed landing identity")
  -- Exercise the rocket handler's shared LuaEntity API; this is NOT a rocket flight test.
  Campaign.rocket({rocket = camp.ship})
  assert(camp.ship.minable and camp.rocket_launched)

  surface.clear_pollution()
  Pollution.sample(world, surface)
  for _ = 1, #world.chunks do Pollution.step(world, surface) end
  for _, axis in ipairs(C.axes) do world.values[axis] = 100 end
  world.toxicity, world.clean_since = 0, game.tick - 7200
  Model.refresh(world)
  assert(Model.ready(world), "clean mature probe world: stage=" .. world.stage .. " air=" .. serpent.line(world.air))
  local biter = assert(surface.create_entity({name = "small-biter", position = {45, 16}, force = "enemy"}))
  local nest = assert(surface.create_entity({name = "biter-spawner", position = {52, 16}, force = "enemy"}))
  assert(Natives.choose(world, "symbiosis"))
  for _ = 1, math.ceil(#world.native_queue / 32) do Natives.tick(world) end
  assert(not biter.valid and not nest.valid, "native conversion queue did not consume originals")
  assert(surface.count_entities_filtered({name = "sn-bloomback"}) > 0)
  assert(surface.count_entities_filtered({name = "sn-bloom-nest"}) > 0)
  local friend = game.forces["sn-symbiosis"]
  assert(friend and friend.get_friend(force) and force.get_friend(friend), "asymmetric friendly diplomacy")
  assert(not game.forces.enemy.get_friend(force), "symbiosis allied the enemy force with players")
  assert(not Natives.choose(world, "eradication"), "native fate was reversible")

  -- A separate test case in isolated state, not a production reset operation.
  world.native_outcome, world.native_queue = nil, nil
  local worm = assert(surface.create_entity({name = "small-worm-turret", position = {60, 16}, force = "enemy"}))
  assert(Natives.choose(world, "eradication"))
  Natives.tick(world)
  assert(not worm.valid, "eradication left a worm")
  local new_biter = assert(surface.create_entity({name = "small-biter", position = {60, 20}, force = "enemy"}))
  Natives.spawned({entity = new_biter})
  assert(not new_biter.valid, "future spawned native escaped the chosen policy")
  -- Actual commandables: warn, dispatch specifically at a cleaner, then retreat.
  world.native_outcome, world.native_queue = nil, nil
  surface.peaceful_mode = false
  surface.request_to_generate_chunks({128, 0}, 1); surface.force_generate_chunk_requests()
  surface.clear_pollution()
  local target = assert(surface.create_entity({name = "sn-air-scrubber", position = {0, 0}, force = force}))
  local dirty = assert(surface.create_entity({name = "sn-forcing-tower", position = {0, 8}, force = force}))
  local target_record, dirty_record = S.register(target), S.register(dirty)
  target_record.last_effect, dirty_record.last_effect = game.tick, game.tick
  local raid_nest = assert(surface.create_entity({name = "biter-spawner", position = {128, 0}, force = "enemy"}))
  world.stage, world.pressure, world.first_operation, world.next_raid_check = 2, 80, game.tick - 72001, 0
  Resistance.tick(world, surface)
  assert(world.warning and world.warning.target == target.unit_number, "raid did not choose the clean machine")
  world.warning.at = game.tick
  Resistance.tick(world, surface)
  assert(#world.groups == 1 and #world.groups[1].group.members > 0, "real native group dispatch failed")
  surface.pollute(target.position, 220)
  Resistance.tick(world, surface)
  assert(world.groups[1].retreated, "real raid did not retreat under pollution")
  local group = world.groups[1].group
  for _, unit in ipairs(group.members) do if unit.valid then unit.destroy() end end
  if group.valid then group.destroy() end
  target.destroy(); dirty.destroy(); raid_nest.destroy()
  surface.clear_pollution(); surface.peaceful_mode = true
  log("SECOND_NATURE_ENGINE_CAMPAIGN_PROBES_OK")
end
return Probe
