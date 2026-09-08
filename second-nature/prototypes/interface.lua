local C = require("shared.constants")
local M = require("shared.model")
local H = require("prototypes.helpers")
data:extend({
  {type="custom-input",name="sn-configure-inserter",key_sequence="SHIFT + I",consuming="none"},
  {type="custom-input",name="sn-open-jukebox",key_sequence="CONTROL + SHIFT + J",consuming="none"},
  {type="shortcut",name="sn-inserter-vectors",action="lua",icon=H.icon("vector-inserter"),icon_size=64,small_icon=H.icon("vector-inserter"),small_icon_size=64,associated_control_input="sn-configure-inserter",order="z-sn-c"},
  {type="shortcut",name="sn-jukebox",action="lua",icon=H.icon("jukebox"),icon_size=64,small_icon=H.icon("jukebox"),small_icon_size=64,associated_control_input="sn-open-jukebox",order="z-sn-d"},
  {type = "surface-property", name = "sn-restoration-domain", default_value = 0, order = "z-sn-a"},
  {type = "surface-property", name = "sn-planet-identity", default_value = 0, order = "z-sn-b"},
  {type = "surface-property", name = "sn-ecological-stage", default_value = 0, order = "z-sn-c"},
  {type = "custom-input", name = "sn-toggle-pollution", key_sequence = "CONTROL + SHIFT + P", consuming = "none"},
  {type = "shortcut", name = "sn-pollution-overlay", action = "lua", toggleable = true,
    icon = H.icon("signal-atmosphere"), icon_size = 64, small_icon = H.icon("signal-atmosphere"), small_icon_size = 64,
    associated_control_input = "sn-toggle-pollution", style = "blue", order = "z[second-nature]-b"},
  {type = "custom-input", name = "sn-toggle-dashboard", key_sequence = "SHIFT + T", consuming = "none"},
  {type = "shortcut", name = "sn-dashboard", action = "lua", toggleable = true,
    icon = H.icon("second-nature"), icon_size = 64, small_icon = H.icon("second-nature"), small_icon_size = 64,
    associated_control_input = "sn-toggle-dashboard", style = "green", order = "z[second-nature]"},
  {type = "sprite", name = "sn-logo", filename = H.icon("second-nature"), width = 64, height = 64},
  {type = "sprite", name = "sn-garden", filename = "__second-nature__/graphics/garden.png", width = 256, height = 192}
})
for _, name in ipairs(C.planets) do
  local planet = assert(data.raw.planet[name], "Second Nature requires the Space Age planet " .. name)
  -- Clean industry matters on every world. Keep Gleba's spores, and enable the
  -- ordinary pollution layer on stock worlds that vanilla leaves non-polluting.
  -- This does not introduce enemy spawners or change pressure/temperature.
  planet.pollutant_type = planet.pollutant_type or "pollution"
  planet.surface_properties = planet.surface_properties or {}
  planet.surface_properties["sn-restoration-domain"] = 1
  planet.surface_properties["sn-planet-identity"] = C.profiles[name].id
  planet.surface_properties["sn-ecological-stage"] = M.new(name).stage
end
for index, name in ipairs({"atmosphere", "temperature", "water", "soil", "biodiversity", "toxicity", "pressure", "stability", "stage"}) do
  data:extend({{
    type = "virtual-signal", name = "sn-" .. name, icon = H.icon("signal-" .. name), icon_size = 64,
    subgroup = "sn-signals", order = tostring(index)
  }})
end
for _, name in ipairs({"smog-total", "smog-local"}) do
  data:extend({{type = "virtual-signal", name = "sn-" .. name, icon = H.icon("signal-atmosphere"), icon_size = 64,
    subgroup = "sn-signals", order = "z-" .. name}})
end
local styles = data.raw["gui-style"].default
styles.sn_heading = {type = "label_style", parent = "label", font = "default-large-bold", font_color = {0.68, 0.9, 0.64}}
styles.sn_muted = {type = "label_style", parent = "label", font_color = {0.69, 0.74, 0.71}, single_line = false}
styles.sn_body = {type = "label_style", parent = "label", single_line = false, maximal_width = 690}
styles.sn_metric_name = {type = "label_style", parent = "label", width = 140}
styles.sn_metric_value = {type = "label_style", parent = "label", width = 90, horizontal_align = "right"}
styles.sn_progress = {type = "progressbar_style", parent = "progressbar", width = 235, bar_width = 10}
styles.sn_panel = {type = "vertical_flow_style", vertical_spacing = 10, padding = 12}
