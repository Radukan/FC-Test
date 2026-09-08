# Ironbound campaign design · stable 0.3

## Premise

The protagonist arrives in an **intact atmospheric landing craft**, not a destroyed spaceship. Its orbital stage is gone, but the craft remains a permanently protected cargo camp. Normal rocket progression is the only route off Nauvis.

A new Nauvis is stripped of natural trees/fish and seeded with real legacy smog. The broods tolerate that contamination, but react to successful cleaning. The factory must supply ecological change, close its waste loops and defend the resulting habitat.

The five-planet Space Age economy remains. This is not a removal of lava, lightning, spoilage, orbital logistics or Aquilo heat/support.

## Closing the gaps in a lifeless start

A finite pile of wood is not a structural solution. Iron/stone composite stocks now replace wooden stocks in initial crates and shotguns. Riveted poles use iron sticks, cable and stone and are available immediately. Algae replaces wood in pioneer seed preparation. Wood recovery is still possible after cultivation, but not mandatory for initial electricity, storage or armaments.

The lack of wild fish also matters: sterile field dressings provide a real craftable healing route. All equipment uses normal crafting, inventory, ammunition, damage, energy and armor APIs rather than custom invincibility scripts.

Fresh shared cargo and four preloaded sentries make arrival survivable without automating the whole factory. The kit is per force, not per reconnect. New crew members receive practical personal gear. Surviving older landers are protected on upgrade; neither replacement cargo nor retroactive terrain erasure occurs.

## Three defensive eras

- **Frontier:** compatible ballistic magazines/carbine, riveted sentries and barricades, field armor and healing dressings.
- **Electrical:** battery-fed induction shots, capacitor turrets, composite walls and 6 × 6 equipment-grid armor. Power outages matter.
- **Bastion:** costly rail lances, heavy turrets, 10 × 10 armor and powered shields. Line weapons retain friendly-fire/firing-lane consequences.

Vanilla weapon choices remain useful. The new equipment augments the restoration campaign rather than replacing every military recipe with unrelated intermediates.

## Long-horizon ecology

The old fast coefficients are retained in the catalog, but default work/drift scale to **30%**, with physical pollution capture separately scaled to **25%**. Recipe throughput and sample/byproduct outputs remain physical and unchanged. This creates time to build the factory while the world responds.

Habitat condition is a distinct local state, not an immediate conversion whenever a meter crosses a stage:

1. Productive clean work establishes nursery support.
2. A low-stress chunk slowly moves toward the condition its soil, biodiversity and water can sustain.
3. Stable clustered thresholds render pioneer patches, dry grass, meadow and lush ground.
4. Mod-grown forests appear later and sparingly.
5. Sustained contamination raises stress, degrades cover and withers tracked trees. After recovery, tracked dead trees can regenerate.

Ideal growth is around three hours of supported local time, with sustained heavy contamination able to reverse mature habitat over about two hours after stress builds. Mild pollution is slower. Sampling budgets and a ten-minute elapsed-credit cap prevent giant unobserved instant transformations.

Three bounded optimization technologies offer total +15%, +30%, +45% clean work/capture and supported growth. That is at most about 31% less ideal growth time - not an instant terraform button or infinite research multiplier. Damage rates, recipe speeds, grace periods and victory holds are not accelerated by this research.

## Pollutants and native resistance

Nauvis pollution recruitment is explicitly suppressed with zero nest uptake and an unreachable unit pollution recruitment cost. Ordinary pollution evolution is disabled. Native proximity aggression, obstruction, retaliation and expansion are not blanket-disabled.

Restoration raids choose recently productive **clean** installations supported by real nearby nests. Smog reduces their effective pressure/size, cancels warnings and recalls tracked groups at polluted targets. Dirty installations are not selected. Gleba retains ordinary spores and its separate ecology; pollution does not calm pentapods.

This is a meaningful compromise: dirty industry can buy temporary safety, but it creates waste/debt, blocks living gains and can undo habitat that took hours to establish.

## Measurement and readiness

The global inventory is the engine's whole-surface total, including pollution-only engine chunks. Hotspot/habitat surveys cover fully generated terrain. Local overlays follow the current position. None of these pretends to measure an infinite unexplored map.

Final readiness requires every fitness axis ≥ 90, toxicity ≤ 8, total pollution ≤ 500 and no known sampled hotspot above 10. **Nauvis also requires at least 80% surveyed eligible habitat condition.** The habitat value is an ecological sample - not an exact percentage of rendered ground tiles.

After two continuously ready minutes, the player confirms Nauvis's irreversible future: friendly Bloombacks/flowering gardens or eradication. A one-time entity index catches moving natives; bounded workers and generation/spawning events enforce later policy. Other planets/player-owned organisms are protected. Multiplayer administrators decide for the shared world.

The five-world beacon network remains the separate sustained logistics victory. Later pollution can still damage a world after either native outcome.

## Visual direction

The chosen direction is **heavy industrial**: dark steel, mineral composites, rivets, hazard panels, copper systems and contained biological color. All 22 production/restoration/monitor buildings have original authored primary graphics. Working loops, 64-direction turret sets, connected wall pieces, an animated intact lander and an adult feminine expedition explorer form one coherent set.

Sprites are generated from original procedural mesh geometry with depth-aware CPU rasterization, directional lighting and antialiasing. No downloaded Wube model or building sprite is redistributed. Existing collision, ports, wires, sounds, projectiles and inventory mechanics are reused. Walls/static crates need no fictitious moving mechanism; the monitor uses an animated status indicator.

The explorer is fitted and stylish but fully covered, with armor, movement, tool, weapon and corpse variants. A startup toggle preserves vanilla/another character appearance. The engine's character/controller/inventory mechanics remain intact. Armed locomotion and exact in-client port/alignment fidelity remain graphical review tasks, not claims made from headless tests.

## Safety and performance

- Schema 3 adds habitat/research state without resetting existing ecological values or duplicating cargo.
- The lander remains unmineable and indestructible after launch/force merges.
- Terrain updates respect ore, buildings, ghosts, paving, hidden support, crop soils, lava/oil seas and Aquilo ice.
- Only trees tracked as mod-grown are withered/regenerated; untracked player trees are not claimed.
- Four chunk visits per second share the survey budget; no recurring whole-map entity scan is introduced.
- Chunk iterators/callbacks never enter storage. Persistent Lua entity/render references are guarded before use.
- All runtime dependencies resolve at control parsing; no runtime `require` or `on_load` mutation.
- GUI children remain namespaced, and permanent-choice confirmation is cleared on closing.
- Actual stable-engine checks remain mandatory before publishing. Full graphical/campaign/multiplayer balance is still alpha work.

## Industry that argues with itself (0.10)

Most overhaul mods answer "should I keep the vanilla machine?" with a flat no: the modded furnace is simply better, and the stock one becomes dead weight. Second Nature deliberately refuses that. The seventeen buildings added in 0.10 are designed so the honest answer is "it depends", and so a mature factory ends up running stock, clean and dirty machines side by side for different jobs.

Three levers make the choice real:

**Speed against emissions.** A coke blast furnace is about twice as fast per raw ore as a sealed crucible, and it is cheap to build. It also emits 18 pollution a minute against 0.2, and its recipes carry an explicit toxicity effect. The restoration model scores exactly that, so the blast furnace is genuinely the right early answer and genuinely the wrong late one. Nothing forces the switch: the pollution does.

**Throughput against logistics.** Ore concentration returns 2.8 plates per ore instead of 1.0, which is a large prize. It is deliberately gated behind three separate buildings, a water loop, a tailings byproduct and an oxygen feed, so it reads as a factory project rather than a research unlock. A player who does not want that complexity can smelt ore directly forever and never feel punished.

**Capability against cost.** The deep core drill is unambiguously more powerful than a stock drill. It is also seven tiles across, draws 3.5 MW and pollutes. The two green mining heads invert the same trade: no emissions at all, and no speed advantage whatsoever.

The pollution-control buildings follow the same principle in reverse. Direct air capture removes 520 pollution a cycle, thirteen times a scrubber, which makes "clean up after yourself" a viable late strategy. But it costs 5 MW plus a consumable catalyst chain, so out-capturing a filthy factory is measurably more expensive than not dirtying the air in the first place. Cleanup is a legitimate strategy; it is never the cheap one.

Everything here is enforced rather than asserted. `tests/test_industry.py` fails the build if a clean recipe ever becomes faster per unit than its dirty counterpart, if a green mining head out-mines a stock drill, or if a cleanup operation stops consuming real inputs.
