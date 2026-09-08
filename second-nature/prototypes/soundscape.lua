-- Audio pass. Runs in data-updates so every Second Nature prototype already
-- exists, including the ones built after prototypes/audio.lua in the data stage.
--
-- Two gaps are closed here:
--   1. Silent working entities. A building that moves but makes no sound reads
--      as broken; generating plants get a loop matched to their mechanism.
--   2. Silent inventory items. Stock items have move/pick/drop sounds keyed to
--      their material; ours were using the engine default for everything.
local Audio = require("shared.audio_catalog")
local K = require("shared.catalog")

for name, layer in pairs(Audio.entities) do
  for _, collection in pairs(data.raw) do
    local p = collection[name]
    if p and p.type and not p.working_sound then p.working_sound = Audio.working_sound(layer) end
  end
end

-- Material families for inventory handling sounds. Every referenced file is a
-- stock base-game asset; nothing is copied into this mod.
local function inventory(key, volume)
  local function sound(suffix, gain)
    return {filename = "__base__/sound/item/" .. key .. "-inventory-" .. suffix .. ".ogg",
      volume = gain, aggregation = {max_count = 1, remove = true}}
  end
  return {move = sound("move", volume), pick = sound("pickup", volume)}
end
local families = {
  -- Catalog material families.
  mineral = inventory("resource", .8), carbon = inventory("resource", .7),
  crystal = inventory("science", .6), culture = inventory("science", .6),
  data = inventory("science", .6), leaf = inventory("wood", .7),
  soil = inventory("brick", .5), seed = inventory("wood", .7),
  filter = inventory("mechanical", .7), thermal = inventory("steam", .6),
  waste = inventory("metal-barrel", .5), science = inventory("science", .6),
  -- Placeable and carried equipment, keyed by prototype kind.
  machine = inventory("metal-large", .7), fluid = inventory("metal-barrel", .5),
  ["solar-panel"] = inventory("electric-large", .7),
  ["electric-energy-interface"] = inventory("electric-large", .7),
  ["burner-generator"] = inventory("metal-large", .7),
  generator = inventory("metal-large", .7), reactor = inventory("nuclear", .6),
  ["fusion-generator"] = inventory("electric-large", .7),
  locomotive = inventory("metal-large", .7), inserter = inventory("inserter", .8),
  ["transport-belt"] = inventory("metal-small", .8),
  ["underground-belt"] = inventory("metal-small", .8),
  splitter = inventory("metal-small", .8), wall = inventory("brick", .5),
  gun = inventory("weapon-large", .7), ammo = inventory("ammo-small", .8),
  armor = inventory("armor-large", .7), capsule = inventory("resource", .6),
  ["ammo-turret"] = inventory("metal-large", .7),
  ["electric-turret"] = inventory("electric-large", .7),
  ["energy-shield-equipment"] = inventory("electric-small", .8),
  ["programmable-speaker"] = inventory("electric-small", .8),
  ["electric-small"] = inventory("electric-small", .8),
  item = inventory("mechanical", .7)
}

local function apply(name, family)
  local set = families[family]
  if not set then return end
  for kind in pairs(defines.prototypes.item) do
    local p = data.raw[kind] and data.raw[kind][name]
    if p and not p.inventory_move_sound then
      p.inventory_move_sound = table.deepcopy(set.move)
      p.pick_sound = table.deepcopy(set.pick)
      p.drop_sound = table.deepcopy(set.move)
    end
  end
end

for _, x in ipairs(K.items) do apply("sn-" .. x.name, x.family) end
for _, x in ipairs(K.machines) do apply("sn-" .. x.name, "machine") end
for _, x in ipairs(K.fluids) do apply("sn-" .. x.name .. "-barrel", "fluid") end
-- Expedition, logistics, drone, power and rail items all declare their kind.
for _, x in ipairs(K.expedition) do apply("sn-" .. x.name, x.kind) end
-- Locked rail equipment is never in an inventory, but the placeable items are.
for tier = 1, 3 do
  apply("sn-solar-rail-panel-" .. tier, "solar-panel")
  apply("sn-solar-rail-battery-" .. tier, "electric-small")
end
