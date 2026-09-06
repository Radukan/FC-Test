-- Time-integrated local ecology, independent of rendering and the engine.
local C = require("shared.constants")
local M = require("shared.model")
local T = {}
function T.target(world)
  local v = world.values
  return M.clamp(math.min(v.soil, v.biodiversity + 10, v.water + 10) / 100, 0, 1)
end
function T.advance(chunk, world, pollution, minutes, bonus, broods)
  minutes = math.min(math.max(0, minutes), C.pace.maximum_sample_minutes)
  local stress_target = M.clamp((pollution - C.air.green_limit) / (C.air.sedation - C.air.green_limit), 0, 1)
  if broods then stress_target = math.max(.6, stress_target) end
  local stress = chunk.stress or 0
  local stress_step = minutes / C.pace.stress_minutes
  chunk.stress = stress + M.clamp(stress_target - stress, -stress_step, stress_step)
  local target = T.target(world) * (1 - chunk.stress)
  if pollution > C.air.green_limit then target = math.min(target, chunk.cover or 0) end
  if pollution >= C.air.wilt_limit or broods then target = 0 end
  local cover = chunk.cover or 0
  local grow = minutes / C.pace.growth_minutes * math.min(1.45, bonus or 1)
  local loss = minutes / C.pace.loss_minutes * math.max(.25, chunk.stress)
  chunk.cover = M.clamp(cover + M.clamp(target - cover, -loss, grow), 0, 1)
  return chunk.cover
end
function T.tile(x,y,cover,original)
  -- Stable clustered patches rather than checkerboard/random terrain writes.
  local hash = (math.floor(x/5)*92821 + math.floor(y/5)*68917) % 104729
  local threshold = (hash % 1000) / 1000
  if threshold < cover then
    if cover >= .72 then return "grass-1" elseif cover >= .48 then return "grass-2"
    elseif cover >= .24 then return "grass-3" else return "grass-4" end
  end
  return C.barren_tiles[original] or original
end
return T
