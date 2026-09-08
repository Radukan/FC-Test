# Milestones, the field guide and the soundscape

Second Nature 0.9.0 adds three things that a finished mod is expected to have and
0.8.0 did not: recorded progression milestones, in-game teaching entries, and a
working sound on every building that visibly runs.

Nothing in this release changes a recipe, a research cost, an output rating or an
ecological rate. It is presentation, feedback and completeness.

## Milestones

Nineteen medallions appear in the game's achievement window. They are **modded
achievements**: Factorio keeps a separate list for saves that load mods, so these
never touch vanilla or Steam progress, and loading Second Nature does not put a
vanilla achievement at risk that was not already disabled by loading any mod.

All nineteen are declared once in `second-nature/shared/achievements.lua`. The
prototypes, the runtime ledger, the dashboard tab, the localization and the tests
all read that single list.

### Tracked by the mod

Twelve milestones depend on the restoration model, which the engine knows nothing
about, so the mod evaluates them and calls `unlock_achievement`. Only the plain
`achievement` prototype type can be unlocked from a script; the tests enforce
that no script ever tries to unlock a condition type, which would silently fail.

| Medallion | Earned by |
|---|---|
| First breath | Reach stage 1 on any planet |
| Root systems | Reach stage 3 on any planet |
| A living world | Reach stage 5 with clean air and a matured landscape |
| New growth | 1,000 trees established by restoration on one world |
| Terraformer | 10,000 tiles reclaimed on one world |
| Deep green | 50,000 pollution or spores captured on one world |
| Signal restored | Launch the first rocket from the wreck camp |
| Common ground | Choose symbiosis on Nauvis |
| Quiet eden | Choose eradication on Nauvis |
| Hold the line | Survive an ecological-response wave with the target intact |
| Field stations | Record restoration work on all five worlds |
| Second nature | Complete the ten-minute five-world network hold |

### Evaluated by the game

Seven use native condition prototypes. The mod defines them and then stays out of
the way; the engine decides when they are met.

| Medallion | Condition type |
|---|---|
| First gust | Take power from a helical wind turbine |
| Network nodes | Build five planetary beacons |
| Coordination cells | Produce 200 Gaia coordination cells |
| Matrix gardener | Produce 100 biodiversity matrices |
| Read the world | Research with restoration science |
| No shortcuts | Finish without building a retort or forcing tower |
| Nightglass grid | 100 GJ in an hour with no emitting generator |

### Ownership rules

Awards belong to a **force**, not to whoever happened to be online.

- Planetary milestones are granted to every force with recorded restoration
  cycles on that world. A force that never worked a planet gets no credit for it.
- The record lives in `storage`, so a player who was offline when their force
  earned a medal receives it the moment they join.
- Merging forces keeps the **earlier** of two award times and never
  double-awards. The destination force's members are re-synced immediately.
- The same award is never recorded twice, so the chat notice fires exactly once.

A **Milestones** tab in the field station (SHIFT + T) lists all twelve tracked
medallions with their goals. Locked ones are drawn in grey; earned ones show how
long ago your force earned them.

## In-game field guide

Eleven entries were added to the native tips-and-tricks window, in a new
`Second Nature` category. No stock Factorio tip is replaced, reordered or hidden,
and a test asserts that no entry outside our own list carries our category.

Entries offer themselves when they become relevant: the briefing after a minute of
play, the first restoration cycle when Environmental monitoring finishes, the
closed-loop entry with Nothing left behind, the resistance entry with Planetary
ecology, and so on. Skip triggers suppress a tip whose lesson the player has
clearly already absorbed, such as having built six scrubbers already.

The topics are: the restoration briefing, starting from stone rather than wood,
your first restoration cycle, byproducts as real inventory, the hotspot survey
gate, the two kinds of native pressure, circuit telemetry, the eighteen power
systems, the solar railway, field crews without a robot network, and finishing
the network.

## Soundscape

In 0.8.0, sixteen of the eighteen generating plants had no `working_sound` at all.
A machine that visibly turns but makes no noise reads as a bug.

`second-nature/shared/audio_catalog.lua` declares named layers keyed by mechanism,
so two plants that work the same way sound the same way:

| Layer | Used by |
|---|---|
| Photovoltaic | Copperleaf bank, heliostat tower |
| Wind | Helical turbine |
| Hydro | River paddle station |
| Combustion | Burner alternator, biomass engine, producer-gas alternator |
| Heavy engine | Residue cogenerator |
| Steam | Twin-cylinder engine |
| Turbine | High-pressure recovery turbine, combined-cycle plant |
| Gas turbine | Anaerobic biogas turbine |
| Deep earth | Geothermal bore, planetary thermal tap |
| Electro | Photonic canopy, solid-oxide cellbank |
| Telemetry | Ecology circuit monitor |

Every referenced file is a **stock Factorio 2.0 asset** already shipped with base
or Space Age. Nothing is copied into this mod, and a test verifies that each path
is genuinely referenced by an upstream prototype in the pinned 2.0.77 data, so a
misspelled filename cannot ship.

Generating loops scale with real activity, so a becalmed wind turbine, a solar
bank at midnight and a starved gas turbine go quiet rather than droning at full
volume. The reactor and plasma converter keep the loops they already inherited.

Inventory handling audio was also missing on 95 of our items. Every carried item
now has move, pick and drop sounds matched to its material family: minerals rattle,
glass and cultures click like science, composites thud, barrels ring, armor and
weapons use their own stock handling sets.

## Verification

Twenty-three new source tests cover milestone declaration and uniqueness, the
script-versus-engine type split, reachability of every scripted milestone from
the runtime, prototype and icon existence, condition targets that resolve to real
prototypes, medallion art distinctness at list size, per-force isolation, offline
joins, force merges, the dashboard tab, tip categories not colliding with stock
entries, and the complete absence of silent plants and silent items.

Two native-engine markers were added, `SECOND_NATURE_ENGINE_MILESTONES_OK` and
`SECOND_NATURE_ENGINE_AUDIO_OK`, which run against a real `LuaForce` and real
loaded prototypes in the headless job.

Not claimed: how the achievement window looks on screen, notification timing in a
graphical client, mixing levels judged by ear on real speakers, or interaction
with third-party achievement mods.
