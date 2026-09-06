# Second Nature 0.2.0 · Last Landing

**Stable Factorio 2.0.77 + Space Age + Quality + Elevated Rails. Alpha.**

You land on a stripped Nauvis with a spent descent engine, shared emergency cargo and two loaded turrets. No forests or fish remain. Build the factory that brings life back—then build a rocket to leave. Pollution calms the broods, but prevents the planet you want to create.

## Start and upgrade

- Install this ZIP without extracting it. Replace older Second Nature copies rather than mixing stable/experimental packages.
- For the intended opening, start new Space Age freeplay with **Second Nature / Last Landing** as the map preset. Keep **Desolate Nauvis landing**, **Pollution-fed Nauvis broods** and map pollution enabled.
- **Brood Frontier** is a harder start; **Quiet Reclamation** is peaceful ecological engineering.
- Back up older saves. Updating preserves factories, ecological scores and existing terrain. It does **not** sterilize an old map, provide a second cargo load or retrofit the landing scene.
- Experimental 2.1 builds are discontinued.

## Controls

- **Shift + T**, leaf shortcut or `/second-nature`: dashboard with Planet, Air & natives, Living network and a six-topic field guide.
- **Ctrl + Shift + P**, smog shortcut: private local pollution overlay.
- `/sn-status`: read-only status report.
- `/sn-reindex`: administrator reconciliation, not an ecology reset or cargo grant.

The reported v0.1 dashboard error is fixed by prefixing every named GUI child. The ecology monitor's crafting-only API call, runtime utility import and event-time module-loading issues are also corrected. Dashboard construction failures are caught and logged rather than stopping the factory.

## Emergency cargo

One shared lander per force carries 200 iron plates, 100 copper plates, 40 steel, 120 stone, 160 coal, 40 wood, 40 gears, 40 circuits, 100 belts, 20 inserters, 20 poles, 40 pipes, 4 burner drills, 6 stone furnaces, 1 pump, 1 boiler, 2 steam engines, 100 spare magazines, 20 repair packs and 40 spare walls.

Two turrets receive 75 magazines each, with ten short wall segments. If terrain prevents a defense placement, the items remain in cargo. Crew members receive a pistol and 20 magazines. Cargo is not duplicated on reconnect, respawn or update.

The hull is initially protected and has **no launch function**. Launch a normal Nauvis rocket before returning to orbit. After that first launch, the hull becomes salvageable.

## First living factory

1. Recover supplies, establish water/steam power and keep defenses supplied.
2. Hand-crush **stone → silica** and smelt **glass**. Overhaul red science needs glass.
3. Research **Pioneer biology**: mineral nutrients → pioneer culture → algae. No natural seed or tree is needed.
4. Compost algae and make biochar/living substrate. Green science consumes compost.
5. Soil stations produce **ecological samples**. Samples still emerge while smog blocks the living-soil bonus, so treatment research is reachable.
6. Supply atmospheric scrubbers. Empty spent-filter/effluent outputs and develop closed-loop reclamation.
7. Add watersheds, forests, thermal balancing and detoxification. Defend the machines whose cleanup removes your protective pollution blanket.

## Smog and broods

The global reading uses Factorio's whole-surface pollution inventory, including pollution-only engine chunks outside generated terrain. The hotspot survey covers fully generated chunks. The local reading follows your current location. Totals refresh roughly every ten seconds; four chunks per second are surveyed across visited worlds.

- **≤ 10 local pollution:** soil/biodiversity bonuses and new vegetation can work.
- **> 10:** those living bonuses stop; physical recipe outputs and non-living treatment still work.
- **≥ 200:** Nauvis restoration warnings are suppressed, and tracked raiders turn back from polluted targets.

With default inverse metabolism, pollution no longer recruits vanilla biter attack parties or drives pollution evolution. Recently productive **clean restoration machines** draw the scripted raids; dirty retorts and forcing towers are not targets. Lower concentrations reduce effective resistance and wave size.

Waves require a real nest 96–512 tiles away, give 45 seconds of warning, and respect peaceful mode. Balanced defaults: 20-minute grace after first ecological work, eight-minute cooldown, maximum 40 units and three tracked groups per world. Cleaner advanced ecosystems face stronger scripted brood variants.

**Pollution is not invulnerability:** proximity aggression, retaliation and blocked-path combat can still happen. Gleba retains ordinary spore behavior and smaller ecological-response groups; pollution does not pacify pentapods.

The optional overlay covers 5 × 5 nearby chunks: green ≤ 10, amber > 10, magenta ≥ 200. The map's native pollution layer provides the wider spatial overlay.

## Visible restoration and the final choice

Five fitness axes represent atmosphere, thermal balance, water, soil and biodiversity. They do not turn off lava, lightning, spoilage or Aquilo's heat/support mechanics.

Early gardens grow around successful clean machines. At stage 4, safe Nauvis terrain greens gradually across generated chunks. Smog browns exposed grass; native water becomes murky and clears again after treatment. Paving, buildings, ghosts, ore, foundations, crop soils, oil seas, lava and Aquilo ice are protected.

Stage 5 needs **every axis ≥ 90**, **toxicity ≤ 8**, **total pollution/spores ≤ 500**, and **a completed survey with no known sampled hotspot above 10**. Exploration adds territory to survey. Pollution readings have disclosed sampling latency; this is not an instantaneous scan of an infinite map.

Keep Nauvis fully ready for **two minutes**, then choose in **Air & natives**:

- **Symbiosis:** biters/spitters become original flowering Bloomback grazers; nests/worms become bloom gardens. Friendly to every force, no attack damage or expansion. Their living spaces remain occupied.
- **Eradication:** remove native organisms/colonies and free the land.

The choice requires confirmation, is permanent, and affects only Nauvis. In multiplayer an administrator decides. Bounded workers handle existing/mobile natives; later generated and spawned populations inherit the policy. Optional global mod settings can choose an automatic outcome instead. Neither choice prevents future ecological damage from dirty industry.

## Five-world economy and victory

- **Nauvis:** mineral biology, legacy contamination, pioneer forests and the native choice.
- **Vulcanus:** basalt conditioning and thermophile exports. Lava/demolishers remain.
- **Fulgora:** heavy-metal remediation and holmium biocatalysts. Preserve islands/oil seas.
- **Gleba:** symbionts, balanced spores and spoilage-aware production.
- **Aquilo:** imported biodiversity matrices, cryogenic gardens and real heating infrastructure.

**Victory:** research Second Nature and supply your force's Gaia beacon on each of the five self-sustaining worlds for ten uninterrupted minutes. Each beacon must complete a cycle at least every 90 seconds. Interrupted readiness resets the hold; the factory can continue after winning.

Ecology monitors emit eleven signals: five fitness axes, toxicity, resistance, stability, stage, global pollution and local pollution. The first manual section is reserved; it never shares a named group across planets.

## Presentation, testing and removal

The Last Landing menu illustration is optional in startup settings. It replaces menu simulations; disabling it restores the normal menu behavior. Bloombacks use original eight-direction/four-frame sprite art.

This is an alpha. Source/runtime regression tests and a required real stable headless workflow cover progressively stronger engine checks; they are not a graphical review, full campaign playthrough or multiplayer/UPS certification. See the repository verification ledger for exact evidence.

Before removing the mod, disable **Network victory**, save, and back up. Mod removal can delete its items/entities. Terrain changes and a native decision are not reversed.

Project, full catalog and verification: https://github.com/Radukan/FC-Test (private; repository access required).

MIT license for project code/original art. Installed Factorio assets are reused, not redistributed. The menu is an original AI-assisted illustration; friendly sprites/gardens are original procedural artwork, not screenshots.
