local A = require("shared.art")
local Art = {}
function Art.animation(name, speed)
  local p = table.deepcopy(assert(A[name], "Missing expedition art: " .. name))
  p.animation_speed = speed or 0.18
  return p
end
function Art.sprite(name)
  local p = table.deepcopy(assert(A[name], "Missing expedition art: " .. name))
  p.frame_count, p.direction_count, p.line_length = nil, nil, nil
  return p
end
function Art.four_way(name, animated)
  local p = {}
  for _, direction in ipairs({"north", "east", "south", "west"}) do
    p[direction] = animated and Art.animation(name .. "-" .. direction) or Art.sprite(name .. "-" .. direction)
  end
  return p
end
function Art.turret(p, name)
  p.graphics_set = nil -- No inherited vanilla base, masks or shadow hiding under our model.
  p.water_reflection, p.corpse = nil, nil
  p.special_effect, p.resource_indicator_animation = nil, nil
  p.folded_animation = Art.animation(name .. "-idle")
  p.prepared_animation = Art.animation(name .. "-idle")
  p.preparing_animation = Art.animation(name .. "-fire")
  p.folding_animation = Art.animation(name .. "-fire")
  p.attacking_animation = Art.animation(name .. "-fire", 0.5)
  if p.starting_attack_animation then p.starting_attack_animation = Art.animation(name .. "-fire") end
  if p.ending_attack_animation then p.ending_attack_animation = Art.animation(name .. "-fire") end
end
function Art.wall(p, name)
  p.pictures = {}
  for _, key in ipairs({"single", "straight_vertical", "straight_horizontal", "corner_right_down", "corner_left_down", "t_up",
    "ending_right", "ending_left", "filling", "water_connection_patch", "gate_connection_patch"}) do p.pictures[key] = Art.sprite(name .. "-" .. key) end
  p.water_reflection, p.corpse = nil, nil
end
return Art
