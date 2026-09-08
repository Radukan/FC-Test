# Field Crew / 0.8.0

## Activation: carry the kit, no armor or power

The 0.6.1 inventory-based drones and field controller are retained, as requested after the activation clarification. They are **not** replaced with native robots or a power-armor requirement.

Research **Field construction robotics** after **Automation**, for **20 red science packs**. Carry a **field controller**, **wind-up drones** and suitable building materials in the **character's main inventory**. New crews are **enabled automatically**. A one-time message and monitor explain the controls.

**Ctrl + Shift + B** pauses/resumes the crew and opens its monitor. The controller-only button is in the upper-left mod-button area, not the toolbar. It is removed when the controller leaves the character inventory. Hiding the monitor does not disable the crew. Deliberate pauses saved by 0.6.1 are retained; use the key or button to resume such a crew.

No equipment grid, armor, batteries, charging station or electric power is needed. The drones remain outside all logistic networks; the packed items cannot dock in native roboports or perform logistic deliveries.

## Native planner tools, personal inventory jobs

The native blueprint, blueprint-book, copy, cut, paste, undo, redo, import-string, deconstruction and upgrade shortcuts unlock with the early field-robotics technology. Their native hotkeys/actions are retained.

- **Construction:** entity and tile ghosts consume matching-quality items reserved from your inventory. Native ghost revival preserves blueprint settings, recipes, direction, wires and inserter vectors.
- **Deconstruction:** explicitly marked, mineable, same-force or neutral entities are mined into an escrow inventory. The actual building and its actual contents, quality and item metadata are returned to your inventory. It is not an automatic chest collection service. Full containers may take multiple sorties.
- **Upgrades:** eligible marked buildings use native in-place upgrades, preserving configuration. The new matching-quality building item is reserved and consumed, and the old item is returned. Connected underground upgrades reserve a pair and reconcile one or two actual replacements.
- Other forces' hardware, occupied/unmineable entities, the protected lander and field drones themselves are not dismantled. Build/deconstruction/upgrade permissions are checked.
- Packed vehicle construction/upgrades, perishable place-items, specialized rail upgrades, repair and item-request/module delivery remain outside this barebones system. Ordinary rail blueprint construction is supported. Later native robots still have broader capabilities.
- Loose items beneath a construction ghost are not silently deleted or collected. Clear them or explicitly mark them for deconstruction first.

Pause/resume never remotely despawns a working drone. A paused crew turns around and flies home with its real cargo; inventory items return at arrival. Turning the crew back on does not interrupt that return flight. Death/logout/force or surface transitions still reconcile immediately when a physical return is not safe or possible.

All jobs share claims across operators. Cancellation, moved/removed targets, failed operations, inventory overflow, loss of controller/range, disconnect/death and force/surface transitions reconcile the real cargo. Overflow is spilled rather than deleted. A destroyed drone is lost, but its unspent cargo is recoverable. Existing in-flight 0.6.1 construction jobs keep their escrow; no extra drones or materials are granted.

## Capacity, movement and early tuning

| Capability | Base | Tuning 1 | Tuning 2 |
|---|---:|---:|---:|
| Science | 20 red after Automation | 40 red | 60 red + green |
| Radius | 18 tiles | 22 tiles | 26 tiles |
| Flight speed | 2.1 tiles/s | 2.52 tiles/s | 3 tiles/s |
| On-site work | 1.5 s | 1.25 s | 1 s |

Tuning applies automatically to the field crew only; it does not buff native robots or military equipment. Capacity remains **64 active drones by default**, adjustable to **128 per player**, with a **512-drone server safety limit**. Packed drones stack to 200.

Positions update **every simulation tick**, rather than jumping every three ticks. The original 3D model now has a raised canopy, layered hull, visible curved body, mechanical outriggers and gripper. Sixteen directional sprite banks provide consistent 3D views and lighting. Factorio still displays pre-rendered 2D sprites, not real-time 3D geometry. Body and ground-shadow layers remain separate.

Scanning is bounded: one local sector every 30 ticks, up to 128 results for each of construction/deconstruction/upgrade searches, a 256-entry pending queue and at most eight examined/dispatch candidates per update. Idle crews avoid full per-tick scans; controller presence is cached briefly and invalidated by inventory changes.

## Explorer refinements

The protected, fully clothed chest profile uses an asymmetric loft rather than oversized spheres: less projection and upper bulk, fuller lower volume and a tapered join into the thorax. Secondary motion is reduced further. Boots have a rounded heel/toe outline, layered sole and curved toe cap rather than three box primitives.

The right palm grips at **48% of the shaft length from its lower end**, near the midpoint. The left palm supports at **16%**. Both hands stay attached through the existing weighted mining cycle, with constant arm lengths, safe framing and unchanged gameplay mining speed.

## Verification scope

Source tests cover startup/default activation, preserved pauses, planner gates, item/quality accounting, marked versus unmarked targets, deconstruction contents, upgrade refunds and configuration, underground-pair accounting, cancellation, lifecycle events, tuning, smooth movement, directional art, chest/boot geometry and grip placement.

The official stable-engine harness uses real inventories/entities/ghosts and native mining/upgrading. It exercises saved in-flight work, real construction, a marked loaded chest, a rare inserter upgrade with custom vectors and an underground pair. Its LuaPlayer-facing shell remains a fixture, not an interactive GUI playtest.

Native client appearance/hotkey interaction, all third-party mod combinations, a complete long campaign and live multiplayer/GPU/UPS profiling remain unverified. Previews are source-art studies, not gameplay recordings. See the verification ledger for executed results.
