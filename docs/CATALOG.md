# Complete content catalog

Generated from `second-nature/shared/catalog.lua` by `python tools/generate_docs.py`. Do not hand-edit tables.

**22 machines · 88 recipes · 20 technologies · 31 material/science items · 6 fluids.**

Times are seconds at crafting speed 1. Fitness effects are percentage points per completed cycle before planetary multipliers and support ceilings. No custom recipe supports productivity. Native recipe quality is disabled for operations and closed/catalytic loops.

## Machines

Footprints: chemical-plant / assembling-machine-2 / biochamber derivatives are 3×3; cryogenic-plant derivatives are 5×5; the circuit monitor is 1×1. All crafting machines are electric and require heat on Aquilo.

| Machine | Power | Recipe role | Unlock |
|---|---:|---|---|
| Pioneer bioreactor | 180kW | bioculture | Pioneer biology |
| Aerobic composter | 120kW | composting | The living substrate |
| Hydroponics bay | 650kW | hydroponics | Pioneer forests |
| Electrochemical works | 1.8MW | electrochemistry | Climate control |
| Closed-loop reclamation plant | 800kW | reclamation | The water cycle |
| Electric materials kiln | 900kW | kiln | Nothing left behind |
| Dirty pyrolysis retort | 350kW | pyrolysis | Industrial forcing |
| Atmospheric scrubber | 450kW | Fixed: Restore atmospheric balance | Atmospheric engineering |
| Soil restoration station | 300kW | Fixed: Restore living soil | Field ecology |
| Pioneer seed disperser | 500kW | Fixed: Seed pioneer ecosystems | Pioneer forests |
| Watershed restoration plant | 750kW | Fixed: Restore the water cycle | The water cycle |
| Climate heat exchanger | 4MW | Fixed: Normalize thermal balance | Climate control |
| Mineral detoxification plant | 1.5MW | Fixed: Bind planetary toxins | Nothing left behind |
| Pheromone dampener | 400kW | Fixed: Mask ecological disturbance | Atmospheric engineering |
| Atmospheric forcing stack | 600kW | Fixed: Force the atmosphere [dirty] | Industrial forcing |
| Basalt weathering station | 2.5MW | Fixed: Weather Vulcanus basalt | Weather the furnace |
| Fulgoran remediation works | 2MW | Fixed: Recover Fulgoran legacy waste | Life after the scrapyard |
| Symbiotic spore tower | 1.2MW | Fixed: Rebalance Gleban spores | Beyond the monoculture |
| Cryogenic garden | 3.5MW | Fixed: Cultivate sheltered thaw zones | A garden beneath the ice |
| Biodiversity sanctuary | 2.2MW | Fixed: Establish a biodiversity sanctuary | Many worlds, one biosphere |
| Gaia planetary beacon | 5MW | Fixed: Coordinate the living-world network | The Gaia network |
| Ecology circuit monitor | Passive sensor | Circuit telemetry | Field ecology |

## Restoration operations

| Operation | Time | Inputs → Outputs | Ecological effect / cycle | Conditions |
|---|---:|---|---|---|
| Restore atmospheric balance | 10 s | 1 Carbon filter cartridge + 25 Water [fluid] → 1 Spent filter cartridge + 1 Climate samples | atmosphere +0.14; toxicity -0.045; pollution -40 | Any stock planet |
| Restore living soil | 15 s | 3 Soil substrate + 1 Pioneer culture + 20 Water [fluid] → 2 Ecological samples | soil +0.18; biodiversity +0.045; toxicity -0.06; pollution -8 | Any stock planet |
| Seed pioneer ecosystems | 15 s | 1 Pioneer seed mix + 1 Soil substrate + 20 Purified water [fluid] → 2 Ecological samples | atmosphere +0.025; water +0.015; biodiversity +0.18; pollution -12 | Any stock planet |
| Restore the water cycle | 12 s | 100 Purified water [fluid] + 1 Ceramic membrane → 2 Climate samples + 10 Toxic effluent [fluid] | water +0.2; soil +0.035; toxicity -0.025; pollution -10 | Any stock planet |
| Normalize thermal balance | 20 s | 1 Charged thermal buffer + 100 Water [fluid] → 1 Depleted thermal buffer + 2 Climate samples | atmosphere +0.025; temperature +0.24 | Any stock planet |
| Bind planetary toxins | 15 s | 2 Neutralization charge + 50 Water [fluid] → 2 Hazardous sludge + 1 Climate samples | atmosphere +0.05; soil +0.025; toxicity -0.38; pollution -30 | Any stock planet |
| Mask ecological disturbance | 12 s | 2 Engineered biofilm + 1 Activated carbon + 20 Water [fluid] → 1 Ecological samples | pressure -0.85 | Any stock planet |
| Force the atmosphere [dirty] | 6 s | 8 Coal + 1 Mineral nutrients + 20 Water [fluid] → 1 Climate samples + 1 Hazardous sludge | atmosphere +0.36; temperature -0.06; water -0.03; toxicity +0.48; pollution +45 | Any stock planet |
| Weather Vulcanus basalt | 15 s | 10 Calcite + 2 Tungsten ore + 50 Water [fluid] → 4 Mineral nutrients + 2 Climate samples | atmosphere +0.06; temperature +0.4; soil +0.24; toxicity -0.12 | Vulcanus |
| Recover Fulgoran legacy waste | 12 s | 10 Scrap + 30 Mineral electrolyte [fluid] → 2 Heavy-metal concentrate + 2 Climate samples | atmosphere +0.16; water +0.1; soil +0.24; toxicity -0.5 | Fulgora |
| Rebalance Gleban spores | 12 s | 5 Nutrients + 1 Carbon filter cartridge + 50 Water [fluid] → 1 Spent filter cartridge + 1 Symbiotic culture | atmosphere +0.1; soil +0.12; biodiversity +0.25; toxicity -0.15; pollution -45 | Gleba |
| Cultivate sheltered thaw zones | 15 s | 1 Charged thermal buffer + 10 Ice + 30 Ammonia [fluid] → 80 Water [fluid] + 1 Depleted thermal buffer + 2 Biosphere samples | temperature +0.5; water +0.32; biodiversity +0.05; toxicity -0.035 | Aquilo |
| Establish a biodiversity sanctuary | 20 s | 1 Biodiversity matrix + 5 Mineral nutrients + 100 Purified water [fluid] → 2 Biosphere samples | water +0.04; soil +0.08; biodiversity +0.42; toxicity -0.07; pollution -20 | Any stock planet, stage ≥ 2 |
| Coordinate the living-world network | 60 s | 1 Gaia coordination cell + 50 Purified water [fluid] → 2 Restoration science pack | atmosphere +0.05; temperature +0.05; water +0.05; soil +0.05; biodiversity +0.05; toxicity -0.025 | Any stock planet, stage ≥ 4 |

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
| Prepare pioneer seed mix | 3 s | 1 Pioneer culture + 2 Wood + 2 Living compost | 2 Pioneer seed mix | Pioneer forests |
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

## Materials and fluids

- **Silica** (`sn-silica`): Crushed stone for glass. A separate feedstock keeps automatic furnaces from choosing between glass and stone bricks.
- **Laboratory glass** (`sn-glass`): Vessels, membranes and the first automation science packs.
- **Mineral nutrients** (`sn-mineral-nutrients`): Stable mineral feed for pioneer cultures. Not the perishable Gleban nutrient fuel.
- **Pioneer culture** (`sn-microbial-culture`): A sealed, shelf-stable inoculum. Can be synthesized from minerals without wood, eggs or a starter seed.
- **Algal biomass** (`sn-algal-biomass`): Renewable organic feedstock. Its embodied energy comes from an electrically powered bioreactor.
- **Living compost** (`sn-compost`): The foundation of soil restoration and logistic science.
- **Biochar** (`sn-biochar`): Stable carbon from biomass. Useful as sorbent, soil amendment or fuel.
- **Activated carbon** (`sn-activated-carbon`): High-surface-area sorbent. Renewable activation is slow; coal activation is fast and dirty.
- **Carbon filter cartridge** (`sn-filter-cartridge`): Used by scrubbers and water filtration. Route spent cartridges back to reclamation.
- **Spent filter cartridge** (`sn-spent-filter`): Not disposable: reclaim the carbon and glass, then treat the captured effluent.
- **Soil substrate** (`sn-soil-substrate`): Compost, mineral grains and biochar engineered into a stable rooting medium.
- **Pioneer seed mix** (`sn-seed-mix`): A robust starter community for reclaimed ground.
- **Ceramic membrane** (`sn-ceramic-membrane`): A mineral water-cycle component, made without oil chemistry.
- **Charged thermal buffer** (`sn-thermal-buffer`): A recyclable heat-transfer cartridge. Thermal fitness is climate suitability, not the game's temperature property.
- **Depleted thermal buffer** (`sn-depleted-thermal-buffer`): Recharge with clean water, biofilm and electricity. Never recycle for free fresh buffers.
- **Neutralization charge** (`sn-neutralization-charge`): A mineral/carbon charge that binds toxic material into sludge.
- **Hazardous sludge** (`sn-hazardous-sludge`): Toxic debt made tangible. Vitrify it; stockpiling does not count as detoxification twice.
- **Vitrified aggregate** (`sn-vitrified-waste`): Bound, inert industrial waste suitable for concrete.
- **Engineered biofilm** (`sn-biofilm`): A renewable membrane and pheromone carrier, recovered from composting.
- **Ecological samples** (`sn-ecological-data`): Physical field samples from completed restoration cycles. Research them or reclaim their contents.
- **Climate samples** (`sn-climate-data`): Instrument samples from atmospheric, thermal and watershed operations.
- **Biosphere samples** (`sn-biosphere-data`): Complex habitat samples for biodiversity matrices and advanced research.
- **Thermophile culture** (`sn-thermophile-culture`): Vulcanus-exclusive organisms that stabilize mineral and thermal cycles.
- **Heavy-metal concentrate** (`sn-heavy-metal-cake`): Recovered Fulgoran contamination. Refine it into useful metals and catalysts.
- **Holmium biocatalyst** (`sn-holmium-catalyst`): A Fulgoran catalyst for resilient, interplanetary ecosystems.
- **Symbiotic culture** (`sn-symbiotic-culture`): Gleban life rebalanced toward diversity rather than invasive monoculture.
- **Biodiversity matrix** (`sn-biodiversity-matrix`): Thermophiles, holmium catalysts and Gleban symbionts woven into one ecological community.
- **Gaia coordination cell** (`sn-gaia-cell`): An interplanetary maintenance consumable. Beacons need regular shipments, not just a one-time build.
- **Ecology science pack** (`sn-ecology-science-pack`): Field-driven research into sustainable industrial systems.
- **Climate science pack** (`sn-climate-science-pack`): Cross-planet climate research using the specialties of Vulcanus, Fulgora and Gleba.
- **Restoration science pack** (`sn-restoration-science-pack`): Produced only by operating planetary beacons on living worlds.
- **Purified water** (`sn-clean-water`): A high-purity process fluid; not a replacement for native water or ocean tiles.
- **Oxygen** (`sn-oxygen`): Electrolysis coproduct used for clean metallurgy and nutrient processing.
- **Hydrogen** (`sn-hydrogen`): Power-intensive reducing agent and feedstock for renewable chemical fuels.
- **Mineral electrolyte** (`sn-electrolyte`): An aqueous mineral solution for Fulgoran reclamation.
- **Bioleachate** (`sn-bioleachate`): A biological alternative to fossil-fuel smelting. Captured metal-bearing effluent still needs treatment.
- **Toxic effluent** (`sn-toxic-effluent`): Captured pollution is not gone until neutralized. Treat it into water and hazardous sludge.
