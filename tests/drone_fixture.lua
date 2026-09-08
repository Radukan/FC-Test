-- Focused LuaInventory / ghost doubles for field-drone accounting. These do not
-- claim native collision, controller or rendering behavior; engine probes cover that.
defines.input_action={build=1,build_rail=2,build_terrain=3,deconstruct=4,upgrade=5}
prototypes.item=prototypes.item or {}
prototypes.quality={normal={level=0},uncommon={level=1},rare={level=2},epic={level=3},legendary={level=5}}
for _,name in ipairs({'sn-field-drone','sn-field-controller','stone-wall','stone-brick','iron-plate','iron-chest','transport-belt','fast-transport-belt','underground-belt','fast-underground-belt','inserter','fast-inserter'}) do
  prototypes.item[name]={type='item',stack_size=name=='sn-field-controller' and 1 or (name=='sn-field-drone' and 200 or 100)}
end
prototypes.item['packed-vehicle']={type='item-with-entity-data',stack_size=1}
mock.inventories={};mock.spills={};mock.revivals={}
local function q(v) return type(v)=='table' and v.name or v or 'normal' end
function mock.inventory(size)
  local inv={valid=true}
  for i=1,size do
    local stack={valid_for_read=false,count=0}
    stack.clear=function() stack.valid_for_read=false;stack.count=0;stack.name=nil;stack.quality=nil end
    inv[i]=stack
  end
  inv.insert=function(spec)
    assert(inv.valid);local wanted=spec.count or 1;local inserted=0;local quality=q(spec.quality)
    local max=prototypes.item[spec.name] and prototypes.item[spec.name].stack_size or 100
    for i=1,#inv do
      local stack=inv[i]
      if stack.valid_for_read and stack.name==spec.name and q(stack.quality)==quality then
        local n=math.min(max-stack.count,wanted-inserted);stack.count=stack.count+n;inserted=inserted+n
      end
    end
    for i=1,#inv do
      local stack=inv[i]
      if not stack.valid_for_read and inserted<wanted then
        local n=math.min(max,wanted-inserted)
        stack.name=spec.name;stack.quality={name=quality};stack.count=n;stack.valid_for_read=true;inserted=inserted+n
      end
    end
    return inserted
  end
  inv.get_item_count=function(spec)
    assert(inv.valid);local count=0
    for i=1,#inv do
      local s=inv[i]
      if s.valid_for_read and (not spec or (s.name==(type(spec)=='string' and spec or spec.name) and q(s.quality)==q(type(spec)=='table' and spec.quality or nil))) then count=count+s.count end
    end
    return count
  end
  inv.remove=function(spec)
    assert(inv.valid);local count=0
    for i=1,#inv do
      local s=inv[i]
      if s.valid_for_read and s.name==spec.name and q(s.quality)==q(spec.quality) then
        local n=math.min(s.count,spec.count-count);s.count=s.count-n;count=count+n;if s.count==0 then s.clear() end
      end
    end
    return count
  end
  inv.get_contents=function()
    assert(inv.valid);local result={}
    for i=1,#inv do local s=inv[i];if s.valid_for_read then result[#result+1]={name=s.name,count=s.count,quality=q(s.quality)} end end
    return result
  end
  inv.destroy=function() assert(inv.valid);inv.valid=false end
  inv.clear=function() for i=1,#inv do inv[i].clear() end end
  mock.inventories[#mock.inventories+1]=inv
  return inv
end
game.create_inventory=mock.inventory
script.raise_script_built=function(event) mock.event("script_raised_built",event) end
local create=mock.entity
mock.entity=function(name,surface,pos,force,no_event)
  local e=create(name,surface,pos,force,no_event)
  e.quality={name='normal'};e.minable=true
  e.to_be_deconstructed=function() return e.marked or false end
  e.to_be_upgraded=function() return e.upgrade_target~=nil end
  e.is_registered_for_deconstruction=function(force) return e.marked and (not e.deconstruction_force or e.deconstruction_force==force) end
  if name=='sn-field-drone-worker' then e.type='simple-entity-with-owner';e.logistic_network=nil end
  e.teleport=function(pos)
    assert(e.valid)
    if e.teleport_blocked then return false end
    e.position={x=pos.x,y=pos.y};return true
  end
  return e
end
function mock.drone_surface(surface)
  surface.spill_item_stack=function(spec)
    assert(spec.allow_belts==false and spec.use_start_position_on_failure==true)
    local stack={name=spec.stack.name,count=spec.stack.count,quality=q(spec.stack.quality)}
    mock.spills[#mock.spills+1]=stack
    local item=mock.entity('item-on-ground',surface,{x=spec.position.x,y=spec.position.y},mock.neutral,true)
    item.type='item-entity';item.stack=stack
    return {item}
  end
end
mock.drone_surface(game.surfaces[1])
function mock.drone_player(index,drone_count,material_count,quality)
  local p=mock.player(index);p.connected=true;p.valid=true
  local character=mock.entity('character',p.surface,p.position,p.force,true);character.type='character'
  local inv=mock.inventory(80);p.character=character;p.inventory=inv
  character.get_main_inventory=function() return inv end
  p.get_main_inventory=character.get_main_inventory
  p.force.technologies['sn-field-robotics']={researched=true}
  inv.insert({name='sn-field-controller',count=1})
  inv.insert({name='sn-field-drone',count=drone_count or 1,quality=quality or 'normal'})
  inv.insert({name='stone-wall',count=material_count or 1,quality=quality or 'normal'})
  game.connected_players[#game.connected_players+1]=p
  return p
end
function mock.ghost(player,name,pos,quality,tile)
  local g=mock.entity(tile and 'tile-ghost' or 'entity-ghost',player.surface,pos,player.force,true)
  g.type=tile and 'tile-ghost' or 'entity-ghost';g.ghost_name=name;g.quality={name=quality or 'normal'}
  g.ghost_prototype={type='wall',items_to_place_this={{name=tile and 'stone-brick' or name,count=1}}}
  g.bounding_box={left_top={x=pos.x-.45,y=pos.y-.45},right_bottom={x=pos.x+.45,y=pos.y+.45}}
  g.to_be_deconstructed=function() return g.marked or false end
  g.revive=function(options)
    assert(g.valid and options.raise_revive and options.overflow and options.overflow.valid)
    if g.revive_error then error('deliberate native revival failure') end
    if g.blocked then return nil,nil,nil end
    local entity
    if not tile then
      entity=mock.entity(name,g.surface,g.position,g.force,true);entity.quality=g.quality
      entity.pickup_position=g.pickup_position;entity.drop_position=g.drop_position
      mock.event('script_raised_revive',{entity=entity})
    end
    g.valid=false;mock.revivals[#mock.revivals+1]={name=name,quality=q(g.quality),entity=entity,tile=tile}
    return {},entity,nil
  end
  return g
end
function mock.drone_steps(ticks)
  local D=require('scripts.field_drones')
  for _=1,ticks do game.tick=game.tick+1;D.tick() end
end
function mock.spill_count(name,quality)
  local n=0;for _,s in ipairs(mock.spills) do if s.name==name and s.quality==(quality or 'normal') then n=n+s.count end end;return n
end

function mock.drone_target(player,name,pos,contents)
  local e=mock.entity(name,player.surface,pos,player.force,true)
  e.type=name:find('underground') and 'underground-belt' or (name:find('belt') and 'transport-belt' or (name:find('inserter') and 'inserter' or 'container'))
  e.prototype={name=name,type=e.type,items_to_place_this={{name=name,count=1}}}
  e.contents=contents or {}
  e.mine=function(options)
    assert(options.inventory and options.force==false and options.raise_destroyed)
    if e.mine_blocked then return false end
    for _,stack in ipairs(e.contents) do
      local inserted=options.inventory.insert(stack);stack.count=stack.count-inserted
      if stack.count>0 then return false end
    end
    if options.inventory.insert({name=name,count=1,quality=q(e.quality)})~=1 then return false end
    mock.event('script_raised_destroy',{entity=e});e.destroy();return true
  end
  e.get_upgrade_target=function() return e.upgrade_target,{name=e.upgrade_quality or 'normal'} end
  e.apply_upgrade=function()
    if e.upgrade_blocked then return nil end
    local target=e.upgrade_target
    local new=mock.drone_target(player,target.name,e.position,e.contents)
    new.quality={name=e.upgrade_quality or 'normal'}
    new.pickup_position=e.pickup_position;new.drop_position=e.drop_position;new.saved_recipe=e.saved_recipe
    e.destroy()
    local other
    if e.upgrade_pair and e.neighbours and e.neighbours.valid then
      local old=e.neighbours;old.upgrade_target=target;old.upgrade_quality=e.upgrade_quality
      other=old.apply_upgrade()
    end
    return new,other
  end
  return e
end
