-- No game globals, RNG or entity references in this module. All rates use minutes.
local C = require("shared.constants")
local M = {}
function M.clamp(n, lo, hi) return math.max(lo or 0, math.min(hi or 100, n)) end
function M.new(planet)
  local p = assert(C.profiles[planet], "Unknown restoration domain: " .. tostring(planet))
  local s = {planet = planet, values = {}, toxicity = p.toxicity, pressure = 0, ambient = 0,
    stage = 0, score = 0, cycles = 0, restored_tiles = 0, grown_trees = 0, removed_pollution = 0,
    contributions = {}, recent = {}, last_raid = 0, groups = {}}
  for _, key in ipairs(C.axes) do s.values[key] = p.initial[key] end
  M.refresh(s)
  return s
end
function M.air_ready(s)
  local air = s.air
  -- Pure-model simulations omit a surface; runtime records always have an air survey.
  return not air or (air.measured and air.survey_complete and air.total <= C.air.total_goal and air.peak <= C.air.green_limit)
end
function M.cap(s, axis)
  local v = s.values
  if axis == "water" then return math.min(100, v.atmosphere + 30, v.temperature + 35) end
  if axis == "soil" then return math.min(100, v.water + 35, 110 - s.toxicity * 0.4) end
  if axis == "biodiversity" then
    return M.clamp(math.min(v.atmosphere + 15, v.temperature + 20, v.water + 20, v.soil + 15, 100 - s.toxicity * 0.7, 100 - (s.air and s.air.mean or 0) * 0.5))
  end
  return 100
end
function M.refresh(s)
  local total = 0
  for _, key in ipairs(C.axes) do total = total + s.values[key] end
  s.score = total / #C.axes * (1 - s.toxicity * 0.004)
  s.stage = 0
  for index, stage in ipairs(C.stages) do
    local eligible = s.toxicity <= stage.max_toxicity
    for i, key in ipairs(C.axes) do eligible = eligible and s.values[key] >= stage.minimum[i] end
    if eligible and (index < #C.stages or M.air_ready(s)) then s.stage = index - 1 end
  end
end
function M.apply(s, effect, cycles, speed)
  if cycles <= 0 then return 0 end
  local p, total = C.profiles[s.planet], 0
  local scale = cycles * (speed or 1)
  s.toxicity = M.clamp(s.toxicity + (effect.toxicity or 0) * scale)
  for _, key in ipairs(C.axes) do
    local amount = (effect[key] or 0) * (p.gain[key] or 1) * scale
    local before = s.values[key]
    if amount > 0 then
      -- Never drop an existing value when adding a capped positive benefit.
      s.values[key] = math.max(before, math.min(M.cap(s, key), before + amount))
    else s.values[key] = M.clamp(before + amount) end
    total = total + math.max(0, s.values[key] - before) * (key == "biodiversity" and 1.7 or 1)
  end
  s.pressure = M.clamp(s.pressure + total * 0.7 + (effect.pressure or 0) * scale)
  s.cycles = s.cycles + cycles
  M.refresh(s)
  return total
end
function M.advance(s, seconds, speed)
  if not s.first_operation then return end -- No off-screen attrition on untouched worlds.
  local minutes = seconds / 60 * (speed or 1)
  local p = C.profiles[s.planet]
  local resilient = s.stage >= 4 and 0.25 or 1
  -- Local measured pollution/spores is a pressure on the ecosystem, not a second global pollution simulator.
  local exposure = math.min(4, math.max(0, s.ambient) / 150)
  s.toxicity = M.clamp(s.toxicity + (exposure * 0.12 - s.values.biodiversity / 100 * 0.028) * minutes)
  for _, key in ipairs(C.axes) do
    local extra = math.max(0, s.values[key] - M.cap(s, key)) * 0.015
    s.values[key] = M.clamp(s.values[key] - (p.erosion[key] * resilient + extra + (key == "atmosphere" and exposure * 0.02 or 0)) * minutes)
  end
  -- Pressure is adaptation to CHANGE. A mature, maintained world eventually quiets down.
  s.pressure = M.clamp(s.pressure - (s.stage >= 4 and 1.25 or 0.7) * minutes)
  M.refresh(s)
end
function M.requirements(s, stage_number)
  local stage = C.stages[math.min(#C.stages, stage_number + 1)]
  local missing = {}
  for i, key in ipairs(C.axes) do
    if s.values[key] < stage.minimum[i] then missing[#missing + 1] = {axis = key, target = stage.minimum[i]} end
  end
  if s.toxicity > stage.max_toxicity then missing[#missing + 1] = {axis = "toxicity", target = stage.max_toxicity} end
  if stage_number >= 5 and s.air and not M.air_ready(s) then
    missing[#missing + 1] = {axis = "smog", target = C.air.total_goal, less = true}
    missing[#missing + 1] = {axis = "hotspot", target = C.air.green_limit, less = true}
  end
  return missing
end
function M.ready(s) return s and s.stage == #C.stages - 1 and M.air_ready(s) end
-- Total produced is a monotonic engine counter. Recipe switches are intentionally conservative:
-- establish a new baseline rather than attributing the old recipe's work to a new one.
function M.completed(record, produced, recipe)
  local delta = 0
  if record.recipe == recipe and produced >= record.produced then delta = produced - record.produced end
  record.produced, record.recipe = produced, recipe
  return delta
end
return M
