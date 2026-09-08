# Verification ledger: Nightglass Foundry 0.8.0 alpha

## Current 0.8.0 candidate

This update fixes starter iron sticks, visible crew recall and controller-only upper-left controls; humanizes the original goth explorer; rebuilds 117 inventory/building icons; and expands power to six distinct systems in each stage. See [POWER-ROSTER.md](POWER-ROSTER.md) for ratings and constraints.

The native harness adds real recall after a mid-flight pause, a fresh force with starter sticks/poles before green science, and native electrical/fuel/fluid/heat output checks for all eighteen systems. Required markers include `SECOND_NATURE_ENGINE_CREW_RECALL_OK` and `SECOND_NATURE_ENGINE_POWER_STAGES_OK`. Existing solar-rail, field-planner and campaign probes remain.

Source tests verify changed controls/accounting, top-left button gating, icon uniqueness/legibility at native size, stage counts, genuine energy inputs and geothermal regional/legacy limits. The source suite contains 257 tests covering the updated contracts; the completed full-suite result is recorded with the local commit. Native stage-power/recall validation remains pending GitHub reconnection and CI. Graphical-client appearance/hotkey behavior and long-run campaign, multiplayer and performance profiling remain unverified.

## Historical Nightglass 0.7.0 evidence

## Current Nightglass 0.7.0

This larger update adds the HD goth explorer, three solar-only locomotive tiers and six power options. See [NIGHTGLASS.md](NIGHTGLASS.md) for the installed-panel/battery design, metered motor credit, night derating, native fuel behavior, planetary power models and remaining client limitations.

The new native engine scenario begins with empty solar batteries at night beside an ordinary powered grid, charges them from actual roof equipment in daylight, drives scheduled trains, checks reduced night limits, then verifies that exhausted batteries receive no hidden traction. A separate labeled test seed exercises saved motor credit. Real generating plants charge native accumulator loads, burn fuel and produce pollution/ash where appropriate.

The required new markers are `SECOND_NATURE_ENGINE_SOLAR_RAIL_OK` and `SECOND_NATURE_ENGINE_POWER_OPTIONS_OK`, in a 6,000-tick run alongside the prior campaign, construction and planner probes. Source tests include energy conservation, locked equipment, fuel rejection, safe speed capping, new research and the doubled-resolution striped sprite contract.

The completed source build passes **246 local tests** with the pinned official 2.0.77 data. **Official engine: PASS.** [Run 34173627767](https://github.com/Radukan/FC-Test/actions/runs/34173627767), code/test commit `4b84f66ac137cd270c99a2822a0d744cb0b0a581`, passed the source job and the official 2.0.77 create/reload/6,000-tick job. Real panel charging, native scheduled traction, reduced night limits, empty-battery rejection, fuel/pollution/ash and accumulator output all passed. The first run exposed an invalid reverse test route for single-ended locomotives; the rerun uses a valid forward night route, rather than bypassing the energy assertions. No graphical-client playthrough, elevated-rail visual certification, full campaign balance or long-run GPU/UPS/multiplayer result is claimed.

The installable archive contains **500 mod files**, is **100,635,307 bytes**, and passes ZIP CRC and SHA-256 verification. The release publisher revalidates the final tagged source and re-downloads its assets before reporting success.

```text
3fb4558a44d9cf74bf68e6d617b3172321503c69ccae6e74ac0174b95e69e22c  second-nature_0.7.0.zip
```

## Historical Field Crew 0.6.2 evidence

## Current 0.6.2 release

The existing no-power inventory drone/controller system is retained, per the activation clarification. New crews automatically enable, a visible notice/monitor explains Ctrl + Shift + B, and native blueprint/planner shortcuts unlock with the early research. New task tests cover explicit deconstruction, upgrade material/old-item accounting, preserved configurations and paired underground upgrades. The renderer now exports 16 directional drone views and updates positions every tick.

Character regressions cover the reduced teardrop profile, rounded boot mesh and exact right/left grip fractions of 48%/16% along the shaft. Existing articulation, tool contact and framing guards remain.

The expanded official-engine scenario uses native mining/upgrading on real entities, including a loaded chest, a rare inserter with custom vectors, and an underground pair. It requires `SECOND_NATURE_ENGINE_FIELD_PLANNERS_OK` during a 3,300-tick create/reload run, in addition to all prior markers. Native GUI/hotkey use and long-run GPU/UPS/multiplayer profiling are not claimed.

The completed source export passes **235 local tests** with the pinned 2.0.77 prototype data present, and `git diff --check` is clean. **Official engine: PASS.** [Run 34166208791](https://github.com/Radukan/FC-Test/actions/runs/34166208791), code commit `2a013829fafbd08b92cf370922604eeb94d45a87`, passed the source job and the official 2.0.77 create/reload/3,300-tick job. The native planner marker passed for real chest contents, rare inserter configuration, old/new upgrade item accounting and an underground pair, alongside all existing markers. Native GUI/hotkey interaction is still not a headless claim.

The local installable archive contains **435 mod files**, is **67,941,618 bytes**, and passes ZIP CRC and SHA-256 verification. The publisher independently revalidates the tagged source and re-downloads its release assets before reporting success.

```text
7242933b07cb5ff3671704d58ddcaa6343e3a761089a3acd0559ef83e1640d0b  second-nature_0.6.2.zip
```

## Historical Field Crew 0.6.1 evidence

## Field Crew 0.6.1

This update adds a construction-only personal drone system and revises the explorer's whole-body motion. [FIELD-CREW.md](FIELD-CREW.md) records the mechanics, limits and inventory safeguards. [AGENT-REPORT.md](AGENT-REPORT.md) records the available agent/usage information without inventing model identities or token totals.

Added checks cover exact material reservation/refund, quality, two operators claiming one ghost, a 64-drone crew, lowered limits, research/controller/permission gates, entity and tile ghosts, loose-item protection, packed-item exclusion, cancellation, failed movement/revival, disconnect/death/surface/controller changes, destroyed-drone cargo recovery, saved escrow and separate body/shadow render cleanup.

Motion checks measure pelvis/shoulder counter-rotation, independent head movement, opposing arm/leg swing, constant limb lengths, right-hand-leading grips, attachment to the shaft, fast downstroke versus wind-up, body drive, sole clearance, bounded armor-damped secondary motion and loop continuity. Export bounds and actual sprite/preview fingerprints remain required.

The required native marker is `SECOND_NATURE_ENGINE_FIELD_DRONES_OK`. Its companion scenario saves with four drones in flight, cancels one ghost, reloads, constructs a normal wall, a rare chest and a tile, preserves exact material/drone totals across two operators, leaves loose cargo untouched, and verifies that a nearby powered roboport cannot dock or network these workers. Real engine characters/inventories/ghosts/render objects are used; a LuaPlayer-facing shell is a fixture, not an interactive GUI or per-player-settings playtest.

The finished candidate passes **223 local source/offline tests**, including the pinned official 2.0.77 prototype data. `git diff --check` is clean. **Official engine: PASS.** [Run 34147961483](https://github.com/Radukan/FC-Test/actions/runs/34147961483), code commit `a8cbd9045c53df7a315b1a47326e8abe03361872`, passed both the source job and the official Factorio 2.0.77 create/reload/2,100-tick job. The new required `SECOND_NATURE_ENGINE_FIELD_DRONES_OK` marker passed alongside the existing campaign, lander, logistics, layout and smoke markers. This includes real normal/rare construction, a tile, cancellation, two-operator accounting, preserved in-flight escrow and isolation from the powered reference roboport. No graphical Factorio client, long-run UPS/GPU profile or two-client desync test has been run. Actual native movement/Mech transitions and subjective appearance still need client review.

### Installable archive

The release publisher revalidates the final tagged commit and re-downloads the uploaded ZIP/checksum before reporting success. The local 0.6.1 archive contains **432 mod files**, is **66,818,242 bytes**, and passes ZIP CRC and SHA-256 verification:

```text
6e41c5d1286ce7b4fe65279844e95fb01a9a4dbb1063c5a284f45e6180f42091  second-nature_0.6.1.zip
```

The README inside the ZIP points source-only documents at the immutable 0.6.1 tag. The source and generated assets are committed to the session branch; a pull request targets `main`, rather than a direct push to that branch.

## Historical Verdant Works 0.6.0 evidence

## Current continuation / 7 September 2026

The previous 0.6 source commit, `eb8213737c055de109d0ee3a9c192fa110e4e9e9`, passed [source and official stable-engine CI](https://github.com/Radukan/FC-Test/actions/runs/34088602288). It also passed **178 tests** after recovery into this workspace with the pinned official 2.0.77 prototype data present. See [the continuation audit](CONTINUATION-AUDIT.md) for what was already done versus finished here.

The finished continuation passes **192 local tests** with that same pinned data. `git diff --check` passes. The deterministic 0.6.0 ZIP was built, and its SHA-256 sidecar verifies successfully.

Added verification covers:

- Every current machine sheet's complete alpha margins, canonical view and compensated ground/pipe pivot.
- Mesh and cast-shadow bounds in all rotations; the exporter checks every generated frame.
- The Wayfarer model's physical bounds inside the preserved lander collision box.
- One static hull/shadow plus a cropped opaque overlay: every composed frame exactly matches its complete reference render.
- Render-only migration of an existing camp, depleted cargo preservation, unchanged entity/position/rocket history, missing-ship behavior, and no duplicate animation after repeated configuration changes.
- Current contact/locomotion/mining/process/ship previews tied to actual source sprites by SHA-256, with complete loops and explicit source-review timing.
- Updated generated footprint documentation and all README art links.

**Current official-engine rerun: PASS.** [Run 34136511528](https://github.com/Radukan/FC-Test/actions/runs/34136511528), code commit `ee35420e77e16877be7cc9a4a1e4bfaca96deb6d`, passed both the source job and the official Factorio 2.0.77 headless job. This includes native save creation, reload and the 2,100-tick probe run. The new required marker is `SECOND_NATURE_ENGINE_LANDER_REFIT_OK`; existing Verdant layout, pipe/vector, audio API, campaign and smoke markers remain mandatory. The lander refit probe uses a real render object, removes 197 iron plates from the camp, and verifies that the remaining three are not replenished by configuration changes.

The sandbox could not reach the Factorio binary host or the Actions log/artifact CDN. Native validation therefore ran on GitHub's runner; success was confirmed through the GitHub run/job API. A local-versus-CI artifact re-download comparison was attempted but blocked by the CDN and is **not claimed as a pass**. The local deterministic package build and checksum check did pass:

```text
3638625478b1f32d233425bcdfc8db09ff36a02aed3bef6063489e49b72c0181  second-nature_0.6.0.zip
```

That earlier source-build archive was 62,299,192 bytes and contained 420 mod files. Its checksum is historical: the release preparation changes the bundled README to use permanent release/tag links, which changes the ZIP bytes without changing gameplay. Use the checksum attached to the release for the published download. The publisher requires tagged-source validation followed by an asset re-download and byte comparison.

No graphical Factorio client or two-client multiplayer test was run here. Source-art review is not a screenshot/playthrough certificate. In particular, native character/Mech transitions, exact client pipe seams, audible arrival/music/jukebox behavior, GPU use and long-term campaign balance remain unverified. The [0.6.0 prerelease](https://github.com/Radukan/FC-Test/releases/tag/v0.6.0-factorio-2.0) distributes the installable ZIP and checksum. The release workflow separately validates the exact tagged source and verifies its uploaded assets; a successful branch run alone does not certify a completed release upload.

## Historical Living World 0.5.0 evidence

## Completed stable-engine evidence

Run [34081716276](https://github.com/Radukan/FC-Test/actions/runs/34081716276), code commit `fc2e379b7a614617eed72d8002c5c99930e716af`, passed the source validator and official Factorio 2.0.77 headless job. The exercised code passed 169 tests. A final complete-audio/lyrics regression brings the local suite to **170 tests**. Release publishing independently revalidates the exact tagged source and re-downloads its assets for checksum/byte comparison.

The source contact sheet, revised pipe-nozzle images, mining frames and complete audio files were generated. Source-art previews are not in-game footage, and waveform/file checks do not establish native-client listening behavior.

## What was actually exercised

| Check | Result / scope |
|---|---|
| Lua compilation and strict runtime doubles | Pass; existing campaign, GUI naming, parse-time import and accounting regressions retained |
| Stable source data stages | Pass; all new prototypes, references, research dependencies, ammo categories and custom vector flags |
| Original art contracts | Pass; atlas bounds, visible working motion, paired aim poses, full mining/shadow envelope and pointed impact geometry |
| Fluid-port source contract | Pass; data prototypes and mesh anchors read the same connection coordinates, with every quarter-turn checked |
| Official C++ prototype load | Pass for buildings, stickers, beam, endgame logistics, hero/music entries and jukebox instruments |
| Real save creation/reload and 2,100-tick run | Pass |
| Actual inserter endpoint setters | Pass; diagonal two-tile vectors accepted and out-of-range editor request rejected |
| Native blueprint vector persistence | Pass; custom pickup/drop values present in the blueprint |
| Actual custom-vector item transfer | Pass; a powered vector inserter moves four iron plates between the configured diagonal chests |
| Physical pipe connectivity | Pass in all four machine rotations; visible nozzle boundary agrees with the midpoint between connected pipe centers |
| Jukebox native calls | Pass; correct instrument/note indices, track selection and stop/replacement call accepted |
| Combat/campaign probes | Pass; all defense tiers instantiate and accept ammunition, native outcomes and attack/retreat APIs continue to work |
| Audio asset integrity | Pass; complete stereo Vorbis duration/hash checks, narration-before-song file layout and saved lyrical text |
| Copy and punctuation | Pass; physical object descriptions and no prohibited long dash characters in current project text |

## Engine-found corrections

- Blueprint vector tables returned array coordinates; the probe now validates the actual representation rather than assuming named fields.
- Programmable-speaker instrument and note arguments are one-based. The jukebox maps its UI track indices onto the native one-based archive and the stop note.
- Pipe connection `position` and `target_position` describe their respective centers. The visible seam is their midpoint, not the machine-side center. The art contract and rotated connectivity probe agree on that boundary.

## Audio implementation and limits

The selected synthetic female voice performs an original personal log and spoken lyrics. The synthesis tool cannot sing. The 160-second industrial-punk/metal arrangement is an original synthesized instrumental with spoken vocals, not a sung-metal performance or a recording of a human performer.

The native Nauvis hero track is a single 206.46-second file: 45.76 seconds of narration, a short pause and the anthem. A native arrival track owns the sequence instead of simulation-tick sound fragments. The jukebox is an actual programmable-speaker entity, with local playback by default and administrator-gated surface broadcasting in multiplayer.

Headless mode has audio disabled. It verifies accepted sound/music/instrument structures and play/stop calls, **not** audible first-arrival timing, music-volume balance, native jukebox UI or overlap behavior. Those remain graphical-client checks.

## New editor and logistics limits

Custom pickup/drop positions are integral offsets in [-2,2] on each axis, with the center and identical endpoints excluded. Server-side code checks types, range, ownership and the startup flag. This is a two-tile per-axis range, not a literal four-tile area. Other mods retain their own scripting APIs; no per-tick factory-wide enforcement scan is added.

Native custom-vector state is retained for blueprints. The engine probe verifies a real transfer through configured diagonal positions. Complete rotation/paste/robot/quality combinations and the relative GUI require further client testing.

The vital transport family shares a 90-item-per-second base rate before stacking. Native tread/corner/stack geometry is retained, with original rounded platforms/manifold art. The canopy manipulator retains the game's four-item belt-stack limit.

## Still not certified

- Audible new-game hero-track triggering, narration mix, replay/stop behavior heard through a client and multiplayer audio scope.
- Every native editor interaction, alternate permissions, rotation/paste, robot construction and controller mode.
- Pixel-perfect pipe seams and all ports at all zooms, qualities and rotations in a graphical client.
- Every pickaxe/aiming/armor/Mech transition and native movement combination.
- Full no-cheat campaign balance, long-term logistics throughput, every weapon target/resistance interaction and friendly firing lanes.
- Existing-save migration/removal across all possible states, two-client desync tests and large-map/GPU/UPS profiling.

## Focused retest

1. Start fresh Space Age freeplay on Nauvis. Confirm the log is visible and the voice precedes the anthem. Check the opening-audio setting.
2. Open the landing jukebox; play both scores, replay the transmission and stop playback. Check local versus authorized surface broadcast.
3. Configure every vanilla inserter type and both new arms. Test both grids, reset, diagonal positions, prohibited cells, blueprints, pasting and robot placement.
4. Build the whole vital belt family; confirm matched flow, stacking, routing and the sixteen-tile tunnel range.
5. Attach pipes to each active machine port in all rotations. Compare the real seam against the source alignment diagrams.
6. Mine in every direction. The tapered point must lead the impact without clipping or foot-pivot shifts.
7. Use mycelial rounds, resonance effects and pressure-lance impacts. Contamination capture must never manufacture pollution or award free fitness/science.
8. Recheck preserved campaign state, native decisions, existing defense ammunition and the five-world victory loop.

Record game version, mod list, save and reproduction steps. Keep unrun checks labeled unrun.
