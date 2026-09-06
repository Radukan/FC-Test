# Second Nature — Planetary Restoration

**Build a factory. Grow a world.** A Factorio: Space Age campaign overhaul, v0.1.0 alpha.

Restore atmosphere, thermal balance, watersheds, living soil and biodiversity on Nauvis, Vulcanus, Fulgora, Gleba and Aquilo. Close industrial loops—or take a dirty shortcut and repay its toxic debt. Native organisms resist ecological change even when your factory gets cleaner.

## Install

Use the archive built for **your Factorio branch**, leave it zipped in the game's `mods` directory, and enable Space Age, Quality, Elevated Rails and Second Nature. Start a fresh Space Age freeplay game. Do not install both archives at once. Folder installation from this repository targets 2.0.77; the package builder also makes a 2.1.17 archive with adapted metadata.

- Windows: `%APPDATA%\Factorio\mods`
- Linux: `~/.factorio/mods`
- macOS: `~/Library/Application Support/factorio/mods`

**Alpha notice:** Lua 5.2 logic tests and full official source-data loading are covered. A binary-based smoke test and full campaign playtest must still be run before calling this a production-ready release. Back up existing saves.

## Start here

Press **Shift + T**, use the leaf shortcut, or run `/second-nature` for the in-game dashboard and complete field guide.

1. Crush **stone → silica** in your inventory; smelt **silica → laboratory glass**. Red science now needs one glass.
2. Research **Pioneer biology**. Power and pipe water to a pioneer bioreactor. Make mineral nutrients, pioneer cultures, then algae.
3. Research **The living substrate**. Compost algae. Green science now needs compost. Make biochar and soil substrate.
4. Research **Field ecology**. A supplied soil restoration station earns ecological samples for ecology science.
5. Scrub air, rebuild watersheds, seed forests, balance heat and remove toxins. Physical completed crafts—not idle buildings—earn progress.
6. Develop each world's specialty, export its biological products, and unite them in biodiversity sanctuaries.
7. Build Gaia beacons, research **Second Nature**, then maintain all five self-sustaining worlds and regular beacon cycles for ten uninterrupted minutes.

**Self-sustaining:** all five fitness axes ≥ 90, toxicity ≤ 8. Each force needs its own recent beacon cycle on each planet (at least one every 90 seconds). A broken link resets the hold.

## Factory rules worth knowing

- All five worlds have an airborne pollution layer: Gleba retains spores; the other four use pollution. This does not create native enemies on lifeless worlds.
- Output-blocked, ingredient-starved, frozen or unpowered machines earn nothing. Route all spent filters, effluent, sludge and depleted buffers.
- Water and soil support biodiversity. If growth stalls, read the dashboard's support ceiling instead of adding more identical machines.
- On Nauvis and Gleba, recovery can provoke native nests. Balanced mode gives a local 20-minute grace period and 45 seconds of warning; no nearby nests means no scripted waves. Peaceful mode works.
- Restoration never rewrites physical planet pressure/temperature. Lava, oil seas, crop soils, ice platforms, foundations, resources and player infrastructure stay protected.
- Aquilo gardens are sheltered visual overlays; heat pipes and native heating remain necessary.
- Circuit monitors output 0–100 fitness, toxicity, resistance and stability; ecological stage is 0–5. Their first section is reserved for telemetry.
- Disable **Overhaul vanilla progression** at startup for additive content. Other settings control speed, attacks, terrain, trees and victory independently.

## Safety and compatibility

Designed for the five stock Space Age planets and standard freeplay. Other major overhauls, alternate victory scenarios and third-party planets are not supported integrations. Script-building mods should raise build events or call `remote.call("second_nature", "register_entity", entity)`.

For existing-save installation, back up first and expect changed science recipes. Before uninstalling, **disable Network victory, save, then remove the mod**; this restores the prior Space Age finish setting. Removing a content overhaul can remove its items and machines. Terrain changes already made are not rolled back.

`/sn-status` prints a read-only report. `/sn-reindex` is an administrator-only recovery command that preserves ecological progress.

Source, complete catalog, design, test commands and the verification ledger: **https://github.com/Radukan/FC-Test**.

Original code and generated art: MIT. Machine animations and sounds reference installed Factorio/Space Age assets; Wube's proprietary artwork is not redistributed. Not affiliated with Wube Software or Planet Crafter's creators.
