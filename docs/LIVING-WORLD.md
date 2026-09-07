# Living World 0.5 design and test contract

## Audio and lore

The selected human-style female voice delivers the protagonist's personal log. Its anguished but determined text acknowledges the harm of prior industry and commits to a living planetary future. The same voice performs the anthem's lyrics over original synthesized distorted guitars, bass, percussion and industrial textures.

The speech synthesizer cannot sing. The delivered vocal is a spoken lyrical performance, not a sung metal vocal or a recording of a human performer. This is stated in the score manifest and release notes.

The full arrival file contains 45.76 seconds of narration, a short pause and a 160-second track. A native Nauvis hero-track definition owns the sequence rather than a simulation-tick audio splice. The entry is optional at startup. First-arrival triggering and audible mix need a graphical client; headless checks cannot establish that listening result.

The expedition jukebox is a real programmable-speaker entity with a four-note archive: silence, After the Ash, We Need a Living World and the full transmission. The custom UI uses native play-note replacement/stop behavior. Local playback is the default. Surface-wide playback requires administrator permission in multiplayer; players near a local jukebox can hear it together.

## Inserter vectors

The user-facing limit is two tiles on each axis. Both endpoint selectors use integral offsets in [-2,2], exclude the inserter's own tile and reject coincident pickup/drop tiles. Server-side handlers validate types, range, ownership and the startup setting, not merely disabled UI buttons.

The feature enables native custom vectors on all inserter prototypes. Endpoints remain native entity state, so blueprints and construction robots can retain them. The editor preserves filters, stacks, electricity and quality. Reset uses the current-direction prototype defaults, clamped to the editor's range. Other mods can still use their own scripting APIs; this editor is not a per-tick policing scan of the entire factory.

## Endgame logistics

The vector inserter improves bulk-arm movement and rotation. The canopy inserter inherits native stack placement, with the game's four-item belt-stack limit intact. Vital belts, undergrounds and splitters have matching 0.1875 tile/tick speed, a nominal 90 items/second across both lanes before stacking. Tunnels span sixteen tiles. Native belt treads/corners and inserter hand mechanics are retained/tinted for correct alignment; new platforms, manifolds and icons are original.

## Ecological defense

Mycelial flechettes add a native slowing sticker and mixed physical/poison damage while remaining in the ballistic ammunition family. Rootweaver visuals use curved seed chambers rather than ordinary gun barrels.

Resonance diffusers use a dedicated electrical beam plus a movement-disruption sticker. Pressure rounds retain rail line damage and add a bounded script trigger that removes at most four actual pollution/spore units at impact. This gives no ecological fitness, crafting cycles or science and never creates pollution for its own benefit.

Ordinary ammunition remains compatible with surviving equipment. Existing saves are not silently refilled. New expedition defenses receive mycelial magazines.

## Pipe alignment and shape

`shared/fluid_ports.lua` is the canonical native fluid-connection map. Data-stage prototypes and the art exporter both read it. Each mesh nozzle terminates at the actual connection boundary: the fluid-box tile center plus half a tile in its direction. Building ground axes are map-aligned, and the old inherited pipe-picture stubs are removed. Fluid-box counts, flow directions and recipe requirements remain intact.

The metal bodies use curved process vessels and rounded supports instead of merely beveling large square cabinets. Generic decorative side flanges that looked like nonexistent ports are removed. The art contract tests every nozzle transform under all four rotations; the engine test verifies physical connectivity independently of visual assessment.

## Pickaxe

The shaft follows an overhead-to-ground arc. The tapered forged point lies along the arc's leading tangent, points down at contact and reaches the target before the flat rear head. The hands remain on the shaft. The expanded common canvas preserves a fixed foot pivot and covers the full tool/shadow envelope across armor and facing variants.

## Remaining client checks

Verify the native first-arrival soundtrack, local/surface jukebox audibility, GUI placement, blueprint/rotation/paste behavior, real item transfer at every configured vector, all pipe seams, mining contact and live combat effects. Audio/model checks and C++ prototype validation are necessary, not a full graphical or multiplayer certification.
