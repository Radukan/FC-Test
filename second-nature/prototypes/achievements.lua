-- Restoration milestones.
--
-- Modded achievements are tracked by the game in its separate modded list and
-- never touch vanilla or Steam progress. Two kinds exist:
--   * script milestones are plain "achievement" prototypes. Only that type can
--     be unlocked from a script, which is why every mod-tracked goal uses it.
--   * engine milestones are condition prototypes the game evaluates by itself;
--     the mod does not unlock those.
local A = require("shared.achievements")
local function art(name) return "__second-nature__/graphics/achievement/" .. name .. ".png" end
local prototypes = {}
for _, x in ipairs(A.script) do
  prototypes[#prototypes + 1] = {
    type = "achievement", name = "sn-" .. x.name, order = x.order,
    icon = art(x.name), icon_size = 128,
    localised_name = {"achievement-name.sn-" .. x.name},
    localised_description = {"achievement-description.sn-" .. x.name}
  }
end
for _, x in ipairs(A.engine) do
  local p = {
    type = x.kind, name = "sn-" .. x.name, order = x.order,
    icon = art(x.name), icon_size = 128,
    localised_name = {"achievement-name.sn-" .. x.name},
    localised_description = {"achievement-description.sn-" .. x.name}
  }
  for key, value in pairs(x.fields) do p[key] = table.deepcopy(value) end
  prototypes[#prototypes + 1] = p
end
-- The field station shows the same medallions, so each one also needs a sprite.
for _, x in ipairs(A.all) do
  prototypes[#prototypes + 1] = {type = "sprite", name = "sn-medal-" .. x.name,
    filename = art(x.name), width = 128, height = 128, mipmap_count = 2}
end
data:extend(prototypes)
