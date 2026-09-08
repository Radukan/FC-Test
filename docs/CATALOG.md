# Complete content catalog

Generated from `second-nature/shared/catalog.lua` by `python tools/generate_docs.py`. Do not hand-edit tables.

**22 machines · 140 recipes · 50 technologies · 32 material/science items · 9 fluids.**

Times are seconds at crafting speed 1. Fitness effects are percentage points per completed cycle before planetary multipliers and support ceilings. No custom recipe supports productivity. Native recipe quality is disabled for operations and closed/catalytic loops.

## Machines

New construction uses the canonical footprints below. Complex processes occupy 5 x 5 or 7 x 7 tiles; simple stations remain compact. Existing compact entities and their blueprint geometry are preserved, but mining one returns the item for the new larger plant. All crafting machines are electric and require heat on Aquilo.

| Machine | New footprint | Legacy footprint | Power | Recipe role | Unlock |
|---|---:|---:|---:|---|---|
| Pioneer bioreactor | 5 x 5 | 3 x 3 | 180kW | bioculture | Pioneer biology |
| Aerobic composter | 3 x 3 | 3 x 3 | 120kW | composting | The living substrate |
| Hydroponics bay | 5 x 5 | 3 x 3 | 650kW | hydroponics | Pioneer forests |
| Electrochemical works | 5 x 5 | 3 x 3 | 1.8MW | electrochemistry | Climate control |
| Closed-loop reclamation plant | 5 x 5 | 3 x 3 | 800kW | reclamation | The water cycle |
| Electric materials kiln | 5 x 5 | 3 x 3 | 900kW | kiln | Nothing left behind |
| Dirty pyrolysis retort | 3 x 3 | 3 x 3 | 350kW | pyrolysis | Industrial forcing |
| Atmospheric scrubber | 3 x 3 | 3 x 3 | 450kW | Fixed: Restore atmospheric balance | Atmospheric engineering |
| Soil restoration station | 3 x 3 | 3 x 3 | 300kW | Fixed: Restore living soil | Field ecology |
| Pioneer seed disperser | 3 x 3 | 3 x 3 | 500kW | Fixed: Seed pioneer ecosystems | Pioneer forests |
| Watershed restoration plant | 5 x 5 | 3 x 3 | 750kW | Fixed: Restore the water cycle | The water cycle |
| Climate heat exchanger | 5 x 5 | 3 x 3 | 4MW | Fixed: Normalize thermal balance | Climate control |
| Mineral detoxification plant | 5 x 5 | 3 x 3 | 1.5MW | Fixed: Bind planetary toxins | Nothing left behind |
| Pheromone dampener | 3 x 3 | 3 x 3 | 400kW | Fixed: Mask ecological disturbance | Atmospheric engineering |
| Atmospheric forcing stack | 3 x 3 | 3 x 3 | 600kW | Fixed: Force the atmosphere [dirty] | Industrial forcing |
| Basalt weathering station | 5 x 5 | 3 x 3 | 2.5MW | Fixed: Weather Vulcanus basalt | Weather the furnace |
| Fulgoran remediation works | 5 x 5 | 3 x 3 | 2MW | Fixed: Recover Fulgoran legacy waste | Life after the scrapyard |
| Symbiotic spore tower | 5 x 5 | 3 x 3 | 1.2MW | Fixed: Rebalance Gleban spores | Beyond the monoculture |
| Cryogenic garden | 7 x 7 | 5 x 5 | 3.5MW | Fixed: Cultivate sheltered thaw zones | A garden beneath the ice |
| Biodiversity sanctuary | 7 x 7 | 3 x 3 | 2.2MW | Fixed: Establish a biodiversity sanctuary | Many worlds, one biosphere |
| Gaia planetary beacon | 7 x 7 | 5 x 5 | 5MW | Fixed: Coordinate the living-world network | The Gaia network |
| Ecology circuit monitor | 1 x 1 | 1 x 1 | Passive sensor | Circuit telemetry | Field ecology |

## Restoration operations

| Operation | Time | Inputs → Outputs | Ecological effect / cycle | Conditions |
|---|---:|---|---|---|
| Restore atmospheric balance | 10 s | 1 Carbon filter cartridge + 25 Water [fluid] → 1 Spent filter cartridge + 1 Climate samples | atmosphere +0.042; toxicity -0.0135; pollution -10 | Any stock planet |
| Restore living soil | 15 s | 3 Soil substrate + 1 Pioneer culture + 20 Water [fluid] → 2 Ecological samples | soil +0.054; biodiversity +0.0135; toxicity -0.018; pollution -2 | Any stock planet |
| Seed pioneer ecosystems | 15 s | 1 Pioneer seed mix + 1 Soil substrate + 20 Purified water [fluid] → 2 Ecological samples | atmosphere +0.0075; water +0.0045; biodiversity +0.054; pollution -3 | Any stock planet |
| Restore the water cycle | 12 s | 100 Purified water [fluid] + 1 Ceramic membrane → 2 Climate samples + 10 Toxic effluent [fluid] | water +0.06; soil +0.0105; toxicity -0.0075; pollution -2.5 | Any stock planet |
| Normalize thermal balance | 20 s | 1 Charged thermal buffer + 100 Water [fluid] → 1 Depleted thermal buffer + 2 Climate samples | atmosphere +0.0075; temperature +0.072 | Any stock planet |
| Bind planetary toxins | 15 s | 2 Neutralization charge + 50 Water [fluid] → 2 Hazardous sludge + 1 Climate samples | atmosphere +0.015; soil +0.0075; toxicity -0.114; pollution -7.5 | Any stock planet |
| Mask ecological disturbance | 12 s | 2 Engineered biofilm + 1 Activated carbon + 20 Water [fluid] → 1 Ecological samples | pressure -0.255 | Any stock planet |
| Force the atmosphere [dirty] | 6 s | 8 Coal + 1 Mineral nutrients + 20 Water [fluid] → 1 Climate samples + 1 Hazardous sludge | atmosphere +0.108; temperature -0.018; water -0.009; toxicity +0.144; pollution +45 | Any stock planet |
| Weather Vulcanus basalt | 15 s | 10 Calcite + 2 Tungsten ore + 50 Water [fluid] → 4 Mineral nutrients + 2 Climate samples | atmosphere +0.018; temperature +0.12; soil +0.072; toxicity -0.036 | Vulcanus |
| Recover Fulgoran legacy waste | 12 s | 10 Scrap + 30 Mineral electrolyte [fluid] → 2 Heavy-metal concentrate + 2 Climate samples | atmosphere +0.048; water +0.03; soil +0.072; toxicity -0.15 | Fulgora |
| Rebalance Gleban spores | 12 s | 5 Nutrients + 1 Carbon filter cartridge + 50 Water [fluid] → 1 Spent filter cartridge + 1 Symbiotic culture | atmosphere +0.03; soil +0.036; biodiversity +0.075; toxicity -0.045; pollution -11.25 | Gleba |
| Cultivate sheltered thaw zones | 15 s | 1 Charged thermal buffer + 10 Ice + 30 Ammonia [fluid] → 80 Water [fluid] + 1 Depleted thermal buffer + 2 Biosphere samples | temperature +0.15; water +0.096; biodiversity +0.015; toxicity -0.0105 | Aquilo |
| Establish a biodiversity sanctuary | 20 s | 1 Biodiversity matrix + 5 Mineral nutrients + 100 Purified water [fluid] → 2 Biosphere samples | water +0.012; soil +0.024; biodiversity +0.126; toxicity -0.021; pollution -5 | Any stock planet, stage ≥ 2 |
| Coordinate the living-world network | 60 s | 1 Gaia coordination cell + 50 Purified water [fluid] → 2 Restoration science pack | atmosphere +0.015; temperature +0.015; water +0.015; soil +0.015; biodiversity +0.015; toxicity -0.0075 | Any stock planet, stage ≥ 4 |

## Processing recipes

Recipes tagged **dirty** also emit vanilla pollution/spores and incur explicit toxicity; switching/clearing a dirty retort recipe cannot launder that debt.

| Recipe | Time | Inputs | Outputs | Unlock / condition |
|---|---:|---|---|---|
| Crush silica | 1 s | 2 Stone | 2 Silica | Available from start |
| Smelt laboratory glass | 3.2 s | 2 Silica | 2 Laboratory glass | Available from start |
| Dissolve mineral nutrients | 4 s | 3 Stone + 1 Iron ore + 20 Water [fluid] | 4 Mineral nutrients | Pioneer biology |
| Synthesize pioneer culture | 14 s | 2 Stone + 1 Iron ore + 30 Water [fluid] | 2 Pioneer culture | Pioneer biology |
| Cultivate algae | 8 s | 1 Pioneer culture + 1 Mineral nutrients + 40 Water [fluid] | 8 Algal biomass + 1 Pioneer culture | Pioneer biology |
| Aerobic composting | 5 s | 6 Algal biomass | 4 Living compost + 1 Engineered biofilm | The living substrate |
| Compost wood | 6 s | 4 Wood | 4 Living compost + 1 Engineered biofilm | The living substrate |
| Recover spoiled organics | 4 s | 10 Spoilage | 5 Living compost + 1 Engineered biofilm | The living substrate |
| Slow biomass carbonization | 10 s | 8 Algal biomass | 3 Biochar | The living substrate |
| Renewable carbon activation | 6 s | 2 Biochar + 10 Water [fluid] | 2 Activated carbon | Atmospheric engineering |
| Carbon filter cartridges | 2 s | 2 Activated carbon + 1 Laboratory glass + 1 Iron plate | 2 Carbon filter cartridge | Atmospheric engineering |
| Living soil substrate | 5 s | 3 Living compost + 2 Silica + 1 Biochar | 4 Soil substrate | The living substrate |
| Ecology science | 8 s | 2 Ecological samples + 2 Laboratory glass + 2 Electronic circuit | 2 Ecology science pack | Field ecology |
| Porous ceramic membrane | 4 s | 3 Stone brick + 2 Silica + 1 Laboratory glass | 2 Ceramic membrane | The water cycle |
| Purify process water | 5 s | 1 Carbon filter cartridge + 100 Water [fluid] | 90 Purified water [fluid] + 1 Spent filter cartridge | The water cycle |
| Mineral neutralization charge | 3 s | 6 Stone + 1 Biochar | 2 Neutralization charge | The water cycle |
| Pioneer timber cultivation | 18 s | 12 Algal biomass + 2 Living compost + 30 Water [fluid] | 6 Wood | Pioneer forests |
| Prepare pioneer seed mix | 3 s | 1 Pioneer culture + 4 Algal biomass + 2 Living compost | 2 Pioneer seed mix | Pioneer forests |
| Established timber cultivation | 12 s | 1 Pioneer seed mix + 2 Mineral nutrients + 40 Purified water [fluid] | 12 Wood + 1 Pioneer seed mix | Pioneer forests; Any stock planet, stage ≥ 2 |
| Charge a new thermal buffer | 5 s | 1 Steel plate + 3 Copper plate + 2 Laboratory glass | 2 Charged thermal buffer | Climate control |
| Water electrolysis | 10 s | 100 Purified water [fluid] | 80 Hydrogen [fluid] + 40 Oxygen [fluid] | Climate control |
| Recharge thermal buffers | 10 s | 1 Depleted thermal buffer + 1 Engineered biofilm + 40 Purified water [fluid] | 1 Charged thermal buffer | Climate control |
| Reclaim spent filters | 8 s | 2 Spent filter cartridge + 30 Purified water [fluid] | 2 Activated carbon + 1 Laboratory glass + 20 Toxic effluent [fluid] | Nothing left behind |
| Neutralize captured effluent | 10 s | 100 Toxic effluent [fluid] + 2 Neutralization charge | 80 Water [fluid] + 4 Hazardous sludge | Nothing left behind |
| Vitrify hazardous sludge | 12 s | 4 Hazardous sludge + 2 Laboratory glass | 2 Vitrified aggregate | Nothing left behind |
| Concrete from bound waste | 10 s | 1 Vitrified aggregate + 4 Stone brick + 20 Water [fluid] | 10 Concrete | Nothing left behind |
| Electric glass firing | 4 s | 4 Silica | 4 Laboratory glass | Nothing left behind |
| Electric ceramic firing | 4 s | 4 Stone + 2 Silica | 4 Ceramic membrane | Nothing left behind |
| Coal activation [dirty] | 3 s | 3 Coal + 1 Silica | 6 Activated carbon + 1 Hazardous sludge | Industrial forcing |
| Chemically forced substrate [dirty] | 3 s | 2 Coal + 4 Stone + 1 Living compost | 8 Soil substrate + 1 Hazardous sludge | Industrial forcing |
| Prepare bioleachate | 5 s | 2 Living compost + 30 Purified water [fluid] | 40 Bioleachate [fluid] | Post-fossil chemistry |
| Biological iron refining | 8 s | 4 Iron ore + 20 Bioleachate [fluid] | 6 Iron plate + 10 Toxic effluent [fluid] | Post-fossil chemistry |
| Biological copper refining | 8 s | 4 Copper ore + 20 Bioleachate [fluid] | 6 Copper plate + 10 Toxic effluent [fluid] | Post-fossil chemistry |
| Renewable bioplastic | 6 s | 5 Algal biomass + 20 Hydrogen [fluid] | 2 Plastic bar | Post-fossil chemistry |
| Renewable solid fuel | 8 s | 4 Algal biomass + 50 Hydrogen [fluid] | 2 Solid fuel | Post-fossil chemistry |
| Oxygen-assisted steel | 12 s | 10 Iron plate + 50 Oxygen [fluid] | 3 Steel plate | Post-fossil chemistry |
| Biomineral concrete | 8 s | 2 Living compost + 4 Silica + 4 Stone brick + 30 Water [fluid] | 10 Concrete | Post-fossil chemistry |
| Mineral electrolyte | 5 s | 4 Stone + 50 Purified water [fluid] | 50 Mineral electrolyte [fluid] | Planetary ecology |
| Cultivate thermophiles | 12 s | 2 Pioneer culture + 5 Calcite + 50 Sulfuric acid [fluid] | 2 Thermophile culture | Weather the furnace; Vulcanus, stage ≥ 1 |
| Refine recovered metals | 10 s | 3 Heavy-metal concentrate + 20 Sulfuric acid [fluid] | 1 Holmium ore + 3 Iron ore + 2 Copper ore | Life after the scrapyard |
| Holmium biocatalyst | 8 s | 2 Heavy-metal concentrate + 1 Holmium plate + 20 Mineral electrolyte [fluid] | 2 Holmium biocatalyst | Life after the scrapyard; Fulgora, stage ≥ 1 |
| Symbiotic egg fermentation | 8 s | 1 Pentapod egg + 10 Nutrients + 30 Purified water [fluid] | 4 Symbiotic culture | Beyond the monoculture; Gleba, stage ≥ 2 |
| Feed the Gleban nutrient loop | 4 s | 4 Living compost + 20 Oxygen [fluid] | 20 Nutrients | Beyond the monoculture |
| Sheltered yumako cultivation | 25 s | 1 Yumako seed + 10 Nutrients + 100 Purified water [fluid] | 20 Yumako + 1 Yumako seed | Beyond the monoculture; Gleba, stage ≥ 3 |
| Sheltered jellynut cultivation | 25 s | 1 Jellynut seed + 10 Nutrients + 100 Purified water [fluid] | 20 Jellynut + 1 Jellynut seed | Beyond the monoculture; Gleba, stage ≥ 3 |
| Assemble a living community | 15 s | 1 Thermophile culture + 1 Holmium biocatalyst + 1 Symbiotic culture + 2 Engineered biofilm | 2 Biodiversity matrix | Many worlds, one biosphere; Any stock planet, stage ≥ 3 |
| Interplanetary climate science | 15 s | 2 Climate samples + 1 Thermophile culture + 1 Holmium biocatalyst + 1 Symbiotic culture | 4 Climate science pack | Comparative climatology; Any stock planet, stage ≥ 2 |
| Propagate an established community | 10 s | 4 Biosphere samples + 1 Biodiversity matrix + 50 Purified water [fluid] | 2 Biodiversity matrix | Many worlds, one biosphere; Any stock planet, stage ≥ 4 |
| Gaia coordination cells | 20 s | 1 Biodiversity matrix + 1 Superconductor + 1 Carbon fiber + 1 Lithium plate | 2 Gaia coordination cell | The Gaia network; Any stock planet, stage ≥ 3 |
| Recover surplus ecological samples | 5 s | 5 Ecological samples + 20 Water [fluid] | 1 Mineral nutrients + 10 Purified water [fluid] | The water cycle |
| Recover surplus climate samples | 5 s | 5 Climate samples + 20 Water [fluid] | 1 Laboratory glass + 10 Purified water [fluid] | The water cycle |
| Recover surplus biosphere samples | 5 s | 5 Biosphere samples | 2 Living compost | Many worlds, one biosphere |
| Form mineral-composite stocks | 1 s | 2 Iron plate + 2 Stone | 2 Mineral-composite stock | Available from start |
| Assemble expedition magazines | 2 s | 4 Iron plate + 1 Copper plate | 1 Sn ballistic magazine | Available from start |
| Prepare sterile field dressings | 3 s | 2 Engineered biofilm + 1 Laboratory glass | 2 Sn field dressing | Frontier defense |
| Pack bioactive flechettes | 4 s | 3 Iron plate + 3 Algal biomass + 1 Engineered biofilm | 2 Sn mycelial magazine | Frontier defense |
| Build an expedition carbine | 6 s | 12 Iron plate + 8 Iron gear wheel + 4 Mineral-composite stock + 5 Copper plate | 1 Sn carbine | Frontier defense |
| Build an expedition field suit | 8 s | 30 Iron plate + 10 Copper plate + 6 Mineral-composite stock | 1 Sn field armor | Frontier defense |
| Build a riveted sentry | 12 s | 25 Iron plate + 15 Iron gear wheel + 8 Electronic circuit + 8 Mineral-composite stock | 1 Sn sentry turret | Frontier defense |
| Pack riveted field barricades | 4 s | 4 Iron plate + 10 Stone | 2 Sn field barricade | Available from start |
| Build an induction rifle | 15 s | 20 Steel plate + 10 Advanced circuit + 12 Battery + 8 Mineral-composite stock | 1 Sn induction rifle | Electrical defense doctrine |
| Assemble induction cells | 5 s | 2 Battery + 3 Copper plate + 1 Electronic circuit | 1 Sn induction cell | Electrical defense doctrine |
| Build a capacitor arc turret | 20 s | 35 Steel plate + 15 Advanced circuit + 30 Battery + 10 Ceramic membrane | 1 Sn arc turret | Electrical defense doctrine |
| Build composite bastion walls | 6 s | 2 Sn field barricade + 4 Steel plate + 4 Engineered biofilm + 5 Stone brick | 2 Sn composite wall | Electrical defense doctrine |
| Build powered expedition armor | 30 s | 40 Steel plate + 30 Advanced circuit + 30 Battery + 20 Engineered biofilm | 1 Sn expedition armor | Electrical defense doctrine |
| Build a heavy lance rifle | 45 s | 1 Railgun + 30 Tungsten plate + 10 Supercapacitor + 5 Biodiversity matrix | 1 Sn lance rifle | Bastion defense doctrine |
| Assemble dense-core lance rounds | 10 s | 1 Railgun ammo + 4 Tungsten carbide + 2 Superconductor | 1 Sn lance cell | Bastion defense doctrine |
| Build a bastion lance turret | 60 s | 1 Railgun turret + 60 Tungsten plate + 20 Supercapacitor + 5 Quantum processor + 10 Biodiversity matrix | 1 Sn lance turret | Bastion defense doctrine |
| Build bastion expedition armor | 60 s | 1 Power armor mk2 + 40 Tungsten plate + 10 Quantum processor + 20 Biodiversity matrix | 1 Sn bastion armor | Bastion defense doctrine |
| Build a biosphere shield module | 30 s | 2 Energy shield mk2 equipment + 10 Supercapacitor + 5 Biodiversity matrix | 1 Sn ecoshield equipment | Bastion defense doctrine |
| Assemble a vector servo inserter | 8 s | 1 Bulk inserter + 4 Processing unit + 2 Superconductor + 4 Carbon fiber | 1 Sn vector inserter | Living-world logistics |
| Assemble a canopy stack inserter | 12 s | 1 Stack inserter + 1 Quantum processor + 4 Superconductor + 2 Biodiversity matrix | 1 Sn canopy inserter | Living-world logistics |
| Assemble vital transport sections | 3 s | 4 Turbo transport belt + 1 Superconductor + 2 Carbon fiber + 1 Gaia coordination cell | 4 Sn vital belt | Living-world logistics |
| Assemble a sealed transfer tunnel | 8 s | 2 Turbo underground belt + 8 Sn vital belt + 10 Tungsten plate + 2 Gaia coordination cell | 2 Sn vital underground belt | Living-world logistics |
| Assemble a distribution manifold | 10 s | 1 Turbo splitter + 10 Processing unit + 4 Superconductor + 2 Gaia coordination cell | 1 Sn vital splitter | Living-world logistics |
| Assemble an expedition jukebox | 5 s | 5 Electronic circuit + 10 Iron plate + 10 Copper cable | 1 Sn jukebox | Available from start |
| Assemble a wind-up construction drone | 2 s | 2 Iron plate + 1 Iron gear wheel + 1 Electronic circuit + 2 Copper cable | 1 Sn field drone | Field construction robotics |
| Build a field drone controller | 5 s | 8 Iron plate + 6 Iron gear wheel + 5 Electronic circuit + 6 Copper cable | 1 Sn field controller | Field construction robotics |
| Build Copperleaf photovoltaic bank | 10 s | 20 Iron plate + 25 Copper plate + 20 Laboratory glass + 10 Electronic circuit | 1 Sn micro solar | Practical field power |
| Build Trailblazer burner alternator | 10 s | 25 Iron plate + 15 Iron gear wheel + 25 Copper cable + 2 Stone furnace | 1 Sn burner set | Practical field power |
| Build Helical wind turbine | 15 s | 20 Steel plate + 20 Iron gear wheel + 15 Electronic circuit + 30 Copper cable | 1 Sn wind turbine | Atmospheric wind power |
| Build River paddle station | 15 s | 40 Iron plate + 25 Iron gear wheel + 10 Pipe + 10 Electronic circuit | 1 Sn river turbine | Shoreline mechanics |
| Build Twin-cylinder steam engine | 15 s | 2 Steam engine + 12 Steel plate + 15 Iron gear wheel | 1 Sn steam piston | Compact steam engineering |
| Build Producer-gas alternator | 15 s | 20 Steel plate + 6 Engine unit + 20 Pipe + 12 Electronic circuit | 1 Sn producer gas engine | Coal gasification power |
| Build Closed-loop biomass engine | 15 s | 60 Steel plate + 20 Engine unit + 20 Advanced circuit + 25 Ceramic membrane + 20 Carbon filter cartridge | 1 Sn biopellet engine | Closed-loop biomass power |
| Build Deep-loop geothermal plant | 25 s | 180 Steel plate + 12 Pumpjack + 80 Advanced circuit + 120 Pipe + 40 Charged thermal buffer + 40 Ceramic membrane | 1 Sn geothermal bore | Deep geothermal exchange |
| Build Residue-fired cogenerator | 20 s | 150 Steel plate + 50 Engine unit + 60 Advanced circuit + 25 Charged thermal buffer + 60 Pipe | 1 Sn cogenerator | Industrial residue power |
| Build Heliostat power tower | 35 s | 20 Sn micro solar + 100 Steel plate + 40 Advanced circuit + 120 Laboratory glass + 20 Charged thermal buffer | 1 Sn solar tower | Solar concentration |
| Build Anaerobic biogas turbine | 25 s | 80 Steel plate + 25 Engine unit + 30 Advanced circuit + 60 Pipe + 30 Engineered biofilm | 1 Sn biogas turbine | Anaerobic power |
| Build High-pressure recovery turbine | 25 s | 3 Steam turbine + 60 Steel plate + 20 Advanced circuit + 25 Ceramic membrane | 1 Sn heat recovery turbine | High-pressure power conversion |
| Build Photonic solar canopy | 45 s | 200 Solar panel + 120 Low density structure + 80 Processing unit + 40 Superconductor + 200 Laboratory glass | 1 Sn photonic canopy | Photonic power fields |
| Build Planetary thermal tap | 45 s | 2 Sn geothermal bore + 150 Tungsten plate + 80 Processing unit + 80 Charged thermal buffer + 80 Ceramic membrane | 1 Sn planetary thermal tap | Planetary thermal extraction |
| Build Catalytic combined-cycle plant | 35 s | 4 Sn producer gas engine + 250 Steel plate + 80 Processing unit + 80 Engine unit + 150 Pipe + 60 Ceramic membrane | 1 Sn combined cycle | Catalytic combined cycles |
| Build Solid-oxide biogas cellbank | 30 s | 2 Sn biogas turbine + 60 Processing unit + 30 Superconductor + 120 Ceramic membrane + 60 Engineered biofilm | 1 Sn biofuel cell | Solid-oxide biological cells |
| Build Lead-cooled modular reactor | 25 s | 2 Nuclear reactor + 50 Heat pipe + 60 Processing unit + 50 Charged thermal buffer + 60 Ceramic membrane | 1 Sn salt reactor | Load-following fission |
| Build Magnetoplasma generator | 25 s | 3 Fusion generator + 40 Superconductor + 10 Quantum processor + 100 Ceramic membrane | 1 Sn plasma generator | Magnetoplasma conversion |
| Assemble Sunseed solar shunter | 20 s | 1 Locomotive + 8 Solar panel + 6 Accumulator + 20 Electronic circuit + 20 Laboratory glass | 1 Sn sunseed locomotive | Solar railway |
| Assemble Heliograph solar locomotive | 40 s | 1 Sn sunseed locomotive + 12 Solar panel + 10 Accumulator + 30 Advanced circuit + 10 Charged thermal buffer | 1 Sn heliograph locomotive | Solar freight engineering |
| Assemble Daybreak solar express | 60 s | 1 Sn heliograph locomotive + 16 Solar panel + 16 Accumulator + 30 Processing unit + 30 Low density structure + 25 Engineered biofilm | 1 Sn daybreak locomotive | Advanced solar traction |
| Press a prepared biopellet | 4 s | 6 Algal biomass + 1 Biochar | 1 Sn biopellet | Closed-loop biomass power |
| Recover ash nutrients | 3 s | 4 Sn bio ash + 2 Stone | 1 Mineral nutrients | Closed-loop biomass power |
| Gasify coal | 4 s | 4 Coal + 20 Water [fluid] | 24 Producer gas [fluid] | Coal gasification power |
| Digest cultivated biomass | 8 s | 12 Algal biomass + 2 Living compost + 30 Water [fluid] | 40 Refined biogas [fluid] | Anaerobic power |
| Refine synthesis gas | 20 s | 8 Solid fuel + 50 Oxygen [fluid] + 20 Water [fluid] | 40 Catalytic synthesis gas [fluid] | Catalytic combined cycles |

## Construction recipes

| Machine | Craft time | Materials |
|---|---:|---|
| Pioneer bioreactor | 5 s | 12 Iron plate + 5 Copper plate + 8 Pipe + 10 Laboratory glass |
| Aerobic composter | 5 s | 10 Iron plate + 5 Iron gear wheel + 8 Stone brick |
| Ecology circuit monitor | 2 s | 5 Electronic circuit + 5 Iron plate + 2 Laboratory glass |
| Soil restoration station | 5 s | 8 Steel plate + 8 Electronic circuit + 10 Pipe + 10 Soil substrate |
| Atmospheric scrubber | 5 s | 10 Steel plate + 12 Electronic circuit + 10 Pipe + 10 Laboratory glass |
| Closed-loop reclamation plant | 5 s | 15 Steel plate + 12 Electronic circuit + 15 Pipe + 12 Laboratory glass |
| Watershed restoration plant | 5 s | 15 Steel plate + 15 Electronic circuit + 20 Pipe + 12 Ceramic membrane |
| Pioneer seed disperser | 5 s | 12 Steel plate + 10 Electronic circuit + 8 Pipe + 10 Pioneer seed mix |
| Hydroponics bay | 5 s | 20 Steel plate + 20 Electronic circuit + 30 Laboratory glass + 20 Engineered biofilm |
| Pheromone dampener | 5 s | 10 Steel plate + 12 Electronic circuit + 15 Engineered biofilm |
| Dirty pyrolysis retort | 5 s | 12 Steel plate + 20 Stone brick + 5 Electronic circuit |
| Atmospheric forcing stack | 5 s | 15 Steel plate + 20 Pipe + 20 Stone brick + 10 Electronic circuit |
| Climate heat exchanger | 10 s | 30 Steel plate + 15 Advanced circuit + 20 Pipe + 10 Charged thermal buffer |
| Electrochemical works | 10 s | 20 Steel plate + 15 Advanced circuit + 30 Copper plate + 10 Ceramic membrane |
| Electric materials kiln | 10 s | 20 Steel plate + 10 Advanced circuit + 30 Stone brick |
| Mineral detoxification plant | 10 s | 25 Steel plate + 15 Advanced circuit + 20 Ceramic membrane + 20 Pipe |
| Basalt weathering station | 15 s | 20 Tungsten plate + 50 Calcite + 15 Processing unit + 20 Charged thermal buffer |
| Fulgoran remediation works | 15 s | 20 Holmium plate + 30 Steel plate + 15 Processing unit + 20 Ceramic membrane |
| Symbiotic spore tower | 15 s | 1 Biochamber + 15 Processing unit + 30 Carbon filter cartridge + 30 Engineered biofilm |
| Cryogenic garden | 20 s | 1 Cryogenic plant + 20 Lithium plate + 10 Biodiversity matrix + 20 Charged thermal buffer |
| Biodiversity sanctuary | 20 s | 1 Biochamber + 30 Processing unit + 20 Biodiversity matrix + 40 Laboratory glass |
| Gaia planetary beacon | 30 s | 1 Cryogenic plant + 20 Quantum processor + 30 Superconductor + 30 Biodiversity matrix + 30 Charged thermal buffer |

## Research

`Ecology`, `Climate`, and `Restoration` are the new science packs. All other packs are stock Space Age. Numbers are research units, not individual items in the ingredients column.

| Technology | Units × time | Science ingredients per unit | Prerequisites |
|---|---:|---|---|
| Pioneer biology | 30 × 30 s | Automation | Automation |
| The living substrate | 40 × 30 s | Automation | Pioneer biology |
| Field ecology | 80 × 30 s | Automation, Logistic | The living substrate, Logistic science pack, Steel processing |
| Atmospheric engineering | 120 × 30 s | Automation, Logistic | Field ecology, Fluid handling |
| The water cycle | 120 × 30 s | Automation, Logistic, Ecology | Atmospheric engineering |
| Pioneer forests | 150 × 30 s | Automation, Logistic, Ecology | The water cycle |
| Industrial forcing | 80 × 30 s | Automation, Logistic | Atmospheric engineering |
| Climate control | 180 × 30 s | Automation, Logistic, Chemical, Ecology | The water cycle, Chemical science pack |
| Nothing left behind | 220 × 30 s | Automation, Logistic, Chemical, Ecology | Climate control, Concrete |
| Post-fossil chemistry | 250 × 30 s | Automation, Logistic, Chemical, Ecology | Nothing left behind, Plastics, Sulfur processing |
| Planetary ecology | 350 × 30 s | Automation, Logistic, Chemical, Space, Ecology | Pioneer forests, Nothing left behind, Space science pack |
| Weather the furnace | 250 × 30 s | Automation, Logistic, Chemical, Space, Ecology, Metallurgic | Planetary ecology, Metallurgic science pack |
| Life after the scrapyard | 250 × 30 s | Automation, Logistic, Chemical, Space, Ecology, Electromagnetic | Planetary ecology, Electromagnetic science pack |
| Beyond the monoculture | 250 × 30 s | Automation, Logistic, Chemical, Space, Ecology, Agricultural | Planetary ecology, Agricultural science pack |
| Many worlds, one biosphere | 400 × 30 s | Automation, Logistic, Chemical, Space, Production, Utility, Metallurgic, Electromagnetic, Agricultural, Ecology | Weather the furnace, Life after the scrapyard, Beyond the monoculture |
| Comparative climatology | 300 × 30 s | Automation, Logistic, Chemical, Space, Metallurgic, Agricultural, Electromagnetic, Ecology | Many worlds, one biosphere |
| A garden beneath the ice | 350 × 30 s | Automation, Logistic, Chemical, Space, Cryogenic, Ecology, Climate | Comparative climatology, Cryogenic science pack |
| The Gaia network | 600 × 30 s | Automation, Logistic, Chemical, Space, Production, Utility, Metallurgic, Electromagnetic, Agricultural, Cryogenic, Ecology, Climate | A garden beneath the ice, Quantum processor |
| Second Nature | 200 × 60 s | Automation, Logistic, Chemical, Space, Production, Utility, Metallurgic, Electromagnetic, Agricultural, Cryogenic, Ecology, Climate, Restoration | The Gaia network |
| Ecological research productivity | 1000*1.5^(L-1) × 60 s | Automation, Logistic, Chemical, Space, Production, Utility, Metallurgic, Electromagnetic, Agricultural, Cryogenic, Ecology, Climate, Restoration | Second Nature |
| Frontier defense | 80 × 30 s | Automation | Military, Steel processing |
| Electrical defense doctrine | 250 × 30 s | Automation, Logistic, Chemical, Military, Ecology | Laser turret, Climate control |
| Bastion defense doctrine | 600 × 30 s | Automation, Logistic, Chemical, Military, Utility, Space, Cryogenic, Climate | Railgun, The Gaia network |
| Ecological process optimization 1 | 150 × 30 s | Automation, Logistic, Ecology | Atmospheric engineering |
| Ecological process optimization 2 | 350 × 30 s | Automation, Logistic, Chemical, Ecology | Ecological process optimization 1, Climate control |
| Ecological process optimization 3 | 700 × 30 s | Automation, Logistic, Chemical, Space, Ecology, Climate | Ecological process optimization 2, Comparative climatology |
| Living-world logistics | 750 × 30 s | Automation, Logistic, Chemical, Production, Utility, Space, Climate | The Gaia network, Stack inserter, Turbo transport belt |
| Field construction robotics | 20 × 15 s | Automation | Automation |
| Field crew tuning 1 | 40 × 15 s | Automation | Field construction robotics |
| Field crew tuning 2 | 60 × 15 s | Automation, Logistic | Field crew tuning 1, Logistic science pack |
| Practical field power | 20 × 20 s | Automation | Automation |
| Atmospheric wind power | 60 × 20 s | Automation, Logistic | Practical field power, Logistic science pack |
| Closed-loop biomass power | 80 × 20 s | Automation, Logistic, Ecology | The living substrate, Practical field power, Field ecology |
| Deep geothermal exchange | 200 × 20 s | Automation, Logistic, Chemical, Ecology | Climate control, Advanced material processing 2 |
| Industrial residue power | 150 × 20 s | Automation, Logistic, Chemical, Ecology | Advanced oil processing, Climate control |
| Shoreline mechanics | 35 × 20 s | Automation | Practical field power, Logistics |
| Compact steam engineering | 40 × 20 s | Automation | Practical field power, Steel processing |
| Coal gasification power | 60 × 20 s | Automation, Logistic | Oil processing, Practical field power |
| Solar concentration | 160 × 20 s | Automation, Logistic, Chemical | Solar energy, Advanced material processing 2 |
| Anaerobic power | 160 × 20 s | Automation, Logistic, Chemical, Ecology | Closed-loop biomass power, Chemical science pack |
| High-pressure power conversion | 160 × 20 s | Automation, Logistic, Chemical, Ecology | Nuclear power, Climate control |
| Photonic power fields | 240 × 20 s | Automation, Logistic, Chemical, Production, Utility, Ecology | Solar concentration, Electromagnetic plant, Utility science pack |
| Planetary thermal extraction | 260 × 20 s | Automation, Logistic, Chemical, Production, Utility, Ecology | Deep geothermal exchange, Tungsten steel, Utility science pack |
| Catalytic combined cycles | 220 × 20 s | Automation, Logistic, Chemical, Production, Utility, Ecology | Industrial residue power, Production science pack, Utility science pack |
| Solid-oxide biological cells | 220 × 20 s | Automation, Logistic, Chemical, Production, Utility, Ecology | Anaerobic power, Electromagnetic plant, Utility science pack |
| Load-following fission | 220 × 20 s | Automation, Logistic, Chemical, Production, Utility, Ecology | Nuclear power, Deep geothermal exchange, Utility science pack |
| Magnetoplasma conversion | 300 × 20 s | Automation, Logistic, Chemical, Production, Utility, Cryogenic, Ecology | Fusion reactor, Comparative climatology |
| Solar railway | 80 × 20 s | Automation, Logistic | Railway, Solar energy, Electric energy accumulators, Practical field power |
| Solar freight engineering | 150 × 20 s | Automation, Logistic, Chemical, Ecology | Solar railway, Climate control |
| Advanced solar traction | 200 × 20 s | Automation, Logistic, Chemical, Production, Utility, Ecology | Solar freight engineering, Production science pack, Utility science pack |

## Materials and fluids

- **Silica** (`sn-silica`): Crushed silicate grains used to melt laboratory glass and fire porous ceramics.
- **Laboratory glass** (`sn-glass`): Chemically resistant glass for culture vessels, instruments and filtration assemblies.
- **Mineral nutrients** (`sn-mineral-nutrients`): A stable blend of mineral salts that feeds pioneer microorganisms.
- **Pioneer culture** (`sn-microbial-culture`): A sealed inoculum of hardy microorganisms for nutrient processing and ecological seeding.
- **Algal biomass** (`sn-algal-biomass`): Cultivated algae rich in organic carbon. Feedstock for compost, membranes and biological fuels.
- **Living compost** (`sn-compost`): A living mixture of decomposed biomass and microorganisms that enriches mineral soil.
- **Biochar** (`sn-biochar`): Porous carbon that retains nutrients, stabilizes soil and adsorbs impurities.
- **Activated carbon** (`sn-activated-carbon`): High-surface-area carbon for purification cartridges and chemical processing.
- **Carbon filter cartridge** (`sn-filter-cartridge`): A replaceable sorbent cartridge for atmospheric scrubbers and water filters.
- **Spent filter cartridge** (`sn-spent-filter`): A saturated cartridge containing recoverable carbon, glass and captured contaminants.
- **Soil substrate** (`sn-soil-substrate`): A stable rooting medium composed of mineral grains, compost and porous carbon.
- **Pioneer seed mix** (`sn-seed-mix`): A blend of pioneer seeds and microbial cultures adapted to recovering ground.
- **Ceramic membrane** (`sn-ceramic-membrane`): A porous, heat-resistant barrier that separates suspended contaminants from process water.
- **Charged thermal buffer** (`sn-thermal-buffer`): A charged heat-transfer cartridge for climate exchangers and sheltered habitats.
- **Depleted thermal buffer** (`sn-depleted-thermal-buffer`): A discharged heat-transfer cartridge. Its casing and working medium can be reconditioned.
- **Neutralization charge** (`sn-neutralization-charge`): Reactive minerals and carbon that bind dissolved contaminants into separable sludge.
- **Hazardous sludge** (`sn-hazardous-sludge`): Concentrated industrial contaminants. Vitrification locks the residue into an inert matrix.
- **Vitrified aggregate** (`sn-vitrified-waste`): An inert glass-mineral aggregate suitable for durable construction materials.
- **Engineered biofilm** (`sn-biofilm`): A cultivated polymer matrix used in membranes, composite reinforcement and pheromone carriers.
- **Ecological samples** (`sn-ecological-data`): Preserved field samples documenting soil structure, microbial activity and pioneer growth.
- **Climate samples** (`sn-climate-data`): Instrument samples recording atmospheric composition, heat transfer and water-cycle recovery.
- **Biosphere samples** (`sn-biosphere-data`): Complex habitat samples used to study interactions within established ecological communities.
- **Thermophile culture** (`sn-thermophile-culture`): Heat-tolerant organisms cultivated in mineral-rich volcanic conditions.
- **Heavy-metal concentrate** (`sn-heavy-metal-cake`): A concentrated mixture of metals separated from contaminated scrap and processing residues.
- **Holmium biocatalyst** (`sn-holmium-catalyst`): A stabilized holmium catalyst that supports resilient biological and electrochemical systems.
- **Symbiotic culture** (`sn-symbiotic-culture`): A balanced consortium of Gleban organisms used to establish diverse habitats.
- **Biodiversity matrix** (`sn-biodiversity-matrix`): An organized community of thermophiles, symbionts and mineral catalysts for habitat restoration.
- **Gaia coordination cell** (`sn-gaia-cell`): A biological coordination cartridge consumed by planetary beacons to maintain a synchronized ecosystem network.
- **Ecology science pack** (`sn-ecology-science-pack`): A research package containing ecological samples, preserved media and analytical electronics.
- **Climate science pack** (`sn-climate-science-pack`): A research package combining climate measurements with specialized planetary cultures.
- **Restoration science pack** (`sn-restoration-science-pack`): A research package produced from the operating data of a coordinated living-world network.
- **Mineral-composite stock** (`sn-alloy-stock`): An iron-reinforced mineral composite used for structural frames, storage casings and firearm stocks.
- **Purified water** (`sn-clean-water`): High-purity water for sensitive biological cultures, thermal circuits and chemical processing.
- **Oxygen** (`sn-oxygen`): Concentrated oxygen for clean metallurgy, nutrient preparation and oxidation reactions.
- **Hydrogen** (`sn-hydrogen`): A light reducing gas used in metallurgy and synthetic fuel production.
- **Mineral electrolyte** (`sn-electrolyte`): An aqueous mineral electrolyte for selective metal recovery and electrochemical reactions.
- **Bioleachate** (`sn-bioleachate`): A biologically active solution that releases useful metals from mineral feedstocks.
- **Toxic effluent** (`sn-toxic-effluent`): Contaminated process liquid containing captured pollutants and dissolved industrial residues.
- **Producer gas** (`sn-producer-gas`): Coal-derived combustible gas. Its production loses part of the coal's energy and consumes water; used by producer-gas alternators.
- **Refined biogas** (`sn-biogas`): Combustible gas from cultivated biomass and compost. Used in biological turbines and solid-oxide cellbanks.
- **Catalytic synthesis gas** (`sn-synthetic-gas`): A processed chemical fuel gas made from solid fuel, oxygen and water. Its declared energy is below that of its fuel feedstock.
