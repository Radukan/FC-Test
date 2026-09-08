# Nightglass / 0.7.0

A larger content increment after the focused 0.6.x releases: an HD goth explorer, three solar-only locomotive tiers and six power options. The restoration economy, existing factory footprints, field drones, military systems and recorded audio remain.

## The explorer

The adult explorer has pale skin, a layered black/violet wolf cut, dark makeup, original botanical/circuit tattoos on exposed arms/thighs, a short pleated skirt over opaque undershorts, black gloves and rounded boots. Armor tiers keep their own protective equipment. Existing hip/shoulder/head motion, native aiming rows and the right-hand-leading mining grip are retained.

Art is **rendered at 160 pixels per authored unit instead of 80**, with sprite scale reduced from 0.5 to 0.25. Thus texture detail doubles on each axis without doubling the character's world size. Fixed per-pose crops remove transparent padding and compensate both native shift axes. Large sheets use native `stripes`; every input page remains at or below 8192 pixels. This is a fresh render, not an enlargement of the previous PNGs.

`tools/goth_details.py` authors the outfit, hair and tattoos. `character_export.py` performs the HD render/crop/page export. `atlas_io.py` lets previews/tests read pages without assembling a giant image. `docs/art/character-render.json` records views, crops and fingerprints.

## Solar-only railway

| Locomotive | Stage | Roof PV | Battery | Day ceiling | Night ceiling | Motor |
|---|---|---:|---:|---:|---:|---:|
| Sunseed solar shunter | Early rail / red + green | 240 kW | 24 MJ | 90.7 km/h | 47.5 km/h | 180 kW |
| Heliograph solar locomotive | Mid / blue + ecology | 420 kW | 45 MJ | 146.9 km/h | 90.7 km/h | 300 kW |
| Daybreak solar express | Late / production + utility | 600 kW | 72 MJ | 194.4 km/h | 129.6 km/h | 450 kW |

The base conventional locomotive is 259.2 km/h before fuel bonuses, so all three solar tiers are slower. The tiers have original chassis, cockpit, roof-panel, wheel and shadow sprites. They retain normal rail connections, schedules, train stops, wagons and train control.

### Where the energy comes from

Each crafted locomotive pays for its fitted panels and battery. Its locked, dedicated equipment grid contains only its own **native solar-panel equipment and native battery equipment**. The battery starts empty. The native game charges it according to daylight and the surface's solar multiplier, including while parked. No recipe refuels the motor; no electric pole, factory network, generator equipment or ordinary fuel slot can charge it.

Native locomotive traction expects a burner. The adapter does **not** create a free fuel item: it withdraws a small, bounded quantity of stored battery joules and exposes exactly that quantity in an inaccessible internal burner reserve. Unspent motor credit is reconciled back to the same battery before the next allocation. The native engine's consumption is accounted for. Foreign fuel and unsupported grid contents cannot be credited as solar energy.

Reserved credit is persisted across save/reload and flushed before ordinary/field-drone mining so the equipment grid can travel with its item. Reconfiguration does not refill existing batteries. Hidden fitted components are not ordinary craftable/free inventory items.

### Night behavior and operational limits

As darkness increases, available traction power and the speed ceiling fall toward the night limits. The controller only **decreases** excessive train speed; it never accelerates a train by script, changes manual mode, or rewrites schedules. The lowest solar cap applies to a consist containing solar locomotives. An ordinary engine may physically tow a solar locomotive, but does not charge or fuel that solar unit.

An empty battery provides **no traction**. Trains can coast under native physics; no hidden reserve keeps them powered. Park or schedule daytime dwell time to recharge. Quoted PV values are peak ratings, not guaranteed continuous output; darkness, surface solar multipliers, load, stops and native traction consumption affect runtime.

Open a solar locomotive's normal GUI to see the onboard battery monitor, current mode and speed ceiling. Its grid is factory-fitted and locked against normal equipment replacement. No non-solar generator is accepted.

## Six power choices

| Source | Stage | Behavior | Rated output | Direct pollution |
|---|---|---|---:|---:|
| Copperleaf solar rack | Early red | Passive daylight photovoltaic | 18 kW | 0 |
| Trailblazer burner set | Early red | Active chemical-fuel generator | 180 kW | 12/min at full activity |
| Helical wind turbine | Red + green | Passive variable atmospheric wind | Up to 120 kW | 0 |
| Closed-loop biomass engine | Mid / ecology | Active, dedicated biopellet fuel | 500 kW | 0 |
| Deep-loop geothermal plant | Mid-late / production | Passive planet-dependent geothermal | Up to 1.5 MW | 0 |
| Residue-fired cogenerator | Mid-late heavy industry | Active chemical-fuel generator | 3 MW | 35/min at full activity |

Photovoltaics and fuel generators use native energy/fuel mechanics. Wind and geothermal sources are output-only native electric-energy interfaces with bounded, scripted production; their GUI cannot be used to edit free power values. Neither draws energy from the factory grid.

Wind follows native surface wind, local atmospheric pressure and a slowly varying deterministic weather envelope shared by nearby turbines. It does not work in a vacuum. Geothermal output is modeled by planet: Nauvis 80%, Gleba 65%, Fulgora 55%, Vulcanus 100%, Aquilo 30% of the rating; unsupported custom worlds and platforms produce none. These are game balance models, not a claim of real geological simulation.

Biopellets combine six biomass and one biochar into an 8 MJ fuel charge, below their combined feedstock fuel value. The engine's exhaust treatment emits no direct pollution. Burning produces mineral ash in the native residue inventory; a blocked ash output eventually stops the generator. Ash recovery returns mineral nutrients but does not create an infinite fuel cycle. Dirty sources consume real chemical fuel and emit real pollution; no ecological fitness is granted just for generating power.

## Validation and remaining checks

Source tests cover research/recipe references, source-only panel grids, no fuel slots, battery-credit conservation, foreign-energy rejection, dark-speed limits, generation bounds, art fingerprints, doubled texel density, compensated pivots and texture-page limits.

The official engine companion exercises actual native solar charging, fuel rejection, rail schedules/traction, day/night limits, depleted batteries, native generator output into accumulator loads, fuel use, emissions and biomass ash, alongside the prior campaign and field-planner probes. The code and results are recorded in `VERIFICATION.md`.

Source artwork is not game footage. A graphical client is still needed for subjective appearance, all elevation/Mech transitions, UI interaction, GPU/UPS profiling and long multiplayer campaigns. In particular, flat rolling-stock art is the fallback on slopes; no graphical elevated-rail inspection is claimed.
