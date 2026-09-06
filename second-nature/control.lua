require("util") -- table.deepcopy is not preloaded in a mod's runtime environment.
local C = require("shared.constants")
local Model = require("shared.model")
local State = require("scripts.state")
local Machines = require("scripts.machines")
local Resistance = require("scripts.resistance")
local Network = require("scripts.network")
local Gui = require("scripts.gui")
local Pollution = require("scripts.pollution")
local Campaign = require("scripts.campaign")
local Natives = require("scripts.natives")
local function initialize(fresh)
  State.init()
  Campaign.init(fresh == true)
  -- Reconcile removed prototypes and invalid references before the install-only scan.
  local invalid = {}
  for id, rec in pairs(State.root().machines) do if not rec.entity.valid then invalid[#invalid + 1] = id end end
  table.sort(invalid)
  for _, id in ipairs(invalid) do State.remove(id) end
  State.scan()
  for _, planet in ipairs(C.planets) do
    local world = State.by_planet(planet)
    local surface = world and game.surfaces[world.surface_index]
    if surface then
      if fresh == true and State.root().campaign.active and planet == "nauvis" then
        for chunk in surface.get_chunks() do
          Campaign.chunk(surface, chunk, {{chunk.x * 32, chunk.y * 32}, {chunk.x * 32 + 32, chunk.y * 32 + 32}})
        end
      end
      Pollution.index(world, surface)
    end
  end
  Natives.diplomacy()
  Network.configure_victory()
  for _, player in pairs(game.players) do
    if player.gui.screen.sn_dashboard then Gui.close(player) end
    Gui.welcome(player)
  end
  State.root().last_environment_tick = game.tick
end
script.on_init(function() initialize(true) end)
script.on_configuration_changed(function() initialize(false) end)
-- No on_load mutations: all mutable state is in storage; all module upvalues are constants/functions.
local built = {}
for _, name in ipairs({"on_built_entity", "on_robot_built_entity", "script_raised_built", "script_raised_revive", "on_space_platform_built_entity"}) do
  if defines.events[name] then built[#built + 1] = defines.events[name] end
end
script.on_event(built, function(event) State.register(event.entity or event.created_entity) end)
local removing = {}
for _, name in ipairs({"on_pre_player_mined_item", "on_robot_pre_mined", "on_entity_died", "script_raised_destroy"}) do
  if defines.events[name] then removing[#removing + 1] = defines.events[name] end
end
script.on_event(removing, function(event) Machines.flush(event.entity) end)
script.on_event(defines.events.on_entity_cloned, function(event) State.register(event.destination) end)
script.on_event(defines.events.on_object_destroyed, function(event)
  local id = State.root().registrations[event.registration_number]
  if id then State.remove(id) end
end)
script.on_event(defines.events.on_surface_created, function(event)
  local surface = game.surfaces[event.surface_index]
  local world = State.world(surface)
  if world then Pollution.index(world, surface) end
end)
script.on_event(defines.events.on_chunk_generated, function(event)
  Campaign.chunk(event.surface, event.position, event.area)
  local world = State.world(event.surface)
  if world then Natives.chunk(world, event.surface, event.position) end
end)
script.on_event(defines.events.on_force_created, Natives.diplomacy)
script.on_event(defines.events.on_entity_spawned, Natives.spawned)
script.on_event(defines.events.on_biter_base_built, function(event)
  local entity = event.entity
  if entity and entity.valid then
    local world = State.world(entity.surface)
    if world then Natives.chunk(world, entity.surface, {x = math.floor(entity.position.x / 32), y = math.floor(entity.position.y / 32)}) end
  end
end)
script.on_event(defines.events.on_rocket_launched, Campaign.rocket)
script.on_event(defines.events.on_cutscene_cancelled, function(event)
  local player = game.get_player(event.player_index)
  if player then Campaign.end_pan(player) end
end)
script.on_event(defines.events.on_surface_deleted, function(event) State.delete_surface(event.surface_index) end)
script.on_event(defines.events.on_surface_cleared, function(event)
  State.delete_surface(event.surface_index)
  State.world(game.surfaces[event.surface_index])
end)
script.on_event(defines.events.on_forces_merged, function(event)
  Network.merge(event.source_index, event.destination.index)
  local camps = State.root().campaign.camps
  local source, destination = camps[event.source_index], camps[event.destination.index]
  if source and destination then
    destination.rocket_launched = destination.rocket_launched or source.rocket_launched
    if source.ship and source.ship.valid then source.ship.minable = true end
    if destination.rocket_launched and destination.ship and destination.ship.valid then destination.ship.minable = true end
  end
  camps[event.destination.index] = destination or source
  camps[event.source_index] = nil
  Natives.diplomacy()
end)
script.on_nth_tick(C.poll_ticks, Machines.tick)
script.on_nth_tick(C.environment_ticks, function()
  local root = State.root()
  Campaign.tick()
  Pollution.tick()
  local elapsed = game.tick - root.last_environment_tick
  root.last_environment_tick, root.visual_budget = game.tick, 20
  for _, planet in ipairs(C.planets) do
    local world = State.by_planet(planet)
    if world then
      local surface = game.surfaces[world.surface_index]
      if surface and surface.valid then
        if game.tick % (C.poll_ticks * C.bucket_count) == 0 then
          world.ambient = world.ambient * 0.8 + (world.sample_max or 0) * 0.2
          world.sample_max = 0
        end
        Model.advance(world, elapsed / 60, settings.global["sn-restoration-speed"].value)
        if world.stage ~= world.synced_stage then
          surface.set_property("sn-ecological-stage", world.stage)
          if world.stage > (world.highest_stage or 0) then
            world.highest_stage = world.stage
            game.print({"sn-message.milestone", {"space-location-name." .. planet}, {"sn-stage." .. C.stages[world.stage + 1].name}}, {color = C.colors.biodiversity})
          end
          world.synced_stage = world.stage
        end
        Natives.tick(world)
        Resistance.tick(world, surface)
      end
    end
  end
  Network.tick(elapsed)
end)
script.on_nth_tick(C.gui_ticks, function()
  for _, player in pairs(game.connected_players) do
    Gui.update(player)
    local prefs = State.root().players[player.index]
    if prefs and prefs.air_overlay then Pollution.overlay(player, true) end
  end
end)
script.on_event({defines.events.on_player_created, defines.events.on_player_joined_game}, function(event)
  local player = game.get_player(event.player_index)
  if player then State.world(player.surface); Gui.welcome(player); Campaign.arrive(player) end
end)
script.on_event(defines.events.on_player_removed, function(event) State.root().players[event.player_index] = nil end)
script.on_event(defines.events.on_gui_click, Gui.click)
script.on_event(defines.events.on_gui_selection_state_changed, Gui.selection)
script.on_event(defines.events.on_gui_closed, function(event)
  local player = game.get_player(event.player_index)
  if player and event.element and event.element.valid and event.element.name == "sn_dashboard" then Gui.close(player) end
end)
script.on_event(defines.events.on_lua_shortcut, function(event)
  if event.prototype_name == "sn-dashboard" then Gui.toggle(game.get_player(event.player_index))
  elseif event.prototype_name == "sn-pollution-overlay" then Gui.toggle_overlay(game.get_player(event.player_index)) end
end)
script.on_event("sn-toggle-pollution", function(event) Gui.toggle_overlay(game.get_player(event.player_index)) end)
script.on_event("sn-toggle-dashboard", function(event) Gui.toggle(game.get_player(event.player_index)) end)
script.on_event(defines.events.on_runtime_mod_setting_changed, function(event)
  if event.setting == "sn-native-fate" then
    local world = State.by_planet("nauvis")
    if world then Natives.tick(world) end
  end
  if event.setting == "sn-network-victory" then Network.configure_victory() end
  if event.setting == "sn-living-terrain" and not settings.global["sn-living-terrain"].value then rendering.clear("second-nature") end
end)
commands.add_command("second-nature", {"sn-command.dashboard"}, function(command)
  local player = command.player_index and game.get_player(command.player_index)
  if player then Gui.toggle(player) else log("Second Nature: use /sn-status for a server-readable planetary report.") end
end)
commands.add_command("sn-status", {"sn-command.status"}, function(command)
  local player = command.player_index and game.get_player(command.player_index)
  for _, planet in ipairs(C.planets) do
    local world = State.by_planet(planet)
    local line = world and string.format("[Second Nature] %s: %s | stability %.1f | toxicity %.1f | resistance %.1f | cycles %d",
      planet, C.stages[world.stage + 1].name, world.score, world.toxicity, world.pressure, world.cycles) or ("[Second Nature] " .. planet .. ": unvisited")
    if player then player.print(line) else log(line) end
  end
end)
commands.add_command("sn-reindex", {"sn-command.reindex"}, function(command)
  local player = command.player_index and game.get_player(command.player_index)
  if player and not player.admin then player.print({"sn-message.admin-only"}); return end
  initialize()
  if player then player.print({"sn-message.reindexed"}) else log("Second Nature: machine index reconciled.") end
end)
remote.add_interface("second_nature", {
  get_world = State.snapshot,
  get_profiles = function() return table.deepcopy(C.profiles) end,
  get_network = function(force_index)
    local n = State.root().networks[force_index]
    return n and {held_ticks = n.held, won = n.won, reason = table.deepcopy(n.reason)} or nil
  end,
  register_entity = function(entity) State.register(entity) end
})
