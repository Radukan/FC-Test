-- Unmodified runtime module copies run in THIS test mod's isolated storage,
-- against real engine surfaces/entities. No debug/mutation API ships in Second Nature.
local C = require("shared.constants")
local S = require("scripts.state")
local Campaign = require("scripts.campaign")
local Pollution = require("scripts.pollution")
local Model = require("shared.model")
local Natives = require("scripts.natives")
local Resistance = require("scripts.resistance")
local Inserters = require("scripts.inserters")
local Jukebox = require("scripts.jukebox")
local Ports = require("shared.fluid_ports")
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
  assert(force.recipes["small-electric-pole"].enabled, "wood-free poles not available")
  for _, name in ipairs({"small-electric-pole","wooden-chest","shotgun","combat-shotgun","sn-seed-mix"}) do
    for _, ingredient in pairs(force.recipes[name].ingredients) do assert(ingredient.name ~= "wood", name .. " still needs wood") end
  end
  local turrets = surface.find_entities_filtered({name = "sn-sentry-turret", force = force})
  assert(#turrets == 4, "deployed starter turrets")
  for _, turret in ipairs(turrets) do assert(turret.get_item_count("sn-mycelial-magazine") == 60) end
  Campaign.init(false)
  assert(Campaign.land(force, surface).ship == camp.ship, "configuration changed landing identity")
  -- Exercise the rocket handler's shared LuaEntity API; this is NOT a rocket flight test.
  Campaign.rocket({rocket = camp.ship})
  assert(not camp.ship.minable and not camp.ship.destructible and camp.rocket_launched)

  surface.clear_pollution()
  Pollution.sample(world, surface)
  for _ = 1, #world.chunks do Pollution.step(world, surface) end
  for _, axis in ipairs(C.axes) do world.values[axis] = 100 end
  world.toxicity, world.clean_since = 0, game.tick - 7200
  world.landscape = {mean = 1, measured = true, samples = #world.chunks}
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
  -- All three combat tiers and their real item/prototype contracts.
  local weapons = {{"sn-sentry-turret","sn-ballistic-magazine"},{"sn-arc-turret"},{"sn-lance-turret","sn-lance-cell"}}
  for i, entry in ipairs(weapons) do
    local entity = assert(surface.create_entity({name=entry[1],position={-28+i*10,32},force=force}))
    if entry[2] then assert(entity.insert({name=entry[2],count=10})==10,entry[1].." rejects ammo") end
  end
  for i, name in ipairs({"sn-field-barricade","sn-composite-wall"}) do
    assert(surface.create_entity({name=name,position={-12+i*2,40},force=force}))
  end
  local character = assert(surface.create_entity({name="character",position={-20,32},force=force}))
  assert(character.insert({name="sn-carbine",count=1})==1)
  assert(character.insert({name="sn-induction-rifle",count=1})==1)
  assert(character.insert({name="sn-lance-rifle",count=1})==1)
  assert(character.insert({name="sn-field-dressing",count=5})==5)
  -- Native vector setters, blueprints, belts and sound-note controls.
  local operator={force=force,admin=true,index=999,print=function(text) log(serpent.line(text)) end}
  local inserter=assert(surface.create_entity({name="sn-vector-inserter",position={40,40},force=force}))
  assert(Inserters.set(operator,inserter,"pickup",2,-2))
  assert(Inserters.set(operator,inserter,"drop",-2,2))
  assert(inserter.pickup_position.x==inserter.position.x+2 and inserter.drop_position.y==inserter.position.y+2)
  assert(not Inserters.set(operator,inserter,"pickup",3,0))
  local inventory=game.create_inventory(1);local blueprint=inventory[1]
  blueprint.set_stack({name="blueprint",count=1})
  blueprint.create_blueprint({surface=surface,force=force,area={{39.4,39.4},{40.6,40.6}}})
  local entities=blueprint.get_blueprint_entities()
  assert(entities and #entities==1 and entities[1].pickup_position and entities[1].drop_position,"custom vectors missing from blueprint")
  local pickup,drop=entities[1].pickup_position,entities[1].drop_position
  assert((pickup.x or pickup[1])==2 and (drop.y or drop[2])==2,"blueprint vectors: "..serpent.line(entities[1]))
  inventory.destroy()
  for i,name in ipairs({"sn-canopy-inserter","sn-vital-belt","sn-vital-underground-belt","sn-vital-splitter"}) do
    assert(surface.create_entity({name=name,position={44+i*4,40},force=force}))
  end
  local jukebox=assert(camp.jukebox,"landing jukebox missing")
  assert(Jukebox.play(operator,jukebox,2,false),"anthem note unavailable")
  assert(Jukebox.play(operator,jukebox,0,false),"jukebox stop note unavailable")
  -- Physical pipe connectivity and the shared visible boundary in all four rotations.
  local first_port=Ports["air-scrubber"][1]
  for quarter=0,3 do
    local machine=assert(surface.create_entity({name="sn-air-scrubber",position={-40+quarter*10,52},direction=quarter*4,force=force}))
    local angle=quarter*math.pi/2;local c,s=math.cos(angle),math.sin(angle)
    local function world(x,y) return {x=machine.position.x+x*c-y*s,y=machine.position.y+x*s+y*c} end
    local external=world(first_port.position[1],first_port.position[2]-1)
    local pipe=assert(surface.create_entity({name="pipe",position=external,force=force}))
    local connections=machine.fluidbox.get_pipe_connections(1)
    assert(connections[1] and connections[1].target,"pipe did not attach to rotated input")
    local expected=world(first_port.position[1],first_port.position[2]-.5)
    local a,b=connections[1].position,connections[1].target_position
    local actual={x=(a.x+b.x)/2,y=(a.y+b.y)/2}
    assert(math.abs(actual.x-expected.x)<.001 and math.abs(actual.y-expected.y)<.001,"connector boundary: "..serpent.line(connections[1]))
    pipe.destroy();machine.destroy()
  end
  -- The scene has a native hero track; headless cannot verify audible playback.
  log("SECOND_NATURE_ENGINE_LOGISTICS_AUDIO_OK")
  log("SECOND_NATURE_ENGINE_CAMPAIGN_PROBES_OK")
end
return Probe
