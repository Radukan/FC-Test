local A = {}
function A.lander(camp)
  local entity = camp.ship
  if not (entity and entity.valid) then return end
  entity.destructible, entity.minable = false, false
  if not (camp.animation and camp.animation.valid) then
    camp.animation = rendering.draw_animation({animation="sn-lander-idle",target={entity=entity},surface=entity.surface,
      render_layer="higher-object-above",animation_speed=.035})
  end
end
function A.monitor(entity)
  return rendering.draw_animation({animation="sn-status-light",target={entity=entity,offset={.25,-.68}},surface=entity.surface,
    render_layer="higher-object-above",animation_speed=.09,time_to_live=250,x_scale=.35,y_scale=.35})
end
return A
