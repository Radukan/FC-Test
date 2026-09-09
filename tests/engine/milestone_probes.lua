-- Real-engine checks for the 0.9 milestone ledger and the audio pass. These
-- run against actual prototypes and a real LuaForce, so they catch what the
-- offline doubles cannot: a prototype the engine rejected at load, an
-- achievement name that does not resolve, or a working sound the engine
-- refused because its file is missing from the installed game data.
--
-- The earlier campaign/native probes deliberately drive real award paths, so
-- the shared player force already holds milestones by the time this runs. The
-- ledger assertions therefore use a dedicated force and measure deltas rather
-- than assuming an empty starting record.
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

  S.init()
  -- The real campaign and native probes already awarded through production code
  -- paths, so the shared force must show a non-empty, well-formed ledger.
  local shared_earned, shared_total = Achievements.count(force.index)
  assert(shared_total == #Definitions.script, "ledger total is not the scripted milestone count")
  assert(shared_earned > 0, "earlier real campaign probes recorded no milestone at all")
  assert(shared_earned <= shared_total, "ledger counted more awards than declared milestones")
  assert(Achievements.earned(force.index, "signal-restored"),
    "the real rocket handler did not record its milestone")

  -- Award against a dedicated real force so the counts are exact and this probe
  -- cannot be perturbed by whatever the earlier scenarios happened to earn.
  local ledger_force = game.forces["sn-milestone-ledger"] or game.create_force("sn-milestone-ledger")
  assert(select(1, Achievements.count(ledger_force.index)) == 0, "a fresh force started with awards")
  assert(Achievements.award(ledger_force, "first-breath"), "first award was rejected")
  assert(not Achievements.award(ledger_force, "first-breath"), "award was granted twice")
  assert(Achievements.earned(ledger_force.index, "first-breath"), "award was not recorded")
  local earned, total = Achievements.count(ledger_force.index)
  assert(earned == 1 and total == #Definitions.script, "ledger count is wrong: " .. earned .. "/" .. total)
  assert(#Achievements.report(ledger_force.index) == #Definitions.script, "report is incomplete")
  -- An unknown name is refused rather than silently stored.
  assert(not Achievements.award(ledger_force, "not-a-milestone"), "an undeclared milestone was awarded")
  assert(select(1, Achievements.count(ledger_force.index)) == 1, "a rejected award still changed the ledger")

  storage.milestone_force = ledger_force.index
  storage.milestone_shared_force = force.index
  storage.milestone_shared_earned = shared_earned
  log("SECOND_NATURE_ENGINE_MILESTONES_OK")
end

function X.tick()
  if storage.milestone_done or not storage.milestone_force then return end
  -- Real per-force isolation: a third force must not inherit either ledger.
  local other = game.forces["sn-milestone-probe"] or game.create_force("sn-milestone-probe")
  assert(not Achievements.earned(other.index, "first-breath"), "milestone leaked across forces")
  assert(select(1, Achievements.count(other.index)) == 0, "an untouched force accumulated awards")
  assert(Achievements.earned(storage.milestone_force, "first-breath"), "the ledger lost its award")

  -- A real merge keeps the earlier award and empties the source record.
  local donor = game.forces["sn-milestone-donor"] or game.create_force("sn-milestone-donor")
  assert(Achievements.award(donor, "root-systems"), "donor award was rejected")
  Achievements.migrate(donor.index, other)
  assert(Achievements.earned(other.index, "root-systems"), "merge did not transfer the award")
  assert(not Achievements.earned(donor.index, "root-systems"), "merge left the source record populated")

  -- Inventory handling audio survived data-updates on a representative item.
  assert(prototypes.item["sn-glass"], "missing sn-glass item prototype")
  storage.milestone_done = true
  log("SECOND_NATURE_ENGINE_AUDIO_OK")
end
return X
