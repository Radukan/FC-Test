local H = require("prototypes.helpers")
local packs = {"sn-ecology-science-pack", "sn-climate-science-pack", "sn-restoration-science-pack"}
for _, lab in pairs(data.raw.lab) do
  if H.contains(lab.inputs, "automation-science-pack") or H.contains(lab.inputs, "space-science-pack") then
    for _, pack in ipairs(packs) do H.append(lab.inputs, pack) end
  end
end
if settings.startup["sn-overhaul-progression"].value then
  local function ingredient(recipe, name, amount)
    local p = assert(data.raw.recipe[recipe], recipe)
    for _, i in ipairs(p.ingredients) do if i.name == name then return end end
    p.ingredients[#p.ingredients + 1] = {type = "item", name = name, amount = amount}
  end
  local function prerequisite(technology, name)
    local p = assert(data.raw.technology[technology], technology)
    p.prerequisites = p.prerequisites or {}; H.append(p.prerequisites, name)
  end
  -- Front-load ecology without replacing every vanilla ingredient with its own bespoke intermediate.
  ingredient("automation-science-pack", "sn-glass", 1)
  ingredient("logistic-science-pack", "sn-compost", 1)
  ingredient("chemical-science-pack", "sn-filter-cartridge", 1)
  ingredient("production-science-pack", "sn-ceramic-membrane", 1)
  ingredient("utility-science-pack", "sn-biofilm", 1)
  prerequisite("logistic-science-pack", "sn-composting")
  prerequisite("chemical-science-pack", "sn-atmospheric-engineering")
  prerequisite("production-science-pack", "sn-water-cycle")
  prerequisite("utility-science-pack", "sn-reforestation")
  prerequisite("rocket-silo", "sn-closed-loops")
end
