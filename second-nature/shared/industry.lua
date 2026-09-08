-- Second Nature industry expansion.
--
-- Design rule for everything in this file: it must COMPLEMENT vanilla, never
-- replace it. No entry here is a strict upgrade of a stock machine, so the
-- correct play is to run ours alongside Factorio's, not to tear the stock ones
-- out. Each family therefore trades something real:
--
--   * Green machines: lower or zero emissions, real byproducts, but they need
--     inputs vanilla does not (clean water, cultures, oxygen) and are slower
--     per unit of raw throughput.
--   * Polluting machines: genuinely faster or richer output, paid for with
--     heavy emissions and toxic residue that the restoration model notices.
--
-- Ore multiplication is deliberately a LINE, not a switch: each stage is a
-- separate building with its own fluid and power demand, so richer ore costs
-- real factory space, water and pollution handling rather than one better drill.
local I = {machines = {}, recipes = {}, technologies = {}, items = {}, fluids = {}}

local function item(name, title, family, description, extra)
  local x = {name = name, title = title, family = family, description = description}
  for key, value in pairs(extra or {}) do x[key] = value end
  I.items[#I.items + 1] = x
end

local function fluid(name, title, color, description)
  I.fluids[#I.fluids + 1] = {name = name, title = title, color = color, description = description}
end

-- Categories are declared bare here. prototypes/entities.lua prefixes "sn-",
-- so writing "sn-" in this list would produce "sn-sn-".
local function machine(name, title, base, categories, energy, pollution, description, options)
  local x = {name = name, title = title, base = base, categories = categories, energy = energy,
    pollution = pollution, description = description, family = "machine", color = "biodiversity"}
  for key, value in pairs(options or {}) do x[key] = value end
  I.machines[#I.machines + 1] = x
end

local function recipe(name, title, category, seconds, ingredients, results, options)
  local x = {name = name, title = title, category = category, seconds = seconds,
    ingredients = ingredients, results = results}
  for key, value in pairs(options or {}) do x[key] = value end
  I.recipes[#I.recipes + 1] = x
end

------------------------------------------------------------------------------
-- Fluids and materials
------------------------------------------------------------------------------
fluid("ore-slurry", "Ore slurry", {0.55, 0.47, 0.38},
  "Finely milled ore suspended in water. An intermediate stage of wet concentration, not a finished product.")
fluid("flotation-froth", "Flotation froth", {0.72, 0.68, 0.52},
  "Mineral-bearing froth skimmed from a flotation cell. Carries the valuable fraction of a slurry charge.")
fluid("smelter-flue-gas", "Smelter flue gas", {0.44, 0.40, 0.36},
  "Hot particulate-laden exhaust drawn off a sealed furnace. Treat it or vent it; venting has consequences.")

item("ore-concentrate", "Ore concentrate", "mineral",
  "Upgraded ore with most of its gangue removed. Smelts into substantially more metal than the raw rock.")
item("mineral-tailings", "Mineral tailings", "waste",
  "The stripped rock fraction left by concentration. Inert once bound, a soil contaminant if simply dumped.")
item("refractory-brick", "Refractory brick", "mineral",
  "A high-alumina brick that survives sustained furnace heat. Structural material for kilns and smelters.")
item("catalyst-mesh", "Catalytic mesh", "filter",
  "A precious-metal mesh that converts furnace flue gas into inert products. Degrades slowly with use.")
item("spent-catalyst-mesh", "Spent catalytic mesh", "waste",
  "A poisoned catalyst mesh. Its metal content is recoverable through reclamation.")
item("machine-frame", "Composite machine frame", "mechanical",
  "A rigid mineral-composite chassis used by Second Nature's heavier production buildings.")
item("precision-assembly", "Precision assembly kit", "mechanical",
  "Matched bearings, guides and drives for high-tolerance automated assembly.")

------------------------------------------------------------------------------
-- FURNACES. Two families that are genuinely different tools.
--
-- These are recipe-selectable assembling machines rather than furnace-type
-- prototypes on purpose: a furnace picks its recipe from the input item, and
-- iron and copper concentrate are the SAME item, so the player must choose.
------------------------------------------------------------------------------
machine("crucible-furnace", "Sealed crucible furnace", "assembling-machine-2", {"clean-smelting"}, "480kW", 0.2,
  "An electrically heated sealed crucible. It smelts more slowly than a stock furnace but captures its own flue gas and emits very little.",
  {color = "atmosphere"})
machine("oxy-smelter", "Oxygen-blown smelter", "assembling-machine-3", {"clean-smelting", "concentrate-smelting"}, "1.6MW", 0.4,
  "A high-temperature smelter fed with concentrated oxygen. Fast, clean and hungry for both power and gas.",
  {color = "atmosphere"})
machine("arc-refinery", "Electric arc refinery", "assembling-machine-3", {"clean-smelting", "concentrate-smelting", "alloying"}, "3.2MW", 0.5,
  "A three-electrode arc furnace for concentrates and alloys. The cleanest route to bulk metal, at a serious power cost.",
  {color = "atmosphere"})
machine("blast-furnace", "Coke blast furnace", "assembling-machine-2", {"dirty-smelting", "concentrate-smelting"}, "300kW", 18,
  "A coke-fired blast furnace. Cheap, fast and filthy: it doubles raw smelting throughput and pours emissions into the sky.",
  {color = "temperature", dirty = true})
machine("cupola-furnace", "Reverberatory cupola", "assembling-machine-2", {"dirty-smelting", "alloying"}, "220kW", 26,
  "A crude reverberatory cupola that melts almost anything, including scrap and tailings, with no regard for air quality.",
  {color = "temperature", dirty = true})

------------------------------------------------------------------------------
-- ASSEMBLING MACHINES. Complementary, not a replacement ladder.
------------------------------------------------------------------------------
machine("biopolymer-assembler", "Biopolymer assembler", "assembling-machine-3", {"bio-assembly"}, "420kW", 0,
  "A clean, humid assembly cell for biological and polymer components. It cannot machine metal, but it never pollutes.",
  {color = "biodiversity"})
machine("precision-assembler", "Precision assembly cell", "assembling-machine-3", {"precision-assembly"}, "900kW", 0.6,
  "A vibration-isolated cell for high-tolerance mechanisms. Slower than a stock assembler on simple work and far better on complex work.",
  {color = "soil"})
machine("foundry-press", "Hydraulic foundry press", "assembling-machine-3", {"heavy-assembly"}, "1.4MW", 12,
  "A heavy press for structural components. It is loud, hot and dirty, and it makes frames nothing else can.",
  {color = "temperature", dirty = true})

------------------------------------------------------------------------------
-- ORE MULTIPLICATION LINE. Three separate buildings, three real costs.
--   raw ore -> (mill) slurry -> (flotation) froth + tailings
--           -> (dewater) concentrate -> smelted in an oxy-smelter or arc furnace.
------------------------------------------------------------------------------
machine("ore-mill", "Wet ore mill", "chemical-plant", {"milling"}, "700kW", 3,
  "A ball mill that grinds ore into a pumpable water slurry. The first stage of real ore concentration.",
  {color = "soil"})
machine("flotation-cell", "Froth flotation bank", "chemical-plant", {"flotation"}, "850kW", 1.5,
  "Aerated cells that float valuable mineral away from waste rock using biosurfactant. Produces froth and tailings.",
  {color = "soil"})
machine("dewatering-press", "Dewatering press", "assembling-machine-2", {"dewatering"}, "500kW", 0.5,
  "Squeezes flotation froth into dry concentrate and returns most of its process water.",
  {color = "soil"})

------------------------------------------------------------------------------
-- MINING. Greener extraction that trades speed for a clean footprint.
------------------------------------------------------------------------------
machine("electric-auger", "Electric auger drill", "electric-mining-drill", {}, "420kW", 0,
  "A slow, silent electric auger. It mines less per second than a stock drill and emits nothing at all.",
  {entity_type = "mining-drill", color = "biodiversity", mining_speed = 0.35, mining_radius = 2.49})
machine("hydraulic-miner", "Hydraulic mining head", "electric-mining-drill", {}, "1.1MW", 0,
  "A water-assisted cutting head. It matches a stock drill's rate without emissions, but it must be plumbed.",
  {entity_type = "mining-drill", color = "biodiversity", mining_speed = 0.5, mining_radius = 2.49, needs_water = true})
machine("deep-core-drill", "Deep core drill", "big-mining-drill", {}, "3.5MW", 4,
  "A wide-radius core drill that reaches ore an ordinary head cannot. Substantial output, moderate emissions and a large footprint.",
  {entity_type = "mining-drill", color = "soil", mining_speed = 2.6, mining_radius = 3.99})

------------------------------------------------------------------------------
-- POLLUTION. Something that cleans strongly, and honestly expensive.
------------------------------------------------------------------------------
machine("smog-precipitator", "Electrostatic smog precipitator", "chemical-plant", {"precipitation"}, "2.4MW", 0,
  "An electrostatic array that strips particulates from a wide area of open air. Power hungry, and it produces real captured residue.",
  {fixed = "smog-precipitation", color = "atmosphere"})
machine("carbon-capture-tower", "Direct air capture tower", "chemical-plant", {"air-capture"}, "5MW", 0,
  "A sorbent tower that pulls pollution out of the atmosphere at industrial scale. The strongest cleanup building in the mod, and the most expensive to run.",
  {fixed = "direct-air-capture", color = "atmosphere"})

------------------------------------------------------------------------------
-- RESEARCH. A mid-game lab that is a genuine sidegrade.
------------------------------------------------------------------------------
machine("field-laboratory", "Field ecology laboratory", "lab", {}, "320kW", 0,
  "A laboratory that researches faster than a stock lab while drawing far more power. It accepts every science package the stock lab does.",
  {entity_type = "lab", color = "biodiversity", researching_speed = 1.6})

------------------------------------------------------------------------------
-- RECIPES
------------------------------------------------------------------------------
-- Materials. Frames and precision kits are plain crafts: the buildings that
-- specialise in them are themselves BUILT from them, so a machine-only recipe
-- would be an unsatisfiable bootstrap.
recipe("refractory-brick", "Fire refractory brick", "sn-kiln", 6,
  {{"stone-brick", 4}, {"sn-silica", 2}, {"sn-vitrified-waste", 1}}, {{"sn-refractory-brick", 4}})
recipe("machine-frame", "Weld a composite frame", "crafting", 8,
  {{"steel-plate", 6}, {"sn-refractory-brick", 2}, {"concrete", 4}}, {{"sn-machine-frame", 2}})
recipe("precision-assembly", "Build a precision kit", "crafting", 10,
  {{"iron-gear-wheel", 8}, {"steel-plate", 4}, {"advanced-circuit", 2}, {"lubricant", 20, "fluid"}},
  {{"sn-precision-assembly", 2}})
recipe("catalyst-mesh", "Weave a catalytic mesh", "sn-precision-assembly", 12,
  {{"copper-plate", 4}, {"sn-holmium-catalyst", 1}, {"sn-ceramic-membrane", 2}}, {{"sn-catalyst-mesh", 2}})
recipe("catalyst-recovery", "Recover a poisoned catalyst", "sn-reclamation", 10,
  {{"sn-spent-catalyst-mesh", 2}, {"sn-electrolyte", 30, "fluid"}},
  {{"sn-holmium-catalyst", 1}, {"copper-plate", 4}}, {recycle = false})

-- Ore multiplication line.
recipe("mill-iron-ore", "Mill iron ore", "sn-milling", 3,
  {{"iron-ore", 5}, {"water", 50, "fluid"}}, {{"sn-ore-slurry", 50, "fluid"}}, {recycle = false})
recipe("mill-copper-ore", "Mill copper ore", "sn-milling", 3,
  {{"copper-ore", 5}, {"water", 50, "fluid"}}, {{"sn-ore-slurry", 50, "fluid"}}, {recycle = false})
recipe("flotation", "Froth flotation", "sn-flotation", 4,
  {{"sn-ore-slurry", 50, "fluid"}, {"sn-biofilm", 1}},
  {{"sn-flotation-froth", 40, "fluid"}, {"sn-mineral-tailings", 2}}, {recycle = false})
recipe("dewater-concentrate", "Dewater concentrate", "sn-dewatering", 3,
  {{"sn-flotation-froth", 40, "fluid"}},
  {{"sn-ore-concentrate", 4}, {"water", 25, "fluid"}}, {recycle = false})
recipe("tailings-binding", "Bind mineral tailings", "sn-kiln", 8,
  {{"sn-mineral-tailings", 4}, {"sn-compost", 1}}, {{"stone", 5}}, {recycle = false})

-- Smelting. The point of concentrate: it is worth far more per unit than ore.
recipe("clean-iron-smelting", "Sealed iron smelting", "sn-clean-smelting", 6,
  {{"iron-ore", 2}, {"sn-oxygen", 10, "fluid"}}, {{"iron-plate", 2}, {"sn-smelter-flue-gas", 10, "fluid"}}, {recycle = false})
recipe("clean-copper-smelting", "Sealed copper smelting", "sn-clean-smelting", 6,
  {{"copper-ore", 2}, {"sn-oxygen", 10, "fluid"}}, {{"copper-plate", 2}, {"sn-smelter-flue-gas", 10, "fluid"}}, {recycle = false})
recipe("concentrate-iron", "Smelt iron concentrate", "sn-concentrate-smelting", 8,
  {{"sn-ore-concentrate", 2}, {"sn-oxygen", 20, "fluid"}},
  {{"iron-plate", 7}, {"sn-smelter-flue-gas", 20, "fluid"}}, {recycle = false})
recipe("concentrate-copper", "Smelt copper concentrate", "sn-concentrate-smelting", 8,
  {{"sn-ore-concentrate", 2}, {"sn-oxygen", 20, "fluid"}},
  {{"copper-plate", 7}, {"sn-smelter-flue-gas", 20, "fluid"}}, {recycle = false})
recipe("blast-iron", "Blast-furnace iron [dirty]", "sn-dirty-smelting", 3,
  {{"iron-ore", 4}, {"coal", 2}}, {{"iron-plate", 6}},
  {effects = {toxicity = 0.05}, emissions = 6, recycle = false})
recipe("blast-copper", "Blast-furnace copper [dirty]", "sn-dirty-smelting", 3,
  {{"copper-ore", 4}, {"coal", 2}}, {{"copper-plate", 6}},
  {effects = {toxicity = 0.05}, emissions = 6, recycle = false})
recipe("cupola-scrap", "Remelt scrap and tailings [dirty]", "sn-dirty-smelting", 5,
  {{"sn-mineral-tailings", 4}, {"coal", 2}},
  {{"iron-plate", 2}, {"copper-plate", 2}, {"sn-hazardous-sludge", 1}},
  {effects = {toxicity = 0.1}, emissions = 8, recycle = false})
recipe("clean-steel", "Arc-furnace steel", "sn-alloying", 10,
  {{"iron-plate", 5}, {"sn-oxygen", 30, "fluid"}, {"sn-refractory-brick", 1}},
  {{"steel-plate", 3}}, {recycle = false})
recipe("dirty-steel", "Cupola steel [dirty]", "sn-alloying", 5,
  {{"iron-plate", 6}, {"coal", 3}}, {{"steel-plate", 3}},
  {effects = {toxicity = 0.06}, emissions = 9, recycle = false})

-- Flue gas: treat it, or it becomes everyone's problem.
recipe("flue-treatment", "Catalytic flue treatment", "sn-scrubbing", 8,
  {{"sn-smelter-flue-gas", 100, "fluid"}, {"sn-catalyst-mesh", 1}},
  {{"sn-activated-carbon", 2}, {"sn-spent-catalyst-mesh", 1}}, {recycle = false})

-- Heavy assembly. The press is the only route to these, and it is filthy, so a
-- clean factory has to import them or accept the emissions locally.
recipe("pressed-frame", "Press a heavy frame [dirty]", "sn-heavy-assembly", 6,
  {{"steel-plate", 8}, {"sn-refractory-brick", 2}},
  {{"sn-machine-frame", 3}}, {emissions = 4, recycle = false})
recipe("pressed-girder", "Press structural girders [dirty]", "sn-heavy-assembly", 8,
  {{"steel-plate", 10}, {"concrete", 5}},
  {{"low-density-structure", 2}}, {emissions = 5, recycle = false})

-- Clean assembly.
recipe("bio-membrane-assembly", "Assemble membrane cartridges", "sn-bio-assembly", 6,
  {{"sn-ceramic-membrane", 2}, {"sn-biofilm", 2}, {"sn-clean-water", 20, "fluid"}},
  {{"sn-filter-cartridge", 4}})

-- Pollution control operations. Fixed-recipe, domain-gated, and they consume
-- real consumables while producing real residue.
recipe("smog-precipitation", "Precipitate airborne smog", "sn-precipitation", 12,
  {{"sn-catalyst-mesh", 1}, {"sn-clean-water", 50, "fluid"}},
  {{"sn-hazardous-sludge", 2}, {"sn-climate-data", 1}, {"sn-spent-catalyst-mesh", 1}},
  {effects = {atmosphere = 0.1, pollution = -180, toxicity = -0.05}, domain = true, operation = true, recycle = false})
recipe("direct-air-capture", "Direct atmospheric capture", "sn-air-capture", 20,
  {{"sn-activated-carbon", 4}, {"sn-clean-water", 100, "fluid"}, {"sn-oxygen", 20, "fluid"}},
  {{"sn-biochar", 2}, {"sn-climate-data", 3}},
  {effects = {atmosphere = 0.22, pollution = -520, toxicity = -0.1}, domain = true, operation = true, recycle = false})

------------------------------------------------------------------------------
-- CONSTRUCTION RECIPES for the buildings themselves.
------------------------------------------------------------------------------
local builds = {
  {"crucible-furnace", {{"steel-plate", 12}, {"sn-refractory-brick", 10}, {"electronic-circuit", 8}}, 6},
  {"oxy-smelter", {{"sn-machine-frame", 2}, {"sn-refractory-brick", 20}, {"advanced-circuit", 10}, {"pipe", 10}}, 10},
  {"arc-refinery", {{"sn-machine-frame", 4}, {"sn-refractory-brick", 30}, {"processing-unit", 12}, {"copper-cable", 40}}, 15},
  {"blast-furnace", {{"steel-plate", 20}, {"stone-brick", 30}, {"iron-gear-wheel", 15}}, 8},
  {"cupola-furnace", {{"steel-plate", 14}, {"stone-brick", 24}, {"pipe", 8}}, 6},
  {"biopolymer-assembler", {{"sn-machine-frame", 1}, {"sn-biofilm", 15}, {"sn-glass", 20}, {"electronic-circuit", 10}}, 8},
  {"precision-assembler", {{"sn-machine-frame", 2}, {"sn-precision-assembly", 4}, {"processing-unit", 8}}, 12},
  {"foundry-press", {{"sn-machine-frame", 3}, {"steel-plate", 30}, {"sn-refractory-brick", 12}, {"advanced-circuit", 8}}, 12},
  {"ore-mill", {{"sn-machine-frame", 2}, {"steel-plate", 20}, {"iron-gear-wheel", 25}, {"pipe", 12}}, 10},
  {"flotation-cell", {{"sn-machine-frame", 2}, {"sn-glass", 24}, {"pipe", 16}, {"advanced-circuit", 6}}, 10},
  {"dewatering-press", {{"sn-machine-frame", 1}, {"steel-plate", 16}, {"sn-ceramic-membrane", 8}, {"pipe", 8}}, 8},
  {"electric-auger", {{"steel-plate", 10}, {"iron-gear-wheel", 12}, {"electronic-circuit", 6}}, 5},
  {"hydraulic-miner", {{"sn-machine-frame", 1}, {"steel-plate", 16}, {"pipe", 10}, {"advanced-circuit", 6}}, 8},
  {"deep-core-drill", {{"sn-machine-frame", 4}, {"sn-precision-assembly", 4}, {"processing-unit", 10}, {"tungsten-plate", 20}}, 20},
  {"smog-precipitator", {{"sn-machine-frame", 3}, {"sn-catalyst-mesh", 4}, {"processing-unit", 10}, {"sn-glass", 30}}, 15},
  {"carbon-capture-tower", {{"sn-machine-frame", 6}, {"sn-catalyst-mesh", 10}, {"processing-unit", 20}, {"sn-ceramic-membrane", 20}}, 25},
  {"field-laboratory", {{"sn-machine-frame", 1}, {"sn-glass", 20}, {"advanced-circuit", 10}, {"sn-ecological-data", 10}}, 12},
}
for _, entry in ipairs(builds) do
  local name, ingredients, seconds = entry[1], entry[2], entry[3]
  -- machine = true routes these to the production subgroup and takes the name
  -- and icon from the entity, exactly like the core restoration buildings.
  recipe(name, "Build " .. name, "crafting", seconds, ingredients, {{"sn-" .. name, 1}}, {machine = true})
end

------------------------------------------------------------------------------
-- TECHNOLOGY
------------------------------------------------------------------------------
local function tech(name, title, prerequisites, packs, count, unlocks, description)
  local science = {}
  for _, p in ipairs(packs) do science[#science + 1] = {p, 1} end
  I.technologies[#I.technologies + 1] = {name = name, title = title, prerequisites = prerequisites,
    science = science, count = count, seconds = 30, unlocks = unlocks, description = description}
end

local r, g, b, p, u = "automation-science-pack", "logistic-science-pack", "chemical-science-pack",
  "production-science-pack", "utility-science-pack"
local E = "sn-ecology-science-pack"

tech("refractories", "Refractory materials", {"sn-closed-loops", "steel-processing"}, {r, g}, 60,
  {"refractory-brick", "machine-frame"},
  "High-alumina brick and composite frames: the structural basis of every heavy Second Nature building.")
tech("clean-smelting", "Sealed smelting", {"sn-refractories", "sn-thermal-engineering"}, {r, g, E}, 90,
  {"crucible-furnace", "clean-iron-smelting", "clean-copper-smelting"},
  "Seal the furnace and capture its flue gas. Slower than an open furnace, and almost silent in the pollution budget.")
tech("dirty-smelting", "Coke blast smelting", {"sn-refractories"}, {r, g}, 70,
  {"blast-furnace", "cupola-furnace", "blast-iron", "blast-copper", "cupola-scrap", "dirty-steel"},
  "Cheap coke-fired furnaces that double raw throughput. The emissions are severe and the restoration model counts them.")
tech("ore-concentration", "Ore concentration", {"sn-refractories", "fluid-handling"}, {r, g, b}, 120,
  {"ore-mill", "flotation-cell", "dewatering-press", "mill-iron-ore", "mill-copper-ore",
   "flotation", "dewater-concentrate", "tailings-binding"},
  "Mill, float and dewater ore into concentrate. Three buildings and real water logistics for a much richer smelter feed.")
tech("oxygen-smelting", "Oxygen-blown metallurgy", {"sn-clean-smelting", "sn-ore-concentration"}, {r, g, b, E}, 160,
  {"oxy-smelter", "concentrate-iron", "concentrate-copper", "catalyst-mesh", "flue-treatment", "catalyst-recovery"},
  "Burn concentrate in pure oxygen and treat the exhaust catalytically. This is where ore multiplication actually pays off.")
tech("arc-metallurgy", "Electric arc metallurgy", {"sn-oxygen-smelting", "production-science-pack"}, {r, g, b, p, E}, 220,
  {"arc-refinery", "clean-steel"},
  "Three-phase arc melting for concentrates and alloys. The cleanest bulk metal available, priced in megawatts.")
tech("green-mining", "Low-impact extraction", {"sn-environmental-monitoring", "electronics"}, {r, g}, 70,
  {"electric-auger", "hydraulic-miner"},
  "Quiet electric and water-assisted mining heads. They give up speed in exchange for producing no pollution at all.")
tech("deep-extraction", "Deep core extraction", {"sn-green-mining", "sn-arc-metallurgy", "utility-science-pack"}, {r, g, b, p, u}, 250,
  {"deep-core-drill"},
  "A wide-radius core drill for depleted fields. Large output and a large footprint, with emissions you must plan around.")
tech("specialised-assembly", "Specialised assembly", {"sn-refractories", "advanced-circuit"}, {r, g, b}, 140,
  {"biopolymer-assembler", "precision-assembler", "foundry-press",
   "precision-assembly", "bio-membrane-assembly", "pressed-frame", "pressed-girder"},
  "Three assembly cells that each do one thing better than a general assembler, and other things worse.")
tech("field-laboratory", "Field laboratory", {"sn-environmental-monitoring", "sn-refractories"}, {r, g, E}, 120,
  {"field-laboratory"},
  "A faster laboratory. It draws far more power than a stock lab and accepts every package a stock lab does.")
tech("smog-precipitation", "Electrostatic precipitation", {"sn-atmospheric-engineering", "sn-oxygen-smelting"}, {r, g, b, E}, 200,
  {"smog-precipitator", "smog-precipitation"},
  "Strip particulates straight out of the open air over a wide radius, at a genuine cost in power and consumables.")
tech("direct-air-capture", "Direct air capture", {"sn-smog-precipitation", "sn-arc-metallurgy", "utility-science-pack"}, {r, g, b, p, u, E}, 300,
  {"carbon-capture-tower", "direct-air-capture"},
  "The strongest cleanup building in the mod. A sorbent tower that removes pollution faster than any scrubber, and costs accordingly.")

I.by_machine = {}
for _, m in ipairs(I.machines) do I.by_machine[m.name] = m end
return I
