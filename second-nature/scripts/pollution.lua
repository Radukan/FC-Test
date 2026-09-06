local C = require("shared.constants")
local S = require("scripts.state")
local Model = require("shared.model")
local P = {}
function P.ensure(world)
  world.chunks = world.chunks or {}
  world.chunk_keys = world.chunk_keys or {}
  world.air = world.air or {total = 0, mean = 0, peak = 0, trend = 0, dirty = 0, measured = false,
    survey_complete = false, cursor = 0, scan_peak = 0, scan_dirty = 0, scan_count = 0, sampled_at = -C.air.sample_ticks}
end
function P.track(world, x, y)
  P.ensure(world)
  local key = x .. ":" .. y
  if world.chunk_keys[key] then return false end
  world.chunk_keys[key] = #world.chunks + 1
  world.chunks[#world.chunks + 1] = {x = x, y = y, stripe = 0}
  world.air.survey_complete = false
  return true
end
function P.index(world, surface)
  P.ensure(world)
  -- One install/configuration scan. Iterators themselves must NEVER enter storage.
  for chunk in surface.get_chunks() do
    -- The iterator also includes pollution-only / not-yet-generated chunks.
    if surface.is_chunk_generated(chunk) then P.track(world, chunk.x, chunk.y) end
  end
  P.sample(world, surface)
end
function P.local_amount(surface, position)
  return surface.pollutant_type and surface.get_pollution(position) or 0
end
function P.calm(surface, position)
  if not settings.startup["sn-biter-metabolism"].value then return 0 end
  return math.min(1, P.local_amount(surface, position) / C.air.sedation)
end
function P.sample(world, surface)
  P.ensure(world)
  local air = world.air
  local total = surface.pollutant_type and surface.get_total_pollution() or 0
  if air.measured and game.tick > air.sampled_at then
    air.trend = (total - air.total) * 3600 / (game.tick - air.sampled_at)
  end
  air.total, air.mean, air.measured, air.sampled_at = total, total / math.max(1, #world.chunks), true, game.tick
  if #world.chunks == 0 then air.survey_complete, air.peak = true, 0 end
  Model.refresh(world)
end
local function finish_survey(world)
  local air = world.air
  air.peak, air.dirty, air.surveyed_at = air.scan_peak, air.scan_dirty, game.tick
  air.survey_complete = air.scan_count >= #world.chunks
  air.scan_count, air.scan_peak, air.scan_dirty = 0, 0, 0
  Model.refresh(world)
end
function P.step(world, surface)
  P.ensure(world)
  local air, list = world.air, world.chunks
  if game.tick - air.sampled_at >= C.air.sample_ticks then P.sample(world, surface) end
  if #list == 0 then return end
  air.cursor = air.cursor + 1
  if air.cursor > #list then air.cursor = 1 end
  local chunk = list[air.cursor]
  if not surface.is_chunk_generated({chunk.x, chunk.y}) then
    world.chunk_keys[chunk.x .. ":" .. chunk.y] = nil
    local last = list[#list]
    list[air.cursor] = last
    list[#list] = nil
    if air.cursor <= #list then world.chunk_keys[last.x .. ":" .. last.y] = air.cursor end
    air.cursor = air.cursor - 1 -- Visit the swapped tail next; don't restart the whole planet.
    if air.cursor == #list then finish_survey(world) end
    return
  end
  local amount = P.local_amount(surface, {x = chunk.x * 32 + 16, y = chunk.y * 32 + 16})
  chunk.pollution = amount
  air.scan_peak = math.max(air.scan_peak, amount)
  if amount > C.air.green_limit then air.scan_dirty = air.scan_dirty + 1 end
  air.scan_count = air.scan_count + 1
  if air.cursor == #list then
    finish_survey(world)
  end
  return chunk, amount
end
function P.tick()
  local visits = {}
  local root = S.root()
  -- Four chunk visits TOTAL per second, round-robin over visited worlds.
  root.air_world_cursor = root.air_world_cursor or 0
  for _ = 1, C.air.chunk_budget do
    local world
    for _ = 1, #C.planets do
      root.air_world_cursor = root.air_world_cursor % #C.planets + 1
      world = S.by_planet(C.planets[root.air_world_cursor])
      if world then break end
    end
    local surface = world and game.surfaces[world.surface_index]
    if world and surface and surface.valid then
      local chunk, amount = P.step(world, surface)
      if chunk then
        visits[#visits + 1] = {world = world, surface = surface, chunk = chunk, pollution = amount}
      end
    end
  end
  return visits
end
function P.overlay(player, enabled)
  local prefs = S.root().players[player.index]
  if not prefs then return end
  for _, object in ipairs(prefs.air_render or {}) do if object.valid then object.destroy() end end
  prefs.air_render = {}
  if not enabled or not S.planet(player.surface) then return end
  local x, y = math.floor(player.position.x / 32), math.floor(player.position.y / 32)
  for dx = -2, 2 do for dy = -2, 2 do
    local cx, cy = x + dx, y + dy
    if player.surface.is_chunk_generated({cx, cy}) then
      local amount = P.local_amount(player.surface, {cx * 32 + 16, cy * 32 + 16})
      local color = amount <= C.air.green_limit and {0.15, 0.75, 0.5, 0.11}
        or (amount >= C.air.sedation and {0.70, 0.28, 0.60, 0.22} or {0.93, 0.48, 0.12, 0.18})
      prefs.air_render[#prefs.air_render + 1] = rendering.draw_rectangle({surface = player.surface,
        left_top = {cx * 32, cy * 32}, right_bottom = {cx * 32 + 32, cy * 32 + 32},
        color = color, filled = true, draw_on_ground = true, players = {player.index}, time_to_live = C.gui_ticks + 30})
    end
  end end
end
return P
