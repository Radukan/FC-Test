# Campaign design · stable 0.2

## Premise and boundaries

Second Nature is a Space Age ecological-industrial overhaul inspired by the feeling of earning a living planet in Planet Crafter. The factory remains the means of progress, not a cosmetic backdrop to a score that rises while idle.

**Last Landing:** the descent engine is spent. A stranded cargo lander and finite defenses support a mineral-biological bootstrap on Nauvis. Native trees and fish have disappeared; the broods remain. No platform, free rocket or orbital teleport is granted. Standard rocket progression is the route out.

The five-planet economy, three scientific disciplines and sustained logistics victory remain. This is not a replacement map for every planet or a removal of Space Age's hazards.

## The central choice: safety now or life later

Nauvis broods tolerate contamination. Pollution-driven vanilla biter recruitment is disabled with zero spawner uptake and an unreachable pollution recruitment cost; pollution evolution is disabled. Gleba's spores are untouched.

Successful clean-machine work raises ecological resistance. Nearby real nests organize warned, bounded strikes against productive restoration targets. Ordinary dirty factories are not selected. Pollution reduces effective resistance and group size; heavy contamination cancels warnings and recalls tracked raiders from their targets.

The compromise cannot win the campaign:

- Living-soil and biodiversity bonuses require local pollution ≤ 10.
- Positive capture/thermal/chemical work still runs; samples and waste still emerge.
- Mean generated-world pollution constrains biodiversity.
- Final readiness requires low global inventory and a completed clean hotspot survey.
- Dirty recipes create actual pollution, inventory waste and toxic debt.

Proximity combat, retaliation, obstruction and native territorial expansion remain. “Pollution calms broods” does not mean a pollution emitter has damage immunity.

## Campaign arc

1. **Recover the expedition.** Cargo, basic power, ammunition and finite wood. Stone becomes silica and glass; mineral nutrients start a culture/algae loop without natural seeds.
2. **Make a clearing fit for life.** Samples unlock treatment even before local living bonuses work. Supply scrubbers, close filter and effluent loops, and improve water/soil/thermal support. First gardens appear around successful installations.
3. **Defend ecological change.** The pollution blanket retreats. Pressure rises around cleaner infrastructure; perimeter defense, nest removal and supplied dampeners become useful investments.
4. **Connect planetary specialties.** Vulcanus thermophiles, Fulgoran biocatalysts and Gleban symbionts form biodiversity matrices. Aquilo needs heated, imported ecosystems.
5. **Resolve Nauvis.** Hold complete, clean readiness for two minutes. Choose permanent symbiosis or eradication in a confirmed dialog; multiplayer administrators decide for the shared planet.
6. **Sustain the living network.** Own-force, recent beacon cycles across five ready worlds for ten uninterrupted minutes. Winning does not end the factory.

## World state versus the rendered world

Five suitability axes plus toxicity/resistance describe the managed ecosystem. They are not the game's physical temperature or pressure: lava, lightning, spoilage and Aquilo heat/support stay relevant.

Physical changes are real but bounded:

- New campaign Nauvis chunks exclude trees/fish while retaining ore, rocks, native nests and worms.
- Fresh grass becomes barren dirt/sand; legacy pollution is seeded once per new chunk.
- Early recovery is sparse and local to productive machines, with pollution checks at both machine and destination tile.
- At stage 4+, generated Nauvis ground undergoes rolling succession in 128-tile strips. Smog and surviving broods prevent recovery; heavy smog browns grass.
- Native water/deepwater switch between normal and green-tinted variants without altering their collision/support class.
- Structures, ghosts, resources, paving, hidden support, crop soils, lava, oil seas and Aquilo ice are protected.

“Global” inventory is the engine's whole-surface total, including pollution-only chunks beyond generated terrain—not every coordinate of an infinite map. A total is exact at sampling time; hotspot coverage explicitly surveys fully generated terrain and also respects newly detected hotspots. Exploration extends the survey and can introduce additional legacy smog before native resolution.

## Native futures

### Symbiosis

Biters/spitters become original flowering Bloomback grazers. Nests and worms become bloom gardens. The separate non-expanding force is friendly to every force; it does not ally existing hostile forces with each other. Bloombacks deal no attack damage. Gardens remain as inhabited space rather than free factory floor.

### Eradication

Known Nauvis native species, including Second Nature's brood variants, are removed without replacement. Other planets and player-owned organisms are not swept.

The decision is irreversible through normal UI/settings. It does not make ecological scores immune to later neglect. Automatic outcomes are available as explicit global mod settings; the default requires an in-game choice.

A one-time, save-safe entity index prevents moving units from outrunning the chunk survey. Up to 32 indexed natives are handled per second. Bounded chunk sweeps plus native spawning/expansion events cover later populations. No periodic whole-map entity scan is used.

## Shared state and save safety

- Schema 2 preserves existing ecological values, research, production registries, contribution records and network progress.
- Desolation/landing require a genuinely new, tick-zero freeplay game and the startup setting. Installing/updating on an existing save does not sterilize its terrain or provide new cargo.
- Cargo is per force. Arrival records are per player; reconnects and configuration changes are idempotent. Force merges preserve the surviving camp and unlock redundant hulls rather than stranding unmineable wrecks.
- Ecology/pollution are shared by planet. Beacon logistics and victory are force-specific.
- Module dependencies resolve during `control.lua` parsing. No runtime `require` or `on_load` mutation is used.
- `storage` contains persistent state and supported Lua object references, never chunk iterators or callbacks. Remote reports exclude native work queues and return copied primitive snapshots.

## Presentation

The dashboard has four tabs: Planet, Air & natives, Living network and Field guide. Every named child uses `sn_`; reserved GUI member names are forbidden by the test contract. Opening failures are caught and logged so a presentation defect does not stop a running factory.

The original Last Landing illustration replaces menu simulations when enabled. Bloombacks use original procedural eight-direction/four-frame walking sprites. Ordinary machines and the lander reuse installed Factorio artwork; no Wube sprites are redistributed.

## Deliberate non-goals for this alpha

- No fake whole-infinite-map pollution percentage.
- No orbital starting base or automatic rocket launch.
- No instant world repaint, foundation deletion or universal hazard removal.
- No claim of a complete graphical, multiplayer or full-campaign playthrough.
- No new experimental 2.1 build or unverified compatibility with other total overhauls.
