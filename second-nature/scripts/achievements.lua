-- Milestone ledger.
--
-- The engine can only be asked to unlock a plain "achievement" prototype, and
-- only for the local player, so this module records the award per force in
-- storage and calls unlock_achievement for every connected member of that
-- force. Rejoining players are reconciled on join, so an award earned while
-- offline is never lost and never granted twice.
--
-- Awards belong to the force that actually did the work. A force that never
-- ran a restoration cycle on a world does not inherit its neighbour's progress.
local C = require("shared.constants")
local Model = require("shared.model")
local Definitions = require("shared.achievements")
local S = require("scripts.state")
local A = {}

local function ledger()
  local root = S.root()
  root.achievements = root.achievements or {forces = {}}
  return root.achievements
end

local function force_record(force_index)
  local book = ledger()
  book.forces[force_index] = book.forces[force_index] or {}
  return book.forces[force_index]
end

-- Push every recorded award to a player. Cheap, idempotent, and the engine
-- ignores an unlock the player already has.
function A.sync(player)
  if not (player and player.valid) then return end
  local record = ledger().forces[player.force.index]
  if not record then return end
  for name in pairs(record) do
    if Definitions.by_name[name] then player.unlock_achievement("sn-" .. name) end
  end
end

-- Award a milestone to a force. Returns true only the first time.
function A.award(force, name)
  if not (force and force.valid and Definitions.by_name[name]) then return false end
  local record = force_record(force.index)
  if record[name] then return false end
  record[name] = game.tick
  local definition = Definitions.by_name[name]
  for _, player in pairs(force.players) do
    if player.valid and player.connected then player.unlock_achievement("sn-" .. name) end
  end
  force.print({"sn-message.milestone-earned", {"achievement-name.sn-" .. name}}, {color = C.colors.biodiversity})
  log("Second Nature milestone: " .. force.name .. " / " .. name .. " / " .. definition.title)
  return true
end

-- Award to every force with recorded restoration work on this world, so shared
-- planetary progress is not silently credited to whoever happened to be online.
function A.award_world(world, name)
  local granted = false
  for index in pairs(world.contributions or {}) do
    local force = game.forces[index]
    if force and force.valid then granted = A.award(force, name) or granted end
  end
  return granted
end

function A.earned(force_index, name)
  local record = ledger().forces[force_index]
  return record ~= nil and record[name] ~= nil
end

-- Called from the environment tick for each visited world.
function A.world_tick(world)
  if world.stage >= 1 then A.award_world(world, "first-breath") end
  if world.stage >= 3 then A.award_world(world, "root-systems") end
  if Model.ready(world) then A.award_world(world, "a-living-world") end
  if (world.grown_trees or 0) >= 1000 then A.award_world(world, "new-growth") end
  if (world.restored_tiles or 0) >= 10000 then A.award_world(world, "terraformer") end
  if (world.removed_pollution or 0) >= 50000 then A.award_world(world, "deep-green") end
end

-- Five field stations is a per-force expedition milestone: the force must have
-- actually worked on every world, not merely have someone standing on it.
function A.network_tick()
  local reached = {}
  for _, planet in ipairs(C.planets) do
    local world = S.by_planet(planet)
    if not world then return end
    for index, cycles in pairs(world.contributions or {}) do
      if cycles > 0 then reached[index] = (reached[index] or 0) + 1 end
    end
  end
  for index, count in pairs(reached) do
    local force = game.forces[index]
    if count == #C.planets and force and force.valid then A.award(force, "field-stations") end
  end
end

function A.migrate(source_index, destination)
  local book = ledger()
  local from, into = book.forces[source_index], force_record(destination.index)
  if from then
    for name, tick in pairs(from) do into[name] = math.min(into[name] or tick, tick) end
    book.forces[source_index] = nil
  end
  for _, player in pairs(destination.players) do if player.connected then A.sync(player) end end
end

function A.report(force_index)
  local record = ledger().forces[force_index] or {}
  local result = {}
  for _, x in ipairs(Definitions.script) do
    result[#result + 1] = {name = x.name, title = x.title, description = x.description,
      earned = record[x.name] ~= nil, at = record[x.name]}
  end
  return result
end

function A.count(force_index)
  local record = ledger().forces[force_index] or {}
  local earned = 0
  for _ in pairs(record) do earned = earned + 1 end
  return earned, #Definitions.script
end
return A
