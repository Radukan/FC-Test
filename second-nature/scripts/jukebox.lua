local S=require("scripts.state")
local J={}
local function data(player)
  local root=S.root();root.radios=root.radios or {};root.radios[player.index]=root.radios[player.index] or {}
  return root.radios[player.index]
end
local function valid(player,entity)
  return entity and entity.valid and entity.name=="sn-jukebox" and entity.force.index==player.force.index
end
function J.close(player)
  local f=player.gui.screen.sn_jukebox;if f then f.destroy() end
end
function J.play(player,entity,note,surface_broadcast)
  if not valid(player,entity) or type(note)~="number" or note<0 or note>3 or note~=math.floor(note) then return false end
  if surface_broadcast and game.is_multiplayer() and not player.admin then player.print({"sn-jukebox.admin"});return false end
  local parameters=entity.parameters
  parameters.playback_volume=.85;parameters.allow_polyphony=false;parameters.volume_controlled_by_signal=false
  parameters.playback_mode=surface_broadcast and "surface" or "local"
  entity.parameters=parameters
  -- Native programmable-speaker playback can stop a previous note cleanly.
  local ok=entity.play_note(1,note+1,true)
  if ok then local d=data(player);d.note=note end
  return ok
end
function J.open(player,entity)
  if not valid(player,entity) then
    local found=player.surface.find_entities_filtered({name="sn-jukebox",position=player.position,radius=64,force=player.force,limit=1})
    entity=found[1]
  end
  if not valid(player,entity) then player.print({"sn-jukebox.place"});return end
  J.close(player);local d=data(player);d.entity=entity
  local f=player.gui.screen.add({type="frame",name="sn_jukebox",caption={"sn-jukebox.title"},direction="vertical"})
  f.auto_center=true
  local intro=f.add({type="label",name="sn_radio_description",caption={"sn-jukebox.description"}});intro.style.single_line=false;intro.style.maximal_width=460
  for index,key in ipairs({"after-ash","living-world","transmission"}) do
    f.add({type="button",name="sn_play_"..index,caption={"sn-jukebox."..key},tags={sn_track=index}})
  end
  f.add({type="checkbox",name="sn_surface_broadcast",caption={"sn-jukebox.broadcast"},state=d.broadcast or false})
  local row=f.add({type="flow",name="sn_radio_actions",direction="horizontal"})
  row.add({type="button",name="sn_radio_stop",caption={"sn-jukebox.stop"}})
  row.add({type="button",name="sn_radio_close",caption={"gui.close"}})
  player.opened=f
end
function J.opened(event)
  local player=game.get_player(event.player_index)
  if player and valid(player,event.entity) then J.open(player,event.entity) end
end
function J.click(event)
  local player=game.get_player(event.player_index);local element=event.element
  if not player or not (element and element.valid) then return false end
  if element.name=="sn_transmission_close" then local f=player.gui.left.sn_transmission;if f then f.destroy() end;return true end
  if element.name=="sn_radio_close" then J.close(player);return true end
  local d=data(player);local tags=element.tags or {}
  if tags.sn_track or element.name=="sn_radio_stop" then
    local f=player.gui.screen.sn_jukebox
    d.broadcast=f and f.sn_surface_broadcast.state or false
    J.play(player,d.entity,tags.sn_track or 0,d.broadcast)
    return true
  end
  return false
end
function J.transmission(player)
  local d=data(player)
  if d.transmission_seen then return end
  d.transmission_seen=true
  local f=player.gui.left.add({type="frame",name="sn_transmission",direction="vertical",caption={"sn-lore.title"}})
  local text=f.add({type="label",name="sn_lore_text",caption={"sn-lore.transmission"}})
  text.style.single_line=false;text.style.maximal_width=440
  f.add({type="button",name="sn_transmission_close",caption={"sn-lore.close"}})
end
return J
