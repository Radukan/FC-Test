local C = require("shared.constants")
local K = require("shared.catalog")
local Model = require("shared.model")
local S = {}
function S.root() return storage.second_nature end
function S.init()
  storage.second_nature = storage.second_nature or {
    schema = C.schema, worlds = {}, planets = {}, machines = {}, buckets = {}, registrations = {}, players = {}, networks = {}, cursor = 0,
    visual_budget = 20, last_environment_tick = game.tick
  }
  local root = S.root()
  root.schema = C.schema
  for i = 1, C.bucket_count do root.buckets[i] = root.buckets[i] or {} end
  return root
end
function S.planet(surface)
  if not (surface and surface.valid and surface.planet) then return nil end
  local name = surface.planet.name
  return C.profiles[name] and name or nil
end
function S.world(surface)
  local name = S.planet(surface)
  if not name then return nil end
  local root = S.root()
  local world = root.worlds[surface.index]
  if not world then
    world = Model.new(name)
    world.surface_index, world.machine_count, world.active_count = surface.index, 0, 0
    world.machine_ids, world.beacon_ids = {}, {}
    root.worlds[surface.index], root.planets[name] = world, surface.index
    surface.set_property("sn-restoration-domain", 1)
    surface.set_property("sn-planet-identity", C.profiles[name].id)
    surface.set_property("sn-ecological-stage", world.stage)
    world.synced_stage = world.stage
  end
  return world
end
function S.by_planet(name)
  local root = S.root()
  return root.planets[name] and root.worlds[root.planets[name]] or nil
end
function S.recipe(entity)
  local recipe = entity.get_recipe()
  return recipe and recipe.name or nil
end
function S.register(entity)
  if not (entity and entity.valid and entity.unit_number and K.by_machine[entity.name]) then return end
  local root, id = S.root(), entity.unit_number
  if root.machines[id] then return root.machines[id] end
  local world = S.world(entity.surface)
  -- Do not silently terraform a platform, editor surface or third-party planet.
  if not world then return end
  local bucket = id % C.bucket_count + 1
  local list = root.buckets[bucket]
  local monitor = entity.type == "constant-combinator"
  -- Mining drills and laboratories are catalog machines but they never run a
  -- recipe and expose no products_finished counter, so they are tracked purely
  -- for placement/statistics and are skipped by the restoration processor.
  local inert = entity.type == "mining-drill" or entity.type == "lab"
  local recipe
  if not monitor and not inert then recipe = S.recipe(entity) end
  local rec = {entity = entity, id = id, surface_index = entity.surface.index, bucket = bucket, slot = #list + 1,
    produced = (monitor or inert) and 0 or entity.products_finished, recipe = recipe, sequence = 0, inert = inert,
    last_cycle = -C.beacon_freshness, active = false, monitor = monitor}
  rec.registration = script.register_on_object_destroyed(entity)
  root.registrations[rec.registration] = id
  list[#list + 1], root.machines[id], world.machine_ids[id] = id, rec, true
  world.machine_count = world.machine_count + 1
  if K.by_machine[entity.name].name == "planetary-beacon" then world.beacon_ids[id] = true end
  return rec
end
function S.remove(id)
  local root, rec = S.root(), S.root().machines[id]
  if not rec then return end
  local list = root.buckets[rec.bucket]
  local last_id = list[#list]
  list[rec.slot] = last_id
  list[#list] = nil
  if last_id ~= id and root.machines[last_id] then root.machines[last_id].slot = rec.slot end
  local world = root.worlds[rec.surface_index]
  if world then
    world.machine_ids[id], world.beacon_ids[id] = nil, nil
    world.machine_count = math.max(0, world.machine_count - 1)
    if rec.active then world.active_count = math.max(0, world.active_count - 1) end
  end
  if rec.garden and rec.garden.valid then rec.garden.destroy() end
  root.registrations[rec.registration], root.machines[id] = nil, nil
end
function S.active(rec, active)
  if rec.active == active then return end
  local world = S.root().worlds[rec.surface_index]
  if world then world.active_count = math.max(0, world.active_count + (active and 1 or -1)) end
  rec.active = active
end
function S.scan()
  -- A one-time install/configuration scan, never a periodic whole-map entity search.
  local names = {}
  for name in pairs(K.by_machine) do names[#names + 1] = name end
  table.sort(names)
  local surfaces = {}
  for _, surface in pairs(game.surfaces) do surfaces[#surfaces + 1] = surface end
  table.sort(surfaces, function(a, b) return a.index < b.index end)
  for _, surface in ipairs(surfaces) do
    local world = S.world(surface)
    if world then
      -- Reassert our own properties after prototype/configuration changes, never native climate properties.
      surface.set_property("sn-restoration-domain", 1)
      surface.set_property("sn-planet-identity", C.profiles[world.planet].id)
      surface.set_property("sn-ecological-stage", world.stage)
      world.synced_stage = world.stage
      local entities = surface.find_entities_filtered({name = names})
      table.sort(entities, function(a, b) return a.unit_number < b.unit_number end)
      for _, entity in ipairs(entities) do S.register(entity) end
    end
  end
end
function S.delete_surface(index)
  local root, world = S.root(), S.root().worlds[index]
  if not world then return end
  local ids = {}; for id in pairs(world.machine_ids) do ids[#ids + 1] = id end
  table.sort(ids)
  for _, id in ipairs(ids) do S.remove(id) end
  for _, entry in ipairs(world.groups) do if entry.group.valid then entry.group.destroy() end end
  root.worlds[index], root.planets[world.planet] = nil, nil
  for _, network in pairs(root.networks) do network.held = 0 end
end
function S.snapshot(name)
  local world = type(name) == "number" and S.root().worlds[name] or S.by_planet(name)
  if not world then return nil end
  return {planet = world.planet, surface_index = world.surface_index, values = table.deepcopy(world.values), stage = world.stage,
    score = world.score, toxicity = world.toxicity, pressure = world.pressure, ambient = world.ambient, cycles = world.cycles,
    machines = world.machine_count, active = world.active_count, restored_tiles = world.restored_tiles, grown_trees = world.grown_trees,
    removed_pollution = world.removed_pollution, contributions = table.deepcopy(world.contributions),
    air = world.air and table.deepcopy(world.air), landscape = world.landscape and table.deepcopy(world.landscape), generated_chunks = #(world.chunks or {}), native_outcome = world.native_outcome and table.deepcopy(world.native_outcome)}
end
return S
