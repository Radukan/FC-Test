local K = require("shared.catalog")
local H = require("prototypes.helpers")
local prototypes = {{type = "item-group", name = "sn-restoration", icon = H.icon("second-nature"), icon_size = 64, order = "z-a"}}
for index, group in ipairs({"materials", "biology", "fluids", "science", "production", "restoration", "planetary", "operations", "recovery", "signals", "defense", "logistics", "energy"}) do
  prototypes[#prototypes + 1] = {type = "item-subgroup", name = "sn-" .. group, group = "sn-restoration", order = string.format("%02d", index)}
end
data:extend(prototypes)
-- Science packs became ordinary items in 2.1; 2.0 labs consume tool durability.
local legacy_science = data.raw.tool and data.raw.tool["automation-science-pack"] ~= nil
for index, x in ipairs(K.items) do
  local p = {
    type = (x.tool and legacy_science) and "tool" or "item", name = "sn-" .. x.name, icon = H.icon(x.name), icon_size = 64,
    subgroup = x.tool and "sn-science" or ((x.family == "leaf" or x.family == "seed" or x.family == "culture" or x.family == "soil") and "sn-biology" or "sn-materials"),
    order = string.format("%03d", index), stack_size = x.tool and 200 or 100, weight = x.tool and 1 * kg or 2 * kg,
    localised_name = {"item-name.sn-" .. x.name}, localised_description = {"item-description.sn-" .. x.name},
    -- No default self-recycling: an expensive, power-consuming waste loop is the intended route.
    auto_recycle = false
  }
  if x.tool and legacy_science then p.durability = 1; p.durability_description_key = "description.science-pack-remaining-amount-key"; p.durability_description_value = "description.science-pack-remaining-amount-value" end
  if x.fuel_value then p.fuel_category = "chemical"; p.fuel_value = x.fuel_value; p.fuel_emissions_multiplier = 0.5 end
  data:extend({p})
end
for index, x in ipairs(K.fluids) do
  data:extend({{
    type = "fluid", name = "sn-" .. x.name, icon = H.icon(x.name), icon_size = 64,
    subgroup = "sn-fluids", order = string.format("%02d", index), default_temperature = 25,
    base_color = x.color, flow_color = x.color, auto_barrel = true, fuel_value=x.fuel_value,
    localised_name = {"fluid-name.sn-" .. x.name}, localised_description = {"fluid-description.sn-" .. x.name}
  }})
end
