# Scalable power roster / 0.8.0

There are **six distinct systems in each stage**, not six for the whole mod. Ratings describe real electrical output except the reactor's explicitly labeled thermal rating. Steam/plasma converters need their supplied energy; they do not create it.

## Early: red and green science

| System | Rating | Distinct requirement / tradeoff | Units for 10 MW nameplate |
|---|---:|---|---:|
| Copperleaf photovoltaic bank | 120 kW | Passive daylight only; substantially higher material cost than the old starter rack | 84 |
| Trailblazer burner alternator | 600 kW | Chemical fuel, 55% efficiency, 18 pollution/min at full activity | 17 |
| Helical wind turbine | Up to 400 kW | Passive wind and air pressure; nearby units share weather, including lulls | 25 at peak |
| River paddle station | 350 kW | Four natural water tiles within four tiles; landfill can stop it | 29 |
| Twin-cylinder steam engine | 1.8 MW | Real 165 C steam, water and boiler infrastructure | 6 |
| Producer-gas alternator | 1.2 MW | Coal gasification, water, chemistry, pipes and 20 pollution/min | 9 |

A modest early factory can use a few alternators or steam sets. Passive options require more space and/or suitable geography, but no longer deliver only a few kilowatts per machine. Nameplate solar/wind output is not continuous average output; account for night, lulls and storage.

## Mid: blue science and ecology

| System | Rating | Distinct requirement / tradeoff | Units for 100 MW nameplate |
|---|---:|---|---:|
| Closed-loop biomass engine | 3 MW | Prepared biological pellets, residue handling; no direct emissions | 34 |
| Deep-loop geothermal plant | Up to 8 MW | Planet-dependent regional thermal budget, substantial well capital | 13 at rated yield |
| Residue-fired cogenerator | 12 MW | Bulk chemical fuel, 72% efficiency, 80 pollution/min | 9 |
| Heliostat power tower | 1.8 MW | Passive daylight concentration; expensive panels/glass/thermal components | 56 |
| Anaerobic biogas turbine | 6 MW | Cultivated gas production, pipe throughput, 90% conversion efficiency | 17 |
| High-pressure recovery turbine | 18 MW | Real 500 C steam and sufficient heat/steam flow | 6 |

The turbine's footprint/output is comparable to several vanilla turbines bundled into one installation, and its fluid demand scales with output. The biomass systems need a substantial biological supply chain. A high rating does not bypass fuel or steam requirements.

## Late: production, utility and interplanetary materials

| System | Rating | Distinct requirement / tradeoff | Units for 1 GW nameplate |
|---|---:|---|---:|
| Photonic solar canopy | 12 MW | 200 conventional panels plus advanced material investment; daylight only | 84 at peak |
| Planetary thermal tap | Up to 30 MW | Deep regional heat and interplanetary drilling materials | 34 at rated yield |
| Catalytic combined-cycle plant | 60 MW | Synthetic gas from real fuel, oxygen and processing; 65 pollution/min | 17 |
| Solid-oxide biogas cellbank | 24 MW | Large biogas throughput and high-grade membranes; no direct emissions | 42 |
| Lead-cooled modular reactor | 80 MW thermal | Uranium fuel, spent cells, heat exchangers, water and turbines; no neighbour bonus | 13 thermal units |
| Magnetoplasma generator | 150 MW | Real fusion plasma and hot-coolant output; costs three conventional converters plus advanced materials | 7 converters |

The reactor converts fuel into heat, not direct electricity. It stops consuming at its heat limit and has no neighbour bonus, unlike adjacency-optimized vanilla nuclear layouts. The plasma converter is only part of a fusion system: fusion fuel, startup power, cold coolant and heat rejection remain necessary. Its higher density does not increase energy extracted per unit of plasma.

## Energy and world safeguards

- Existing 0.7 plant entity IDs and collision footprints remain unchanged, so occupied factories are not expanded in place. New recipes reflect the larger equipment/output investment.
- Generator effectivity never exceeds 100%. Producer gas contains 12 MJ from four coal (16 MJ), biogas contains 10 MJ from at least 12 MJ of biomass, and synthesis gas contains 80 MJ from eight solid fuel (96 MJ), before processing/engine losses.
- Native fuel, steam, fluid and plasma consumption govern active output. Wrong fluids are filtered; zero-energy fluid is not destroyed for power. Full residue/coolant output can stop a generator.
- Geothermal sources in one **32 x 32 region** share the strongest installed unit's output budget, weighted by installed ratings. A bore/tap cluster does not multiply passive power indefinitely.
- Geothermal yield factors are Nauvis 80%, Gleba 65%, Fulgora 55%, Vulcanus 100%, Aquilo 30%. Unsupported worlds/platforms generate none.
- Surviving 0.7 geothermal entities retain a 1.5 MW pre-planet-factor baseline even in crowded legacy regions, so the new sharing rule does not silently erase their old output. Mining/rebuilding uses the new region rules.
- Wind/shoreline/thermal interfaces have output-only connections and no editable free-power GUI. Solar trains remain unchanged and cannot charge from any of these factory sources.
- World-source and icon geometry is original. Fuel/steam generators have two symmetric native input seams; fusion keeps its standard 3 x 5 hookup and plasma/coolant connection categories.

These are explicit game-balance contracts, not claims about real-world engineering. Full campaign economy and long-run multiplayer/UPS/GPU behavior still need client playtesting; the native harness verifies the defined energy, fuel, fluid, heat and output behaviors.
