-- Pure data: shared by prototype generation, the simulation and the test suite.
local C = {}
C.mod = "second-nature"
C.prefix = "sn-"
C.schema = 1
C.axes = {"atmosphere", "temperature", "water", "soil", "biodiversity"}
C.planets = {"nauvis", "vulcanus", "fulgora", "gleba", "aquilo"}
C.colors = {
  atmosphere = {0.42, 0.85, 0.84}, temperature = {1, 0.67, 0.36},
  water = {0.40, 0.66, 0.99}, soil = {0.78, 0.62, 0.40},
  biodiversity = {0.57, 0.86, 0.45}, toxicity = {0.89, 0.43, 0.51},
  pressure = {0.98, 0.52, 0.32}, stability = {0.64, 0.88, 0.63}
}
C.bucket_count = 16
C.poll_ticks = 15                   -- Visit each machine once every four seconds.
C.environment_ticks = 60
C.gui_ticks = 120
C.beacon_freshness = 90 * 60        -- Sixty-second recipe plus reasonable logistics slack.
C.victory_ticks = 10 * 60 * 60
C.warning_ticks = 45 * 60
C.max_wave = 40
C.max_active_groups = 3
C.profiles = {
  nauvis = {
    id = 1, initial = {atmosphere = 35, temperature = 65, water = 35, soil = 20, biodiversity = 10}, toxicity = 30,
    gain = {atmosphere = 1, temperature = 1, water = 1, soil = 1, biodiversity = 1},
    erosion = {atmosphere = 0.018, temperature = 0.006, water = 0.012, soil = 0.009, biodiversity = 0.018},
    native = "biter", terrain = "grass-1", tree = "tree-04", specialty = "soil-enricher"
  },
  vulcanus = {
    id = 2, initial = {atmosphere = 8, temperature = 2, water = 3, soil = 8, biodiversity = 0}, toxicity = 65,
    gain = {atmosphere = 0.65, temperature = 0.5, water = 0.7, soil = 1.3, biodiversity = 0.7},
    erosion = {atmosphere = 0.036, temperature = 0.055, water = 0.032, soil = 0.012, biodiversity = 0.024},
    terrain = "grass-3", tree = "tree-08-brown", specialty = "basalt-conditioner"
  },
  fulgora = {
    id = 3, initial = {atmosphere = 12, temperature = 35, water = 8, soil = 3, biodiversity = 0}, toxicity = 80,
    gain = {atmosphere = 0.85, temperature = 1, water = 0.65, soil = 0.8, biodiversity = 0.8},
    erosion = {atmosphere = 0.025, temperature = 0.014, water = 0.030, soil = 0.024, biodiversity = 0.022},
    terrain = "grass-4", tree = "tree-02-red", specialty = "fulgoran-reclaimer"
  },
  gleba = {
    id = 4, initial = {atmosphere = 50, temperature = 65, water = 65, soil = 30, biodiversity = 20}, toxicity = 40,
    gain = {atmosphere = 1.1, temperature = 1, water = 1.25, soil = 0.8, biodiversity = 0.7},
    erosion = {atmosphere = 0.020, temperature = 0.006, water = 0.009, soil = 0.024, biodiversity = 0.035},
    native = "pentapod", terrain = "grass-2", tree = "tree-09", specialty = "spore-tower"
  },
  aquilo = {
    id = 5, initial = {atmosphere = 10, temperature = 0, water = 2, soil = 0, biodiversity = 0}, toxicity = 25,
    gain = {atmosphere = 0.6, temperature = 0.45, water = 0.8, soil = 0.7, biodiversity = 0.6},
    erosion = {atmosphere = 0.025, temperature = 0.065, water = 0.040, soil = 0.012, biodiversity = 0.030},
    -- Aquilo uses decorative gardens only: never replace ice, foundation or heat-support tiles.
    specialty = "cryogenic-garden"
  }
}
-- Every threshold must be met. Mean scores cannot conceal an uninhabitable axis.
C.stages = {
  {name = "hostile", minimum = {0, 0, 0, 0, 0}, max_toxicity = 100},
  {name = "conditioned", minimum = {25, 25, 10, 10, 0}, max_toxicity = 75},
  {name = "rooted", minimum = {40, 35, 30, 30, 15}, max_toxicity = 50},
  {name = "recovering", minimum = {55, 55, 55, 55, 40}, max_toxicity = 30},
  {name = "living", minimum = {75, 75, 75, 75, 70}, max_toxicity = 15},
  {name = "self-sustaining", minimum = {90, 90, 90, 90, 90}, max_toxicity = 8}
}
-- An allowlist, deliberately NOT "anything without a water collision mask".
-- No agricultural soils, paving, landfill, resources, cliffs, oceans or platforms.
C.safe_tiles = {}
for _, name in ipairs({"dry-dirt", "dirt-1", "dirt-2", "dirt-3", "dirt-4", "dirt-5", "dirt-6", "dirt-7",
  "sand-1", "sand-2", "sand-3", "red-desert-0", "red-desert-1", "red-desert-2", "red-desert-3",
  "grass-1", "grass-2", "grass-3", "grass-4", "volcanic-soil-dark", "volcanic-soil-light", "volcanic-ash-light",
  "volcanic-ash-dark", "volcanic-ash-flats", "fulgoran-dust", "fulgoran-sand", "fulgoran-dunes",
  "midland-cracked-lichen", "midland-cracked-lichen-dull", "midland-cracked-lichen-dark"}) do C.safe_tiles[name] = true end
return C
