local K = require("shared.catalog")
local C = require("shared.constants")
local H = require("prototypes.helpers")
local Art = require("prototypes.artwork")
local Ports = require("shared.fluid_ports")
local categories = {}
for index, x in ipairs(K.machines) do
  local kind = x.entity_type or "assembling-machine"
  local p = H.copy(kind, x.base)
  p.name, p.icon, p.icon_size, p.icons = "sn-" .. x.name, H.icon(x.name), 64, nil
  p.localised_name, p.localised_description = {"entity-name.sn-" .. x.name}, {"entity-description.sn-" .. x.name}
  p.minable = {mining_time = 0.3, result = p.name}
  p.placeable_by = {item = p.name, count = 1}
  p.next_upgrade, p.fast_replaceable_group = nil, "sn-" .. x.name
  p.factoriopedia_simulation = nil
  p.max_health = x.planet and 700 or (x.fixed and 500 or 350)
  local rgb = C.colors[x.color]
  local tint = {0.65 + rgb[1] * 0.35, 0.65 + rgb[2] * 0.35, 0.65 + rgb[3] * 0.35}
  p.water_reflection, p.corpse = nil, nil
  if kind == "assembling-machine" then p.graphics_set = {animation = Art.four_way(x.name, true)}
  else p.sprites = Art.four_way(x.name, false) end
  if kind == "assembling-machine" then
    -- The same coordinates drive the mesh nozzles. Do not draw inherited assembler stubs.
    for _, box in ipairs(p.fluid_boxes or {}) do box.pipe_picture = nil end
    for _, port in ipairs(Ports[x.name] or {}) do
      local box = assert(p.fluid_boxes[port.box], "Missing fluid box for " .. x.name)
      box.pipe_connections = {{position = table.deepcopy(port.position), direction = port.direction, flow_direction = port.flow}}
    end
    p.crafting_categories = {}
    for _, category in ipairs(x.categories) do
      local name = "sn-" .. category
      p.crafting_categories[#p.crafting_categories + 1] = name
      if not categories[name] then categories[name] = true; data:extend({{type = "recipe-category", name = name}}) end
    end
    p.crafting_speed = 1
    p.energy_usage = x.energy
    p.energy_source = {type = "electric", usage_priority = "secondary-input", emissions_per_minute = {pollution = x.pollution, spores = x.pollution}}
    p.heating_energy = x.planet == "aquilo" and "300kW" or "100kW"
    p.effect_receiver = {base_effect = {}}
    p.module_slots = x.fixed and 2 or 3
    -- Effects are earned per craft, never via bonus productivity or quality reroll loops.
    p.allowed_effects = {"consumption", "speed", "pollution"}
    p.fixed_recipe = x.fixed and "sn-" .. x.fixed or nil
    if x.fixed then p.surface_conditions = H.conditions({domain = true, planet = x.planet}) end
    p.production_health_effect = nil

  end
  data:extend({p, {
    type = "item", name = p.name, icon = H.icon(x.name), icon_size = 64,
    subgroup = x.planet and "sn-planetary" or (x.fixed and "sn-restoration" or "sn-production"),
    order = string.format("%02d", index), stack_size = x.fixed and 10 or 20,
    weight = x.planet and 100 * kg or (x.fixed and 50 * kg or 20 * kg), place_result = p.name,
    localised_name = p.localised_name, localised_description = p.localised_description
  }})
end

-- Native mutations are only mobilized by the runtime at an EXISTING Nauvis nest.
-- They never enter the ordinary evolution table and never appear on lifeless worlds.
for _, definition in ipairs({
  {name = "rootbreaker", base = "medium-biter", color = {0.66, 0.83, 0.37}, health = 1.15},
  {name = "canopy-breaker", base = "big-biter", color = {0.52, 0.68, 0.27}, health = 1.10},
  {name = "blight-spitter", base = "medium-spitter", color = {0.77, 0.54, 0.35}, health = 1.10}
}) do
  local p = H.copy("unit", definition.base)
  p.name = "sn-" .. definition.name
  p.icon, p.icons, p.icon_size = H.icon(definition.name), nil, 64
  p.localised_name = {"entity-name." .. p.name}
  p.localised_description = {"entity-description.sn-native"}
  p.max_health = math.floor(p.max_health * definition.health)
  H.tint_sprites(p.run_animation, definition.color)
  H.tint_sprites(p.attack_parameters.animation, definition.color)
  p.factoriopedia_simulation = nil
  data:extend({p})
end
