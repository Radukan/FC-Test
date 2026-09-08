local D = require("shared.field_drones")
local H = require("prototypes.helpers")
local A = require("shared.drone_art")
for index, item in ipairs(D.items) do
  data:extend({{type="item",name="sn-"..item.name,icon=H.icon(item.name),icon_size=64,
    subgroup="sn-logistics",order="a-field-"..index,stack_size=item.name=="field-drone" and 200 or 1,
    weight=item.name=="field-drone" and 1*kg or 5*kg,auto_recycle=false,
    localised_name={"item-name.sn-"..item.name},localised_description={"item-description.sn-"..item.name}}})
end
-- No robot prototype, docking category, logistic cell, equipment grid or network.
-- The inventory items cannot be inserted into a roboport's robot inventory.
local worker=H.copy("simple-entity-with-owner","simple-entity-with-owner")
worker.name=D.entity
worker.icon,worker.icon_size,worker.icons=H.icon("field-drone"),64,nil
worker.localised_name={"item-name.sn-field-drone"}
worker.localised_description={"item-description.sn-field-drone"}
worker.flags={"player-creation","placeable-off-grid","not-on-map","not-blueprintable","not-deconstructable","not-selectable-in-game"}
worker.minable,worker.placeable_by,worker.corpse,worker.dying_explosion=nil,nil,nil,nil
worker.hidden_in_factoriopedia=true
worker.max_health=35
worker.is_military_target=false
worker.collision_mask={layers={}}
worker.collision_box={{-.12,-.12},{.12,.12}}
worker.selection_box={{-.18,-.18},{.18,.18}}
worker.picture={filename="__core__/graphics/empty.png",width=1,height=1}
worker.pictures,worker.animations,worker.integration_patch,worker.factoriopedia_simulation=nil,nil,nil,nil
local animations={worker}
for key,spec in pairs(A) do
  local base="sn-field-drone-"..key:gsub("flying","flight"):gsub("working","work")
  for direction=0,D.directions-1 do
    local animation=table.deepcopy(spec)
    animation.type="animation";animation.name=base.."-"..direction
    animation.y=direction*spec.height
    animation.animation_speed=.3;animation.direction_count=nil
    animations[#animations+1]=animation
  end
  -- Retain the 0.6.1 names so saved LuaRenderObjects can be refitted on load.
  local legacy=table.deepcopy(spec)
  legacy.type="animation";legacy.name=base;legacy.direction_count=nil;legacy.animation_speed=.3
  animations[#animations+1]=legacy
end
data:extend(animations)
data:extend({{type="custom-input",name="sn-toggle-field-drones",key_sequence="CONTROL + SHIFT + B",consuming="none"}})

-- The native shortcuts and their native hotkeys unlock with the early crew.
for _,name in ipairs(D.planner_shortcuts) do
  local shortcut=data.raw.shortcut[name]
  if shortcut and shortcut.technology_to_unlock=="construction-robotics" then shortcut.technology_to_unlock=D.technology end
end
