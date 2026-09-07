# Continuation audit / 7 September 2026

## Where the previous session actually ended

`main` still contained only the initial README. The mod and its history were on the earlier Arena branch, ending at [`eb82137`](https://github.com/Radukan/FC-Test/commit/eb8213737c055de109d0ee3a9c192fa110e4e9e9). That history was fast-forwarded into this session's `arena/01a07c4e-fc-test` branch without replacing or deleting previous work.

The latest published release was [Living World 0.5.0](https://github.com/Radukan/FC-Test/releases/tag/v0.5.0-factorio-2.0), from `0666673`. The following Verdant Works commit had already implemented most of the second request, updated the mod version to 0.6.0, and passed [source and stable-engine CI](https://github.com/Radukan/FC-Test/actions/runs/34088602288). It had **not** been published as a 0.6.0 release.

The recovered source also passed **178 tests locally**, with the pinned official 2.0.77 prototype data present. This was not an empty or failed implementation that needed to be started over.

## Requested features found in the recovered code

| Request | What was present |
|---|---|
| Arrival song and later jukebox access | Original industrial-punk/metal instrumental, archived lyrics and voice stems, a combined narration-before-song Nauvis hero track, and a craftable programmable-speaker jukebox |
| Female first-person introduction | An original anguished expedition log performed by the previously selected synthetic female voice |
| Lyrics about a green, lush home | Present as spoken vocals. The earlier speech tool could not sing; this is not a sung-metal recording or a recording of a human performer |
| Mod-specific defenses | Rootweaver emplacements/mycelial ammunition, resonance diffusers, and atmospheric pressure lances |
| Visually attached fluid inputs | Shared native port/mesh coordinates, visible necks and midpoint seams; enlarged plants have their own port table |
| Every inserter can choose endpoints | Separate pickup/drop editors and native blueprint vectors, bounded to integer offsets -2 through +2 on each axis; this inherited contract is a two-tile per-axis reach, not a literal four-cell area |
| Endgame logistics | Vector servo and canopy stack inserters; a matched 90-item/s vital belt, underground and splitter family |
| Pickaxe orientation | A tapered point oriented along the cutting tangent, with shared hand/tool anchors |
| More detailed player | Curved armor, harnesses, fitted suit, respirator pack, face, tied hair, articulated elbows and actual palm/finger/thumb geometry |
| Bending/lifting knees | Constant-length two-bone legs, planted stance, lifted swing, toe roll and weight transfer; sixteen-frame normal and armed locomotion |
| Faster mining | Twenty frames at 0.26 authored animation speed: about 1.28 seconds rather than 1.78, a roughly 28% shorter visual cycle. Gameplay mining speed remains 0.5 |
| Distinct industrial-solarpunk buildings | Twenty-two process/monitor architectures, including fermentation trains, greenhouse terraces, membranes, clarifiers, furnace drums, cyclone filters and habitat courts |
| Larger complex processes | Eleven new 5 x 5 plants and three 7 x 7 plants. Legacy compact entities, ports and blueprint placement remain available without expanding an occupied factory on load |

Presence of code, source art and engine-accepted prototypes is not the same as a complete graphical-client playthrough. In particular, audible first-arrival behavior, native movement combinations, visual pipe seams and multiplayer behavior remain client checks.

## Gaps completed in this continuation

1. **Actual clipped art, not just stale documentation.** A frame-edge audit found truncated cast shadows in several 0.6 building orientations. The 1 x 1, 3 x 3 and 5 x 5 export canvases now have sufficient vertical room. Ground-pivot compensation preserves placement and pipe alignment. Every exported working frame is bounded during generation, and pixel/geometry regression tests cover the finished sheets. The already-fitting 7 x 7 canvases remain unchanged.
2. **Current source previews.** The contact sheet and industrial GIF still showed old compact art, while the README's locomotion GIF did not exist. The review generator now resolves canonical catalog art keys, produces the missing locomotion review, updates mining timing, and generates a fingerprint ledger tying previews to their actual input sprites.
3. **Truthful handoff.** The README linked to a nonexistent 0.6.0 release, the catalog documented obsolete footprints, and the verification ledger only described 0.5. These have been corrected. The installable README links source-only documents back to the working branch rather than pretending they are inside the ZIP. The first-join version message is generated from current metadata.
4. **Wayfarer ship redesign.** The old broad, square craft is replaced with an elliptical tapered fuselage, divided sloping cockpit glass, swept shoulders, twin engine pods, cold exhaust bells, lift fans, stabilizers, exposed hydraulic landing gear, a cargo ramp, service hatches, folded photovoltaic strips and sealed seed canisters. Materials remain worn steel, sage paint, ceramic plating and copper.
5. **Correct ship compositing.** The previous renderer drew a complete animated ship over its static picture, including a second translucent ground shadow. The new moving-system overlay contains only opaque replacement pixels and is tightly cropped. All eight composite frames must match full reference renders byte for byte.
6. **Save-safe refit.** The lander's existing 9.4 x 5.6 collision box, selection box, 48 inventory slots, entity ID, world position, rocket history and protection are retained. A one-time art revision replaces only the render object. Configuration changes cannot replenish cargo, duplicate animations or recreate a removed hull. Offline and native-engine probes exercise this path.

## Delivery and limits

The follow-up delivery request publishes [0.6.0 / Verdant Works](https://github.com/Radukan/FC-Test/releases/tag/v0.6.0-factorio-2.0) in the same prerelease format as the earlier versions. Download `second-nature_0.6.0.zip`, keep it zipped, and replace older copies in the Factorio `mods` folder. The ZIP and SHA-256 sidecar are release assets, intentionally not committed to Git. `python3 tools/package.py` also builds them locally under `artifacts/factorio-2.0/`. The release publisher requires exact tagged-source validation and a successful asset re-download/checksum comparison.

See [VERIFICATION.md](VERIFICATION.md) for current test evidence and the remaining graphical-client checks. [The ship study](art/lander-review.jpg), [locomotion loop](art/locomotion-review.gif), [mining loop](art/mining-framing-preview.gif) and [building contact sheet](art/ironbound-contact-sheet.jpg) show actual exported assets, not gameplay footage.
