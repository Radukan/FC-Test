local H = require("prototypes.helpers")
local C = require("shared.constants")
local enabled = settings.startup["sn-desolate-start"].value
if enabled then
  local map = data.raw.planet.nauvis.map_gen_settings
  map.autoplace_controls.trees = nil
  local entities = map.autoplace_settings.entity
  entities.treat_missing_as_default = false
  for name in pairs(entities.settings) do
    if data.raw.tree[name] or name == "fish" then entities.settings[name] = nil end
  end
  -- An explicit whitelist must retain native nests/worms as well as ore.
  -- Vanilla normally includes these via treat_missing_as_default=true.
  for _, name in ipairs(C.native_names) do
    local prototype = data.raw["unit-spawner"][name] or data.raw.turret[name]
    if prototype and prototype.autoplace then entities.settings[name] = {} end
  end
  -- Only geological decoratives belong on this stripped world. Gleba is untouched.
  local decorations = map.autoplace_settings.decorative
  decorations.treat_missing_as_default = false
  for name in pairs(decorations.settings) do
    if not (name:find("rock") or name:find("decal")) then decorations.settings[name] = nil end
  end
end
local presets = data.raw["map-gen-presets"].default
local function preset(peaceful, frontier)
  return {
    order = frontier and "a-c" or (peaceful and "a-d" or "a-b"),
    basic_settings = {
      peaceful_mode = peaceful, starting_area = frontier and 0.75 or 1.25,
      autoplace_controls = {trees = {frequency = 0, size = 0, richness = 0},
        ["enemy-base"] = {frequency = frontier and 1.5 or 1, size = frontier and 1.5 or 1},
        ["iron-ore"] = {richness = 1.5}, ["copper-ore"] = {richness = 1.5},
        coal = {richness = 1.5}, stone = {richness = 1.5}},
      property_expression_names = {moisture_bias = -0.35}
    },
    advanced_settings = {pollution = {enabled = true},
      enemy_evolution = {pollution_factor = 0, time_factor = 0.000002, destroy_factor = 0.002}}
  }
end
presets["sn-last-landing"] = preset(false, false)
presets["sn-brood-frontier"] = preset(false, true)
presets["sn-quiet-reclamation"] = preset(true, false)
-- Factorio forbids settings on its special default=true preset. Use the named Last Landing preset.

local lander = H.copy("container", "crash-site-spaceship")
lander.name = "sn-lander"
lander.localised_name = {"entity-name.sn-lander"}
lander.localised_description = {"entity-description.sn-lander"}
lander.inventory_size, lander.hidden, lander.hidden_in_factoriopedia = 48, false, false
lander.flags = {"placeable-neutral", "player-creation", "not-blueprintable", "not-deconstructable"}
lander.minable = {mining_time = 3, results = {{type = "item", name = "steel-plate", amount = 40}}}
lander.dying_explosion = nil
lander.factoriopedia_simulation = nil
H.tint_sprites(lander.picture, {0.83, 1, 0.88})

local bloom = H.copy("unit", "small-biter")
bloom.name, bloom.icon, bloom.icons, bloom.icon_size = "sn-bloomback", H.icon("bloomback"), nil, 64
bloom.localised_name, bloom.localised_description = {"entity-name.sn-bloomback"}, {"entity-description.sn-bloomback"}
bloom.run_animation = {filename = "__second-nature__/graphics/entity/bloomback.png", width = 96, height = 96,
  frame_count = 4, direction_count = 8, line_length = 4, scale = 0.5}
bloom.alternative_attacking_frame_sequence = nil
bloom.attack_parameters.animation = table.deepcopy(bloom.run_animation)
bloom.attack_parameters.damage_modifier = 0
bloom.movement_speed, bloom.distance_per_frame, bloom.vision_distance = 0.055, 0.13, 12
bloom.max_health, bloom.healing_per_tick = 120, 0.02
bloom.dying_sound, bloom.warcry, bloom.walking_sound, bloom.running_sound_animation_positions = nil, nil, nil, nil
bloom.corpse, bloom.dying_explosion, bloom.factoriopedia_simulation = nil, nil, nil
bloom.absorptions_to_join_attack = {}
bloom.ai_settings = {do_separation = true, allow_try_return_to_spawner = false, destroy_when_commands_fail = false}
local garden = {
  type = "simple-entity-with-owner", name = "sn-bloom-nest", icon = H.icon("bloomback"), icon_size = 64,
  localised_name = {"entity-name.sn-bloom-nest"}, localised_description = {"entity-description.sn-bloom-nest"},
  flags = {"placeable-off-grid", "not-blueprintable", "not-deconstructable"}, max_health = 600,
  collision_box = {{-1.7, -1.2}, {1.7, 1.2}}, selection_box = {{-2, -1.5}, {2, 1.5}},
  picture = {filename = "__second-nature__/graphics/entity/bloom-nest.png", width = 256, height = 192, scale = 0.6},
  render_layer = "object", map_color = {0.32, 0.8, 0.62}
}
data:extend({lander, bloom, garden})
