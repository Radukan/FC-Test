-- Restoration Nexus: A new fantastical central building for Second Nature
-- Represents the convergence of sealed industry and living ecology

local H = require("prototypes.helpers")

-- New item
local nexus_item = {
  type = "item",
  name = "sn-restoration-nexus",
  icon = H.icon("restoration-nexus"),
  icon_size = 64,
  subgroup = "sn-restoration",
  order = "z-zz-restoration-nexus",
  stack_size = 1,
  localised_name = {"item-name.sn-restoration-nexus"},
  localised_description = {"item-description.sn-restoration-nexus"},
  place_result = "sn-restoration-nexus"
}

data:extend({nexus_item})

-- Direct animation references to our new fantastical graphics
local nexus_east = {
  filename = "__second-nature__/graphics/entity/restoration_nexus/restoration-nexus-east.png",
  width = 256, height = 256, frame_count = 1, direction_count = 1, line_length = 1,
  scale = 1.0, shift = {0, -0.5}, apply_projection = false
}
local nexus_plant = {
  filename = "__second-nature__/graphics/entity/restoration_nexus/restoration-nexus-plant-east.png",
  width = 256, height = 256, frame_count = 8, direction_count = 1, line_length = 8,
  scale = 1.0, shift = {0, -0.5}, apply_projection = false
}

-- The Restoration Nexus machine: an assembling machine that symbolizes ecological synthesis
local nexus_machine = {
  type = "assembling-machine",
  name = "sn-restoration-nexus",
  icon = H.icon("restoration-nexus"),
  icon_size = 64,
  flags = {"placeable-neutral", "player-creation"},
  minable = {mining_time = 1, result = "sn-restoration-nexus"},
  max_health = 600,
  corpse = "big-remnants",
  dying_explosion = "medium-explosion",
  alert_icon_shift = {0, -0.3},
  selection_box = {{-1.2, -1.2}, {1.2, 1.2}},
  drawing_box = {{-2, -2}, {2, 2}},
  collision_box = {{-1.1, -1.1}, {1.1, 1.1}},
  selection_priority = 50,
  tile_width = 3,
  tile_height = 3,
  energy_source = {type = "electric", usage_priority = "secondary", emissions_per_minute = 10},
  energy_usage = "500kW",
  crafting_speed = 2,
  crafting_categories = {"sn-restoration"},
  fluid_boxes = {{
    production_type = "input-output",
    pipe_picture = require("util").empty_sprite(),
    pipe_covers = require("util").sprite("pipe-covers", {compatibility = {"pipe-covers"}}),
    base_area = 1, height = 1,
    base_level = 0,
    volume = 100,
    filter = "water",
    minimum_temperature = 15,
    maximum_temperature = 100
  }},
  graphics_set = {
    animation = {
      north = nexus_east,
      east = nexus_east,
      south = nexus_east,
      west = nexus_east,
    },
    animation_progress = {
      north = nexus_plant,
      east = nexus_plant,
      south = nexus_plant,
      west = nexus_plant,
    }
  },
  working_sound = {
    sound = {filename = "__base__/sound/metal-large-gear.ogg", volume = 0.6},
    idle_sound = {filename = "__base__/sound/metal-large-gear.ogg", volume = 0.4}
  },
  open_sound = {filename = "__base__/sound/metal-large-gear.ogg", volume = 0.7},
  close_sound = {filename = "__base__/sound/metal-large-gear.ogg", volume = 0.7},
  vehicle_impact_sound = {filename = "__base__/sound/car-metal-impact.ogg", volume = 0.65},
  impact_category = "metal-large",
  localised_name = {"entity-name.sn-restoration-nexus"},
  localised_description = {"entity-description.sn-restoration-nexus"},
  order = "z-z-restoration-nexus"
}

data:extend({nexus_machine})

-- Recipe: synthesis of the Nexus from advanced ecological materials
local nexus_recipe = {
  type = "recipe",
  name = "sn-restoration-nexus",
  enabled = false,
  energy_required = 100,
  ingredients = {
    {"sn-arc-refinery", 1},
    {"sn-biocrystal-core", 10},
    {"sn-mycelial-spore", 20},
    {type = "item", name = "steel-plate", amount = 50},
    {type = "item", name = "advanced-circuit", amount = 20},
    {type = "fluid", name = "water", amount = 200}
  },
  result = "sn-restoration-nexus",
  result_count = 1,
  category = "sn-restoration"
}

data:extend({nexus_recipe})

-- Technology unlock
local nexus_tech = {
  type = "technology",
  name = "sn-restoration-nexus-tech",
  icon = H.icon("restoration-technology"),
  icon_size = 64,
  prerequisites = {"sn-field-laboratory"},
  unit = {
    count = 500,
    ingredients = {
      {"automation-science-pack", 1},
      {"logistic-science-pack", 1},
      {"chemical-science-pack", 1},
      {"production-science-pack", 1},
      {"utility-science-pack", 1}
    },
    time = 30
  },
  effects = {
    {type = "unlock-recipe", recipe = "sn-restoration-nexus"},
    {type = "unlock-recipe", recipe = "sn-biocrystal-core"},
    {type = "unlock-recipe", recipe = "sn-mycelial-spore"}
  },
  order = "z-99-restoration-nexus"
}

data:extend({nexus_tech})

-- New ecological synthesis items
local biocrystal_item = {
  type = "item",
  name = "sn-biocrystal-core",
  icon = H.icon("biocrystal-core"),
  icon_size = 64,
  subgroup = "sn-restoration",
  order = "z-99-biocrystal",
  stack_size = 200,
  localised_name = {"item-name.sn-biocrystal-core"},
  localised_description = {"item-description.sn-biocrystal-core"}
}
local spore_item = {
  type = "item",
  name = "sn-mycelial-spore",
  icon = H.icon("mycelial-spore"),
  icon_size = 64,
  subgroup = "sn-restoration",
  order = "z-99-spore",
  stack_size = 500,
  localised_name = {"item-name.sn-mycelial-spore"},
  localised_description = {"item-description.sn-mycelial-spore"}
}
data:extend({biocrystal_item, spore_item})

-- Recipes for new items (linked to existing technology groups)
local crystal_recipe = {
  type = "recipe",
  name = "sn-biocrystal-core",
  enabled = false,
  energy_required = 2,
  ingredients = {
    {"sn-algal-biomass", 10},
    {"stone", 20},
    {type = "fluid", name = "water", amount = 50}
  },
  result = "sn-biocrystal-core",
  result_count = 4
}
local spore_recipe = {
  type = "recipe",
  name = "sn-mycelial-spore",
  enabled = false,
  energy_required = 1,
  ingredients = {
    {"sn-bio-ash", 5},
    {"wood", 10},
    {type = "fluid", name = "water", amount = 20}
  },
  result = "sn-mycelial-spore",
  result_count = 10
}
data:extend({crystal_recipe, spore_recipe})
