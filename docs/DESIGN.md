# Design: a factory that grows a home

## The promise

The satisfaction of **watching an inhospitable world recover**, expressed through Factorio's belts, pipes, power grids, research and interplanetary logistics. The player is a restoration engineer, not a gardener clicking individual plants and not an accountant servicing twenty nearly identical meters.

The campaign overhauls **why you build, what your factory consumes, and what success means**. It deliberately retains Factorio's excellent transport, space platforms, military progression and local planetary hazards rather than replacing everything merely to justify the word “overhaul.”

This is the implemented v0.1.0 design, not a wishlist. Engine validation and full-playthrough balance are still pending.

## Five design rules

1. **Production, not proximity.** Installed machinery, stored cartridges and electric power alone do not award points. A real, completed craft must consume inputs and make physical outputs.
2. **One cause per layer.** Fitness is the planet's ability to support the target ecosystem; toxicity is contamination; resistance is native response to ecological change. Ordinary pollution still belongs to Factorio. Its pollution layer is enabled on Vulcanus, Fulgora and Aquilo; Gleba retains spores. No new native enemy ecology is invented on those non-biter worlds.
3. **Close loops, not inventories.** Reclamation creates a valuable factory problem. Spent filters, thermal buffers and captured effluent have engineered return routes, and surplus scientific samples have recycling sinks.
4. **Specialize worlds; do not homogenize them.** Vulcanus is a thermal/mineral challenge, Fulgora a toxic legacy, Gleba an unstable biological community, and Aquilo a cold logistics frontier. No deleting their hazards to make all five planets Nauvis.
5. **Complexity must change a decision.** Three new sciences, five fitness axes, one toxic-debt measure, one resistance measure. No redundant varieties of oxygen, universal seed that must never be lost, obligatory hand watering or dozens of nearly identical machines.

## What the ecological index means

A Factorio surface can be effectively infinite. The model therefore describes the **managed planetary restoration network**, not a simulation of every ungenerated chunk, every ocean molecule or an atmosphere's literal pascal value. Visual recovery occurs near active installations. Unvisited terrain remains native.

- **Atmosphere:** suitable composition and atmospheric conditions, combined into one fitness measure.
- **Thermal balance:** climate suitability. Improving either Vulcanus or Aquilo raises this value.
- **Water cycle:** the ability to retain and circulate viable water, not a command to flood land.
- **Living soil:** usable mineral/organic structure and microbial support.
- **Biodiversity:** a stable engineered community, not a count of native trees or total biomass.
- **Toxicity:** legacy/industrial contamination. Capturing pollution is not the same as destroying its waste.
- **Resistance:** organisms defending an ecological niche that restoration is displacing.

A lush Gleba can consequently have low **target ecosystem fitness** without the mod claiming the native planet is lifeless. The indigenous spore network is productive but not the stable community the project is engineering.

Native broods do not literally hate the color green. Pioneer ecosystems change the chemistry and symbiotic networks on which they depend. They attack the installations responsible. Eventually, a mature, maintained ecosystem stops changing so rapidly and resistance subsides.

## Progression in five acts

### I · Pioneer biology — red and green science

**Question:** How can a factory grow its own feedstocks?

Stone is hand-crushed into silica and smelted into glass, integrating the overhaul from the first science pack without hijacking stone-brick smelting. Pioneer bioreactors use minerals and water to create cultures and algae. Composters turn algae into compost, biofilm and biochar.

Cultures are shelf-stable and can be recreated from minerals. The first colony never depends on a finite starter item, a tree-rich seed, captured eggs or material from another planet.

Green science consumes compost. Field ecology unlocks the first soil station and the ecological samples that finance the new research branch. From this point, terraforming and research support one another.

### II · The living factory — green, blue and ecology science

**Question:** Is a cleaner factory actually a closed-loop factory?

Scrubbers create spent filters. Purification feeds watersheds and forests but produces captured contamination. Climate control consumes charged buffers. Closed-loop technology provides the return paths: reclaimed carbon/glass, treated water, vitrified sludge and powered buffer recharging.

Two competing approaches are available:

| Clean route | Dirty route |
|---|---|
| Biologically produced carbon | Cheap coal activation |
| Compost-rich engineered substrate | Chemically forced, high-yield substrate |
| Steady atmospheric scrubbing | Rapid atmospheric forcing |
| More machines, electricity and biological logistics | More coal, pollution, sludge and future detoxification |

The dirty route is useful for startup, constrained power/manufacturing infrastructure or a deliberate burst of atmospheric recovery. It is not a disguised victory path: forcing undermines other fitness axes, and toxicity blocks high biodiversity.

Post-fossil chemistry then replaces petroleum inputs in plastic/fuel and fossil smelting with biological refining and oxygen-assisted steel. These still consume ores, power and treatment capacity. Nuclear, solar, efficiency modules and eventually fusion retain their vanilla roles.

### III · An ecological archipelago — the first three destinations

**Question:** What can each planet contribute that another cannot?

- **Vulcanus:** weather basalt with calcite, tungsten and water. Develop heat-tolerant cultures once basic conditioning is achieved. Export thermophiles.
- **Fulgora:** mine useful catalysts from scrap remediation. Export holmium biocatalysts while retaining the challenge of islands, lightning and oil seas.
- **Gleba:** cultivate symbionts from spore treatment or an egg/nutrient fermentation route. Export symbiotic cultures. Efficient sheltered crops require a recovered ecosystem and still use real seeds and perishable nutrients.

These local products are restricted by native planet identity surface conditions. Importing raw ingredients to a convenient Nauvis assembler cannot bypass the specialization. Any **recovering** world can become the assembly center for biodiversity matrices, connecting the three supply lines.

### IV · Habitats beyond habitability — climate science and Aquilo

**Question:** Can the ecosystem survive its supply chain?

Biodiversity sanctuaries combine all three biological specialties. Comparative climatology consumes climate samples and those same specialties, preventing a detached science factory from ignoring actual restoration.

Aquilo's cryogenic gardens need imported matrices, ice, ammonia, recyclable thermal buffers, electricity and heating. They visibly form sheltered gardens over the machines, not land that erases the native heating and ice-support mechanics.

**A successful ecosystem is a reason to maintain shipping, not to abandon it.**

### V · Second Nature — a sustained network

**Question:** Can the project keep functioning after the construction celebration?

Gaia beacons consume coordination cells built from biodiversity matrices, superconductors, carbon fiber and lithium. On living worlds, they produce restoration science for the final technology.

Then all five worlds must simultaneously be self-sustaining and retain recent beacon production for ten uninterrupted minutes. This is a modest stress test of the real economy: power, heat, waste disposal, local maintenance, platform throughput and defense.

The win is not a hidden inventory quota, a mandatory extermination count or a ship crossing an arbitrary boundary. Afterward, repeatable laboratory productivity gives the network continued use.

## The player-facing contract

- Every support ceiling, stage threshold and next-stage requirement is visible.
- Every operation exposes per-cycle effects in recipe descriptions.
- The field guide is available from the start, not behind research.
- Circuit signals make automation possible without scripting.
- Raids warn before dispatch, require real nests, and respect peaceful mode.
- Removing the source nest during the warning cancels the attack.
- A cleared perimeter works. No secret spawns inside player infrastructure.
- No arbitrary biters on Fulgora or Aquilo. Demolishers remain their own native system.
- Terraforming does not delete resources, roads, ghosts, crops, water or support tiles.
- A planted forest is sparse and grows outside a safety margin around infrastructure.
- No full-map entity scan on a normal update tick.

## Deliberately outside v0.1.0

These are **not claimed features**: global conversion of every chunk, actual atmospheric fluid simulation, physical engine temperature/pressure changes, a new planetary map generator, custom enemy AI pathfinding, replacement animations for every machine, new music/voice acting, third-party planet integration, support for other total conversions, or a completed multiplayer/full-campaign certification.

The included systems form one coherent campaign implementation. Expand its scope only after verifying and balancing that campaign in the real game.
