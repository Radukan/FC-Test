data:extend({
  {type = "bool-setting", name = "sn-overhaul-progression", setting_type = "startup", default_value = true, order = "a"},
  {type = "double-setting", name = "sn-restoration-speed", setting_type = "runtime-global", default_value = 1, minimum_value = 0.25, maximum_value = 5, order = "b"},
  {type = "string-setting", name = "sn-native-resistance", setting_type = "runtime-global", default_value = "balanced", allowed_values = {"off", "balanced", "relentless"}, order = "c"},
  {type = "int-setting", name = "sn-grace-minutes", setting_type = "runtime-global", default_value = 20, minimum_value = 0, maximum_value = 120, order = "d"},
  {type = "bool-setting", name = "sn-living-terrain", setting_type = "runtime-global", default_value = true, order = "e"},
  {type = "bool-setting", name = "sn-tree-growth", setting_type = "runtime-global", default_value = true, order = "f"},
  {type = "bool-setting", name = "sn-network-victory", setting_type = "runtime-global", default_value = true, order = "g"},
  {type = "bool-setting", name = "sn-show-welcome", setting_type = "runtime-per-user", default_value = true, order = "h"}
})
