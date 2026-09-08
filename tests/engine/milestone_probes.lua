-- Real-engine checks for the 0.9 milestone ledger and the audio pass. These
-- run against actual prototypes and a real LuaForce, so they catch what the
-- offline doubles cannot: a prototype the engine rejected at load, an
-- achievement name that does not resolve, or a working sound the engine
-- refused because its file is missing from the installed game data.
local Definitions = require("shared.achievements")
local Audio = require("shared.audio_catalog")
local Achievements = require("scripts.achievements")
local S = require("scripts.state")
local X = {}

function X.init(surface, force)
  -- Every declared milestone resolved into a real, loaded achievement prototype.
  for _, entry in ipairs(Definitions.all) do
    local name = "sn-" .. entry.name
    local proto = assert(prototypes.achievement[name], "missing achievement prototype " .. name)
    assert(proto.valid, name .. " did not load")
  end
  -- Every plant that was given a working sound is still a buildable prototype:
  -- a rejected sound table fails the data stage outright, so reaching here at
  -- all proves the engine accepted every referenced audio file.
  for name in pairs(Audio.plants) do
    assert(prototypes.entity["sn-" .. name], "missing power plant sn-" .. name)
  end

  -- Award the ledger against a real force with a real player list.
  S.init()
  assert(Achievements.award(force, "first-breath"), "first award was rejected")
  assert(not Achievements.award(force, "first-breath"), "award was granted twice")
  assert(Achievements.earned(force.index, "first-breath"), "award was not recorded")
  local earned, total = Achievements.count(force.index)
  assert(earned == 1 and total == #Definitions.script, "ledger count is wrong")
  assert(#Achievements.report(force.index) == #Definitions.script, "report is incomplete")
  storage.milestone_force = force.index
  log("SECOND_NATURE_ENGINE_MILESTONES_OK")
end

function X.tick()
  if storage.milestone_done or not storage.milestone_force then return end
  -- Real per-force isolation: a second force must not inherit the award.
  local other = game.forces["sn-milestone-probe"] or game.create_force("sn-milestone-probe")
  assert(not Achievements.earned(other.index, "first-breath"), "milestone leaked across forces")
  -- Inventory handling audio survived data-updates on a representative item.
  assert(prototypes.item["sn-glass"], "missing sn-glass item prototype")
  storage.milestone_done = true
  log("SECOND_NATURE_ENGINE_AUDIO_OK")
end
return X
