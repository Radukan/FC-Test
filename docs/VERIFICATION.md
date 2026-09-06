# Verification ledger · Ironbound 0.3.0 alpha · 2026-09-07

## Completed evidence

**Stable engine/source run:** [34065931167](https://github.com/Radukan/FC-Test/actions/runs/34065931167), code commit **`f7827159b627eebe2b7a4394786c2facba53b1a0`**. The offline validator and actual official **Factorio 2.0.77** headless job passed. Release publishing reruns validation on the exact tagged commit and re-downloads its uploaded assets for SHA-256/byte comparison.

The engine-evidenced code passed 144 cases; final atlas-boundary and visible-motion regressions raise the complete suite to 146. The local complete suite reports **146 passing tests** with the pinned stable Wube data checkout present. The graphics source contact sheet and individual rendered lander/building/explorer images were visually inspected. The source animation preview demonstrates exported frames, not a game recording.

| Check | Result | What it establishes |
|---|---|---|
| All production Lua parses as 5.2 | **Pass** | Syntax / module loading |
| Full offline suite | **146 passed** | Existing regression contracts plus wood-free recipes, pacing, research, habitat readiness and owned-tree recovery |
| Official stable source data stages | **Pass** | Prototype references, research graph, recipe unlocks, item/ammo categories, art paths and startup toggles |
| Actual C++ prototype loading | **Pass** | New building/defense/player/armor/corpse animation structures accepted by 2.0.77 headless |
| Real new save + reload + 2,100 ticks | **Pass** | No fatal runtime failure in the exercised setup |
| Powered/idle/unpowered crafting | **Pass** | Real completion counters and physical pollution changes; idle/unpowered peers earn none |
| Lander/cargo/defense probes | **Pass** | Actual placement, shared/idempotent cargo, permanent protection after the rocket handler, four loaded sentries and real ammo insertion |
| Wood-free recipe probes | **Pass** | Poles, crates, shotguns and pioneer seed mix have no wood ingredient; pole recipe is enabled |
| Combat/character prototypes | **Pass** | New turret tiers accept expected ammunition; actual character entity accepts new guns/medical items |
| Native policy/commandables | **Pass** | Conversion, eradication, friendly-force relationships and real attack/retreat API commands |
| Slow habitat model | **Pass** | No instant growth after a long timestamp gap, hours-scale gain/loss, bounded optimization, visual toggle separation and final habitat gate |
| Terrain/tree safety | **Pass in doubles** | Protected tiles/resources, tracked-only withering and regrowth, no ungenerated terrain access |
| Art integrity | **Pass** | Original sprite paths and required direction/frame counts; rendered source sheets reviewed |
| Packaging | **Pass locally** | Stable-only reproducible ZIP/metadata/CRC/SHA-256 tests; release performs hosted download verification |

## Engine issues caught and corrected in this update

1. A pole’s picture direction count must equal its wire-position count. The riveted pole now uses a four-direction atlas matching its four connection-point entries.
2. New turrets still require a `graphics_set` container even when the full original rotated frames include the entire base. It is present and empty rather than absent; no old visible base sprite is inherited.
3. Data-stage localized research-effect parameters require strings. Bounded optimization percentages are converted to string parameters rather than passed as numbers.

The earlier GUI reserved-name fix, crafting-only monitor guard, explicit runtime utility import, parse-time dependency resolution and generated-chunk filtering regressions remain in the suite.

## Scope of the real-engine harness

The actual production mod runs its ordinary lifecycle, registry, crafting, pollution, telemetry and animation-render callbacks. A test-only companion also loads unmodified runtime module copies into **isolated test storage**, then deliberately arranges ecology/clocks to exercise long-latency features against actual engine entities and surfaces. No production debug/mutation interface is added.

Both `SECOND_NATURE_ENGINE_CAMPAIGN_PROBES_OK` and `SECOND_NATURE_ENGINE_SMOKE_OK`, plus successful process exit codes, are required. Merely loading prototypes is not enough.

The rocket handler is called with a shared-entity-API fixture; this does **not** prove an actual passenger rocket launch. The character created by the companion is an engine entity, not an interactive player controlling the GUI. Native commands are issued and accepted; this is not exhaustive combat/pathfinding balance testing.

## Still unverified / alpha limitations

- **Graphical client review:** actual building port/wire alignment, sprites at all zoom/UI scales, every animation/firing direction, armed character movement/aiming, armor/Mech flight transitions, corpses, menu composition and the arrival camera.
- **Full no-cheat campaign:** bootstrap pacing, steady byproduct flow, all specialty research/material imports, the complete habitat timeline and five-world victory.
- **Every combat situation:** all enemy tiers, resistances, moving targets, firing-lane/friendly-fire behavior, energy drain under sustained fire and equipment-grid balance.
- **Every production configuration:** all qualities/modules, heat starvation, output/fluid blockage and recipe-switch combinations in the real engine.
- **Existing-save migration/removal:** real 0.2-to-0.3 migration across all controller, raid, tree, hull and network states. Non-duplication/protection contracts are tested in doubles; that is not a full save-migration certification.
- **Multiplayer/desync:** two-client testing, customized permissions, force merges and simultaneous native decisions.
- **Large-map/factory performance:** realistic UPS, GPU sprite memory and long rolling-survey latency. Chunk work is bounded, but no large-factory performance claim is made.

The 18 armed locomotion variants satisfy the stable engine structure; their precise visual aim/movement mapping must be reviewed in a client. A headless pass cannot certify that appearance. Character art can be disabled without replacing player inventories/controllers.

## Focused playtest checklist

1. Fresh Last Landing: confirm intact permanent ship, supplies, four loaded sentries and no wood/fish dependency. Make additional poles/crates/ammo by hand without console items.
2. Check all four dashboard tabs, six guide topics, updated habitat/optimization readings and confirmation cancellation on close. Verify leaf/Shift+T and Ctrl+Shift+P.
3. Inspect the original industrial sprites in each orientation while idle/working. Check turret idle/prepare/fire/rotation, wall connections and actual wire/pipe endpoints.
4. Walk, run, mine and fire in all directions with light/modular/power/Mech armor; test death/recovery and the optional vanilla-character setting.
5. Sustain a clean supported area, observe patch → grass → meadow → forest progression. Pollute it for a sustained period; verify gradual browning/withering, then recovery after cleaning. Player trees/infrastructure must survive.
6. Research/reverse each optimization level; no total bonus above 45%, no free outputs and no shortened victory/raid timers. Check the per-force cache after merging forces.
7. Test all three defense eras, low ammo, low power, blocked firing lanes and hostile groups. The protected lander is not a shield for every other entity.
8. Verify the new Nauvis habitat gate, two-minute native hold, both irreversible outcomes, moving/future natives, and untouched other planets.
9. Save/reload mid-growth, mid-withering, mid-warning, during native conversion and at the final network hold; profile larger maps and multiple players.

Record actual game version, mod list, save and reproduction steps. Keep unrun checks labeled unrun; source/mocked validation is not a substitute for playing the full game.
