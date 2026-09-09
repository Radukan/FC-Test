# The Restoration Warden

The player character was rebuilt from scratch for 0.11.0. The previous explorer
model was deleted along with its rig, its styling module and all 24 of its
atlases; nothing of it is reused.

## Why it was replaced

Two reasons, one artistic and one structural.

**Coherence.** Second Nature is a mod about working inside a poisoned
atmosphere: scrubbers, precipitation towers, direct air capture, respirator-grade
industry. The old character was an unmasked figure in a short skirt with bare
arms and legs, styled after a fashion reference that had nothing to do with the
mod's subject. It fought the fiction of every machine standing next to it.

**Cost.** That character was also the single most expensive asset in the mod:
36.5 MB of the 114 MB archive, 32% of everything shipped, for a figure that
occupies roughly 33x64 screen pixels. The expense went almost entirely into
detail the player can never see - a sculpted face with almond eyes, lips and
brows, individual hair strands, and per-limb tattoos - all of it high-frequency
colour variation, which is precisely what PNG cannot compress.

## The design

A **sealed restoration warden**. The silhouette is built from three shapes that
survive being drawn at 33 pixels wide:

| Element | Purpose |
|---|---|
| Hooded work parka | Reads as cloth, gives a soft flared outline distinct from the mod's hard-edged machinery |
| Full-face respirator | Blunt snout and cheek filters; the reason the character can stand in its own pollution |
| Emissive visor band | One broad lit strip: keeps the character legible on unlit night terrain and marks which way it faces |
| Back seed hopper | Graded stock with a germination lamp - the character carries the mod's actual goal on its back |

Nothing renders bare skin, hair or a face. This is a deliberate fiction choice
and it is enforced by a test.

### Armour tiers

Three appearances, matched to the three armour items. Each tier is a distinct
palette rather than a recoloured copy, and each adds real geometry:

| Tier | Parka | Accent | Added geometry |
|---|---|---|---|
| 0 - field gear | olive drab | oxidised copper | - |
| 1 - expedition gear | slate green | teal | right pauldron, second canister |
| 2 - bastion gear | cold blue-grey | pale cyan | both pauldrons, upper plates, hood crown, helmet lamp |

## Built for size

The model is authored against how PNG actually encodes, which the audit
measured directly on this mod's own art:

* **Ten flat tones per tier**, reused across every part. Every rendered colour is
  either a palette entry or the mesh builder's own 0.7x underside shade of one.
* **Broad uninterrupted panels** - parka front, hopper, visor - instead of
  filigree. Long runs of one colour are what row predictors compress well.
* **`surface_finish='field'`**, a rasterizer mode that keeps low-frequency
  soiling but drops the fine speckle, rust mottling and micro-normal grain used
  on machinery. That grain is invisible at character scale and expensive.
* **~5.2k faces**, down from ~10.4k.

The result renders in **33 MB against the old character's 36.5 MB before any
optimisation**, and **~21 MB after** - while every pose, direction and frame
count is unchanged.

## What did not change

The warden is a drop-in replacement for the renderer and the engine:

* the same skeleton (ground 0, hip 1.10, shoulder 1.65, head 1.95), so
  `gait.py` and `body_motion.py` are untouched;
* the same poses, frame counts and 18-row armed layout;
* the same grip contract - right hand at 48% of the pickaxe shaft, left at 16%;
* the same 1.58-tile projected height, inside the vanilla range;
* the same `PIXELS_PER_UNIT` and `scale`, so no shift or pivot moved.

Sprite keys were renamed `explorer-*` to `warden-*`; `prototypes/expedition.lua`
and the startup toggle are otherwise unchanged, and turning the setting off
still restores the vanilla character.

## Tests

| Test | Guards |
|---|---|
| `test_warden_is_fully_sealed_with_no_exposed_skin` | the fiction: no bare skin in any pose |
| `test_warden_palette_stays_small_and_flat_for_compressible_sprites` | <=10 base tones per tier, `field` finish |
| `test_warden_geometry_budget_stays_below_the_replaced_model` | <7k faces |
| `test_warden_reads_as_sealed_field_gear_with_a_lit_visor_and_seed_pack` | emissive visor, distinct tier palettes |
| `test_warden_stands_at_a_vanilla_character_height` | 1.50-1.65 tiles |

The existing locomotion, IK, grip, framing and atlas-integrity tests all still
apply unchanged.
