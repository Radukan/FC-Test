local C = require("shared.constants")
local K = require("shared.catalog")
local Model = require("shared.model")
local S = require("scripts.state")
local Terrain = require("scripts.terrain")
local Telemetry = require("scripts.telemetry")
local Upgrades = require("scripts.upgrades")
local Artwork = require("scripts.artwork")
local Machines = {}
local max_retort_toxicity = 0
for _, recipe in ipairs(K.recipes) do
  if recipe.category == "sn-pyrolysis" and recipe.effects then
    max_retort_toxicity = math.max(max_retort_toxicity, recipe.effects.toxicity or 0)
  end
end
local function process(rec, world)
  local entity = rec.entity
  if rec.monitor then
    Telemetry.update(entity, world)
    if not (rec.status_light and rec.status_light.valid) then rec.status_light = Artwork.monitor(entity) end
    return
  end
  local recipe_name = S.recipe(entity)
  local produced = entity.products_finished
  local raw_cycles = math.max(0, produced - rec.produced)
  local cycles = Model.completed(rec, produced, recipe_name)
  if raw_cycles > 0 then rec.last_cycle = game.tick end
  S.active(rec, rec.last_cycle > 0 and game.tick - rec.last_cycle <= 60 * 60)
  local has_pollutant = entity.surface.pollutant_type ~= nil
  world.sample_max = math.max(world.sample_max or 0, has_pollutant and entity.surface.get_pollution(entity.position) or 0)
  local recipe = K.by_recipe[recipe_name]
  local definition = K.by_machine[entity.name]
  if definition.dirty and not definition.fixed and raw_cycles > cycles then
    -- Recipe switching must not launder pollution debt. Ambiguous retort batches
    -- get the highest native retort cost, never a positive restoration benefit.
    recipe = {effects = {toxicity = max_retort_toxicity}}
    cycles = raw_cycles
  end
  if not recipe or not recipe.effects or cycles <= 0 then return end
  -- Defend the runtime as well as the prototypes against recipe injection by other mods.
  if recipe.planet and recipe.planet ~= world.planet then return end
  if recipe.stage and world.stage < recipe.stage then return end
  world.first_operation = world.first_operation or game.tick
  local bonus = definition.dirty and 1 or Upgrades.bonus(entity.force)
  if not definition.dirty then
    world.last_clean_operation = game.tick
    if not world.terrain_bonus_until or game.tick >= world.terrain_bonus_until then world.terrain_bonus = bonus
    else world.terrain_bonus = math.max(world.terrain_bonus or 1, bonus) end
    world.terrain_bonus_until = game.tick + 10 * 60 * 60
  end
  local effects = recipe.effects
  if has_pollutant and entity.surface.get_pollution(entity.position) > C.air.green_limit then
    effects = table.deepcopy(effects)
    -- Inputs still become samples/waste, but living gains require clean local air.
    if (effects.soil or 0) > 0 then effects.soil = 0 end
    if (effects.biodiversity or 0) > 0 then effects.biodiversity = 0 end
  end
  Model.apply(world, effects, cycles, settings.global["sn-restoration-speed"].value * bonus)
  local force_index = entity.force.index
  world.contributions[force_index] = (world.contributions[force_index] or 0) + cycles
  world.recent[force_index] = game.tick
  rec.last_effect = game.tick
  local pollution = (recipe.effects.pollution or 0) * cycles
  if has_pollutant and pollution < 0 then
    local removed = math.min(entity.surface.get_pollution(entity.position), -pollution * C.pace.pollution_capture * bonus)
    if removed > 0 then entity.surface.pollute(entity.position, -removed, entity.name) end
    world.removed_pollution = world.removed_pollution + removed
  elseif has_pollutant and pollution > 0 then entity.surface.pollute(entity.position, pollution, entity.name) end
  Terrain.apply(rec, world, recipe.effects, cycles)
end
function Machines.flush(entity)
  if not (entity and entity.valid and entity.unit_number) then return end
  local rec = S.root().machines[entity.unit_number]
  local world = rec and S.root().worlds[rec.surface_index]
  if rec and world and entity.surface.index == rec.surface_index then process(rec, world) end
end
function Machines.tick()
  local root = S.root()
  root.cursor = root.cursor % C.bucket_count + 1
  local list = root.buckets[root.cursor]
  local index = 1
  while index <= #list do
    local rec = root.machines[list[index]]
    if rec and rec.entity.valid then
      -- Teleportation, cloning and force changes must not attribute work to an old planet.
      if rec.surface_index ~= rec.entity.surface.index then
        local entity = rec.entity; S.remove(rec.id); S.register(entity)
      else
        local world = root.worlds[rec.surface_index]
        if world then process(rec, world) end
        index = index + 1
      end
    elseif rec then S.remove(rec.id)
    else table.remove(list, index) end
  end
end
return Machines
