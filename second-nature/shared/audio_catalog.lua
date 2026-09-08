-- Working-sound assignments, declared once and shared by the prototype stage,
-- the documentation generator and the tests.
--
-- Every filename below is a stock Factorio 2.0 asset shipped with base or
-- Space Age. Nothing is copied into this mod and no path is invented: each one
-- is referenced by an upstream prototype in the pinned 2.0.77 data definitions.
--
-- Machines that copy an audible base prototype (chemical plant, biochamber,
-- cryogenic plant, assembling machine, reactor, fusion converter) already
-- inherit a loop. This file fills the genuinely silent prototypes and gives
-- each generating mechanism a voice that matches what it physically does.
local A = {}

local BASE = "__base__/sound/"
local SPACE = "__space-age__/sound/entity/"

-- Named layers, so two plants that work the same way sound the same way.
A.layers = {
  photovoltaic = {file = BASE .. "accumulator-idle.ogg", volume = .32, distance = .5},
  wind         = {file = BASE .. "wind/wind.ogg", volume = .45, distance = .8},
  hydro        = {file = BASE .. "offshore-pump.ogg", volume = .46, distance = .7},
  combustion   = {file = BASE .. "car-engine.ogg", volume = .38, distance = .6},
  heavy_engine = {file = BASE .. "oil-refinery.ogg", volume = .44, distance = .7},
  steam        = {file = BASE .. "steam-engine-90bpm.ogg", volume = .50, distance = .8},
  turbine      = {file = BASE .. "steam-turbine.ogg", volume = .46, distance = .8},
  gas_turbine  = {file = BASE .. "heat-exchanger.ogg", volume = .44, distance = .7},
  deep_earth   = {file = BASE .. "pumpjack.ogg", volume = .42, distance = .8},
  electro      = {file = SPACE .. "electromagnetic-plant/electromagnetic-plant-loop.ogg", volume = .42, distance = .6},
  -- A quiet instrument tick, so a wired monitor is findable by ear.
  telemetry    = {file = BASE .. "combinator.ogg", volume = .28, distance = .4}
}

-- Generating plant name -> layer. Plants absent from this table already own a
-- working sound inherited from the base prototype they are built from.
A.plants = {
  ["micro-solar"]           = "photovoltaic",
  ["solar-tower"]           = "photovoltaic",
  ["photonic-canopy"]       = "electro",
  ["wind-turbine"]          = "wind",
  ["river-turbine"]         = "hydro",
  ["geothermal-bore"]       = "deep_earth",
  ["planetary-thermal-tap"] = "deep_earth",
  ["burner-set"]            = "combustion",
  ["biopellet-engine"]      = "combustion",
  ["cogenerator"]           = "heavy_engine",
  ["steam-piston"]          = "steam",
  ["producer-gas-engine"]   = "combustion",
  ["biogas-turbine"]        = "gas_turbine",
  ["heat-recovery-turbine"] = "turbine",
  ["combined-cycle"]        = "turbine",
  ["biofuel-cell"]          = "electro"
}

-- Other Second Nature entities that are silent in 0.8 and should be audible.
A.entities = {["sn-ecology-monitor"] = "telemetry"}

-- Generating plants report real activity to the engine, so their loop tracks
-- load: a becalmed wind turbine, a solar bank at midnight and a starved gas
-- turbine all fall silent instead of humming at full volume. The circuit
-- monitor is a steady instrument and deliberately does not scale.
A.load_tracking = {}
for key in pairs(A.layers) do A.load_tracking[key] = key ~= "telemetry" end

-- Build a WorkingSound table for a named layer. Kept here so the prototype
-- stage, the engine probes and the offline tests all produce the same shape.
function A.working_sound(key)
  local layer = A.layers[key]
  if not layer then return nil end
  local sound = {
    sound = {filename = layer.file, volume = layer.volume, audible_distance_modifier = layer.distance},
    fade_in_ticks = 4, fade_out_ticks = 20, max_sounds_per_prototype = 3
  }
  if A.load_tracking[key] then
    sound.match_volume_to_activity = true
    sound.volume_smoothing_window_size = 60
  end
  return sound
end

function A.for_plant(name) return A.working_sound(A.plants[name]) end
function A.for_entity(name) return A.working_sound(A.entities[name]) end
return A
