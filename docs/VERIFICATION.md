# Verification ledger: Foundry and Field 0.4.0 alpha

## Reported visual defects

A player reported incorrect shooting direction and the pickaxe disappearing at the top of its frame in 0.3. The earlier headless pass verified accepted prototype structures, not the appearance of those animation rows in a graphical client.

The 0.4 exporter no longer treats the 18 armed rows as a full-circle turnaround. It uses paired gun-facing/stride-axis rows over the engine-mirrored half. Torso, hands and gun share the aim transform; stride is independent. The projected muzzle vector is checked against the intended facing.

Mining has a larger shared-pivot canvas. Authoring checks include every tool vertex and the projected cast shadow across all mining frames, directions and armor looks. A separate pixel-alpha test checks the exported sheets for edge truncation. Character ground axes are already map-aligned, with a second projection correction disabled.

## Validation status

**Completed 0.4 validation:** [34073999327](https://github.com/Radukan/FC-Test/actions/runs/34073999327), code commit `64e7700f0e5bdd4730ac94cb1f6c71f6144bda8f`. All **157 tests** and the official **Factorio 2.0.77 headless** job passed. The source aiming/mining sheets and revised industrial contact sheet were inspected after export. This ledger was updated after observing that result.

Final 0.4 source/engine runs are recorded by the required GitHub validator and release publisher. Do not infer that a prior 0.3 engine run proves later artwork. The publisher must pass the exact tagged source before uploading and re-download both assets for checksum/byte comparison.

The suite retains the campaign, pollution, habitat, weapons, protected lander and strict GUI/import regressions. New checks cover:

- Equipment descriptions that explain the object instead of development or availability commentary.
- No long dash punctuation in current source, in-game localization or GitHub-facing documentation.
- The menu-only music replacement, valid stereo Vorbis headers, duration and the authored waveform report/hash.
- Paired armed row structure, muzzle/torso direction and map-space projection.
- All mining model/shadow bounds, identical state pivots and exported image-edge margins.
- Atlas dimensions, engine texture bounds and visible working-frame differences.

The soundtrack is an original 96-second stereo composition. It is synthesized without borrowed samples or melodies. The authoring pass decodes the exported Ogg and records measured peak/RMS in the score report. Source validation parses its Ogg/Vorbis structure; the game package includes the sound directory explicitly.

Current editable GitHub release titles/bodies have had long dash punctuation removed. Published commit history and other users' historical comments are not rewritten.

## What the real-engine harness establishes

The official Factorio 2.0.77 headless job loads C++ prototypes, creates a save, reloads it and runs 2,100 ticks. It exercises real production counters, powered/idle/unpowered behavior, pollution, circuit telemetry, render-object creation, protected landing cargo, native outcomes and attack/retreat commands. Companion probes arrange isolated state to reach those conditions. No debug mutation API ships in the mod.

Both explicit engine success markers and zero exit status are required. A prototype-only load is not counted as a complete pass.

## Graphical and gameplay checks still required

- Native client aiming while stationary, strafing, retreating and changing direction, for all weapons and armor states.
- The native engine's complete mirrored/reversed locomotion selection under real player controls. Authoring vector tests are not a full client interaction test.
- Pickaxe framing at normal and high zoom, armor/Mech transitions, corpse appearance and all source/shadow alignment.
- Building scale, port/wire endpoints, full rotations, weapon muzzle placement and all working loops at gameplay zoom.
- Audible main-menu playback, loop/fade behavior and balance against the user's music-volume setting.
- Complete no-cheat five-world playthrough, sustained combat balance, multiplayer/desync, older-save migration and large-factory/GPU profiling.

The contact sheets and GIFs demonstrate rendered assets, not in-game footage. Original models, richer shading and more detailed textures are not a claim of graphical-client certification.

## Focused retest

1. Open a stable save with the required official mods and Second Nature. Confirm that inventories, character controllers, research and habitat state remain intact.
2. Aim and fire in all eight facings, then strafe and backpedal. The gun, hands and torso must agree; compare to the source aiming review sheet.
3. Mine continuously in all directions. The pickaxe and shadow must remain inside their frame without shifting the feet.
4. Review all building orientations and turret firing states. Check dark surfaces, gauges, moving parts and pipe/wire endpoints.
5. Read representative material, ammo, armor and building descriptions. They should describe construction/function, not a change request or crafting milestone.
6. Return to the menu, listen to After the Ash, adjust music volume, then disable the setting and confirm standard menu music is restored.
7. Recheck the saved-world/campaign and performance scenarios documented in the development guide.

Record version, mod list, save and reproduction steps for failures. Keep unrun checks explicitly unrun.
