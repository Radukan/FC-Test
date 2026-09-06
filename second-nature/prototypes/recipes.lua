local K = require("shared.catalog")
local H = require("prototypes.helpers")
for index, x in ipairs(K.recipes) do
  local ingredients, results = {}, {}
  for _, value in ipairs(x.ingredients) do ingredients[#ingredients + 1] = {type = value[3] or "item", name = value[1], amount = value[2]} end
  for _, value in ipairs(x.results) do results[#results + 1] = {type = value[3] or "item", name = value[1], amount = value[2]} end
  local icon = x.machine and x.name or nil
  if not icon then
    for _, value in ipairs(x.results) do if value[1]:sub(1, 3) == "sn-" then icon = value[1]:sub(4); break end end
  end
  icon = icon or "second-nature"
  if x.operation then
    for _, m in ipairs(K.machines) do if m.fixed == x.name then icon = m.name; break end end
  end
  data:extend({{
    type = "recipe", name = "sn-" .. x.name, icon = H.icon(icon), icon_size = 64,
    -- Factorio 2.1 replaced the singular category with a list. Probe the loaded base data.
    category = not data.raw.recipe["iron-plate"].categories and x.category or nil,
    categories = data.raw.recipe["iron-plate"].categories and {x.category} or nil,
    enabled = x.enabled or false, energy_required = x.seconds,
    ingredients = ingredients, results = results,
    localised_name = x.machine and {"entity-name.sn-" .. x.name} or {"recipe-name.sn-" .. x.name},
    localised_description = x.effects and {"recipe-description.sn-" .. x.name} or nil,
    subgroup = x.machine and (K.by_machine["sn-" .. x.name].planet and "sn-planetary" or "sn-production") or (x.operation and "sn-operations" or "sn-recovery"),
    order = string.format("%03d", index), main_product = "",
    allow_productivity = false, allow_quality = not x.effects and x.recycle ~= false,
    allow_decomposition = not x.operation, auto_recycle = x.machine or false,
    emissions_multiplier = x.emissions or 1, surface_conditions = H.conditions(x),
    hide_from_player_crafting = x.operation or false,
    always_show_made_in = x.operation or x.planet ~= nil
  }})
end
