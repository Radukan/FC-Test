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
