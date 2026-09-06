# Verification ledger — 2026-09-06

## Current status: alpha, engine verification pending

This repository contains an implemented restoration campaign, installable packages, original small-format art, and automated tests. It does **not** yet contain evidence of a successful real-engine launch or a complete playthrough.

The authoring environment can retrieve Wube's Git repository and Python packages, but direct TLS downloads from Factorio's binary/CDN endpoints fail. No Factorio executable is installed. Tests against the source data are valuable but are not a substitute for running the game.

### Checks actually executed

| Check | Result | Scope |
|---|---|---|
| Lua 5.2 compilation | **Pass** | Every mod Lua file |
| Pure ecological model | **Pass** | Caps, drift, stages, toxicity, dirty forcing, resistance, counters, deterministic restoration and copy/replay behavior |
| Runtime test doubles | **Pass** | Install/config events, idle accounting, polling, clones, dense-bucket removal, teleport rebasing, deletion, force merges, telemetry, combat scheduling/cancellation, terrain guards, GUI handlers, read-only snapshots, sustained network logic |
| Official 2.0.77 data scripts | **Pass** | Full data stages; integration on and off |
| Official 2.1.17 data scripts | **Pass** | Full data stages; integration on and off; category/science-family adapters |
| Content graph | **Pass** | Technology cycles, prerequisites, unlock ownership, custom-chain structural reachability, bootstrap without wood/seeds, fluid port capacity, lab support and surface conditions |
| Safety/recycling | **Pass** | No waste/charge self-recycling exploit; operation productivity/quality disabled; source references intact |
| Localization | **Pass** | Catalog coverage, literal UI keys, no duplicate keys, reproducible generation |
| Art | **Pass** | Custom icon paths, PNG dimensions/transparency; contact sheet and cover visually reviewed |
| Packaging | **Pass** | Both branch-specific zips, complete allowlisted contents, metadata, reproducibility and SHA-256 |
| Full-kit model convergence | **Pass** | Every planet reaches stage 5 in a bounded mathematical simulation with unlimited supplies; **not a playthrough** |
| Automated suite total | **109 passed** | `python3 -m pytest -q`, with both pinned Wube source checkouts present |

Source-data harness limitations: missing proprietary upstream sprite metadata and ambient/menu payloads are explicitly stubbed. C++ prototype validation, actual power/fluid/heat networks and rendering are not executed.

### Checks not yet executed

| Release gate | 2.0.77 | 2.1.17 |
|---|---|---|
| Real headless prototype load and new save | **Not run** | **Not run** |
| Real craft counter, power and pollution smoke test | **Not run** | **Not run** |
| Graphical UI, entity animation and recipe selection review | **Not run** | **Not run** |
| Full fresh-save campaign through five-world victory | **Not run** | **Not run** |
| Real save/load and configuration migration | **Not run** | **Not run** |
| Two-client multiplayer/desync test | **Not run** | **Not run** |
| Large-factory UPS profile | **Not run** | **Not run** |
| Existing-save installation / removal | **Not run** | **Not run** |

## Release checklist

### 1. Binary smoke test

Run `python tools/headless.py --factorio /path/to/factorio` once for each game branch. Preserve `create.log` and `benchmark.log`. Require the explicit success marker, not merely a zero exit code. Confirm all prototypes load without warnings attributable to this mod.

### 2. Graphical quick pass

- Start a fresh Space Age freeplay game with only the required official mods and Second Nature.
- Check first-join text, top button, shortcut, Shift + T, all dashboard tabs and the Escape/close behavior.
- Change selected planets; unvisited worlds must not show fabricated measured progress.
- Review at 100%, 125% and a small-window UI scale. All instructions and close controls must remain reachable.
- Check all entity icons, tinted animations, badges, fluid ports, crafting screens and Factoriopedia entries.
- Check a normal-quality and a higher-quality machine. No duplicated or premature ecological gain.
- Verify monitor signals using an actual decider combinator; no shared named groups across planets.

### 3. Bootstrap and progression

- Reach ecology science without console ingredients on a normal map and on a tree-sparse map.
- Confirm glass does not break automatic stone-brick furnaces.
- Test factory power starvation, missing heat, a stopped inserter, full spent-filter inventory and full fluid output.
- Buffer early waste until closed loops unlock. Verify the water/filter loop can be restarted from a small reserve.
- Check every new research ingredient and each vanilla technology gate in a real research queue.
- Attempt local specialty crafting on the wrong planet; it must fail with understandable surface conditions.
- Reach the stage unlocks by real machines, not by editing custom surface properties.

### 4. Native response

- Nauvis: establish nests in the allowed range; trigger a warning and confirm pathing to the target.
- No nests, too-close nests, distant nests: no arbitrary spawn.
- Remove the nest or target during the warning; verify safe cancellation.
- Disable resistance / enable peaceful mode during a warning; verify cancellation.
- Confirm existing units are recruited and local crowding suppresses new spawns.
- Gleba: test all evolution tiers, wrigglers, strafers and stompers; watch group membership/pathing.
- Vulcanus/Fulgora/Aquilo: no invented biter/pentapod invasions.

### 5. Terrain and heating

- In each biome, place resource patches, cliffs, paving, ghosts, tiles with hidden support, and nearby buildings.
- Verify nothing protected is overwritten and no entities/decoratives are deleted by tile correction.
- Check native crop soils and oil/lava edges specifically.
- Aquilo: confirm overlays are anchored, disappear with the machine, and do not alter ice/foundation support or heat rules.
- Turn terrain/trees off mid-game; existing terrain stays, new changes stop.
- Confirm terrain routines never generate a new chunk.

### 6. Network and persistence

- Complete all five worlds through real supply chains.
- Research the final technology; interrupt a beacon shipment long enough to exceed 90 seconds; the hold must reset.
- Stop at 9:59, save/reload and complete the final second; award victory once, allow continuation.
- Verify another force's beacons cannot satisfy your own goal.
- Merge forces, destroy/rebuild beacons, clear/delete a test surface and rescan the registry.
- Save/reload while a wave is warned or active and while a garden overlay exists.
- Test the victory setting round-trip, including a pre-existing disabled stock victory setting.

### 7. Performance and release decision

- Profile 100, 1,000 and 10,000 tracked machines with UI closed/open.
- Test multiplayer host/client with machines added/removed by construction robots and script-raised events.
- Measure recurring callback budgets and verify no growth in stale registrations, buckets or render objects.
- Complete at least one no-cheat campaign and record bottlenecks, research timing, logistics needs and enemy pressure before tuning rates.
- Update this ledger with actual commands, game versions, logs and results. Do not relabel unrun checks as passed.
