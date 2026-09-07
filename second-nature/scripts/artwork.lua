local Lander = require("shared.lander_layout")
local A = {}
function A.lander(camp)
  local entity = camp.ship
  if not (entity and entity.valid) then return end
  entity.destructible, entity.minable = false, false
  -- Refit only the render object. Never replace the ship, relocate cargo, or
  -- repeat a landing grant. Repeated configuration changes remain idempotent.
  if camp.animation and camp.animation.valid and camp.art_revision ~= Lander.art_revision then
    camp.animation.destroy()
  end
  if not (camp.animation and camp.animation.valid) then
    camp.animation = rendering.draw_animation({animation="sn-lander-idle",target={entity=entity},surface=entity.surface,
      render_layer="higher-object-above",animation_speed=Lander.animation_speed})
    camp.art_revision = Lander.art_revision
  end
end
function A.monitor(entity)
  return rendering.draw_animation({animation="sn-status-light",target={entity=entity,offset={.25,-.68}},surface=entity.surface,
    render_layer="higher-object-above",animation_speed=.09,time_to_live=250,x_scale=.35,y_scale=.35})
end
return A
