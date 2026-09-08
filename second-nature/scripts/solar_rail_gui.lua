local R=require("scripts.solar_rail")
local S=require("scripts.state")
local G={}
function G.close(player)
  if not player then return end
  local frame=player.gui.left.sn_solar_rail
  if frame then frame.destroy() end
  if S.root().solar_inspectors then S.root().solar_inspectors[player.index]=nil end
end
function G.update(player)
  local entities=S.root().solar_inspectors
  local entity=entities and entities[player.index]
  local frame=player.gui.left.sn_solar_rail
  if not frame then return end
  if not (entity and entity.valid and entity.force.index==player.force.index) then G.close(player);return end
  local status=R.status(entity)
  if not status then G.close(player);return end
  frame.sn_rail_charge.caption={"sn-energy.charge",string.format("%.2f",status.energy/1000000),string.format("%.0f",status.capacity/1000000)}
  frame.sn_rail_meter.value=math.max(0,math.min(1,status.energy/status.capacity))
  frame.sn_rail_mode.caption={"sn-energy.mode",{"sn-energy."..status.mode},string.format("%.0f",status.cap*216)}
end
function G.opened(event)
  local player=game.get_player(event.player_index)
  if not player then return end
  G.close(player)
  local entity=event.entity
  if not (R.definition(entity) and entity.force.index==player.force.index) then return end
  S.root().solar_inspectors=S.root().solar_inspectors or {};S.root().solar_inspectors[player.index]=entity
  local frame=player.gui.left.add({type="frame",name="sn_solar_rail",direction="vertical",caption={"sn-energy.solar-rail"}})
  frame.add({type="label",name="sn_rail_charge",caption=""})
  frame.add({type="progressbar",name="sn_rail_meter",value=0})
  frame.add({type="label",name="sn_rail_mode",caption=""})
  frame.add({type="label",name="sn_rail_help",caption={"sn-energy.rail-help"},style="sn_body"})
  frame.sn_rail_help.style.maximal_width=350
  G.update(player)
end
function G.closed(event)
  local player=game.get_player(event.player_index)
  if player then G.close(player) end
end
return G
