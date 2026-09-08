local C = require("shared.constants")
local S = require("scripts.state")
local P = require("scripts.pollution")
local Artwork = require("scripts.artwork")
local Jukebox = require("scripts.jukebox")
local Campaign = {}
local function configure_freeplay()
  local api = remote.interfaces.freeplay
  if not api then return end
  for _, entry in ipairs({{"set_skip_intro", true}, {"set_disable_crashsite", true},
    {"set_created_items", {["sn-carbine"] = 1, ["sn-ballistic-magazine"] = 40, ["sn-field-armor"] = 1}},
    {"set_respawn_items", {["sn-carbine"] = 1, ["sn-ballistic-magazine"] = 10}}}) do
    if api[entry[1]] then
      local ok, err = pcall(remote.call, "freeplay", entry[1], entry[2])
      if not ok then log("Second Nature: freeplay setup deferred: " .. tostring(err)) end
    end
  end
end
function Campaign.init(fresh)
  local root = S.root()
  -- Never raze an existing save or grant a new cargo load during an update/reindex.
  root.campaign = root.campaign or {active = fresh and game.tick == 0 and
    settings.startup["sn-desolate-start"].value and remote.interfaces.freeplay ~= nil,
    camps = {}, arrivals = {}}
  if root.campaign.active then configure_freeplay() end
  for _, camp in pairs(root.campaign.camps) do Artwork.lander(camp) end
end
function Campaign.chunk(surface, position, area)
  local world = S.world(surface)
  if not world then return end
  local added = P.track(world, position.x, position.y)
  if not added or world.planet ~= "nauvis" or not S.root().campaign.active or world.native_outcome then return end
  local tiles = surface.find_tiles_filtered({area = area, name = {"grass-1", "grass-2", "grass-3", "grass-4"}})
  local changes = {}
  for _, tile in ipairs(tiles) do
    if not tile.hidden_tile then changes[#changes + 1] = {name = C.barren_tiles[tile.name], position = tile.position} end
  end
  if #changes > 0 then surface.set_tiles(changes, false, false, false, false) end
  for _, entity in ipairs(surface.find_entities_filtered({area = area, type = {"tree", "fish"}, force = "neutral"})) do
    entity.destroy({raise_destroy = true})
  end
  local smog = settings.startup["sn-legacy-smog"].value
  if smog > 0 and surface.pollutant_type then
    surface.pollute({position.x * 32 + 16, position.y * 32 + 16}, smog)
  end
end
function Campaign.arrive(player)
  local campaign = S.root().campaign
  if not campaign.active or S.planet(player.surface) ~= "nauvis" then return end
  configure_freeplay()
  if not campaign.arrivals[player.index] then campaign.arrivals[player.index] = {at = game.tick + 1} end
end
local function place(surface, force, name, position, radius)
  local pos = surface.find_non_colliding_position(name, position, radius or 12, 1)
  if not pos then return nil end
  return surface.create_entity({name = name, position = pos, force = force, raise_built = true})
end
function Campaign.land(force, surface)
  local camps = S.root().campaign.camps
  if camps[force.index] then Artwork.lander(camps[force.index]);return camps[force.index] end
  local spawn = force.get_spawn_position(surface)
  surface.request_to_generate_chunks(spawn, 2)
  surface.force_generate_chunk_requests()
  local ship = place(surface, force, "sn-lander", {x = spawn.x, y = spawn.y - 12}, 80)
  if not ship then return nil end -- Retry, rather than recording a phantom cargo grant.
  ship.destructible, ship.minable = false, false
  for _, item in ipairs(C.landing_cargo) do
    local count = ship.insert({name = item[1], count = item[2]})
    assert(count == item[2], "Second Nature: emergency cargo does not fit the lander")
  end
  local pos = ship.position
  local camp = {ship = ship, position = {x = pos.x, y = pos.y}, landed_at = game.tick, rocket_launched = false}
  camps[force.index] = camp
  for _, offset in ipairs({{-9,-5},{9,-5},{-9,6},{9,6}}) do
    local turret = place(surface, force, "sn-sentry-turret", {x = pos.x + offset[1], y = pos.y + offset[2]}, 8)
    if turret then turret.insert({name = "sn-mycelial-magazine", count = 60})
    else ship.insert({name = "sn-sentry-turret", count = 1}); ship.insert({name = "sn-mycelial-magazine", count = 60}) end
  end
  for _, side in ipairs({-1,1}) do
    for _, y in ipairs({-8,-7,-6,-5,-4,-3,4,5,6,7,8,9}) do
      local wall = place(surface, force, "sn-field-barricade", {x=pos.x+side*12,y=pos.y+y},2)
      if not wall then ship.insert({name="sn-field-barricade",count=1}) end
    end
  end
  camp.jukebox=place(surface,force,"sn-jukebox",{x=pos.x+4,y=pos.y+5},8)
  if not camp.jukebox then ship.insert({name="sn-jukebox",count=1}) end
  Artwork.lander(camp)
  force.chart(surface, {{pos.x - 64, pos.y - 64}, {pos.x + 64, pos.y + 64}})
  return camp
end
function Campaign.end_pan(player)
  local arrival = S.root().campaign.arrivals[player.index]
  if not arrival or not arrival.pan then return end
  arrival.pan = false
  if player.controller_type == defines.controllers.cutscene then player.exit_cutscene() end
  local label = player.gui.screen.sn_landing_skip
  if label then label.destroy() end
end
function Campaign.tick()
  local campaign = S.root().campaign
  if not campaign.active then return end
  for index, arrival in pairs(campaign.arrivals) do
    local player = game.get_player(index)
    if player and not arrival.done and game.tick >= arrival.at and S.planet(player.surface) == "nauvis" then
      local camp = Campaign.land(player.force, player.surface)
      if camp then
        arrival.done = true
        Jukebox.transmission(player)
        player.print({"sn-campaign.briefing"}, {color = C.colors.biodiversity})
        if player.character and player.controller_type == defines.controllers.character then
          arrival.pan, arrival.pan_until = true, game.tick + 240
          player.set_controller({type = defines.controllers.cutscene,
            start_position = {camp.position.x + 32, camp.position.y - 24}, start_zoom = 0.6,
            waypoints = {{position = camp.position, transition_time = 180, time_to_wait = 60, zoom = 1.3}}})
          player.gui.screen.add({type = "label", name = "sn_landing_skip", caption = {"", {"sn-campaign.landing-pan"}, "  ", {"skip-cutscene"}}})
        end
      end
    end
    if player and arrival.pan and game.tick >= arrival.pan_until then Campaign.end_pan(player) end
  end
end
function Campaign.rocket(event)
  local rocket = event.rocket
  if not (rocket and rocket.valid and S.planet(rocket.surface) == "nauvis") then return end
  local camp = S.root().campaign.camps[rocket.force.index]
  if camp and not camp.rocket_launched then
    camp.rocket_launched = true
    if camp.ship and camp.ship.valid then camp.ship.minable, camp.ship.destructible = false, false end
    rocket.force.print({"sn-campaign.orbit-restored"}, {color = C.colors.atmosphere})
  end
end
return Campaign
