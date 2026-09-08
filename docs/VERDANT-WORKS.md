# Verdant Works design contract

## Locomotion and hands

The former rig interpolated knee positions and barely lifted the ankles. It did not preserve leg-segment lengths, so the motion read as stiff sliding rather than walking.

The new rig solves each leg as a two-bone chain. A stance foot stays at ground height and sweeps backward relative to the advancing root. A shorter swing phase lifts the foot, bends the knee and brings it forward. Toe roll and root-height/lateral motion support contact and weight transfer. Stride axes remain independent of the gun-facing rig.

Hands are explicit palm, cuff, four three-segment fingers and a two-segment thumb. Light glove panels improve readability against dark sleeves and weapons. Elbows are also solved as constant-length chains; neither the hand nor the weapon is independently detached from the aiming rig.

The running cycle has sixteen frames. The tool has twenty frames at 0.26 animation speed, a roughly 28% shorter visual cycle than the prior 16/0.15 combination. The game's actual mining speed remains unchanged. Mining uses a larger pose-specific crop; its compensated Lua shift preserves the same ground/foot pivot.

The kinematic tests measure limb lengths, knee-flexion range, foot clearance, planted-height intervals, stance velocity, finger/thumb joints, aim vectors and frame bounds. These are authoring invariants, not an assertion of a complete graphical-client playthrough.

## Distinct industrial-solarpunk plants

Each production family has a different process silhouette. Biological plants use terraced beds, circulation vessels, greenhouse ribs, small solar shades and contained vegetation. Heavy chemistry retains pipes, accessible valves, gratings, radiators, inspection panels and weathered metal. Dirty processing keeps a darker, more enclosed exhaust architecture.

Complex plants require five-by-five or seven-by-seven footprints. Simple single-function stations remain three-by-three. The footprint, placement entity, art key and native port coordinates are declared in shared layout tables; they must agree in all orientations.

The larger footprint does not silently change production speeds, recipes, energy use or ecological rates. It changes the spatial planning requirement and makes room for the internal process equipment shown by the art.

## Existing-save protection

Expanding a placed entity's collision box on load would overlap adjacent machines and pipes. Instead, compact entity IDs remain available with their old geometry, fixed recipes, ports and item recovery. The existing inventory item places the expanded canonical entity for future construction.

Runtime registration and one-time reindexing recognize both IDs. Both compact and expanded beacons participate in the same force-local network. Old compact blueprints remain valid; no automatic entity replacement or movement occurs. Expanded plants use their own fast-replace group to avoid silently swapping into an occupied compact footprint.

The old variants are hidden from the normal catalog and labeled compact when inspected. Item icons and current construction previews represent the new larger installations.

## Validation priorities

- Native placement dimensions, collisions and every fluid connection of representative 5 x 5 and 7 x 7 plants.
- Compact-save and compact-blueprint compatibility without inventory duplication or forced relocation.
- Registration/accounting for both entity IDs, especially expanded planetary beacons.
- Knees visibly bending and rising in profile; stance feet remaining grounded; gloves readable in every pose.
- Faster mining without clipping the forged point or changing real mining productivity.
- Full client review of strafe/backpedal/armor/Mech transitions, GPU memory, port seams and sustained factory behavior.

The render tools and their previews are offline authoring outputs, not in-game footage.

## Completed continuation

See [CONTINUATION-AUDIT.md](CONTINUATION-AUDIT.md). The recovered rig and process architectures were already implemented; the continuation completes clipped building shadows, current preview generation and delivery documentation, and introduces the Wayfarer shuttle refit. Added canvas height is offset in the prototype shift, preserving the native ground/pipe pivot. Old compact entity geometry and all gameplay rates remain unchanged.

The lander keeps its old collision box and inventory entity. Its single static hull/shadow is combined with a tiny opaque animated-system overlay, checked against full reference frames. An art-revision migration replaces only the render object and is idempotent across configuration changes.
