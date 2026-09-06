# Development and testing

## Layout

```text
second-nature/             Installable mod source; info.json targets stable 2.0
  shared/catalog.lua       Content definitions, recipe effects and technology progression
  shared/constants.lua     Profiles, thresholds, safe tiles and work budgets
  shared/model.lua         Pure-Lua deterministic ecology
  prototypes/              Items, entities, recipes, technology, signals and GUI styles
  scripts/                 State, machine accounting, terrain, resistance, telemetry, network, GUI
  graphics/                Original generated icons, research illustrations and garden sprite
  locale/en/               Generated English locale
  control.lua              Event registration and orchestration
  data-updates.lua          Optional vanilla progression integration
  data-final-fixes.lua      Reference validation
  settings.lua             Startup/runtime/user settings

tools/                     Art/locale/docs generation, source-data harness, simulation, packaging
  headless.py              Opt-in real engine save/benchmark smoke test
  factorio_data.py          Executes official prototype Lua without claiming to be the C++ engine

tests/                     Pure model, runtime-double, source-data and package tests
  engine/control.lua       Actual-engine test mod; never shipped in the user archive

docs/                      Design, exhaustive catalog, balance and verification ledger
artifacts/                 Generated zips/checksums; ignored by Git
.cache/                    Upstream data, engine files/saves/logs; ignored and not distributable
```

## Reproduce the full automated suite

Python **3.11+** is the reference tooling environment. The mod itself runs in Factorio's Lua; Python is not a game dependency.

```bash
python3 -m pip install -r requirements-dev.txt
mkdir -p .cache

git clone --depth 1 --branch 2.0.77 \
  https://github.com/wube/factorio-data.git .cache/factorio-data-2.0.77

git clone --depth 1 --branch 2.1.17 \
  https://github.com/wube/factorio-data.git .cache/factorio-data

python3 -m pytest -q
```

Alternative checkout locations can be supplied as `FACTORIO_DATA_20` and `FACTORIO_DATA_21`. The source-data tests **skip explicitly** when these directories are absent. CI fetches both pinned tags so it runs those tests rather than silently reporting a partial suite.

The `lupa.lua52` interpreter is intentionally used, not a permissive Lua 5.4 parser. Source-data tests execute Wube's core/base/elevated-rails/quality/Space Age stages, plus recycler on 2.1, and the real mod scripts in order. Startup integration is tested both on and off.

### What the source-data harness does not prove

- It is not the C++ prototype validator.
- Proprietary sprite metadata and some ambient/menu assets are absent from the public repository. They are represented by explicitly documented placeholders, not secretly “passed.”
- No engine power, collision, fluid, heat, crafting, spoilage, pathfinding, save serialization or UI layout simulation occurs there.
- Runtime doubles validate logic and API-shaped calls but are not proof that the real game will accept every call or behave identically.

For authoritative engine validation, use the next command and finish the manual checklist.

## Real-engine smoke test (not run in the authoring sandbox)

The official [Factorio download page](https://factorio.com/download) provides a free Linux headless build with Space Age data. Obtain the matching release locally, then run:

```bash
python3 tools/headless.py --factorio /path/to/factorio/bin/x64/factorio
```

The runner:

1. Detects 2.0/2.1 and builds the correct package metadata.
2. Creates isolated mod/config/write directories under `.cache/engine-VERSION/`.
3. Adds a separate test mod, creates all five surfaces, and instantiates all 22 entities.
4. Builds a powered scrubber with one batch, a powered idle scrubber and an unpowered supplied scrubber.
5. Creates a save and reloads it for a 2,100-tick benchmark.
6. Requires the explicit `SECOND_NATURE_ENGINE_SMOKE_OK` log marker; exit code 0 without it is **not** a pass.
7. Preserves logs without opening a server or requiring Factorio account credentials.

This checks one-batch `products_finished` semantics, no idle/unpowered crafts, tracking across a real save/reload, pollution capture and basic prototype initialization. It does **not** replace visual review, complete supply-chain testing, combat pathfinding or multiplayer testing.

The workflow **Validate Second Nature** runs Lua/data/package checks on pushes and pull requests. Its manual-dispatch **engine** option additionally downloads the official headless builds and runs this smoke test on both versions. No CI run is claimed until the workflow actually runs.

## Generate and package

```bash
python3 tools/generate_assets.py       # Original art; requires Pillow and Lupa
python3 tools/generate_locale.py       # English prototype names/descriptions + UI prose
python3 tools/generate_docs.py         # Complete catalog and actual-model reference simulation
python3 tools/simulate.py              # Raw deterministic simulation results as JSON
python3 tools/package.py               # Both archives; generated outputs are ignored
python3 tools/package.py --target 2.1  # Just the experimental package
```

Each package contains one correctly named `second-nature_0.1.0/` root, the required game files, assets, license and short player guide. No test mod, game binary, save, upstream source checkout, configuration file or repository metadata is shipped. Fixed timestamps, file ordering and JSON formatting make builds reproducible. A SHA-256 file accompanies each archive.

Do not create a single ambiguous “2.0 and 2.1” metadata file. Factorio requires a specific `factorio_version`. Source `info.json` remains 2.0; the packager emits separate 2.1 metadata.

### Distribution

Installable archives and their SHA-256 sidecars are uploaded to [GitHub Releases](https://github.com/Radukan/FC-Test/releases), rather than stored in the Git history. Version 0.1.0 uses the prerelease tags `v0.1.0-factorio-2.0` and `v0.1.0-factorio-2.1`, both targeting the same source commit. Separate releases keep the canonical `second-nature_0.1.0.zip` filename without asset-name collisions or a manual renaming step. The automatically generated GitHub source archives are not installable mod packages.

Repository visibility also applies to releases: private-repository downloads require GitHub sign-in and repository access. After publishing, re-download both uploaded ZIPs and checksum sidecars with `gh release download` and verify they match the local builds.

## Version adaptation

Current reference versions: **2.0.77 stable** and **2.1.17 experimental**.

- **Recipe categories:** 2.0 uses `category`; 2.1 uses `categories`. The mod probes the already loaded iron-plate prototype and emits the appropriate shape.
- **Science packs:** 2.0 uses `tool` durability; 2.1 uses ordinary `item` prototypes. The mod mirrors the loaded automation science pack family.
- **AI:** use `LuaEntity.commandable.parent_group` / `LuaCommandable`, not removed `unit_group` APIs.
- **Circuits:** use `LuaConstantCombinatorControlBehavior` sections with dense `LogisticFilter` arrays and explicit normal quality. No legacy `parameters` table and no non-existent filter `index` field.
- **Runtime state:** `storage`, not the old `global` table; `prototypes.entity`, not `game.entity_prototypes`.
- **Rendering:** `LuaRenderObject` references with entity/offset targets, not old numeric rendering IDs or removed `target_offset` arguments.

## Event and state architecture

Mutable state is only in `storage.second_nature`. Module upvalues contain definitions/functions. There are no `on_load` game-state mutations and no runtime filesystem/network access.

Each canonical planet surface gets one ecosystem record. The data stage enables ordinary pollution on the three stock non-polluting worlds, preserving Gleba’s spores; runtime calls also safely tolerate legacy/scenario surfaces without a pollutant. Unknown planets, duplicate named editor surfaces without an actual `LuaPlanet`, and space platforms are not treated as stock planets. No script creates an unvisited surface during ordinary gameplay.

Machines are discovered by build/revive/clone events and registered for object destruction. A single install/configuration scan handles existing saves and external script-built entities. Dense buckets provide O(1) registry removal and spread polls across 16 buckets at 15-tick intervals: roughly one poll per machine every four seconds.

`products_finished` is treated as a monotonic completed-craft counter. A registered machine starts at its current value, so cloning, rescans and save reloads cannot retroactively award old work. Counter resets establish a fresh baseline. Pre-mine, death and raised-destroy handlers flush pending completed work before entity removal; external scripts that destroy entities without raising an event can lose the final polling window. Recipe switches are conservative for positive benefits. Ambiguous dirty-retort batches still incur toxic debt to prevent recipe-switch laundering.

One-second updates handle small planetary records, native responses and network holds. Visible GUIs update every two seconds. Terrain has a **global 20-attempt/second budget**, no chunk generation and an explicit safe-tile allowlist. Forest growth is even sparser. Standard ecological updates never iterate every generated chunk.

Force merges combine contribution history and reset incomplete network holds. Surface deletion/clearing releases trackers and resets the removed ecosystem. Configuration changes preserve completed progress and reconcile valid entities.

The schema starts at 1. Future updates must add explicit migrations rather than discard old `storage` data. A downgrade or untested major-version transition is not currently a supported migration path.

## Remote interface

Namespace: `second_nature`.

```lua
-- Primitive snapshot; mutating this table cannot change the planet.
local state = remote.call("second_nature", "get_world", "nauvis")
-- Also accepts a surface index. Returns nil for unsupported/unvisited worlds.

local profiles = remote.call("second_nature", "get_profiles")
local network = remote.call("second_nature", "get_network", game.forces.player.index)
-- network: held_ticks, won, reason; nil before first evaluation.

-- For script-created buildings only. Prefer raise_built=true at creation.
remote.call("second_nature", "register_entity", entity)
```

There is intentionally no remote “add restoration points,” mutation API or victory bypass.

## Contribution policy

Add content in the catalog, not hand-written duplicated prototype/localization tables. Keep clean and dirty tradeoffs legible. Every new recipe must have a real unlock, a capable machine, sufficient fluid ports and a reachable supply path. Every passive or effectful mechanic needs a test proving what happens when production stops. Never expand terrain changes by replacing the allowlist with a broad “not water” predicate.

## References

- [Official API, 2.0.77](https://lua-api.factorio.com/2.0.77/)
- [Official API, 2.1.17](https://lua-api.factorio.com/2.1.17/)
- [Official prototype source](https://github.com/wube/factorio-data)
- [Mod structure and metadata](https://lua-api.factorio.com/latest/auxiliary/mod-structure.html)

The upstream game data is consulted for compatibility, not copied into the mod or relicensed.
