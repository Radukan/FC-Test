-- Milestones are declared once. Prototypes, the runtime ledger, the dashboard,
-- localization, documentation and tests all read this file.
--
-- Two kinds exist and they are NOT interchangeable:
--   * script  -- plain "achievement" prototypes. Only this type can be unlocked
--               from a script, so every mod-tracked milestone must use it.
--   * engine  -- condition prototypes the engine evaluates by itself. The mod
--               never claims to unlock these; the game does.
local A = {script = {}, engine = {}, by_name = {}}

local function milestone(name, title, description, order, trigger)
  A.script[#A.script + 1] = {name = name, title = title, description = description,
    order = "b[restoration]-" .. order .. "[" .. name .. "]", trigger = trigger, script = true}
end

-- Restoration progress. Granted to the forces that actually did the work.
milestone("first-breath", "First breath",
  "Bring a world out of hostile conditions and into a conditioned atmosphere. Stage 1 on any planet.",
  "a", "world stage 1")
milestone("root-systems", "Root systems",
  "Hold a recovering ecosystem: stage 3 on any planet, with living soil and returning biodiversity.",
  "b", "world stage 3")
milestone("a-living-world", "A living world",
  "Carry one planet all the way to a self-sustaining ecosystem. Stage 5, clean air and a matured landscape.",
  "c", "world stage 5")
milestone("new-growth", "New growth",
  "Let restored ground grow its own forest. One thousand trees established by restoration work on a single world.",
  "d", "world grown_trees >= 1000")
milestone("terraformer", "Terraformer",
  "Reclaim ten thousand tiles of dead ground on a single world. Visible terrain recovery must be enabled.",
  "e", "world restored_tiles >= 10000")
milestone("deep-green", "Deep green",
  "Capture fifty thousand units of pollution or spores on a single world using scrubbers, watersheds and detoxifiers.",
  "f", "world removed_pollution >= 50000")

-- Expedition and narrative decisions.
milestone("signal-restored", "Signal restored",
  "Launch the first rocket from the wreck camp and put the expedition back in contact with orbit.",
  "g", "campaign rocket launched")
milestone("common-ground", "Common ground",
  "Choose symbiosis on Nauvis. The native strain is rebuilt into a part of the ecosystem rather than removed from it.",
  "h", "native fate symbiosis")
milestone("quiet-eden", "Quiet eden",
  "Choose eradication on Nauvis. A restored world, and a decision that cannot be taken back.",
  "i", "native fate eradication")
milestone("hold-the-line", "Hold the line",
  "Defend a working restoration installation until an ecological-response wave is spent. The installation must survive.",
  "j", "resistance wave survived")

-- Network scale.
milestone("field-stations", "Field stations",
  "Establish field-station contact on all five restoration worlds: Nauvis, Vulcanus, Fulgora, Gleba and Aquilo.",
  "k", "all five worlds registered")
milestone("second-nature", "Second nature",
  "Hold five living worlds together for ten uninterrupted minutes and finish the planetary restoration network.",
  "l", "network victory")

local function engine(name, title, description, order, kind, fields)
  local x = {name = name, title = title, description = description, kind = kind,
    order = "c[network]-" .. order .. "[" .. name .. "]", fields = fields}
  A.engine[#A.engine + 1] = x
end

engine("first-gust", "First gust",
  "Take electricity from a helical wind turbine. Weather is a supply, not a guarantee.",
  "a", "use-entity-in-energy-production-achievement", {entity = "sn-wind-turbine"})
engine("network-nodes", "Network nodes",
  "Build five planetary beacons, one for every world in the restoration network.",
  "b", "build-entity-achievement", {to_build = "sn-planetary-beacon-plant", amount = 5})
engine("coordination-cells", "Coordination cells",
  "Produce two hundred Gaia coordination cells. A synchronized network is a supply chain, not a switch.",
  "c", "produce-achievement", {item_product = "sn-gaia-cell", amount = 200, limited_to_one_game = false})
engine("matrix-gardener", "Matrix gardener",
  "Assemble one hundred biodiversity matrices from thermophiles, symbionts and mineral catalysts.",
  "d", "produce-achievement", {item_product = "sn-biodiversity-matrix", amount = 100, limited_to_one_game = false})
engine("read-the-world", "Read the world",
  "Research anything using restoration science, the research package produced by a working living-world network.",
  "e", "research-with-science-pack-achievement", {science_pack = "sn-restoration-science-pack"})
engine("no-shortcuts", "No shortcuts",
  "Finish the game without ever building a pyrolysis retort or an atmospheric forcing tower. The clean chain only.",
  "f", "dont-build-entity-achievement",
  {dont_build = {"sn-pyrolyzer", "sn-forcing-tower"}, objective_condition = "game-finished"})
engine("nightglass-grid", "Nightglass grid",
  "Draw one hundred gigajoules within an hour without taking any power from an emitting generator.",
  "g", "dont-use-entity-in-energy-production-achievement",
  {excluded = {"sn-burner-set", "sn-cogenerator", "sn-producer-gas-engine", "sn-combined-cycle"},
   included = {"sn-micro-solar", "sn-wind-turbine", "sn-river-turbine", "sn-solar-tower",
     "sn-photonic-canopy", "sn-geothermal-bore", "sn-planetary-thermal-tap",
     "sn-biopellet-engine", "sn-biogas-turbine", "sn-biofuel-cell"},
   minimum_energy_produced = "100GJ", last_hour_only = true})

A.all = {}
for _, list in ipairs({A.script, A.engine}) do
  for _, x in ipairs(list) do
    A.all[#A.all + 1] = x
    A.by_name[x.name] = x
  end
end
return A
