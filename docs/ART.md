# Field Crew art notes

The 0.6.1 rig separates pelvis, thorax, head and weapon frames. Shoulders counter-rotate against the hips; the head bobs and stabilizes independently; the unarmed hands swing opposite the advancing leg. Mining uses an asymmetric, right-hand-leading power stroke with native contact particles on frame 11. A fully covered, fuller rounded suit profile has small armor-damped secondary motion. See [FIELD-CREW.md](FIELD-CREW.md) for the contracts and remaining native-client checks.

The drone exporter writes separate opaque body and translucent ground-shadow animations. Their composition is checked against the original render; shadows stay beneath world objects while the drone flies above them. [The field-crew overview](art/field-crew-review.jpg) and [drone loop](art/field-drone-preview.gif) show exported source art, not gameplay footage.

## Prior Verdant Works art notes

The current [contact sheet](art/ironbound-contact-sheet.jpg) uses the canonical expanded plant keys. See [the continuation audit](CONTINUATION-AUDIT.md) for the recovered 0.6 work and the finishing fixes.

## Wayfarer shuttle

`tools/lander_model.py` authors a tapered elliptical fuselage with divided cockpit glazing, twin atmospheric engine pods, lift fans, swept stabilizers, hydraulic landing gear and a cargo ramp. Worn ceramic/steel plating, sage paint, copper service lines, sealed seed canisters and folded solar cells fit the industrial-solarpunk setting. There is no rectangular building plinth or flight flame on the parked craft.

`shared/lander_layout.lua` owns the unchanged collision/selection geometry, render view and standby speed. The static sprite supplies the hull and its single cast shadow. `tools/lander_export.py` exports a narrow opaque overlay for only changing pixels, checks exact reconstruction against eight complete reference renders, and records hashes/crop coordinates in `art/lander-render.json`. Runtime art migration changes only the render object, never the cargo entity.

## Complete framing and reproducible reviews

The compact-sized 0.6 process canvases truncated some long shadows. Canonical `machine_layouts.lua` views now include extra vertical space, with compensated Lua shifts and unchanged pixel density. `sprite_bounds.py` checks all mesh/shadow vertices during export; regressions also check the alpha margin of every finished working frame. Pipe coordinates are not moved to accommodate artwork.

Run `python tools/generate_presentation_previews.py` after asset export. This uses Pillow and the Lua catalog, not the optional rasterizer. It regenerates current building/character/ship reviews and `art/review-manifest.json`, which fingerprints the inputs and outputs. Static contact cards trim transparent margins; animation review panels retain the same crop for the whole loop. Locomotion and production reviews are deliberately slowed for inspection; mining and ship reviews use their declared authoring rates. These are not claims about gameplay timing under every native modifier.

All production/defense/player meshes are authored for this project. The assets are not repainted or redistributed Factorio textures. The visual treatment uses desaturated painted steel, copper, mineral surfaces, worn seams, service fittings and directional light to sit more naturally beside industrial machinery.

## Building work

The revised models add chamfered panel edges, flanges, routed hoses, pressure dials, handwheels, fasteners, service cabinets, ribs, access hatches and grating. Working rotors, agitators, needles and indicators retain visible frame differences in all four machine directions. Turrets retain native directional firing sets.

The CPU renderer has a depth buffer, directional self-shadow map, model-space surface variation and material-dependent highlights. The compiled raster kernels are only an asset-authoring optimization. They are not part of the Factorio simulation.

## Explorer fixes

The former armed export used arbitrary full-circle row indexing and rotated the firearm independently of the hands. The revised export treats the stable 18-row set as paired gun-facing/stride-axis poses over the mirrored north/east/south half. Torso, head, arms and weapon share the aiming transform; stride remains independent.

Ground axes in the character render are already aligned to map/screen axes, so the exported animation disables a second projection correction. A fixed foot pivot is shared by every character state. The expanded canvas is checked against all model vertices and the projected shadow, including the full overhead mining arc.

The explorer remains an adult in fitted protective gear. The model adds a shaped silhouette, curved armor, harnesses, gloves/fingers, facial details and hair. Armor inventory and controller behavior are unchanged.

Authoring tests verify row structure, muzzle vectors, model bounds, frame alpha and pivot alignment. A graphical client is still needed to review every native strafe/backpedal/Mech transition and assess appearance at gameplay zoom. Headless prototype loading cannot certify that subjective result.

## Score

After the Ash is an original 96-second instrumental composition at 80 BPM. The arrangement combines a low industrial pulse, diffuse air, metallic accents and a sparse glass-like motif. Four harmonic fields move from isolated minor color toward restrained warmth.

Every sound is synthesized by the repository tool. No external recording, sample pack or melody is used. The stereo Ogg file uses 32 kHz audio with conservative levels and fades. Its setting affects only the main-menu track and respects the game's music-volume control.

The contact sheet and animation preview show rendered source assets. They are not screenshots or footage from a graphical Factorio client.
