# Balance and simulation contract

Canonical data: [`shared/constants.lua`](../second-nature/shared/constants.lua), [`shared/catalog.lua`](../second-nature/shared/catalog.lua). Canonical equations: [`shared/model.lua`](../second-nature/shared/model.lua).

Fitness values and toxicity/resistance are clamped to **0–100**. All changes are **percentage points**, not percentage multipliers, unless explicitly described otherwise.

## Starting state

| Planet | Atmosphere | Thermal | Water | Soil | Biodiversity | Toxicity |
|---|---:|---:|---:|---:|---:|---:|
| Nauvis | 35 | 65 | 35 | 20 | 10 | 30 |
| Vulcanus | 8 | 2 | 3 | 8 | 0 | 65 |
| Fulgora | 12 | 35 | 8 | 3 | 0 | 80 |
| Gleba | 50 | 65 | 65 | 30 | 20 | 40 |
| Aquilo | 10 | 0 | 2 | 0 | 0 | 25 |

These are ecological suitability scores, not claims about vanilla pressure or temperature. Those engine properties are never changed.

## Planetary gain multipliers

Applied to **fitness gains and losses**, not toxicity, resistance dampening or actual pollution capture.

| Planet | Atmosphere | Thermal | Water | Soil | Biodiversity |
|---|---:|---:|---:|---:|---:|
| Nauvis | 1 | 1 | 1 | 1 | 1 |
| Vulcanus | .65 | .50 | .70 | 1.30 | .70 |
| Fulgora | .85 | 1 | .65 | .80 | .80 |
| Gleba | 1.10 | 1 | 1.25 | .80 | .70 |
| Aquilo | .60 | .45 | .80 | .70 | .60 |

Example: a generic heat exchanger earns `0.24 × .45 = .108` Aquilo thermal points per 20-second cycle. A cryogenic garden earns `0.50 × .45 = .225` per 15-second cycle, and also improves water and biodiversity. The local specialty is substantially better, but the generic route remains possible.

## Hard ecological support ceilings

Let `A, T, W, S, B` be the five fitness values and `X` toxicity:

```text
atmosphere cap   = 100
thermal cap      = 100
water cap        = min(100, A + 30, T + 35)
soil cap         = min(100, W + 35, 110 - 0.4 X)
biodiversity cap = clamp(min(A + 15, T + 20, W + 20, S + 15, 100 - 0.7 X), 0, 100)
```

A positive action never reduces an existing value merely because its cap has fallen. Instead, above-cap excess decays gradually. This avoids the nasty surprise of a “restoration” cycle instantly destroying existing progress.

Adding more seed dispersers cannot solve toxic soil, an unstable atmosphere or a water deficit. Machine power and inputs are still consumed at a cap; circuits are the tool for optimizing duty cycles.

## Six stages

**Every** value in a row must meet its minimum, and toxicity its maximum. A mean can never hide an uninhabitable axis.

| Stage | Atmosphere | Thermal | Water | Soil | Biodiversity | Max toxicity |
|---|---:|---:|---:|---:|---:|---:|
| 0 · Hostile | 0 | 0 | 0 | 0 | 0 | 100 |
| 1 · Conditioned | 25 | 25 | 10 | 10 | 0 | 75 |
| 2 · Rooted | 40 | 35 | 30 | 30 | 15 | 50 |
| 3 · Recovering | 55 | 55 | 55 | 55 | 40 | 30 |
| 4 · Living | 75 | 75 | 75 | 75 | 70 | 15 |
| 5 · Self-sustaining | 90 | 90 | 90 | 90 | 90 | 8 |

The dashboard's summary is `mean(A,T,W,S,B) × (1 - .004 X)`. It is informational; it is **not** the victory check. Production surface conditions use the actual integer stage.

### Stage rewards

- **1:** local thermophile and holmium biocatalyst production.
- **2:** efficient timber cultivation, biodiversity sanctuary operation, climate-science crafting, symbiotic egg fermentation; local safe terrain recovery begins.
- **3:** biodiversity matrix assembly, efficient sheltered Gleban fruit production and sparse forest growth.
- **4:** Gaia beacon cycles, matrix propagation from biosphere samples, 75% lower baseline ecological erosion.
- **5:** eligibility for the sustained network victory.

Technology and planet requirements still apply. The stage alone does not grant recipes.

## Per-cycle examples at speed 1 on Nauvis

| Operation | Cycle | Principal gain | Important externalities |
|---|---:|---:|---|
| Atmospheric scrubbing | 10 s | +.14 atmosphere | −.045 toxicity; capture up to 40 local pollution/spores; spent filter |
| Soil restoration | 15 s | +.18 soil | +.045 biodiversity; −.06 toxicity; ecological samples |
| Pioneer reseeding | 15 s | +.18 biodiversity | Supporting atmosphere/water gain; sparse vegetation |
| Watershed restoration | 12 s | +.20 water | Ceramic demand; contaminated effluent |
| Thermal balancing | 20 s | +.24 thermal | **4 MW**; depleted buffer needing recharge |
| Mineral detoxification | 15 s | −.38 toxicity | **1.5 MW**; sludge requiring vitrification |
| Atmospheric forcing | 6 s | +.36 atmosphere | −.06 thermal, −.03 water, +.48 toxicity; +45 scripted pollution plus normal stack emissions |
| Habitat restoration | 20 s | +.42 biodiversity | Three-planet matrix imports; strong native signature |

See the [full catalog](CATALOG.md) for all costs/effects. Quality can improve the machine according to vanilla rules, and speed/efficiency modules work. Custom operations disable productivity and quality outputs; copied biochambers do not retain the native +50% productivity bonus.

Dirty retorts emit 24 pollution/spores per minute before recipe multipliers. Coal activation multiplies it by 3 and forced substrates by 4, in addition to explicit toxic debt. If a retort's recipe is switched or cleared between polls, ambiguous completed batches incur the conservative maximum native retort toxicity, not zero.

## Environmental drift

No passive drift occurs before a world's first completed ecological/dirty-impact cycle.

Base fitness erosion is modest (per game minute):

| Planet | Atmosphere | Thermal | Water | Soil | Biodiversity |
|---|---:|---:|---:|---:|---:|
| Nauvis | .018 | .006 | .012 | .009 | .018 |
| Vulcanus | .036 | .055 | .032 | .012 | .024 |
| Fulgora | .025 | .014 | .030 | .024 | .022 |
| Gleba | .020 | .006 | .009 | .024 | .035 |
| Aquilo | .025 | .065 | .040 | .012 | .030 |

At stage 4+, multiply base erosion by **.25**. Extra above-cap decay is `.015 × excess` per minute.

Ordinary pollution is enabled on Vulcanus, Fulgora and Aquilo, so native industrial emissions matter there too; Gleba keeps spores. This introduces no new enemy spawners.

Local pollution/spores is sampled at tracked production machines. Every four seconds, the current sample maximum is blended into ambient exposure with 20% new / 80% previous weighting. Circuit monitors cannot dilute the sample. This intentionally is not a second expensive whole-world pollution simulation; faraway unmonitored vanilla industry can still cause vanilla pollution attacks without directly entering this ecological sample.

```text
exposure = clamp(ambient / 150, 0, 4)
toxicity change / minute = .12 × exposure - .028 × biodiversity / 100
extra atmospheric erosion / minute = .02 × exposure
```

Unpowered/blocked machines do **not** earn restoration. Passive natural resilience may still slowly reduce toxicity; that is independent of machine work. The restoration-speed setting scales ecological effects and drift, but not actual recipe throughput, physical pollution capture, raid timers or the ten-minute goal.

## Native resistance

For each actual, uncapped positive fitness gain, add `.7 × gain`; biodiversity receives an additional `× 1.7` weighting. Per-cycle pressure effects such as dampening then apply. Resistance naturally falls `.7/minute`, or `1.25/minute` on a living/mature world. Steady upkeep at saturated meters therefore becomes calmer than a restoration boom.

| Rule | Balanced | Relentless |
|---|---:|---:|
| Trigger resistance | 30 | 20 |
| Warning | 45 s | 45 s |
| Post-dispatch cooldown | 8 min | 4 min |
| Biter count | `floor(6 + .25 pressure + 2 stage)` | `floor(6 + .4 pressure + 2 stage)` |
| Maximum biter count | 40 | 40 |
| Pentapod count | at least 3; about one-third of biter count | same scaling |
| Active scripted-group limit | 3/world | 3/world |

The grace period defaults to 20 minutes per world and is configurable. Existing nests must be 96–512 tiles from a recently working restoration target. New members spawn within 24 tiles of that nest and at least 64 from the target. Nearby unaffiliated native units are recruited first. At 150 local units, the script does not create additional units. Expired groups are unlinked, not erased along with their members.

Peaceful mode, disabling resistance, a destroyed target/nest and changed diplomacy are respected. No scripted native attacks are introduced on the three planets without a relevant biter/pentapod ecology.

## Why upkeep is not another idle timer

The last ten minutes verify a real production system. A beacon takes 60 seconds per recipe and has a 90-second freshness window, allowing logistics slack without permitting a one-time inventory dump to substitute for continued operation. Beacons need real coordination cells and water; full output inventories stop new cycles.

Each world must satisfy all thresholds **simultaneously**. Ecological fitness is shared by all forces, but research, eligible beacons and held time are force-specific.

For a mathematical scale check, see [the reference kit](SIMULATION.md). Its 18–43 model-minute convergence is **not** an estimated campaign duration. Research, supply-chain construction, planetary travel, defense and power are deliberately excluded from that test.
