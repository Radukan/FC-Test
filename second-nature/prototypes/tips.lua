-- The in-game field guide, shown in the native tips-and-tricks window.
--
-- Entries are added to their own category, so no stock Factorio tip is
-- replaced, reordered or hidden. Text lives in the generated locale file.
local T = require("shared.tips")
local prototypes = {{type = "tips-and-tricks-item-category", name = T.category, order = T.category_order}}
for _, x in ipairs(T.items) do
  prototypes[#prototypes + 1] = {
    type = "tips-and-tricks-item", name = "sn-" .. x.name, category = T.category, order = x.order,
    tag = x.tag, indent = x.indent, is_title = x.is_title or nil,
    trigger = x.trigger and table.deepcopy(x.trigger) or nil,
    skip_trigger = x.skip_trigger and table.deepcopy(x.skip_trigger) or nil,
    dependencies = x.dependencies and table.deepcopy(x.dependencies) or nil,
    localised_name = {"tips-and-tricks-item-name.sn-" .. x.name},
    localised_description = {"tips-and-tricks-item-description.sn-" .. x.name}
  }
end
data:extend(prototypes)
