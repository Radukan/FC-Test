# Field Crew / 0.6.1

A small-version continuation of 0.6.0: one early construction system and a focused explorer animation revision. Existing building footprints, ecological rates, music, weapons and landing cargo are unchanged.

## Wind-up construction assistants

Research **Field construction robotics** after **Automation**: 20 automation (red) science packs, 15 seconds per unit. Craft a field controller and wind-up construction drones from iron plates, gears, electronic circuits and copper cable. No engines, batteries, lubricant, robot frames, armor grid or advanced science are required.

Carry the controller, drones and matching construction items in the **character's main inventory**. Press **Ctrl + Shift + B** or use the drone shortcut to enable/pause the crew. The small monitor shows active/packed drones, completed work and the current reason for waiting. Hiding the monitor does not pause the crew; Pause + recall does.

| Contract | Value |
|---|---|
| Operating radius | 18 tiles around the physical, controllable character |
| Flight speed | 0.035 tiles/tick, or 2.1 tiles/second before any simulation slowdown |
| Construction delay | 90 ticks, or 1.5 seconds, after reaching the ghost |
| Default concurrent crew | 64 per player |
| Per-player setting | 1 through 128 drones |
| Server safety cap | 512 active field drones |
| Packed stack size | 200 drones |
| Movement update | Every 3 ticks, separate from the bounded spatial scan |
| Search | One rotating local sector every 30 ticks; at most 128 results |
| Dispatch | At most 8 queued candidates per update; queue capped at 256 |

The carried sequencer rewinds the spring drives between sorties. There is no battery/fuel network or passive factory service. Each sortie reserves a real drone and a real construction load, flies to a ghost, constructs it, then returns the reusable drone. A large local blueprint can dispatch a full crew through the queue rather than being limited to eight drones per complete scan.

### No logistics network

These are **not construction-robot or logistic-robot prototypes**. The worker is a scripted, off-grid simple entity with its own original flight and gripper animation. It has no logistic cell, docking category, equipment grid, chest search or delivery-request behavior. Native roboport robot inventories reject the packed item. Flying near a powered roboport does not connect it to that network.

The assistants build **entity and tile ghosts only**. They do not repair, deconstruct, upgrade existing machines, insert requested modules or deliver items. Later native construction/logistics robots retain those advantages. They do not operate on space platforms, in remote/editor/cutscene control, without the controller or without the required research. Native player build permissions are respected.

### Material and save safety

- Items are removed from the character inventory into a script-owned escrow inventory before launch. There is no free building or ghost-item synthesis.
- The ghost's exact requested quality is required. Drone quality is preserved on return but does not add speed, reach or carrying capacity.
- Native `revive` preserves the ghost's own settings, direction, recipes, wires and inserter vectors. The mod does not replace it with a newly configured approximation.
- Specialized packed vehicle/inventory items are left for native construction because a plain revival cannot safely restore all their embedded state.
- Loose ground items beneath a ghost block this early crew. They are not collected, deleted or turned into an implicit logistics delivery.
- Claims are shared across operators, so two players cannot dispatch paid construction to the same ghost simultaneously.
- Cancellation, failed placement, loss of range, controller changes, disconnects, force/surface changes and pre-death recall reconcile reservations. Inventory overflow is spilled with its quality intact rather than deleted.
- A destroyed drone is actually lost. Its unspent construction material is spilled for recovery, not duplicated or silently destroyed.
- Escrow inventories and worker/render references live in `storage.second_nature.field_drones`. Configuration changes rebuild accounting without minting drones or replacing active reservations. Completed inventories and render objects are destroyed.
- Drone bodies render above objects; their shadows render separately on the ground, not over nearby roofs or the player.

## Human motion revision

`tools/body_motion.py` separates pelvis, thorax and head transforms. Hip yaw/roll and lateral weight transfer are countered by the shoulders, while the head has its own stabilization and bob. Arms solve between moving shoulders and real grip targets. The gun retains the requested native aim direction instead of swaying away from its firing line.

Foot swing velocities now meet the planted-stance velocity continuously. Boot sole clearance is kept above the ground. The existing sixteen-frame locomotion and twenty-frame mining formats, native paired armed rows and gameplay movement/mining speeds are retained.

Mining has a measured anticipation, a much faster downstroke, a brief impact/follow-through and recovery. The torso leans and drops into the strike. The **right palm is closer to the pickaxe head along the shaft** than the left palm in every frame; both remain attached to the handle. A stable perpendicular hand frame removes the old degenerate grip orientation when the shaft crossed horizontal. Native mining particles use frame 11, the contact frame of the twenty-frame cycle.

The adult explorer remains fully clothed in protective equipment. Her suit has a fuller, rounder chest profile. Small, phase-lagged secondary motion is strongest in the field suit and substantially damped by the heavier armor tiers; rigid equipment is not treated as unconstrained soft material.

## Validation scope

Offline tests cover inventory conservation, quality, simultaneous operators, large crews, cancellation, failed placement, lifecycle events, permissions, HUD behavior, motion/grip geometry, complete atlas bounds and current preview fingerprints.

The official 2.0.77 headless probe uses real characters, inventories, entity/tile ghosts, a powered nearby roboport, script escrow and rendering objects. It saves while drones are in flight, reloads, verifies real construction and exact material/quality conservation, and requires `SECOND_NATURE_ENGINE_FIELD_DRONES_OK`. Its LuaPlayer-facing shell is a fixture because headless has no interactive player GUI; per-player settings and the actual shortcut interaction are additionally covered by offline tests, not claimed as a native GUI playtest.

Graphical-client movement/appearance, every Mech/weapon combination, long-run multiplayer/desync behavior and GPU/UPS profiling still need real client playtesting. Source previews are actual exported sprites, not game footage.
