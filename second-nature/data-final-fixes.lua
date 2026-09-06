-- Catch broken cross-mod references at startup, with an actionable error rather than a later save crash.
local K = require("shared.catalog")
local function item_exists(name)
  for kind in pairs(defines.prototypes.item) do if data.raw[kind] and data.raw[kind][name] then return true end end
  return false
end
for _, r in ipairs(K.recipes) do
  assert(data.raw["recipe-category"][r.category], "Second Nature: missing recipe category " .. r.category)
  for _, list in ipairs({r.ingredients, r.results}) do
    for _, entry in ipairs(list) do
      local exists = entry[3] == "fluid" and data.raw.fluid[entry[1]] or item_exists(entry[1])
      assert(exists, "Second Nature: missing ingredient/product " .. entry[1] .. " in " .. r.name)
    end
  end
end
for _, t in ipairs(K.technologies) do
  for _, prerequisite in ipairs(t.prerequisites) do
    assert(data.raw.technology[prerequisite], "Second Nature: missing prerequisite " .. prerequisite)
  end
end
-- Pollutant-fed attack recruitment is replaced for Nauvis species, not pentapods.
-- Empty absorption dictionaries mean no pollution recruitment; zero-cost entries would not.
if settings.startup["sn-biter-metabolism"].value then
  for _, name in ipairs(require("shared.constants").native_names) do
    local unit = data.raw.unit[name]
    if unit then
      unit.absorptions_to_join_attack = unit.absorptions_to_join_attack or {}
      unit.absorptions_to_join_attack.pollution = nil
    end
    local nest = data.raw["unit-spawner"][name]
    if nest then
      nest.absorptions_per_second = nest.absorptions_per_second or {}
      nest.absorptions_per_second.pollution = nil
    end
  end
  data.raw["airborne-pollutant"].pollution.affects_evolution = false
end
if settings.startup["sn-menu-background"].value then
  local constants = data.raw["utility-constants"].default
  constants.main_menu_simulations = {}
  constants.main_menu_background_image_location = "__second-nature__/graphics/menu/last-landing.jpg"
  constants.main_menu_background_vignette_intensity = 18
end
