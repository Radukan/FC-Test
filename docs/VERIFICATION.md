# Verification ledger · 0.2.0 alpha · 2026-09-06

## Status: real stable-engine smoke checks passed; full playtesting remains open

The v0.1 dashboard crash was a real defect. Its permissive GUI double allowed reserved child names that Factorio rejects. Passing source/mocked tests was not sufficient evidence of game correctness. The new validator therefore makes **actual Factorio 2.0.77 execution a required release gate**.

### Recorded engine evidence

**Latest successful stable code-validation run:** [34061920694](https://github.com/Radukan/FC-Test/actions/runs/34061920694), source **`d86adabe6d95f32fbcc465c7364b02e0f3d6c470`**. Both `lua-and-data` and `engine` jobs completed successfully, including the official binary download, save creation and 2,100-tick reload/benchmark. Logs are attached as `stable-engine-logs` (repository access required).

That run covered the finalized Last Landing code and **130 passing offline cases**, including the new-hotspot and canceled-confirmation safeguards. This ledger was updated after observing that result. The release workflow independently revalidates its exact tagged commit before publishing, and refuses to upload if validation fails. The earlier successful core-engine run is [34020350605](https://github.com/Radukan/FC-Test/actions/runs/34020350605).

### Checks actually executed

| Check | Result | Scope / limits |
|---|---|---|
| Lua 5.2 compilation | **Pass** | Every production Lua file |
| Full local suite | **130 passed** | Stable pinned Wube data present; `.venv/bin/python -m pytest -q` |
| Pure ecological model | **Pass** | Caps, drift, dirty debt, stage/readiness gates and supplied-kit convergence; not a playthrough |
| Strict runtime doubles | **Pass** | GUI member-name rejection, event-time import rejection, crafting-only API guard, accounting, lifecycle, pollution, terrain, raids, native choice, persistence contracts and network logic |
| Official stable data stages | **Pass** | 2.0.77; overhaul on/off and startup switches restored to vanilla behavior |
| Content graph / art / locale | **Pass** | Recipe/research references, unlocks, safety, source paths, sprite dimensions/transparency, 491 unique locale entries and deterministic regeneration |
| C++ prototype load | **Pass** | Official 2.0.77 headless with Space Age, Quality and Elevated Rails |
| New save + reload/benchmark | **Pass** | Real `--create`, persisted save loaded again, 2,100 ticks, explicit success markers |
| Production / pollution / telemetry | **Pass** | All production/monitor entities instantiated; supplied powered scrubber completes work and captures pollution; idle and unpowered peers earn none; real monitor section APIs |
| Real campaign API probes | **Pass** | Desolate generation, generated-chunk filtering, actual lander placement/inventory, ammunition, idempotence and configuration preservation |
| Real native API probes | **Pass** | Shape conversion, eradication, symmetric friendly-force relationships without allying enemies to players, future spawned policy, real attack/retreat commandables |
| Packaging | **Pass** | Stable-only deterministic ZIP layout, metadata, allowlist, CRC and SHA-256 tests |

The headless harness requires **both** `SECOND_NATURE_ENGINE_CAMPAIGN_PROBES_OK` and `SECOND_NATURE_ENGINE_SMOKE_OK`, plus successful process exit codes. Loading prototypes alone is not considered a pass.

## What the real probes do—and do not prove

The installed production mod runs its actual lifecycle, registry, crafting, pollution and telemetry callbacks. The companion test mod also runs **unmodified runtime module copies in isolated storage**, using actual engine entities/surfaces. It deliberately arranges ecological state and clocks to reach landing/native/raid test conditions. No debug mutation API ships in the player mod.

This verifies engine API usage and specific invariants; it does not reproduce a human playing from arrival to the ending. The rocket-handler probe uses the shared LuaEntity API of a fixture, **not an actual rocket flight**. The isolated module state is not evidence of a real 0.1-to-0.2 save migration.

Headless mode does not create an interactive player GUI or review rendered artwork. The reported name-collision fix is covered by all three dashboard entry points under a strict reserved-name contract, not by a graphical client click test.

The source-data harness still stubs proprietary sprite/ambient/menu payloads and does not replace the real-engine job. Whole-surface pollution totals include pollution-only engine chunks; hotspot/terrain coverage deliberately includes only fully generated chunks.

## Engine-found issues corrected before release

- Generic GUI child names (`tabs`, `value`, `text`, `state`) collided with LuaGuiElement members. All named children now use `sn_`; opening failure is caught rather than terminating the factory.
- The special `default=true` map preset cannot contain basic/advanced settings. New settings now live only in the named campaign presets.
- Constant combinators cannot call `get_recipe()`. Monitor registration now uses an explicit conditional rather than a nil-valued `and/or` expression.
- `table.deepcopy` is not preloaded in an isolated runtime. Core `util` is imported explicitly.
- Factorio forbids runtime `require` from event callbacks. Dependencies now resolve at parse time, with the control module coordinating chunk visits.
- Deleting a pollutant entry from a Lua prototype table is not a sufficient engine contract for disabled recruitment. Nauvis spawners now have explicit zero uptake and relevant units an unreachable pollution recruitment cost.
- `LuaSurface.get_chunks()` also returns ungenerated/pollution-only chunks. Install-time desolation and the terrain index filter those out; deletion does not repeatedly restart an entire survey.

Regression tests were added or strengthened for these failure modes. No assertion of correctness rests solely on the older 109-test v0.1 result.

## Outstanding checks — not certified

| Check | Status |
|---|---|
| Real client leaf/Shift+T interaction, all tabs and small-window scaling | **Not run by us** |
| Arrival camera and player-controller/cutscene interaction | **Not run by us** |
| In-client main-menu composition and Bloomback animation review | **Not run**; source illustration/icon visually reviewed |
| No-cheat bootstrap through five-world victory | **Not run** |
| Every operation with real heat starvation, full outputs, qualities and module combinations | **Not run comprehensively** |
| Actual rocket launch / passenger travel | **Not run** |
| Existing 0.1 save upgrade and mod removal in the engine | **Not run**; non-destructive contracts covered in doubles |
| Two-client multiplayer, native confirmation/diplomacy and desync checks | **Not run** |
| Real save/reload in every warning, active-wave, native-queue and late-victory state | **Not run comprehensively** |
| Large-factory UPS and large generated-world survey latency | **Not profiled** |
| All Gleba unit tiers and pathfinding under combat | **Not run comprehensively** |

## Focused graphical/playtest checklist

1. **Fresh Last Landing:** only required official mods plus Second Nature; verify the cargo, two turrets, no natural trees/fish, ordinary ores/water and no orbital shortcut. Check the arrival pan and the actual configured skip control.
2. **Dashboard:** leaf, shortcut, Shift+T and command; all four tabs, six guide topics, close/Escape, unsupported/unvisited planets, 100%/125% and small-window UI scales. Check that closing cancels a pending permanent choice.
3. **Local/global pollution:** compare inventory with the engine, walk across chunks, toggle the private overlay, inspect native map pollution. Dirty destinations must not green merely because a nearby machine is clean. Newly sampled hotspots must block readiness before a pass finishes.
4. **Production:** reach ecology without console supplies; test input, output, power and Aquilo heat starvation. Close waste/filter/buffer loops; inspect qualities and every research gate.
5. **Broods:** warn near real nests, remove targets/nests, change diplomacy/peaceful settings, add pollution during warning/attack, confirm the cleaner is the target and pollution emitters have no magical damage immunity. Test Gleba separately.
6. **Terrain:** ore, ghosts, foundations, paving, cliffs, crop soils, water edges and ice. No worker may generate an ungenerated chunk or remove infrastructure. Check murky/clear water transitions and sparse forest growth.
7. **Native choice:** two clean minutes, admin guard, explicit confirm/cancel, both irreversible outcomes, moving natives, expansion and newly explored colonies. Verify other planets remain unchanged.
8. **Persistence/network:** reconnects, respawns, force merges, surface deletion, in-flight saves, ten-minute hold interruption, 90-second beacon expiry, another force's beacons and exactly-once victory.
9. **Scale:** profile 100/1,000/10,000 machines and large maps, with dashboard/overlays on and off. Document observed survey latency rather than calling it instant.

Preserve game version, mod list, save, stack trace and reproduction steps for every failure. Update this ledger with actual evidence; do not relabel unrun checks as passed.
