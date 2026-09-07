-- Inventory-fed construction only. No roboports, logistic cells, chest access,
-- delivery requests, mining, repair or item-request-proxy fulfillment.
local C = require("shared.field_drones")
local S = require("scripts.state")
local D = {}
local function root() return S.root().field_drones end
local function ids(t)
  local result={};for id in pairs(t) do result[#result+1]=id end;table.sort(result);return result
end
local function position(p) return {x=p.x,y=p.y} end
local function distance2(a,b) return (a.x-b.x)^2+(a.y-b.y)^2 end
local function quality(q) return type(q)=="string" and q or (q and q.name or "normal") end
local function owner(index)
  local r=root()
  r.owners[index]=r.owners[index] or {enabled=false,workers={},active=0,cell=0,built=0,reason="off",pending={},pending_keys={},head=1}
  return r.owners[index]
end
local function carried(inv,name)
  local choices={}
  for _,item in pairs(inv.get_contents()) do
    if item.name==name and item.count>0 then choices[#choices+1]={name=name,count=1,quality=quality(item.quality)} end
  end
  table.sort(choices,function(a,b)
    local aq=prototypes.quality and prototypes.quality[a.quality]
    local bq=prototypes.quality and prototypes.quality[b.quality]
    local al=aq and aq.level or (a.quality=="normal" and 0 or 1)
    local bl=bq and bq.level or (b.quality=="normal" and 0 or 1)
    return al==bl and a.quality<b.quality or al<bl
  end)
  return choices[1]
end
local function context(player)
  if not (player and player.valid~=false and player.connected and player.controller_type==defines.controllers.character) then return nil,"character" end
  local character=player.character
  if not (character and character.valid and character.type=="character" and character.force.index==player.force.index) then return nil,"character" end
  local permissions=player.permission_group
  if permissions and not permissions.allows_action(defines.input_action.build) then return nil,"permission" end
  local tech=player.force.technologies[C.technology]
  if not (tech and tech.researched) then return nil,"research" end
  local inv=character.get_main_inventory()
  if not (inv and inv.valid and carried(inv,C.controller)) then return nil,"controller" end
  if character.surface.platform then return nil,"platform" end
  return {character=character,inventory=inv,surface=character.surface,position=character.position,force=player.force,
    tiles=not permissions or permissions.allows_action(defines.input_action.build_terrain),
    rails=not permissions or permissions.allows_action(defines.input_action.build_rail)}
end
function D.limit(player)
  local current=game.get_player(player.index)
  local setting=current and settings.get_player_settings(current)["sn-field-drone-limit"]
  return math.max(1,math.min(C.maximum_limit,math.floor(setting and setting.value or C.default_limit)))
end
local function ghost_key(ghost)
  if ghost.unit_number then return "entity:"..ghost.unit_number end
  return table.concat({ghost.surface.index,ghost.type,ghost.position.x,ghost.position.y,ghost.ghost_name},":")
end
local function loose_items(ghost)
  -- Early assistants cannot collect loose items. Do not let revive delete or
  -- implicitly transport a stranger's dropped cargo beneath a blueprint.
  return #ghost.surface.find_entities_filtered({area=ghost.bounding_box,type="item-entity",limit=1})>0
end
local function valid_target(ghost,ctx)
  if ghost and ghost.valid then
    if ghost.type=="tile-ghost" and not ctx.tiles then return false end
    if ghost.type=="entity-ghost" and not ctx.rails and ghost.ghost_prototype.type:find("rail",1,true) then return false end
  end
  return ghost and ghost.valid and (ghost.type=="entity-ghost" or ghost.type=="tile-ghost")
    and ghost.surface.index==ctx.surface.index and ghost.force.index==ctx.force.index
    and distance2(ghost.position,ctx.position)<=C.range*C.range and not ghost.to_be_deconstructed()
end
local function material(ghost,inv)
  local q=quality(ghost.quality)
  for _,item in ipairs(ghost.ghost_prototype.items_to_place_this or {}) do
    local prototype=prototypes.item[item.name]
    -- Specialized packed vehicles/inventories have state that revive alone
    -- cannot restore. Leave those to native construction, never flatten them.
    if prototype and prototype.type=="item" and item.count>=1 and item.count<=10 then
      local stack={name=item.name,count=item.count,quality=q}
      if inv.get_item_count({name=stack.name,quality=q})>=stack.count then return stack end
    end
  end
end
local function animation(rec,working)
  local name=working and "sn-field-drone-work" or "sn-field-drone-flight"
  if not (rec.visual and rec.visual.valid) then
    rec.visual=rendering.draw_animation({animation=name,target={entity=rec.entity},surface=rec.surface,
      render_layer="air-object",animation_speed=.3})
  elseif rec.animation_name~=name then rec.visual.animation=name end
  if not (rec.shadow and rec.shadow.valid) then
    rec.shadow=rendering.draw_animation({animation=name.."-shadow",target={entity=rec.entity},surface=rec.surface,
      render_layer="ground-patch-higher",animation_speed=.3})
  elseif rec.animation_name~=name then rec.shadow.animation=name.."-shadow" end
  rec.animation_name=name
end

local function refund(rec,player,drop_only)
  local cargo=rec.cargo
  if not (cargo and cargo.valid) then return end
  local character=player and player.character
  if not (character and character.valid) then character=rec.character end
  local inv=not drop_only and character and character.valid and character.get_main_inventory() or nil
  local surface=rec.surface
  local at=rec.last_position
  if not (surface and surface.valid) and character and character.valid then surface=character.surface;at=character.position end
  for i=1,#cargo do
    local stack=cargo[i]
    if stack.valid_for_read then
      local before=stack.count
      local inserted=inv and inv.valid and inv.insert(stack) or 0
      if inserted>=before then stack.clear()
      else
        stack.count=before-inserted
        if surface and surface.valid then
          surface.spill_item_stack({position=at,stack=stack,enable_looted=true,allow_belts=false,
            max_radius=2,use_start_position_on_failure=true,drop_full_stack=true})
        end
        stack.clear()
      end
    end
  end
  cargo.destroy()
end
local function discard(rec,destroy_entity)
  local r=root();local o=r.owners[rec.owner]
  if r.claims[rec.key]==rec.id then r.claims[rec.key]=nil end
  if r.workers[rec.id] then r.workers[rec.id]=nil;r.active=math.max(0,r.active-1) end
  if o and o.workers[rec.id] then o.workers[rec.id]=nil;o.active=math.max(0,o.active-1) end
  if rec.visual and rec.visual.valid then rec.visual.destroy() end
  if rec.shadow and rec.shadow.valid then rec.shadow.destroy() end
  if destroy_entity and rec.entity and rec.entity.valid then rec.entity.destroy() end
end
local function finish(rec,player)
  refund(rec,player,false)
  discard(rec,true)
end
local function lost(rec)
  -- An actual destroyed drone is lost; its unspent construction cargo is not.
  if rec.cargo and rec.cargo.valid then rec.cargo.remove(rec.drone_item) end
  refund(rec,nil,true)
  discard(rec,false)
end
function D.init()
  local state=S.root()
  state.field_drones=state.field_drones or {owners={},workers={},claims={},active=0}
  local r=root();r.active=0;r.claims={}
  for _,o in pairs(r.owners) do o.workers={};o.active=0;o.pending={};o.pending_keys={};o.head=1 end
  for _,id in ipairs(ids(r.workers)) do
    local rec=r.workers[id];local o=owner(rec.owner)
    r.active=r.active+1;o.active=o.active+1;o.workers[id]=true;r.claims[rec.key]=id
  end
end
function D.cancel(index)
  if not root() then return end
  local o=root().owners[index];if not o then return end
  local player=game.get_player(index)
  o.pending={};o.pending_keys={};o.head=1
  for _,id in ipairs(ids(o.workers)) do local rec=root().workers[id];if rec then finish(rec,player) end end
end
function D.remove_player(index)
  D.cancel(index);root().owners[index]=nil
end
function D.surface_removed(index)
  for _,id in ipairs(ids(root().workers)) do
    local rec=root().workers[id]
    if rec.surface.index==index then finish(rec,game.get_player(rec.owner)) end
  end
end
function D.entity_died(event)
  local entity=event.entity
  local rec=entity and entity.valid and entity.unit_number and root().workers[entity.unit_number]
  if rec then rec.last_position=position(entity.position);lost(rec) end
end
function D.set_enabled(player,enabled)
  if not player then return false end
  local o=owner(player.index)
  if enabled then
    local ctx,reason=context(player)
    if not ctx then o.reason=reason;player.print({"sn-drones."..reason});return false end
  else D.cancel(player.index) end
  o.enabled=enabled;o.reason=enabled and "waiting" or "off"
  player.set_shortcut_toggled("sn-field-drones",enabled)
  return true
end
function D.toggle(player)
  return D.set_enabled(player,not owner(player.index).enabled)
end
local function take(inv,cargo,stack)
  local got=inv.remove(stack)
  if got>0 then
    local inserted=cargo.insert({name=stack.name,quality=stack.quality,count=got})
    assert(inserted==got,"Field drone reservation did not fit its escrow")
  end
  return got==stack.count
end
local function launch(player,ctx,ghost,stack,limit)
  local r,o=root(),owner(player.index)
  if o.active>=limit or r.active>=C.global_limit then return false end
  local key=ghost_key(ghost)
  if r.claims[key] then return false end
  local drone=carried(ctx.inventory,C.item);if not drone then return false end
  local cargo=game.create_inventory(C.cargo_slots)
  local rec={owner=player.index,character=ctx.character,surface=ctx.surface,force_index=ctx.force.index,
    cargo=cargo,drone_item=drone,material=stack,target=ghost,key=key,stage="outbound",started=game.tick,
    last_position=position(ctx.position)}
  if not take(ctx.inventory,cargo,drone) or not take(ctx.inventory,cargo,stack) then refund(rec,player,false);return false end
  local entity=ctx.surface.create_entity({name=C.entity,position=ctx.position,force=ctx.force})
  if not entity then refund(rec,player,false);return false end
  rec.entity=entity;rec.id=assert(entity.unit_number,"Field drone needs a unit number")
  r.workers[rec.id]=rec;r.claims[key]=rec.id;r.active=r.active+1;o.workers[rec.id]=true;o.active=o.active+1
  animation(rec,false)
  return true
end
local function build(rec,ctx)
  local ghost=rec.target
  if not valid_target(ghost,ctx) or loose_items(ghost) then return false end
  if rec.cargo.get_item_count({name=rec.material.name,quality=rec.material.quality})<rec.material.count then return false end
  -- Reserve at dispatch, consume at arrival. Native revive keeps blueprint
  -- recipes, directions, wires and inserter vectors; never create a replacement.
  rec.cargo.remove(rec.material)
  local ok,_,revived=pcall(function() return ghost.revive({raise_revive=true,overflow=rec.cargo}) end)
  local succeeded=revived~=nil or not ghost.valid
  if not succeeded then rec.cargo.insert(rec.material) end
  if not ok then log("Second Nature: a field-drone revival failed; its reservation was reconciled.") end
  return succeeded
end
local function move(rec,at)
  local from=rec.entity.position;local dx,dy=at.x-from.x,at.y-from.y
  local distance=math.sqrt(dx*dx+dy*dy);local step=C.speed*C.step_ticks
  if distance<=step then
    if not rec.entity.teleport(at) then return nil end
    rec.last_position=position(at);return true
  end
  local to={x=from.x+dx/distance*step,y=from.y+dy/distance*step}
  if not rec.entity.teleport(to) then return nil end
  rec.last_position=to
  return false
end
function D.step_player(player,index)
  index=index or (player and player.index)
  local o=index and root().owners[index];if not o then return end
  if not o.enabled then
    if o.active>0 then D.cancel(index) end
    o.reason="off";return
  end
  local ctx,reason=context(player)
  if not ctx then
    if o.active>0 then D.cancel(index) end
    o.reason=reason;return
  end
  local limit=D.limit(player)
  for _,id in ipairs(ids(o.workers)) do
    local rec=root().workers[id]
    if not (rec.entity and rec.entity.valid) then lost(rec)
    elseif rec.force_index~=ctx.force.index or rec.surface.index~=ctx.surface.index or game.tick-rec.started>C.lifetime_ticks then finish(rec,player)
    elseif o.active>limit then finish(rec,player)
    else
      animation(rec,rec.stage=="working")
      if rec.stage~="returning" and not valid_target(rec.target,ctx) then rec.stage="returning" end
      if rec.stage=="outbound" then
        local arrived=move(rec,rec.target.position)
        if arrived==nil then finish(rec,player)
        elseif arrived then rec.stage="working";rec.ready=game.tick+C.work_ticks;animation(rec,true) end
      elseif rec.stage=="working" then
        if game.tick>=rec.ready then
          if build(rec,ctx) then o.built=o.built+1 end
          rec.stage="returning";animation(rec,false)
        end
      elseif rec.stage=="returning" then
        local arrived=move(rec,ctx.position)
        if arrived or arrived==nil then finish(rec,player) end
      end
    end
  end
  o.reason=o.active>0 and "working" or "waiting"
  if o.active>=limit or root().active>=C.global_limit then return end
  if not carried(ctx.inventory,C.item) then o.reason="no-drones";return end
  if game.tick%C.scan_ticks==0 then
    -- A bounded, rotating spatial scan feeds a separate dispatch queue. A dense
    -- blueprint can use the whole crew, not just eight drones per scan cycle.
    local cell=o.cell;o.cell=(cell+1)%16
    local width=C.range/2
    local x=ctx.position.x-C.range+(cell%4)*width
    local y=ctx.position.y-C.range+math.floor(cell/4)*width
    local ghosts=ctx.surface.find_entities_filtered({area={{x,y},{x+width,y+width}},
      type={"entity-ghost","tile-ghost"},force=ctx.force,limit=C.scan_limit})
    table.sort(ghosts,function(a,b)
      local da,db=distance2(a.position,ctx.position),distance2(b.position,ctx.position)
      return da==db and ghost_key(a)<ghost_key(b) or da<db
    end)
    for _,ghost in ipairs(ghosts) do
      if #o.pending-o.head+1>=C.queue_limit then break end
      local key=ghost_key(ghost)
      if valid_target(ghost,ctx) and not root().claims[key] and not o.pending_keys[key] then
        o.pending[#o.pending+1]={entity=ghost,key=key};o.pending_keys[key]=true
      end
    end
  end
  local examined=0
  while o.head<=#o.pending and examined<C.dispatch_budget and o.active<limit do
    local entry=o.pending[o.head];o.pending[o.head]=false;o.head=o.head+1
    o.pending_keys[entry.key]=nil;examined=examined+1
    local ghost=entry.entity
    if valid_target(ghost,ctx) and not root().claims[entry.key] then
      if loose_items(ghost) then o.reason="loose-items"
      else
        local stack=material(ghost,ctx.inventory)
        if stack and launch(player,ctx,ghost,stack,limit) then o.reason="working"
        elseif not stack and o.active==0 then o.reason="materials" end
      end
    end
  end
  if o.head>#o.pending then o.pending={};o.pending_keys={};o.head=1
  elseif o.head>128 then
    local remaining={};for i=o.head,#o.pending do remaining[#remaining+1]=o.pending[i] end
    o.pending=remaining;o.head=1
  end
end
function D.tick()
  if not root() then return end
  for _,index in ipairs(ids(root().owners)) do D.step_player(game.get_player(index),index) end
end
function D.status(player)
  local o=owner(player.index)
  local stock=0;local character=player.character
  local inv=character and character.valid and character.get_main_inventory()
  if inv then for _,entry in pairs(inv.get_contents()) do if entry.name==C.item then stock=stock+entry.count end end end
  return {enabled=o.enabled,active=o.active,stock=stock,limit=D.limit(player),built=o.built,reason=o.reason}
end
return D
