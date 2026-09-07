-- Content is declared once. Prototypes, runtime effects, localization, documentation,
-- progression audits and balance simulations all read this catalog.
local K = {items = {}, fluids = {}, machines = {}, recipes = {}, technologies = {}}
local function item(name, title, family, desc, extra)
  local x = {name = name, title = title, family = family, description = desc}
  for key, value in pairs(extra or {}) do x[key] = value end
  K.items[#K.items + 1] = x
end
item("silica", "Silica", "mineral", "Crushed silicate grains used to melt laboratory glass and fire porous ceramics.")
item("glass", "Laboratory glass", "mineral", "Chemically resistant glass for culture vessels, instruments and filtration assemblies.")
item("mineral-nutrients", "Mineral nutrients", "mineral", "A stable blend of mineral salts that feeds pioneer microorganisms.")
item("microbial-culture", "Pioneer culture", "culture", "A sealed inoculum of hardy microorganisms for nutrient processing and ecological seeding.")
item("algal-biomass", "Algal biomass", "leaf", "Cultivated algae rich in organic carbon. Feedstock for compost, membranes and biological fuels.", {fuel_value = "1MJ"})
item("compost", "Living compost", "soil", "A living mixture of decomposed biomass and microorganisms that enriches mineral soil.")
item("biochar", "Biochar", "carbon", "Porous carbon that retains nutrients, stabilizes soil and adsorbs impurities.", {fuel_value = "4MJ"})
item("activated-carbon", "Activated carbon", "carbon", "High-surface-area carbon for purification cartridges and chemical processing.")
item("filter-cartridge", "Carbon filter cartridge", "filter", "A replaceable sorbent cartridge for atmospheric scrubbers and water filters.")
item("spent-filter", "Spent filter cartridge", "waste", "A saturated cartridge containing recoverable carbon, glass and captured contaminants.")
item("soil-substrate", "Soil substrate", "soil", "A stable rooting medium composed of mineral grains, compost and porous carbon.")
item("seed-mix", "Pioneer seed mix", "seed", "A blend of pioneer seeds and microbial cultures adapted to recovering ground.")
item("ceramic-membrane", "Ceramic membrane", "filter", "A porous, heat-resistant barrier that separates suspended contaminants from process water.")
item("thermal-buffer", "Charged thermal buffer", "thermal", "A charged heat-transfer cartridge for climate exchangers and sheltered habitats.")
item("depleted-thermal-buffer", "Depleted thermal buffer", "waste", "A discharged heat-transfer cartridge. Its casing and working medium can be reconditioned.")
item("neutralization-charge", "Neutralization charge", "mineral", "Reactive minerals and carbon that bind dissolved contaminants into separable sludge.")
item("hazardous-sludge", "Hazardous sludge", "waste", "Concentrated industrial contaminants. Vitrification locks the residue into an inert matrix.")
item("vitrified-waste", "Vitrified aggregate", "mineral", "An inert glass-mineral aggregate suitable for durable construction materials.")
item("biofilm", "Engineered biofilm", "culture", "A cultivated polymer matrix used in membranes, composite reinforcement and pheromone carriers.")
item("ecological-data", "Ecological samples", "data", "Preserved field samples documenting soil structure, microbial activity and pioneer growth.")
item("climate-data", "Climate samples", "data", "Instrument samples recording atmospheric composition, heat transfer and water-cycle recovery.")
item("biosphere-data", "Biosphere samples", "data", "Complex habitat samples used to study interactions within established ecological communities.")
item("thermophile-culture", "Thermophile culture", "thermal", "Heat-tolerant organisms cultivated in mineral-rich volcanic conditions.")
item("heavy-metal-cake", "Heavy-metal concentrate", "waste", "A concentrated mixture of metals separated from contaminated scrap and processing residues.")
item("holmium-catalyst", "Holmium biocatalyst", "crystal", "A stabilized holmium catalyst that supports resilient biological and electrochemical systems.")
item("symbiotic-culture", "Symbiotic culture", "culture", "A balanced consortium of Gleban organisms used to establish diverse habitats.")
item("biodiversity-matrix", "Biodiversity matrix", "seed", "An organized community of thermophiles, symbionts and mineral catalysts for habitat restoration.")
item("gaia-cell", "Gaia coordination cell", "crystal", "A biological coordination cartridge consumed by planetary beacons to maintain a synchronized ecosystem network.")
item("ecology-science-pack", "Ecology science pack", "science", "A research package containing ecological samples, preserved media and analytical electronics.", {tool = true, color = "biodiversity"})
item("climate-science-pack", "Climate science pack", "science", "A research package combining climate measurements with specialized planetary cultures.", {tool = true, color = "atmosphere"})
item("restoration-science-pack", "Restoration science pack", "science", "A research package produced from the operating data of a coordinated living-world network.", {tool = true, color = "temperature"})
local function fluid(name, title, color, desc)
  K.fluids[#K.fluids + 1] = {name = name, title = title, color = color, description = desc}
end
fluid("clean-water", "Purified water", {0.35, 0.72, 0.93}, "High-purity water for sensitive biological cultures, thermal circuits and chemical processing.")
fluid("oxygen", "Oxygen", {0.62, 0.89, 0.95}, "Concentrated oxygen for clean metallurgy, nutrient preparation and oxidation reactions.")
fluid("hydrogen", "Hydrogen", {0.78, 0.70, 0.95}, "A light reducing gas used in metallurgy and synthetic fuel production.")
fluid("electrolyte", "Mineral electrolyte", {0.84, 0.68, 0.36}, "An aqueous mineral electrolyte for selective metal recovery and electrochemical reactions.")
fluid("bioleachate", "Bioleachate", {0.52, 0.74, 0.25}, "A biologically active solution that releases useful metals from mineral feedstocks.")
fluid("toxic-effluent", "Toxic effluent", {0.70, 0.31, 0.51}, "Contaminated process liquid containing captured pollutants and dissolved industrial residues.")

local function machine(name, title, base, categories, energy, pollution, desc, options)
  local x = {name = name, title = title, base = base, categories = categories, energy = energy,
    pollution = pollution, description = desc, family = "machine", color = "biodiversity"}
  for key, value in pairs(options or {}) do x[key] = value end
  K.machines[#K.machines + 1] = x
end
machine("algae-vat", "Pioneer bioreactor", "chemical-plant", {"bioculture"}, "180kW", 0.5,
  "An agitated, temperature-regulated culture vessel for growing microorganisms and algal biomass.")
machine("composter", "Aerobic composter", "assembling-machine-2", {"composting"}, "120kW", 1,
  "An aerated processing bed that converts organic feedstock into compost, biofilm and biochar.", {color = "soil"})
machine("hydroponics-bay", "Hydroponics bay", "biochamber", {"hydroponics"}, "650kW", 0.5,
  "A controlled growing enclosure that supplies crops with circulating water, nutrients and sheltered light.")
machine("electrolyzer", "Electrochemical works", "chemical-plant", {"electrochemistry"}, "1.8MW", 0.5,
  "An electrochemical cell bank for gas separation, buffer charging and low-emission chemical processing.", {color = "atmosphere"})
machine("reclamation-plant", "Closed-loop reclamation plant", "chemical-plant", {"reclamation"}, "800kW", 1,
  "A closed-loop separator that recovers useful materials and process water from spent filters and effluent.", {color = "water"})
machine("materials-kiln", "Electric materials kiln", "assembling-machine-2", {"kiln"}, "900kW", 1,
  "An electrically heated furnace for firing ceramics, melting glass and vitrifying hazardous residues.", {color = "temperature"})
machine("pyrolyzer", "Dirty pyrolysis retort", "assembling-machine-2", {"pyrolysis"}, "350kW", 24,
  "A sealed high-temperature retort that converts carbon-rich feedstock into concentrated industrial reagents. Produces substantial emissions and toxic residues.", {color = "toxicity", dirty = true})
machine("air-scrubber", "Atmospheric scrubber", "chemical-plant", {"scrubbing"}, "450kW", 0,
  "A forced-air filtration unit that captures airborne pollutants in replaceable sorbent cartridges.",
  {fixed = "air-scrubbing", color = "atmosphere"})
machine("soil-enricher", "Soil restoration station", "chemical-plant", {"soil-restoration"}, "300kW", 0,
  "A mixing and injection station that distributes mineral substrate, microbial culture and water into recovering soil.",
  {fixed = "soil-restoration", color = "soil"})
machine("seed-disperser", "Pioneer seed disperser", "chemical-plant", {"reseeding"}, "500kW", 0,
  "A metered broadcast system that distributes pioneer seeds and soil treatments across suitable habitat.",
  {fixed = "pioneer-reseeding"})
machine("watershed", "Watershed restoration plant", "chemical-plant", {"watershed"}, "750kW", 0,
  "A treatment reservoir that restores water quality and supports a stable local water cycle.",
  {fixed = "watershed-restoration", color = "water"})
machine("thermal-exchanger", "Climate heat exchanger", "chemical-plant", {"thermal-balancing"}, "4MW", 0,
  "A high-power heat-transfer installation that regulates ecological thermal conditions using rechargeable buffer cartridges.",
  {fixed = "thermal-balancing", color = "temperature"})
machine("detoxifier", "Mineral detoxification plant", "chemical-plant", {"detoxification"}, "1.5MW", 0,
  "A chemical binding plant that concentrates environmental contaminants into hazardous sludge for treatment.",
  {fixed = "mineral-detoxification", color = "toxicity"})
machine("pheromone-dampener", "Pheromone dampener", "chemical-plant", {"dampening"}, "400kW", 0,
  "A controlled-release diffuser that moderates native aggression with a sustained supply of biological pheromone carriers.",
  {fixed = "pheromone-dampening", color = "atmosphere"})
machine("forcing-tower", "Atmospheric forcing stack", "chemical-plant", {"forcing"}, "600kW", 30,
  "An industrial reaction stack that rapidly alters atmospheric chemistry while releasing pollution and accumulating toxic residues.",
  {fixed = "atmospheric-forcing", color = "toxicity", dirty = true})
machine("basalt-conditioner", "Basalt weathering station", "chemical-plant", {"weathering"}, "2.5MW", 0,
  "A heavy mineral-conditioning station that weathers volcanic feedstock into biologically useful substrate.",
  {fixed = "basalt-weathering", color = "temperature", planet = "vulcanus"})
machine("fulgoran-reclaimer", "Fulgoran remediation works", "chemical-plant", {"fulgoran-recovery"}, "2MW", 0,
  "A scrap-remediation installation that separates heavy metals and conditions contaminated mineral residues.",
  {fixed = "fulgoran-recovery", color = "toxicity", planet = "fulgora"})
machine("spore-tower", "Symbiotic spore tower", "biochamber", {"spore-balancing"}, "1.2MW", 0,
  "A vertical filtration and culture system that balances airborne spores and cultivates symbiotic organisms.",
  {fixed = "spore-balancing", planet = "gleba"})
machine("cryogenic-garden", "Cryogenic garden", "cryogenic-plant", {"cryogenic-restoration"}, "3.5MW", 0,
  "An insulated, heated growing installation that maintains living cultures and water circulation in extreme cold.",
  {fixed = "cryogenic-restoration", color = "water", planet = "aquilo"})
machine("sanctuary", "Biodiversity sanctuary", "biochamber", {"habitat-restoration"}, "2.2MW", 0,
  "A sheltered habitat complex that combines specialized cultures into a resilient ecological community.",
  {fixed = "habitat-restoration"})
machine("planetary-beacon", "Gaia planetary beacon", "cryogenic-plant", {"gaia-coordination"}, "5MW", 0,
  "A planetary coordination station that synchronizes habitat maintenance and records the operating state of the living-world network.",
  {fixed = "gaia-coordination", color = "atmosphere"})
machine("ecology-monitor", "Ecology circuit monitor", "constant-combinator", {}, nil, 0,
  "An instrument console that broadcasts ecological fitness, contamination, resistance and pollution readings to the circuit network.",
  {entity_type = "constant-combinator", color = "atmosphere"})

-- Short recipe DSL: ingredient/result entries are {prototype-name, amount, optional "fluid"}.
-- All custom names are explicit, so a vanilla ingredient can never silently resolve to the wrong item.
local function recipe(name, title, category, seconds, ingredients, results, options)
  local x = {name = name, title = title, category = category, seconds = seconds, ingredients = ingredients, results = results}
  for key, value in pairs(options or {}) do x[key] = value end
  K.recipes[#K.recipes + 1] = x
end
recipe("silica", "Crush silica", "crafting", 1, {{"stone", 2}}, {{"sn-silica", 2}}, {enabled = true})
recipe("glass", "Smelt laboratory glass", "smelting", 3.2, {{"sn-silica", 2}}, {{"sn-glass", 2}}, {enabled = true})
recipe("mineral-nutrients", "Dissolve mineral nutrients", "sn-bioculture", 4, {{"stone", 3}, {"iron-ore", 1}, {"water", 20, "fluid"}}, {{"sn-mineral-nutrients", 4}})
recipe("abiogenesis", "Synthesize pioneer culture", "sn-bioculture", 14, {{"stone", 2}, {"iron-ore", 1}, {"water", 30, "fluid"}}, {{"sn-microbial-culture", 2}})
recipe("algae-cultivation", "Cultivate algae", "sn-bioculture", 8, {{"sn-microbial-culture", 1}, {"sn-mineral-nutrients", 1}, {"water", 40, "fluid"}}, {{"sn-algal-biomass", 8}, {"sn-microbial-culture", 1}}, {recycle = false})
recipe("compost", "Aerobic composting", "sn-composting", 5, {{"sn-algal-biomass", 6}}, {{"sn-compost", 4}, {"sn-biofilm", 1}})
recipe("wood-compost", "Compost wood", "sn-composting", 6, {{"wood", 4}}, {{"sn-compost", 4}, {"sn-biofilm", 1}})
recipe("spoilage-compost", "Recover spoiled organics", "sn-composting", 4, {{"spoilage", 10}}, {{"sn-compost", 5}, {"sn-biofilm", 1}})
recipe("biochar", "Slow biomass carbonization", "sn-composting", 10, {{"sn-algal-biomass", 8}}, {{"sn-biochar", 3}})
recipe("activated-carbon", "Renewable carbon activation", "sn-bioculture", 6, {{"sn-biochar", 2}, {"water", 10, "fluid"}}, {{"sn-activated-carbon", 2}})
recipe("filter-cartridge", "Carbon filter cartridges", "crafting", 2, {{"sn-activated-carbon", 2}, {"sn-glass", 1}, {"iron-plate", 1}}, {{"sn-filter-cartridge", 2}})
recipe("soil-substrate", "Living soil substrate", "sn-composting", 5, {{"sn-compost", 3}, {"sn-silica", 2}, {"sn-biochar", 1}}, {{"sn-soil-substrate", 4}})
recipe("ecology-science-pack", "Ecology science", "crafting", 8, {{"sn-ecological-data", 2}, {"sn-glass", 2}, {"electronic-circuit", 2}}, {{"sn-ecology-science-pack", 2}})
recipe("ceramic-membrane", "Porous ceramic membrane", "crafting", 4, {{"stone-brick", 3}, {"sn-silica", 2}, {"sn-glass", 1}}, {{"sn-ceramic-membrane", 2}})
recipe("water-filtration", "Purify process water", "sn-reclamation", 5, {{"sn-filter-cartridge", 1}, {"water", 100, "fluid"}}, {{"sn-clean-water", 90, "fluid"}, {"sn-spent-filter", 1}}, {recycle = false})
recipe("neutralization-charge", "Mineral neutralization charge", "crafting", 3, {{"stone", 6}, {"sn-biochar", 1}}, {{"sn-neutralization-charge", 2}})
recipe("pioneer-timber", "Pioneer timber cultivation", "sn-bioculture", 18, {{"sn-algal-biomass", 12}, {"sn-compost", 2}, {"water", 30, "fluid"}}, {{"wood", 6}})
recipe("seed-mix", "Prepare pioneer seed mix", "crafting", 3, {{"sn-microbial-culture", 1}, {"sn-algal-biomass", 4}, {"sn-compost", 2}}, {{"sn-seed-mix", 2}})
recipe("hydroponic-timber", "Established timber cultivation", "sn-hydroponics", 12, {{"sn-seed-mix", 1}, {"sn-mineral-nutrients", 2}, {"sn-clean-water", 40, "fluid"}}, {{"wood", 12}, {"sn-seed-mix", 1}}, {stage = 2, domain = true, recycle = false})
recipe("thermal-buffer", "Charge a new thermal buffer", "crafting", 5, {{"steel-plate", 1}, {"copper-plate", 3}, {"sn-glass", 2}}, {{"sn-thermal-buffer", 2}}, {recycle = false})
recipe("water-electrolysis", "Water electrolysis", "sn-electrochemistry", 10, {{"sn-clean-water", 100, "fluid"}}, {{"sn-hydrogen", 80, "fluid"}, {"sn-oxygen", 40, "fluid"}})
recipe("buffer-recharging", "Recharge thermal buffers", "sn-electrochemistry", 10, {{"sn-depleted-thermal-buffer", 1}, {"sn-biofilm", 1}, {"sn-clean-water", 40, "fluid"}}, {{"sn-thermal-buffer", 1}}, {recycle = false})
recipe("filter-reclamation", "Reclaim spent filters", "sn-reclamation", 8, {{"sn-spent-filter", 2}, {"sn-clean-water", 30, "fluid"}}, {{"sn-activated-carbon", 2}, {"sn-glass", 1}, {"sn-toxic-effluent", 20, "fluid"}}, {recycle = false})
recipe("effluent-treatment", "Neutralize captured effluent", "sn-reclamation", 10, {{"sn-toxic-effluent", 100, "fluid"}, {"sn-neutralization-charge", 2}}, {{"water", 80, "fluid"}, {"sn-hazardous-sludge", 4}}, {recycle = false})
recipe("waste-vitrification", "Vitrify hazardous sludge", "sn-kiln", 12, {{"sn-hazardous-sludge", 4}, {"sn-glass", 2}}, {{"sn-vitrified-waste", 2}}, {recycle = false})
recipe("aggregate-concrete", "Concrete from bound waste", "crafting-with-fluid", 10, {{"sn-vitrified-waste", 1}, {"stone-brick", 4}, {"water", 20, "fluid"}}, {{"concrete", 10}}, {recycle = false})
recipe("electric-glass", "Electric glass firing", "sn-kiln", 4, {{"sn-silica", 4}}, {{"sn-glass", 4}})
recipe("electric-ceramics", "Electric ceramic firing", "sn-kiln", 4, {{"stone", 4}, {"sn-silica", 2}}, {{"sn-ceramic-membrane", 4}})
recipe("coal-activation", "Coal activation [dirty]", "sn-pyrolysis", 3, {{"coal", 3}, {"sn-silica", 1}}, {{"sn-activated-carbon", 6}, {"sn-hazardous-sludge", 1}}, {effects = {toxicity = 0.08}, emissions = 3, recycle = false})
recipe("forced-substrate", "Chemically forced substrate [dirty]", "sn-pyrolysis", 3, {{"coal", 2}, {"stone", 4}, {"sn-compost", 1}}, {{"sn-soil-substrate", 8}, {"sn-hazardous-sludge", 1}}, {effects = {toxicity = 0.12}, emissions = 4, recycle = false})
recipe("bioleachate", "Prepare bioleachate", "sn-reclamation", 5, {{"sn-compost", 2}, {"sn-clean-water", 30, "fluid"}}, {{"sn-bioleachate", 40, "fluid"}})
recipe("clean-iron", "Biological iron refining", "sn-reclamation", 8, {{"iron-ore", 4}, {"sn-bioleachate", 20, "fluid"}}, {{"iron-plate", 6}, {"sn-toxic-effluent", 10, "fluid"}}, {recycle = false})
recipe("clean-copper", "Biological copper refining", "sn-reclamation", 8, {{"copper-ore", 4}, {"sn-bioleachate", 20, "fluid"}}, {{"copper-plate", 6}, {"sn-toxic-effluent", 10, "fluid"}}, {recycle = false})
recipe("clean-plastic", "Renewable bioplastic", "sn-electrochemistry", 6, {{"sn-algal-biomass", 5}, {"sn-hydrogen", 20, "fluid"}}, {{"plastic-bar", 2}})
recipe("renewable-fuel", "Renewable solid fuel", "sn-electrochemistry", 8, {{"sn-algal-biomass", 4}, {"sn-hydrogen", 50, "fluid"}}, {{"solid-fuel", 2}})
recipe("oxygenated-steel", "Oxygen-assisted steel", "sn-electrochemistry", 12, {{"iron-plate", 10}, {"sn-oxygen", 50, "fluid"}}, {{"steel-plate", 3}})
recipe("green-concrete", "Biomineral concrete", "crafting-with-fluid", 8, {{"sn-compost", 2}, {"sn-silica", 4}, {"stone-brick", 4}, {"water", 30, "fluid"}}, {{"concrete", 10}})
recipe("electrolyte", "Mineral electrolyte", "sn-reclamation", 5, {{"stone", 4}, {"sn-clean-water", 50, "fluid"}}, {{"sn-electrolyte", 50, "fluid"}})
recipe("thermophile-culture", "Cultivate thermophiles", "sn-bioculture", 12, {{"sn-microbial-culture", 2}, {"calcite", 5}, {"sulfuric-acid", 50, "fluid"}}, {{"sn-thermophile-culture", 2}}, {planet = "vulcanus", stage = 1})
recipe("heavy-metal-refining", "Refine recovered metals", "sn-reclamation", 10, {{"sn-heavy-metal-cake", 3}, {"sulfuric-acid", 20, "fluid"}}, {{"holmium-ore", 1}, {"iron-ore", 3}, {"copper-ore", 2}}, {recycle = false})
recipe("holmium-catalyst", "Holmium biocatalyst", "sn-reclamation", 8, {{"sn-heavy-metal-cake", 2}, {"holmium-plate", 1}, {"sn-electrolyte", 20, "fluid"}}, {{"sn-holmium-catalyst", 2}}, {planet = "fulgora", stage = 1})
recipe("symbiotic-fermentation", "Symbiotic egg fermentation", "sn-hydroponics", 8, {{"pentapod-egg", 1}, {"nutrients", 10}, {"sn-clean-water", 30, "fluid"}}, {{"sn-symbiotic-culture", 4}}, {planet = "gleba", stage = 2})
recipe("compost-nutrients", "Feed the Gleban nutrient loop", "sn-hydroponics", 4, {{"sn-compost", 4}, {"sn-oxygen", 20, "fluid"}}, {{"nutrients", 20}})
recipe("hydroponic-yumako", "Sheltered yumako cultivation", "sn-hydroponics", 25, {{"yumako-seed", 1}, {"nutrients", 10}, {"sn-clean-water", 100, "fluid"}}, {{"yumako", 20}, {"yumako-seed", 1}}, {planet = "gleba", stage = 3, recycle = false})
recipe("hydroponic-jellynut", "Sheltered jellynut cultivation", "sn-hydroponics", 25, {{"jellynut-seed", 1}, {"nutrients", 10}, {"sn-clean-water", 100, "fluid"}}, {{"jellynut", 20}, {"jellynut-seed", 1}}, {planet = "gleba", stage = 3, recycle = false})
recipe("biodiversity-matrix", "Assemble a living community", "sn-hydroponics", 15, {{"sn-thermophile-culture", 1}, {"sn-holmium-catalyst", 1}, {"sn-symbiotic-culture", 1}, {"sn-biofilm", 2}}, {{"sn-biodiversity-matrix", 2}}, {domain = true, stage = 3})
recipe("climate-science-pack", "Interplanetary climate science", "crafting", 15, {{"sn-climate-data", 2}, {"sn-thermophile-culture", 1}, {"sn-holmium-catalyst", 1}, {"sn-symbiotic-culture", 1}}, {{"sn-climate-science-pack", 4}}, {domain = true, stage = 2})
recipe("biosphere-matrix", "Propagate an established community", "sn-hydroponics", 10, {{"sn-biosphere-data", 4}, {"sn-biodiversity-matrix", 1}, {"sn-clean-water", 50, "fluid"}}, {{"sn-biodiversity-matrix", 2}}, {domain = true, stage = 4, recycle = false})
recipe("gaia-cell", "Gaia coordination cells", "crafting", 20, {{"sn-biodiversity-matrix", 1}, {"superconductor", 1}, {"carbon-fiber", 1}, {"lithium-plate", 1}}, {{"sn-gaia-cell", 2}}, {domain = true, stage = 3})
recipe("ecological-sample-recovery", "Recover surplus ecological samples", "sn-reclamation", 5, {{"sn-ecological-data", 5}, {"water", 20, "fluid"}}, {{"sn-mineral-nutrients", 1}, {"sn-clean-water", 10, "fluid"}}, {recycle = false})
recipe("climate-sample-recovery", "Recover surplus climate samples", "sn-reclamation", 5, {{"sn-climate-data", 5}, {"water", 20, "fluid"}}, {{"sn-glass", 1}, {"sn-clean-water", 10, "fluid"}}, {recycle = false})
recipe("biosphere-sample-recovery", "Recover surplus biosphere samples", "sn-composting", 5, {{"sn-biosphere-data", 5}}, {{"sn-compost", 2}}, {recycle = false})

-- Every operation has a dedicated, fixed-recipe machine. Only completed crafts earn effects.
local function operation(name, title, category, seconds, ingredients, results, effects, opts)
  opts = opts or {}; opts.effects = effects; opts.domain = true; opts.operation = true; opts.recycle = false
  recipe(name, title, "sn-" .. category, seconds, ingredients, results, opts)
end
operation("air-scrubbing", "Restore atmospheric balance", "scrubbing", 10,
  {{"sn-filter-cartridge", 1}, {"water", 25, "fluid"}}, {{"sn-spent-filter", 1}, {"sn-climate-data", 1}},
  {atmosphere = 0.14, toxicity = -0.045, pollution = -40})
operation("soil-restoration", "Restore living soil", "soil-restoration", 15,
  {{"sn-soil-substrate", 3}, {"sn-microbial-culture", 1}, {"water", 20, "fluid"}}, {{"sn-ecological-data", 2}},
  {soil = 0.18, biodiversity = 0.045, toxicity = -0.06, pollution = -8, terrain = true})
operation("pioneer-reseeding", "Seed pioneer ecosystems", "reseeding", 15,
  {{"sn-seed-mix", 1}, {"sn-soil-substrate", 1}, {"sn-clean-water", 20, "fluid"}}, {{"sn-ecological-data", 2}},
  {biodiversity = 0.18, atmosphere = 0.025, water = 0.015, pollution = -12, terrain = true, trees = true})
operation("watershed-restoration", "Restore the water cycle", "watershed", 12,
  {{"sn-clean-water", 100, "fluid"}, {"sn-ceramic-membrane", 1}}, {{"sn-climate-data", 2}, {"sn-toxic-effluent", 10, "fluid"}},
  {water = 0.20, soil = 0.035, toxicity = -0.025, pollution = -10})
operation("thermal-balancing", "Normalize thermal balance", "thermal-balancing", 20,
  {{"sn-thermal-buffer", 1}, {"water", 100, "fluid"}}, {{"sn-depleted-thermal-buffer", 1}, {"sn-climate-data", 2}},
  {temperature = 0.24, atmosphere = 0.025})
operation("mineral-detoxification", "Bind planetary toxins", "detoxification", 15,
  {{"sn-neutralization-charge", 2}, {"water", 50, "fluid"}}, {{"sn-hazardous-sludge", 2}, {"sn-climate-data", 1}},
  {toxicity = -0.38, atmosphere = 0.05, soil = 0.025, pollution = -30})
operation("pheromone-dampening", "Mask ecological disturbance", "dampening", 12,
  {{"sn-biofilm", 2}, {"sn-activated-carbon", 1}, {"water", 20, "fluid"}}, {{"sn-ecological-data", 1}},
  {pressure = -0.85})
operation("atmospheric-forcing", "Force the atmosphere [dirty]", "forcing", 6,
  {{"coal", 8}, {"sn-mineral-nutrients", 1}, {"water", 20, "fluid"}}, {{"sn-climate-data", 1}, {"sn-hazardous-sludge", 1}},
  {atmosphere = 0.36, temperature = -0.06, water = -0.03, toxicity = 0.48, pollution = 45})
operation("basalt-weathering", "Weather Vulcanus basalt", "weathering", 15,
  {{"calcite", 10}, {"tungsten-ore", 2}, {"water", 50, "fluid"}}, {{"sn-mineral-nutrients", 4}, {"sn-climate-data", 2}},
  {temperature = 0.40, soil = 0.24, atmosphere = 0.06, toxicity = -0.12, terrain = true}, {planet = "vulcanus"})
operation("fulgoran-recovery", "Recover Fulgoran legacy waste", "fulgoran-recovery", 12,
  {{"scrap", 10}, {"sn-electrolyte", 30, "fluid"}}, {{"sn-heavy-metal-cake", 2}, {"sn-climate-data", 2}},
  {atmosphere = 0.16, soil = 0.24, water = 0.10, toxicity = -0.5, terrain = true}, {planet = "fulgora"})
operation("spore-balancing", "Rebalance Gleban spores", "spore-balancing", 12,
  {{"nutrients", 5}, {"sn-filter-cartridge", 1}, {"water", 50, "fluid"}}, {{"sn-spent-filter", 1}, {"sn-symbiotic-culture", 1}},
  {atmosphere = 0.10, biodiversity = 0.25, soil = 0.12, toxicity = -0.15, pollution = -45, terrain = true}, {planet = "gleba"})
operation("cryogenic-restoration", "Cultivate sheltered thaw zones", "cryogenic-restoration", 15,
  {{"sn-thermal-buffer", 1}, {"ice", 10}, {"ammonia", 30, "fluid"}}, {{"water", 80, "fluid"}, {"sn-depleted-thermal-buffer", 1}, {"sn-biosphere-data", 2}},
  {temperature = 0.50, water = 0.32, biodiversity = 0.05, toxicity = -0.035, garden = true}, {planet = "aquilo"})
operation("habitat-restoration", "Establish a biodiversity sanctuary", "habitat-restoration", 20,
  {{"sn-biodiversity-matrix", 1}, {"sn-mineral-nutrients", 5}, {"sn-clean-water", 100, "fluid"}}, {{"sn-biosphere-data", 2}},
  {biodiversity = 0.42, soil = 0.08, water = 0.04, toxicity = -0.07, pollution = -20, terrain = true, trees = true}, {stage = 2})
operation("gaia-coordination", "Coordinate the living-world network", "gaia-coordination", 60,
  {{"sn-gaia-cell", 1}, {"sn-clean-water", 50, "fluid"}}, {{"sn-restoration-science-pack", 2}},
  {atmosphere = 0.05, temperature = 0.05, water = 0.05, soil = 0.05, biodiversity = 0.05, toxicity = -0.025, beacon = true}, {stage = 4})

local function construction(name, ingredients, time)
  recipe(name, "Build " .. name, "crafting", time or 5, ingredients, {{"sn-" .. name, 1}}, {machine = true})
end
construction("algae-vat", {{"iron-plate", 12}, {"copper-plate", 5}, {"pipe", 8}, {"sn-glass", 10}})
construction("composter", {{"iron-plate", 10}, {"iron-gear-wheel", 5}, {"stone-brick", 8}})
construction("ecology-monitor", {{"electronic-circuit", 5}, {"iron-plate", 5}, {"sn-glass", 2}}, 2)
construction("soil-enricher", {{"steel-plate", 8}, {"electronic-circuit", 8}, {"pipe", 10}, {"sn-soil-substrate", 10}})
construction("air-scrubber", {{"steel-plate", 10}, {"electronic-circuit", 12}, {"pipe", 10}, {"sn-glass", 10}})
construction("reclamation-plant", {{"steel-plate", 15}, {"electronic-circuit", 12}, {"pipe", 15}, {"sn-glass", 12}})
construction("watershed", {{"steel-plate", 15}, {"electronic-circuit", 15}, {"pipe", 20}, {"sn-ceramic-membrane", 12}})
construction("seed-disperser", {{"steel-plate", 12}, {"electronic-circuit", 10}, {"pipe", 8}, {"sn-seed-mix", 10}})
construction("hydroponics-bay", {{"steel-plate", 20}, {"electronic-circuit", 20}, {"sn-glass", 30}, {"sn-biofilm", 20}})
construction("pheromone-dampener", {{"steel-plate", 10}, {"electronic-circuit", 12}, {"sn-biofilm", 15}})
construction("pyrolyzer", {{"steel-plate", 12}, {"stone-brick", 20}, {"electronic-circuit", 5}})
construction("forcing-tower", {{"steel-plate", 15}, {"pipe", 20}, {"stone-brick", 20}, {"electronic-circuit", 10}})
construction("thermal-exchanger", {{"steel-plate", 30}, {"advanced-circuit", 15}, {"pipe", 20}, {"sn-thermal-buffer", 10}}, 10)
construction("electrolyzer", {{"steel-plate", 20}, {"advanced-circuit", 15}, {"copper-plate", 30}, {"sn-ceramic-membrane", 10}}, 10)
construction("materials-kiln", {{"steel-plate", 20}, {"advanced-circuit", 10}, {"stone-brick", 30}}, 10)
construction("detoxifier", {{"steel-plate", 25}, {"advanced-circuit", 15}, {"sn-ceramic-membrane", 20}, {"pipe", 20}}, 10)
construction("basalt-conditioner", {{"tungsten-plate", 20}, {"calcite", 50}, {"processing-unit", 15}, {"sn-thermal-buffer", 20}}, 15)
construction("fulgoran-reclaimer", {{"holmium-plate", 20}, {"steel-plate", 30}, {"processing-unit", 15}, {"sn-ceramic-membrane", 20}}, 15)
construction("spore-tower", {{"biochamber", 1}, {"processing-unit", 15}, {"sn-filter-cartridge", 30}, {"sn-biofilm", 30}}, 15)
construction("cryogenic-garden", {{"cryogenic-plant", 1}, {"lithium-plate", 20}, {"sn-biodiversity-matrix", 10}, {"sn-thermal-buffer", 20}}, 20)
construction("sanctuary", {{"biochamber", 1}, {"processing-unit", 30}, {"sn-biodiversity-matrix", 20}, {"sn-glass", 40}}, 20)
construction("planetary-beacon", {{"cryogenic-plant", 1}, {"quantum-processor", 20}, {"superconductor", 30}, {"sn-biodiversity-matrix", 30}, {"sn-thermal-buffer", 30}}, 30)

local packs = {
  r = "automation-science-pack", g = "logistic-science-pack", b = "chemical-science-pack", p = "production-science-pack",
  y = "utility-science-pack", s = "space-science-pack", m = "metallurgic-science-pack", e = "electromagnetic-science-pack",
  a = "agricultural-science-pack", c = "cryogenic-science-pack", E = "sn-ecology-science-pack", C = "sn-climate-science-pack", R = "sn-restoration-science-pack"
}
local function tech(name, title, prerequisites, science, count, unlocks, desc, options)
  local ingredients = {}
  for code in science:gmatch(".") do ingredients[#ingredients + 1] = {assert(packs[code], code), 1} end
  local x = {name = name, title = title, prerequisites = prerequisites, science = ingredients, count = count,
    unlocks = unlocks, description = desc, seconds = 30}
  for key, value in pairs(options or {}) do x[key] = value end
  K.technologies[#K.technologies + 1] = x
end
tech("biofoundations", "Pioneer biology", {"automation"}, "r", 30,
  {"algae-vat", "mineral-nutrients", "abiogenesis", "algae-cultivation"},
  "Start a living industry from stone, iron and water. The electric bioreactor replaces the need for an irreplaceable seed.")
tech("composting", "The living substrate", {"sn-biofoundations"}, "r", 40,
  {"composter", "compost", "wood-compost", "spoilage-compost", "biochar", "soil-substrate"},
  "Turn biomass into the compost needed by logistics and planetary soil recovery.")
tech("environmental-monitoring", "Field ecology", {"sn-composting", "logistic-science-pack", "steel-processing"}, "rg", 80,
  {"soil-enricher", "soil-restoration", "ecology-science-pack", "ecology-monitor"},
  "Real restoration earns field samples. Read ecological fitness and automate responses with circuit telemetry.")
tech("atmospheric-engineering", "Atmospheric engineering", {"sn-environmental-monitoring", "fluid-handling"}, "rg", 120,
  {"activated-carbon", "filter-cartridge", "air-scrubber", "air-scrubbing", "pheromone-dampener", "pheromone-dampening"},
  "Scrub local pollution while rebuilding atmospheric suitability. Native organisms may resist even clean industry.")
tech("water-cycle", "The water cycle", {"sn-atmospheric-engineering"}, "rgE", 120,
  {"ceramic-membrane", "reclamation-plant", "water-filtration", "watershed", "watershed-restoration", "neutralization-charge", "ecological-sample-recovery", "climate-sample-recovery"},
  "Purified water connects climate, biology and industry. Keep byproducts flowing; they are part of the factory.")
tech("reforestation", "Pioneer forests", {"sn-water-cycle"}, "rgE", 150,
  {"pioneer-timber", "seed-mix", "seed-disperser", "pioneer-reseeding", "hydroponics-bay", "hydroponic-timber"},
  "Seed a diverse biosphere, then exploit the efficiency of established cultivation. Forest growth is gentle on existing infrastructure.")
tech("dirty-shortcuts", "Industrial forcing", {"sn-atmospheric-engineering"}, "rg", 80,
  {"pyrolyzer", "coal-activation", "forced-substrate", "forcing-tower", "atmospheric-forcing"},
  "A deliberate compromise: rapid startup and higher material yields, paid for in pollution, sludge and planetary toxicity.")
tech("thermal-engineering", "Climate control", {"sn-water-cycle", "chemical-science-pack"}, "rgbE", 180,
  {"thermal-buffer", "thermal-exchanger", "thermal-balancing", "electrolyzer", "water-electrolysis", "buffer-recharging"},
  "Move beyond temperate Nauvis. High-power heat transfer works in either hot or frozen environments.")
tech("closed-loops", "Nothing left behind", {"sn-thermal-engineering", "concrete"}, "rgbE", 220,
  {"filter-reclamation", "effluent-treatment", "materials-kiln", "waste-vitrification", "aggregate-concrete", "electric-glass", "electric-ceramics", "detoxifier", "mineral-detoxification"},
  "Close the cartridge, water and thermal loops; bind the remaining waste into construction aggregate.")
tech("clean-chemistry", "Post-fossil chemistry", {"sn-closed-loops", "plastics", "sulfur-processing"}, "rgbE", 250,
  {"bioleachate", "clean-iron", "clean-copper", "clean-plastic", "renewable-fuel", "oxygenated-steel", "green-concrete"},
  "Use energy and biology instead of fossil feedstocks. Better ore yields do not make contaminated effluent disappear.")
tech("planetary-ecology", "Planetary ecology", {"sn-reforestation", "sn-closed-loops", "space-science-pack"}, "rgbsE", 350,
  {"electrolyte"}, "Every world has an ecological specialty. Restoration now becomes an interplanetary logistics problem.")
tech("vulcanus-restoration", "Weather the furnace", {"sn-planetary-ecology", "metallurgic-science-pack"}, "rgbsEm", 250,
  {"basalt-conditioner", "basalt-weathering", "thermophile-culture"},
  "Weather volcanic basalt, shelter heat-loving pioneer life and export thermophile cultures. The lava stays lava.")
tech("fulgora-remediation", "Life after the scrapyard", {"sn-planetary-ecology", "electromagnetic-science-pack"}, "rgbsEe", 250,
  {"fulgoran-reclaimer", "fulgoran-recovery", "heavy-metal-refining", "holmium-catalyst"},
  "Mine Fulgora's toxic legacy for useful metals. Rebuild soils on the islands without changing oil seas or lightning.")
tech("gleba-symbiosis", "Beyond the monoculture", {"sn-planetary-ecology", "agricultural-science-pack"}, "rgbsEa", 250,
  {"spore-tower", "spore-balancing", "symbiotic-fermentation", "compost-nutrients", "hydroponic-yumako", "hydroponic-jellynut"},
  "Gleba is alive, not restored. Promote a diverse, stable ecology while retaining spores, spoilage and pentapod risk.")
tech("habitat-engineering", "Many worlds, one biosphere", {"sn-vulcanus-restoration", "sn-fulgora-remediation", "sn-gleba-symbiosis"}, "rgbspymeaE", 400,
  {"biodiversity-matrix", "sanctuary", "habitat-restoration", "biosphere-matrix", "biosphere-sample-recovery"},
  "Combine the specialties of three planets into biodiversity sanctuaries. No single-planet shortcut to mature ecosystems.")
tech("climate-science", "Comparative climatology", {"sn-habitat-engineering"}, "rgbsmaeE", 300,
  {"climate-science-pack"}, "An interplanetary science built from actual climate work and three ecological specialties.")
tech("aquilo-habitats", "A garden beneath the ice", {"sn-climate-science", "cryogenic-science-pack"}, "rgbscEC", 350,
  {"cryogenic-garden", "cryogenic-restoration"}, "Build sheltered cryogenic gardens. Aquilo still needs heat, foundations and long-distance supplies.")
tech("planetary-coordination", "The Gaia network", {"sn-aquilo-habitats", "quantum-processor"}, "rgbspymeacEC", 600,
  {"gaia-cell", "planetary-beacon", "gaia-coordination"},
  "Operate planetary beacons on living worlds. Continuous shipments prove that restoration can outlive its construction phase.")
tech("living-worlds", "Second Nature", {"sn-planetary-coordination"}, "rgbspymeacECR", 200, {},
  "Win by sustaining every planet at self-sustaining status with a recent beacon cycle for ten uninterrupted minutes. No return flight required.", {seconds = 60})
tech("ecological-research", "Ecological research productivity", {"sn-living-worlds"}, "rgbspymeacECR", "1000*1.5^(L-1)", {},
  "Continue using the restored network after victory. Each level adds 2% laboratory productivity.",
  {max_level = "infinite", effects = {{type = "laboratory-productivity", modifier = 0.02}}, seconds = 60})

local Expedition = require("shared.expedition")
for _, x in ipairs(Expedition.items) do
  if x.kind == "item" then x.family = "mineral"; K.items[#K.items + 1] = x end
end
for _, x in ipairs(Expedition.recipes) do K.recipes[#K.recipes + 1] = x end
for _, x in ipairs(Expedition.technologies) do K.technologies[#K.technologies + 1] = x end
local Logistics = require("shared.logistics")
for _, x in ipairs(Logistics.recipes) do K.recipes[#K.recipes + 1] = x end
for _, x in ipairs(Logistics.technologies) do K.technologies[#K.technologies + 1] = x end
K.expedition = {}
for _, x in ipairs(Expedition.items) do K.expedition[#K.expedition + 1] = x end
for _, x in ipairs(Logistics.items) do K.expedition[#K.expedition + 1] = x end
K.by_recipe, K.by_machine = {}, {}
for _, r in ipairs(K.recipes) do K.by_recipe["sn-" .. r.name] = r end
for _, m in ipairs(K.machines) do K.by_machine["sn-" .. m.name] = m end
return K
