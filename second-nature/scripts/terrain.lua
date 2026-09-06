local C = require("shared.constants")
local S = require("scripts.state")
local T = {}
local harmless = {tree = true, corpse = true, ["item-entity"] = true, ["flying-text"] = true, ["smoke-with-trigger"] = true}
local function clear(surface, position, margin)
  local area = {{position.x - margin, position.y - margin}, {position.x + 1 + margin, position.y + 1 + margin}}
  -- Limit the work. More entities than this is itself a good reason not to alter a tile.
  local entities = surface.find_entities_filtered({area = area, limit = 12})
  if #entities == 12 then return false end
  for _, entity in ipairs(entities) do if not harmless[entity.type] then return false end end
  return true
end
function T.apply(rec, world, effect, cycles)
  if not settings.global["sn-living-terrain"].value then return end
  local entity, profile, root = rec.entity, C.profiles[world.planet], S.root()
  if effect.garden and world.stage >= 1 and not (rec.garden and rec.garden.valid) then
    rec.garden = rendering.draw_sprite({sprite = "sn-garden", target = {entity = entity, offset = {0, -0.2}}, surface = entity.surface,
      render_layer = "higher-object-above", x_scale = 0.46, y_scale = 0.46})
  end
  if not effect.terrain or not profile.terrain or world.stage < 2 or root.visual_budget <= 0 then return end
  local radius = world.stage >= 4 and 64 or (world.stage >= 3 and 48 or 32)
  for _ = 1, math.min(3, cycles, root.visual_budget) do
    root.visual_budget = root.visual_budget - 1
    rec.sequence = rec.sequence + 1
    -- Stable per-entity spatial sequence, independent of global random state and GUI activity.
    local hash = (rec.id * 48271 + rec.sequence * 69621) % 2147483647
    local angle = (hash % 6283) / 1000
    local distance = 9 + ((math.floor(hash / 6283) + rec.sequence * 17) % (radius - 8))
    local pos = {x = math.floor(entity.position.x + math.cos(angle) * distance), y = math.floor(entity.position.y + math.sin(angle) * distance)}
    local surface = entity.surface
    if surface.is_chunk_generated({math.floor(pos.x / 32), math.floor(pos.y / 32)}) then
      local tile = surface.get_tile(pos)
      if C.safe_tiles[tile.name] and not tile.hidden_tile and clear(surface, pos, 0.25) then
        if tile.name ~= profile.terrain then
          -- No collision correction, no removal of entities/decoratives, no raised build events.
          surface.set_tiles({{name = profile.terrain, position = pos}}, false, false, false, false)
          world.restored_tiles = world.restored_tiles + 1
        end
        if effect.trees and world.stage >= 3 and settings.global["sn-tree-growth"].value and rec.sequence % 5 == 0
          and clear(surface, pos, 3) and surface.count_entities_filtered({position = pos, radius = 6, type = "tree", limit = 1}) == 0 then
          local location = {x = pos.x + 0.5, y = pos.y + 0.5}
          if prototypes.entity[profile.tree] and surface.can_place_entity({name = profile.tree, position = location}) then
            local tree = surface.create_entity({name = profile.tree, position = location, force = "neutral", raise_built = false})
            if tree then world.grown_trees = world.grown_trees + 1 end
          end
        end
      end
    end
  end
end
return T
