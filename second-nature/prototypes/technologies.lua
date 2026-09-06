local K = require("shared.catalog")
for index, x in ipairs(K.technologies) do
  local effects = table.deepcopy(x.effects or {})
  for _, recipe in ipairs(x.unlocks) do effects[#effects + 1] = {type = "unlock-recipe", recipe = "sn-" .. recipe} end
  local unit = {ingredients = table.deepcopy(x.science), time = x.seconds}
  if type(x.count) == "number" then unit.count = x.count else unit.count_formula = x.count end
  data:extend({{
    type = "technology", name = "sn-" .. x.name, icon = "__second-nature__/graphics/technology/" .. x.name .. ".png", icon_size = 256,
    localised_name = {"technology-name.sn-" .. x.name}, localised_description = {"technology-description.sn-" .. x.name},
    prerequisites = table.deepcopy(x.prerequisites), effects = effects, unit = unit,
    order = string.format("z-sn-%03d", index), max_level = x.max_level, upgrade = x.max_level and true or nil
  }})
end
