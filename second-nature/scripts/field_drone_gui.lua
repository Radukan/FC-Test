local D=require("scripts.field_drones")
local G={}
function G.close(player)
  local frame=player and player.gui.left.sn_field_drones
  if frame then frame.destroy() end
end
function G.update(player)
  local frame=player and player.gui.left.sn_field_drones
  if not (frame and frame.valid) then return end
  local s=D.status(player)
  player.set_shortcut_toggled("sn-field-drones",s.enabled)
  frame.sn_drone_stats.caption={"sn-drones.stats",tostring(s.active),tostring(s.limit),tostring(s.stock),tostring(s.built),tostring(s.deconstructed),tostring(s.upgraded)}
  frame.sn_drone_reason.caption={"sn-drones."..s.reason}
  frame.sn_drone_buttons.sn_drone_toggle.caption={s.enabled and "sn-drones.pause" or "sn-drones.enable"}
end
function G.open(player)
  if not player then return end
  if not player.gui.left.sn_field_drones then
    local frame=player.gui.left.add({type="frame",name="sn_field_drones",direction="vertical",caption={"sn-drones.title"}})
    frame.add({type="label",name="sn_drone_stats",caption="",style="sn_body"})
    frame.add({type="label",name="sn_drone_reason",caption="",style="sn_muted"})
    frame.add({type="label",name="sn_drone_help",caption={"sn-drones.help"},style="sn_body"})
    frame.sn_drone_help.style.maximal_width=360
    frame.sn_drone_reason.style.maximal_width=360
    local buttons=frame.add({type="flow",name="sn_drone_buttons",direction="horizontal"})
    buttons.add({type="button",name="sn_drone_toggle",caption={"sn-drones.enable"}})
    buttons.add({type="button",name="sn_drone_close",caption={"sn-drones.hide"},tooltip={"sn-drones.hide-help"}})
  end
  G.update(player)
end
function G.toggle(player)
  if not player then return end
  D.toggle(player);G.open(player)
end
function G.click(event)
  local element=event.element
  if not (element and element.valid) then return false end
  local player=game.get_player(event.player_index)
  if element.name=="sn_drone_toggle" then G.toggle(player);return true end
  if element.name=="sn_drone_close" then G.close(player);return true end
  return false
end
return G
