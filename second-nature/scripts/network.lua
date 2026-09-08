local C = require("shared.constants")
local Model = require("shared.model")
local S = require("scripts.state")
local N = {}
function N.has_beacon(world, force_index)
  if not world then return false end
  for id in pairs(world.beacon_ids) do
    local rec = S.root().machines[id]
    if rec and rec.entity.valid and rec.entity.force.index == force_index and rec.last_effect
      and game.tick - rec.last_effect <= C.beacon_freshness then return true end
  end
  return false
end
function N.status(force)
  local tech = force.technologies["sn-living-worlds"]
  if not tech or not tech.researched then return false, {"sn-gui.research-goal"} end
  for _, planet in ipairs(C.planets) do
    local world = S.by_planet(planet)
    if not world then return false, {"sn-gui.network-unvisited", {"space-location-name." .. planet}} end
    if not Model.ready(world) then return false, {"sn-gui.network-restore", {"space-location-name." .. planet}} end
    if not N.has_beacon(world, force.index) then return false, {"sn-gui.network-supply", {"space-location-name." .. planet}} end
  end
  return true, {"sn-gui.network-holding"}
end
function N.configure_victory()
  local root = S.root()
  if not (remote.interfaces.space_finish_script and remote.interfaces.space_finish_script.set_no_victory
    and remote.interfaces.space_finish_script.get_no_victory) then return end
  if settings.global["sn-network-victory"].value then
    if not root.victory_override then
      root.previous_no_victory = remote.call("space_finish_script", "get_no_victory")
      root.victory_override = true
    end
    remote.call("space_finish_script", "set_no_victory", true)
  elseif root.victory_override then
    remote.call("space_finish_script", "set_no_victory", root.previous_no_victory or false)
    root.victory_override = false
  end
end
function N.tick(ticks)
  local forces = {}
  for _, force in pairs(game.forces) do if force.technologies["sn-living-worlds"] then forces[#forces + 1] = force end end
  table.sort(forces, function(a, b) return a.index < b.index end)
  for _, force in ipairs(forces) do
    local network = S.root().networks[force.index] or {held = 0, won = false}
    S.root().networks[force.index] = network
    local ready, reason = N.status(force)
    network.reason = reason
    if not network.won then
      if ready and settings.global["sn-network-victory"].value then network.held = math.min(C.victory_ticks, network.held + ticks)
      else
        if network.held > 0 then force.print({"sn-message.network-interrupted", reason}, {color = C.colors.temperature}) end
        network.held = 0
      end
      if network.held >= C.victory_ticks then
        network.won = true
        force.print({"sn-message.victory"}, {color = C.colors.biodiversity})
        game.reset_game_state()
        game.set_game_state({game_finished = true, player_won = true, can_continue = true, victorious_force = force})
      end
    end
  end
end
function N.merge(source, destination)
  for _, world in pairs(S.root().worlds) do
    world.contributions[destination] = (world.contributions[destination] or 0) + (world.contributions[source] or 0)
    world.contributions[source] = nil
    world.recent[destination] = math.max(world.recent[destination] or 0, world.recent[source] or 0)
    world.recent[source] = nil
  end
  S.root().networks[source] = nil
  -- Merging cannot inherit partial timers or award victory by combining incomplete networks.
  if S.root().networks[destination] then S.root().networks[destination].held = 0 end
end
return N
