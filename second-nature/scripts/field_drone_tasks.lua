-- Planner jobs for personal, inventory-fed field drones. No logistic network.
local S=require("scripts.state")
local Machines=require("scripts.machines")
local SolarRail=require("scripts.solar_rail")
local T={}
local function q(value) return type(value)=="string" and value or (value and value.name or "normal") end
local function near(a,b) return (a.x-b.x)^2+(a.y-b.y)^2<.0001 end
local function plain_item(name)
  local p=prototypes.item[name]
  return p and (p.type=="item" or p.type=="rail-planner") and not (p.get_spoil_ticks and p.get_spoil_ticks()>0)
end
local function placement(prototype,quality,inventory,multiplier)
  for _,item in ipairs(prototype.items_to_place_this or {}) do
    local count=item.count*(multiplier or 1)
    if plain_item(item.name) and count>=1 and count<=20 then
      local stack={name=item.name,count=count,quality=quality}
      if not inventory or inventory.get_item_count({name=item.name,quality=quality})>=count then return stack end
    end
  end
end
local function loose(ghost)
  return #ghost.surface.find_entities_filtered({area=ghost.bounding_box,type="item-entity",limit=1})>0
end
local function permitted(e,ctx)
  if not (e and e.valid and e.surface.index==ctx.surface.index) then return false end
  if (e.position.x-ctx.position.x)^2+(e.position.y-ctx.position.y)^2>ctx.range^2 then return false end
  return e.force.index==ctx.force.index or e.force.name=="neutral"
end
local function return_part(e)
  local item=placement(e.prototype,q(e.quality))
  if not item then return nil end
  return {item=item,position={x=e.position.x,y=e.position.y},name=e.name,unit_number=e.unit_number}
end
function T.kind(e)
  if e.type=="entity-ghost" or e.type=="tile-ghost" then return "build" end
  if e.to_be_deconstructed() then return "deconstruct" end
  if e.to_be_upgraded() then return "upgrade" end
end
function T.inspect(e,ctx,inventory)
  if not permitted(e,ctx) then return nil end
  local kind=T.kind(e)
  if kind=="build" then
    if e.force.index~=ctx.force.index or e.to_be_deconstructed() then return nil end
    if e.type=="tile-ghost" and not ctx.tiles then return nil end
    if e.type=="entity-ghost" and not ctx.rails and e.ghost_prototype.type:find("rail",1,true) then return nil end
    if loose(e) then return nil,"loose-items" end
    local item=placement(e.ghost_prototype,q(e.quality),inventory)
    if not item then return nil,"materials" end
    return {kind=kind,material=item,product=e.ghost_name,product_quality=q(e.quality)}
  elseif kind=="deconstruct" then
    if not (ctx.deconstruct and e.minable and e.is_registered_for_deconstruction(ctx.force)) then return nil end
    if e.name=="sn-lander" or e.name=="sn-field-drone-worker" or e.type=="character" then return nil end
    return {kind=kind}
  elseif kind=="upgrade" then
    if not ctx.upgrade or not e.minable or e.force.index~=ctx.force.index then return nil end
    local target,quality=e.get_upgrade_target()
    if not target then return nil end
    -- Packed vehicles/rolling stock and multi-part rails are left untouched.
    local old=return_part(e);if not old or e.type:find("rail",1,true) then return nil,"materials" end
    local parts={old}
    if e.type=="underground-belt" then
      local neighbour=e.neighbours
      if neighbour and neighbour.valid and neighbour.force.index==ctx.force.index then
        local other=return_part(neighbour)
        if not other then return nil,"materials" end
        parts[#parts+1]=other
      end
    end
    local item=placement(target,q(quality),inventory,#parts)
    if not item then return nil,"materials" end
    return {kind=kind,material=item,product=target.name,product_quality=q(quality),old_parts=parts,
      unit_cost=item.count/#parts}
  end
end
function T.valid(rec,ctx)
  local e=rec.target
  if not permitted(e,ctx) then return false end
  local kind=rec.kind or "build"
  if kind=="build" then
    if e.type~="entity-ghost" and e.type~="tile-ghost" then return false end
    return e.force.index==ctx.force.index and not e.to_be_deconstructed()
      and (not rec.product or e.ghost_name==rec.product)
      and (not rec.product_quality or q(e.quality)==rec.product_quality)
      and (e.type~="tile-ghost" or ctx.tiles)
  elseif kind=="deconstruct" then
    return ctx.deconstruct and e.minable and e.to_be_deconstructed() and e.is_registered_for_deconstruction(ctx.force)
  elseif kind=="upgrade" then
    if not (ctx.upgrade and e.minable and e.force.index==ctx.force.index and e.to_be_upgraded()) then return false end
    if e.name~=rec.old_parts[1].name or q(e.quality)~=rec.old_parts[1].item.quality then return false end
    if rec.old_parts[2] then
      local n=e.neighbours;local old=rec.old_parts[2]
      if not (n and n.valid and near(n.position,old.position) and n.name==old.name and q(n.quality)==old.item.quality) then return false end
    end
    local target,quality=e.get_upgrade_target()
    return target and target.name==rec.product and q(quality)==rec.product_quality
  end
  return false
end
function T.perform(rec,ctx)
  if not T.valid(rec,ctx) then return false end
  local e=rec.target;local kind=rec.kind or "build"
  if kind=="deconstruct" then
    -- Native mining preserves inventories, item metadata and quality. A partial
    -- unload is returned normally and a later sortie can finish a full chest.
    SolarRail.flush(e)
    local ok,done=pcall(function() return e.mine({inventory=rec.cargo,force=false,raise_destroyed=true}) end)
    if not ok then log("Second Nature: field deconstruction failed without discarding its cargo.") end
    return ok and done
  end
  if kind=="build" and loose(e) then return false end
  if rec.cargo.get_item_count({name=rec.material.name,quality=rec.material.quality})<rec.material.count then return false end
  rec.cargo.remove(rec.material)
  if kind=="build" then
    local ok,_,revived=pcall(function() return e.revive({raise_revive=true,overflow=rec.cargo}) end)
    local done=revived~=nil or not e.valid
    if not done then rec.cargo.insert(rec.material) end
    if not ok then log("Second Nature: a field revival failed; its reservation was reconciled.") end
    return done
  end
  Machines.flush(e)
  local ok,first,second=pcall(function() return e.apply_upgrade() end)
  if not ok or not first then
    rec.cargo.insert(rec.material)
    if not ok then log("Second Nature: field upgrade failed; reserved materials were returned.") end
    return false
  end
  local changed={first};if second then changed[#changed+1]=second end
  local cost=rec.unit_cost*#changed
  assert(cost<=rec.material.count,"Field upgrade exceeded its reserved material")
  if cost<rec.material.count then
    rec.cargo.insert({name=rec.material.name,quality=rec.material.quality,count=rec.material.count-cost})
  end
  for i,new in ipairs(changed) do
    local old=rec.old_parts[i]
    if new.valid then
      for _,part in ipairs(rec.old_parts) do if near(new.position,part.position) then old=part;break end end
    end
    assert(old,"Field upgrade has no corresponding old item")
    assert(rec.cargo.insert(old.item)==old.item.count,"Field upgrade return did not fit escrow")
    if old.unit_number then S.remove(old.unit_number) end
    if new.valid then S.register(new);script.raise_script_built({entity=new}) end
  end
  return true
end
return T
