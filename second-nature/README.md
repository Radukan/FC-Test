# Second Nature · Ironbound Expedition
### Stable Factorio 2.0 / Space Age restoration overhaul · v0.4.0 alpha

**An intact landing craft. A stripped planet. A factory built to bring life back.**

Nauvis has no natural trees or fish in a fresh campaign. The broods tolerate your pollution - but resist the machines that clean their world. Establish a wood-free factory, defend the expedition and restore five distinct planets. Recovery is measured in sustained industrial work and hours of ecological succession, not a fast green repaint.

## Download

### [Second Nature 0.4.0 - stable Factorio 2.0](https://github.com/Radukan/FC-Test/releases/download/v0.4.0-factorio-2.0/second-nature_0.4.0.zip)

[Release notes and checksum](https://github.com/Radukan/FC-Test/releases/tag/v0.4.0-factorio-2.0). **Private repository: sign in to GitHub with repository access.** Use the named mod ZIP, not GitHub’s automatic source archive.

1. Use **Factorio 2.0.77**, **Space Age**, **Quality** and **Elevated Rails**.
2. Back up saves and replace older Second Nature ZIP/source copies with `second-nature_0.4.0.zip`, still zipped, in the Factorio `mods` folder.
3. For the complete opening, start new Space Age freeplay with **Second Nature / Last Landing** and the default mod settings. **Brood Frontier** and **Quiet Reclamation** offer harder/peaceful alternatives.
4. **Shift + T / leaf:** field station and guide. **Ctrl + Shift + P:** local smog overlay.

Windows: `%APPDATA%\Factorio\mods` · Linux: `~/.factorio/mods` · macOS: `~/Library/Application Support/factorio/mods`.

Stable only; experimental 2.1 builds are discontinued. Existing stable saves retain their factories, ecological values and terrain. They do **not** receive another cargo grant or a replacement defense kit. New habitat-readiness rules can temporarily demote an older mature world while its landscape is surveyed/recovered.

## Foundry and Field: presentation update

The explorer now uses a paired armed-pose layout and a shared torso, arm and weapon rig. Gun directions are authored in map space, and every state keeps the same foot anchor. An expanded canvas contains the full pickaxe swing and cast shadow with audited margins.

The character has a more detailed adult silhouette, curved protective panels, fitted equipment, articulated hands, facial features and tied hair. Machinery has chamfered panels, pressure gauges, handwheels, flanged pipes, routed hoses, fasteners, worn material surfaces and component self-shadows. These are original models and renders with a weathered industrial treatment, not copied Factorio textures.

**After the Ash** is a new original 96-second instrumental menu score: low machinery pulses, restrained metallic tones and a gradually warmer harmonic theme. It uses the normal music-volume control. The **Second Nature menu music** startup setting restores the standard track when disabled.

Item and building descriptions now describe their material, construction and function. Current in-game and repository text uses ordinary punctuation; see [the copy guide](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/COPY-STYLE.md).

[Sprite contact sheet](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/art/ironbound-contact-sheet.jpg) · [Rendered animation preview](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/art/industrial-animation-preview.gif) · [Original menu score](sound/music/after-the-ash.ogg)

The aiming and clipping checks validate authored poses, vectors, anchors and image bounds. They do not substitute for a full graphical client review of every strafe/backpedal/armor combination.

## Ironbound campaign

### An intact, permanent lander

The new original landing-craft model has animated standby systems. It is **not a crash-site wreck** and remains **unmineable and indestructible in normal play**, even after your first rocket. It is a permanent cargo camp, not a free orbital vehicle. Build and launch a normal Nauvis rocket to leave.

Surviving older landers receive the same permanent protection. Already removed old hulls are not recreated with free supplies.

### A genuinely wood-free beginning

| Former dependency | New mineral/biological route |
|---|---|
| Small wooden power pole | Riveted pole: iron sticks, copper cable and stone; available immediately |
| Wooden chest | Mineral-frame equipment crate using hand-formed composite stocks |
| Shotgun / combat-shotgun wooden stocks | Mineral-composite stocks made from iron and stone |
| Pioneer seed mix | Cultivated algae, culture and compost |
| Wild fish for healing | Craftable sterile field dressings, plus a finite emergency supply |

The pole/chest keep their vanilla internal IDs for existing blueprints and logistics, but use new recipes, names and original art. Wood processing/composting remains an **optional** route once cultivation is established; it is not required for starting power, basic storage or weapon manufacture.

### Better supplies and defenses

The shared lander supplies:

- **Materials:** 200 iron plates, 100 copper plates, 40 steel, 120 stone, 160 coal and 40 composite stocks.
- **Factory:** 40 gears, 40 circuits, 100 belts, 20 inserters, 20 riveted poles, 40 pipes, 4 burner drills and 6 furnaces.
- **Power:** 1 offshore pump, 1 boiler and 2 steam engines.
- **Reserves:** 120 expedition magazines, 30 repair packs, 20 field dressings and 48 barricades.
- **Deployed:** **four riveted sentries, 60 magazines each**, and **24 field-barricade segments**. Terrain-blocked defense items remain in cargo instead.

New crew members receive a carbine, 40 magazines and a field suit. Cargo is one grant **per force**, never per reconnect, respawn or configuration change. Defenses are useful - not an invulnerable automated factory. Keep ammunition and repairs flowing.

## Three equipment eras

| Era | Weapons | Defenses and protection | Costs that remain real |
|---|---|---|---|
| **Early / Frontier defense** | Expedition carbine; improved ballistic magazines; ordinary bullet family remains compatible | Riveted sentries, field barricades, field armor, sterile dressings | Iron/copper, reloads and repair logistics |
| **Mid / Electrical doctrine** | Induction rifle and battery-fed electrical cells | Capacitor arc turrets, composite walls, 6 × 6 modular expedition armor | Batteries, circuits, power buffers and continuous electricity |
| **Late / Bastion doctrine** | Heavy lance rifle and dense-core rail rounds | Bastion lance turrets, 10 × 10 armor and powered biosphere shields | Interplanetary materials, native rail charging/ammo, equipment-grid energy |

Lances are line weapons: **keep friendly infrastructure out of their firing lanes**. Electrical defenses fail without adequate power; armor/shields do not make the player immortal. Vanilla weapons remain useful alternatives.

## Original art, not tinted stock buildings

All **22 production/restoration/monitor buildings** have original heavy-industrial primary graphics: tanks, filters, hoppers, rotors, seed arms, radiators, culture towers, grow beds and beacon structures. Working machinery has animated loops; the monitor has an animated status light. New defenses have original art, including **64-direction turret animations** and connected barricade/wall pieces.

The new **adult feminine explorer** wears fitted, fully covered industrial expedition gear. There are armor, idle, running, tool, weapon and corpse variations. The optional startup setting restores vanilla/another mod’s character appearance without replacing inventories or controllers.

The art is procedural authored mesh geometry, CPU-rendered with depth, self-shadow maps, surface wear and material lighting - not redistributed Wube textures. Existing game collision, fluid ports, wiring, sounds, projectiles and equipment mechanics are reused where appropriate. Native in-client strafing, backpedaling, armor transitions and port alignment remain graphical playtest items.

## Slow recovery - and slow damage

### Industrial progress

Default ecological work and drift use **30%** of the old rapid coefficients. Physical pollution capture uses **25%** of its former rate: an unupgraded scrubber captures up to **10 pollution units per completed 10-second recipe**, not 40. Physical recipes still produce their declared samples, products and waste.

You still need every fitness axis - atmosphere, thermal balance, water, soil and biodiversity - to develop together. These are ecological suitability scores, not replacements for the game’s pressure, lava, lightning, spoilage or Aquilo heat mechanics.

### A living landscape, not a paint command

Each surveyed eligible chunk tracks **habitat condition** and **pollution stress** over time. Local productive installations support early growth; living-stage ecosystems can sustain succession naturally.

- Sparse pioneer patches develop into dry grass, meadow, lush ground and sparse forests.
- Ideal bare-to-full habitat development takes about **three hours of supported local time** before research bonuses.
- Heavy pollution builds stress over roughly **twenty minutes**. Sustained contamination can degrade mature cover over roughly **two hours**, with weaker contamination acting more slowly.
- Grass loses its lushness before disappearing. Tracked mod-grown trees wither into dead trees and can regenerate after the habitat recovers.
- Ore, paving, ghosts, buildings, crop soils, support tiles and untracked player trees are protected. Aquilo’s ice/foundation support is never replaced.

Four chunks per second are surveyed across visited worlds, with 128 tile candidates per visit. Samples conservatively cap elapsed-time credit at ten minutes. Large maps therefore recover more slowly; these figures are model scales, **not guaranteed whole-campaign durations**. “Habitat condition” is a sampled ecological state, not a claim that an exact percentage of infinite terrain has been painted.

### Research can help, but cannot skip the process

Three **Ecological process optimization** technologies give total bonuses of **+15%, +30%, +45%** to the researching force’s productive clean work/capture and recently supported habitat growth. They are bounded, not infinite. They do not increase recipe speed, shorten raid/victory timers, accelerate damage, or remove the need to clean pollution and supply materials.

## Pollution and native resistance

The dashboard reports the **whole-surface pollution inventory**, including engine-known pollution-only chunks outside generated terrain. The rolling hotspot/habitat survey covers fully generated terrain. The local reading follows the current location.

| Local pollution | Meaning |
|---|---|
| **≤ 10** | Living-soil/biodiversity bonuses can work; habitat recovery is possible |
| **> 10** | Living bonuses stop; samples and chemical/thermal treatment still work |
| **≥ 200** | Strong enough to suppress Nauvis restoration warnings and recall tracked raiders from their targets |

The private overlay covers 5 × 5 nearby chunks; use the native map pollution layer for a wider view. Pollution is not invulnerability: proximity combat, retaliation and obstruction still exist.

With the default inverse-metabolism rule, Nauvis pollution does not recruit vanilla biter attack parties or drive pollution evolution. Scripted raids choose **recently productive clean restoration machines**, not dirty retorts/forcing towers. They require real nests 96-512 tiles away, give 45 seconds of warning, respect peaceful mode and have bounded group sizes. Balanced defaults: 20-minute grace after first ecological work, eight-minute cooldown, up to 40 units and three tracked groups per planet. Greener advanced ecosystems can mobilize stronger variants.

Gleba retains ordinary spores and smaller ecological-response groups; pollution does not pacify pentapods. No arbitrary biter invasion is introduced on Vulcanus, Fulgora or Aquilo.

## The native choice and five-world victory

Final readiness requires:

- **Every fitness axis ≥ 90** and **toxicity ≤ 8**.
- **Total pollution/spores ≤ 500** and **no known sampled hotspot > 10**.
- On Nauvis, **surveyed habitat condition ≥ 80%**.

After two continuously ready minutes on Nauvis, confirm **symbiosis** or **eradication** in **Air & natives**. Symbiosis creates peaceful Bloombacks and flowering gardens; eradication removes known hostile native populations. The permanent policy covers mobile and future populations and affects only Nauvis. Multiplayer administrators decide for the shared planet. Later pollution can still damage either ecosystem.

The original interplanetary economy remains:

- **Vulcanus:** basalt weathering and thermophiles; lava/demolishers remain.
- **Fulgora:** heavy-metal remediation and holmium biocatalysts; preserve islands/oil seas.
- **Gleba:** symbiotic cultures, spores and spoilage-aware cultivation.
- **Aquilo:** imported biodiversity, cryogenic gardens and real heat logistics.

**Victory:** research Second Nature, keep all five worlds self-sustaining and supply your force’s Gaia beacon on each for **ten uninterrupted minutes**, with a completed beacon cycle at least every **90 seconds**. Continue building afterward.

## First factory

Recover cargo → steam power → stone/silica/glass → Pioneer biology → nutrients/culture/algae → compost/substrate → ecological samples → atmospheric treatment → closed filter/waste loops. Samples still emerge before dirty local air allows living bonuses, preventing a cleanup-research softlock.

**Frontier defense** provides replacements for expedition equipment; improved magazines and basic barricades are craftable immediately. Progress through electrical defenses and process optimization while the landscape catches up with your industry. The six-topic field guide is available inside the dashboard.

## Testing and development

This is an **alpha**, not a claim of a completed balanced campaign. [Verification ledger](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/VERIFICATION.md) distinguishes offline/source tests, actual headless checks and outstanding graphical/full-game/multiplayer work. Releases require real stable-engine validation and a re-download/checksum comparison.

- [Full catalog](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/CATALOG.md) · [Balance equations](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/BALANCE.md) · [Model-only timing](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/SIMULATION.md)
- [Campaign design](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/DESIGN.md) · [Development and art regeneration](https://github.com/Radukan/FC-Test/blob/arena/01a07515-fc-test/docs/DEVELOPING.md)

`python3 tools/package.py` builds the stable ZIP. The optional art toolchain is in `requirements-art.txt`; generated game binaries/saves/ZIPs stay out of Git.

**Removal:** back up first, disable Network victory, save, then remove the mod. Modded items/entities may disappear. Terraforming and a completed native choice are not undone.

**License:** MIT for project code and original art. Existing installed Factorio mechanics/assets referenced by the mod remain Wube’s. The optional menu illustration is AI-assisted concept art; the new industrial sprites are original procedural mesh renders, not game screenshots.
