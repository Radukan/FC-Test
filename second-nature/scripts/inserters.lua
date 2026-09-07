local S=require("scripts.state")
local I={}
local function prefs(player)
  local root=S.root();root.inserter_editors=root.inserter_editors or {};return root.inserter_editors
end
local function allowed(player,entity)
  return entity and entity.valid and entity.type=="inserter" and entity.force.index==player.force.index
    and settings.startup["sn-inserter-vectors"].value and entity.prototype.allow_custom_vectors
end
local function point(v) return {x=v.x or v[1],y=v.y or v[2]} end
local function rounded(n) return math.floor(n+.5) end
function I.close(player)
  for _,parent in ipairs({player.gui.screen,player.gui.relative}) do
    if parent then local f=parent.sn_inserter_editor;if f then f.destroy() end end
  end
  prefs(player)[player.index]=nil
end
function I.set(player,entity,kind,x,y)
  if not allowed(player,entity) or (kind~="pickup" and kind~="drop") then return false end
  if type(x)~="number" or type(y)~="number" or x~=math.floor(x) or y~=math.floor(y) or math.abs(x)>2 or math.abs(y)>2 or (x==0 and y==0) then return false end
  local other=kind=="pickup" and entity.drop_position or entity.pickup_position
  if rounded(other.x-entity.position.x)==x and rounded(other.y-entity.position.y)==y then return false end
  local target={x=entity.position.x+x,y=entity.position.y+y}
  if kind=="pickup" then entity.pickup_position=target else entity.drop_position=target end
  return true
end
function I.reset(player,entity)
  if not allowed(player,entity) then return false end
  local a=entity.direction*math.pi/8;local c,s=math.cos(a),math.sin(a)
  local function rotate(v)
    v=point(v)
    return {x=entity.position.x+math.max(-2,math.min(2,v.x*c-v.y*s)),y=entity.position.y+math.max(-2,math.min(2,v.x*s+v.y*c))}
  end
  entity.pickup_position=rotate(entity.prototype.inserter_pickup_position or {0,-1})
  entity.drop_position=rotate(entity.prototype.inserter_drop_position or {0,1})
  return true
end
function I.open(player,entity,relative)
  I.close(player)
  if not allowed(player,entity) then player.print({"sn-inserter.select"});return end
  local parent=relative and player.gui.relative or player.gui.screen
  local spec={type="frame",name="sn_inserter_editor",direction="vertical",caption={"sn-inserter.title"}}
  if relative then spec.anchor={gui=defines.relative_gui_type.inserter_gui,position=defines.relative_gui_position.right} end
  local f=parent.add(spec);if not relative then f.auto_center=true;player.opened=f end
  prefs(player)[player.index]={entity=entity,relative=relative}
  local text=f.add({type="label",name="sn_range_note",caption={"sn-inserter.range"}});text.style.single_line=false;text.style.maximal_width=380
  local row=f.add({type="flow",name="sn_vector_grids",direction="horizontal"})
  for _,kind in ipairs({"pickup","drop"}) do
    local column=row.add({type="flow",name="sn_"..kind.."_column",direction="vertical"})
    column.add({type="label",name="sn_"..kind.."_heading",caption={"sn-inserter."..kind}})
    local grid=column.add({type="table",name="sn_"..kind.."_grid",column_count=5})
    local selected=kind=="pickup" and entity.pickup_position or entity.drop_position
    local other=kind=="pickup" and entity.drop_position or entity.pickup_position
    for y=-2,2 do for x=-2,2 do
      local on=rounded(selected.x-entity.position.x)==x and rounded(selected.y-entity.position.y)==y
      local blocked=(x==0 and y==0) or (rounded(other.x-entity.position.x)==x and rounded(other.y-entity.position.y)==y)
      local button=grid.add({type="button",name="sn_vector_"..kind.."_"..x.."_"..y,caption=on and "●" or (x==0 and y==0 and "I" or "·"),
        tags={sn_vector=kind,x=x,y=y},enabled=not blocked,tooltip={"sn-inserter.offset",x,y}})
      button.style.width,button.style.height=31,31
    end end
  end
  local buttons=f.add({type="flow",name="sn_vector_actions",direction="horizontal"})
  buttons.add({type="button",name="sn_vector_reset",caption={"sn-inserter.reset"}})
  buttons.add({type="button",name="sn_vector_close",caption={"gui.close"}})
end
function I.opened(event)
  local player=game.get_player(event.player_index)
  if settings.startup["sn-inserter-vectors"].value and player and event.entity and event.entity.valid and event.entity.type=="inserter" then I.open(player,event.entity,true) end
end
function I.click(event)
  local player=game.get_player(event.player_index);local element=event.element
  if not player or not (element and element.valid) then return false end
  if element.name=="sn_vector_close" then I.close(player);return true end
  local record=prefs(player)[player.index];if not record then return false end
  if not allowed(player,record.entity) then I.close(player);return false end
  local tags=element.tags or {}
  if element.name=="sn_vector_reset" then I.reset(player,record.entity)
  elseif tags.sn_vector then I.set(player,record.entity,tags.sn_vector,tags.x,tags.y)
  else return false end
  I.open(player,record.entity,record.relative)
  return true
end
function I.refresh(event)
  local player=event.player_index and game.get_player(event.player_index)
  if player then local r=prefs(player)[player.index];if r and r.entity.valid then I.open(player,r.entity,r.relative) end end
end
return I
