local C = require("shared.constants")
local S = require("scripts.state")
local P = require("scripts.pollution")
local Habitat = require("shared.succession")
local T = {}
local harmless = {tree=true,corpse=true,["item-entity"]=true,["flying-text"]=true,["smoke-with-trigger"]=true}
local function clear(surface,position,margin)
  local entities=surface.find_entities_filtered({area={{position.x-margin,position.y-margin},{position.x+1+margin,position.y+1+margin}},limit=12})
  if #entities==12 then return false end
  for _,entity in ipairs(entities) do if not harmless[entity.type] then return false end end
  return true
end
function T.apply(rec,world,effect,cycles)
  if not effect.terrain or cycles<=0 then return end
  local entity=rec.entity
  if P.local_amount(entity.surface,entity.position)>C.air.green_limit then return end
  -- Actual productive installations support nearby habitat; they do not paint instant grass.
  rec.sequence=rec.sequence+1
  local x,y=math.floor(entity.position.x/32),math.floor(entity.position.y/32)
  local offset=rec.sequence%5
  local dx,dy=({{0,0},{1,0},{0,1},{-1,0},{0,-1}})[offset+1][1],({{0,0},{1,0},{0,1},{-1,0},{0,-1}})[offset+1][2]
  local index=world.chunk_keys and world.chunk_keys[(x+dx)..":"..(y+dy)]
  if index then world.chunks[index].nursery_until=game.tick+10*60*60 end
end
local function initialize_chunk(world,surface,chunk)
  if chunk.cover~=nil then return end
  local total,green=0,0
  for _,offset in ipairs({{4,4},{12,20},{20,12},{28,28}}) do
    local tile=surface.get_tile({x=chunk.x*32+offset[1],y=chunk.y*32+offset[2]})
    if C.safe_tiles[tile.name] and not tile.hidden_tile then total=total+1;if C.barren_tiles[tile.name] then green=green+1 end end
  end
  chunk.land=total>0
  -- Preserve old terrain on upgrade; a fresh barren expedition starts near zero.
  chunk.cover=world.native_outcome and Habitat.target(world) or (total>0 and green/total or 0)
  chunk.stress=0;chunk.ecology_tick=game.tick;chunk.trees=chunk.trees or {}
end
local function tree_life(world,surface,chunk,pollution,broods)
  local trees=chunk.trees or {};chunk.trees=trees
  local dead=chunk.dead_trees or {};chunk.dead_trees=dead
  for i=#dead,1,-1 do if not dead[i].valid then table.remove(dead,i) end end
  for i=#trees,1,-1 do if not trees[i].valid then table.remove(trees,i) end end
  if chunk.cover<.38 and chunk.stress>.35 and #trees>0 then
    local tree=table.remove(trees)
    if tree.valid then
      local pos=tree.position
      tree.destroy({raise_destroy=true})
      world.withered_trees=(world.withered_trees or 0)+1
      if prototypes.entity["dead-dry-hairy-tree"] then
        local stump=surface.create_entity({name="dead-dry-hairy-tree",position=pos,force="neutral"})
        if stump then dead[#dead+1]=stump end
      end
    end
    return
  end
  if not settings.global["sn-tree-growth"].value or chunk.cover<.64 or pollution>C.air.green_limit or broods then return end
  if game.tick-(chunk.tree_tick or 0)<5*60*60 or #trees>=8 then return end
  if #dead>0 then
    local stump=dead[#dead];local pos=stump.position;local name=C.profiles[world.planet].tree
    if name and clear(surface,pos,3) then
      stump.destroy({raise_destroy=false});table.remove(dead)
      if surface.can_place_entity({name=name,position=pos}) then
        local tree=surface.create_entity({name=name,position=pos,force="neutral",raise_built=false})
        if tree then trees[#trees+1]=tree;chunk.tree_tick=game.tick;world.grown_trees=world.grown_trees+1 end
      end
    end
    return
  end
  local x0,y0=chunk.x*32,chunk.y*32
  local pos={x=x0+4+(chunk.stripe*7)%24,y=y0+4+(chunk.stripe*11)%24}
  local tile=surface.get_tile(pos)
  local name=C.profiles[world.planet].tree
  if name and C.safe_tiles[tile.name] and not tile.hidden_tile and clear(surface,pos,3)
    and surface.count_entities_filtered({position=pos,radius=6,type="tree",limit=1})==0
    and surface.can_place_entity({name=name,position=pos}) then
    local tree=surface.create_entity({name=name,position=pos,force="neutral",raise_built=false})
    if tree then trees[#trees+1]=tree;chunk.tree_tick=game.tick;world.grown_trees=world.grown_trees+1 end
  end
end
function T.succession(world,surface,chunk,pollution)
  if not surface.is_chunk_generated({chunk.x,chunk.y}) then return end
  local profile=C.profiles[world.planet]
  if not profile.terrain then return end -- Aquilo never loses heat-supporting ice/foundations.
  initialize_chunk(world,surface,chunk)
  local minutes=math.max(0,game.tick-(chunk.ecology_tick or game.tick))/3600
  chunk.ecology_tick=game.tick
  local x0,y0=chunk.x*32,chunk.y*32
  local area={{x0-1,y0-1},{x0+33,y0+33}}
  local broods=surface.count_entities_filtered({area=area,force="enemy",type={"unit-spawner","unit"},limit=1})>0
  local bonus=world.terrain_bonus_until and game.tick<world.terrain_bonus_until and world.terrain_bonus or 1
  local supported=world.stage>=4 or (world.last_clean_operation and game.tick-world.last_clean_operation<15*60*60)
    or (chunk.nursery_until and game.tick<chunk.nursery_until)
  local before=chunk.cover
  Habitat.advance(chunk,world,pollution,minutes,supported and bonus or 0,broods)
  if not supported and chunk.cover>before then chunk.cover=before end
  if not settings.global["sn-living-terrain"].value then return end
  local occupants=surface.find_entities_filtered({area=area,limit=256})
  if #occupants>=256 then return end
  local blocked={}
  for _,entity in ipairs(occupants) do
    if entity.valid and not harmless[entity.type] then
      local b=entity.bounding_box
      local left=b and b.left_top or {x=entity.position.x-2,y=entity.position.y-2}
      local right=b and b.right_bottom or {x=entity.position.x+2,y=entity.position.y+2}
      for x=math.max(x0,math.floor(left.x)-1),math.min(x0+31,math.ceil(right.x)) do
        for y=math.max(y0,math.floor(left.y)-1),math.min(y0+31,math.ceil(right.y)) do blocked[x..":"..y]=true end
      end
    end
  end
  chunk.stripe=((chunk.stripe or 0)+1)%8
  local changes={}
  for offset=0,C.air.tile_batch-1 do
    local index=chunk.stripe*C.air.tile_batch+offset
    local pos={x=x0+index%32,y=y0+math.floor(index/32)}
    if not blocked[pos.x..":"..pos.y] then
      local tile=surface.get_tile(pos)
      if not tile.hidden_tile then
        local name
        if C.safe_tiles[tile.name] then name=Habitat.tile(pos.x,pos.y,chunk.cover,tile.name)
        elseif world.planet=="nauvis" and chunk.stress>.45 and (tile.name=="water" or tile.name=="deepwater") then name=tile.name.."-green"
        elseif world.planet=="nauvis" and chunk.stress<.15 and tile.name=="water-green" then name="water"
        elseif world.planet=="nauvis" and chunk.stress<.15 and tile.name=="deepwater-green" then name="deepwater" end
        if name and name~=tile.name then
          changes[#changes+1]={name=name,position=pos}
          if C.barren_tiles[name] then world.restored_tiles=world.restored_tiles+1
          elseif C.barren_tiles[tile.name] then world.degraded_tiles=(world.degraded_tiles or 0)+1 end
        end
      end
    end
  end
  if #changes>0 then surface.set_tiles(changes,false,false,false,false) end
  tree_life(world,surface,chunk,pollution,broods)
end
return T
