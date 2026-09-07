# Foundry and Field art notes

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
