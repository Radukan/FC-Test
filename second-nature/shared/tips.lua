-- In-game field guide entries for the native tips-and-tricks window.
--
-- Every entry is declared once here: the prototype builder, the locale generator
-- and the documentation generator all read this list. Triggers are what makes a
-- tip OFFER itself; skip triggers suppress a tip the player has clearly already
-- understood. No entry replaces or hides a stock Factorio tip.
local T = {category = "sn-restoration", category_order = "l-[second-nature]", items = {}}

local function tip(name, options)
  options.name = name
  options.order = string.format("%02d", #T.items + 1)
  T.items[#T.items + 1] = options
end

tip("restoration-briefing", {
  is_title = true,
  tag = "[item=sn-ecology-science-pack]",
  trigger = {type = "time-elapsed", ticks = 60 * 60},
  title = "Second Nature: restoring a planet",
  text = "This world is not a resource to spend. It is the project.\n\n" ..
    "Five fitness axes describe every planet: atmosphere, thermal balance, water cycle, living soil and biodiversity. " ..
    "Restoration machines raise them only on completed recipe cycles, and only when their local air is clean. " ..
    "Toxicity works against all of it.\n\n" ..
    "Press SHIFT + T for the field station. It shows the current stage, every support ceiling and the exact requirements for the next stage."
})

tip("silica-and-glass", {
  indent = 1,
  tag = "[item=sn-glass]",
  trigger = {type = "time-elapsed", ticks = 90 * 60},
  skip_trigger = {type = "craft-item", item = "sn-glass", event_type = "crafting-finished", count = 20},
  title = "Start with stone, not wood",
  text = "Crush stone into silica by hand, then smelt silica into laboratory glass.\n\n" ..
    "With overhaul progression enabled, every automation science pack also needs one glass, and iron sticks are available immediately so power poles never depend on wood. " ..
    "The whole restoration chain is designed to bootstrap on a treeless planet."
})

tip("first-operation", {
  indent = 1,
  tag = "[item=sn-soil-enricher]",
  trigger = {type = "research", technology = "sn-environmental-monitoring"},
  skip_trigger = {type = "build-entity", entity = "sn-soil-enricher", count = 2},
  title = "Your first restoration cycle",
  text = "A soil restoration station consumes substrate, pioneer culture and water, and returns ecological samples.\n\n" ..
    "Progress is credited per FINISHED cycle. An unpowered station, a starved station or one whose output slot is full earns nothing at all. " ..
    "Local pollution above ten also blocks soil and biodiversity gains, so scrub the air around your restoration block before scaling it up."
})

tip("close-the-loops", {
  indent = 1,
  tag = "[item=sn-filter-cartridge]",
  trigger = {type = "research", technology = "sn-closed-loops"},
  skip_trigger = {type = "build-entity", entity = "sn-reclamation-plant-plant", count = 2},
  title = "Byproducts are inventory, not scenery",
  text = "Spent cartridges, toxic effluent, hazardous sludge and depleted thermal buffers are real items. Nothing evaporates.\n\n" ..
    "Filter loop: biochar to activated carbon to cartridges to scrubbers, then reclamation back to carbon, glass and effluent.\n" ..
    "Waste loop: effluent plus neutralization charges to water and sludge, then vitrification to inert aggregate.\n" ..
    "Thermal loop: charged buffers to exchangers to depleted buffers to electrochemical recharge.\n\n" ..
    "Leave one output backed up and the machine feeding it stops crediting progress."
})

tip("air-survey", {
  indent = 1,
  tag = "[virtual-signal=sn-smog-total]",
  trigger = {type = "research", technology = "sn-atmospheric-engineering"},
  skip_trigger = {type = "build-entity", entity = "sn-air-scrubber", count = 6},
  title = "The hotspot survey is a real gate",
  text = "Stage 5 needs total planetary pollution at or below 500 AND no surveyed chunk above 10.\n\n" ..
    "The survey walks four chunks per second across all visited worlds, so a single forgotten smelter column can hold a finished planet at stage 4 indefinitely. " ..
    "Press CTRL + SHIFT + P for the local overlay: green is clean, orange is over the limit, violet is heavy enough to sedate nearby natives."
})

tip("native-resistance", {
  indent = 1,
  tag = "[item=sn-pheromone-dampener]",
  trigger = {type = "research", technology = "sn-planetary-ecology"},
  title = "Two different pressures",
  text = "Ordinary pollution still drives ordinary attacks wherever natives already live.\n\n" ..
    "Ecological CHANGE is separate. Fast biodiversity growth raises native resistance, and a scripted response wave can be dispatched against a working restoration installation on Nauvis or Gleba. " ..
    "It needs an existing nest between 96 and 512 tiles away, and it always announces itself 45 seconds in advance with a map ping.\n\n" ..
    "Clearing that perimeter is a valid answer. So is a supplied pheromone dampener. Mature, maintained worlds eventually settle down on their own."
})

tip("circuit-telemetry", {
  indent = 1,
  tag = "[item=sn-ecology-monitor]",
  trigger = {type = "build-entity", entity = "sn-ecology-monitor"},
  title = "Wire the planet into your factory",
  text = "An ecology circuit monitor emits every axis as an integer from 0 to 100, plus toxicity, resistance, stability, stage, and both total and local pollution.\n\n" ..
    "Its FIRST logistic section is reserved and overwritten each update. Put your own filters in a second section.\n\n" ..
    "Useful conditions: run detoxifiers while toxicity is above 5; hold seed supply while biodiversity is under 96; produce thermal buffers while thermal balance is under 97. Use a decider latch for separate start and stop thresholds."
})

tip("power-roster", {
  indent = 1,
  tag = "[item=sn-wind-turbine]",
  trigger = {type = "research", technology = "sn-practical-power"},
  title = "Eighteen ways to make electricity",
  text = "Six distinct generating systems exist in each of the early, mid and late stages.\n\n" ..
    "Wind needs atmospheric pressure of at least 300 and pays out with the weather. River paddles need four natural water tiles within four tiles of their center, and landfill can switch one off. " ..
    "Geothermal bores and thermal taps share a finite budget within each 32 by 32 tile region, so stacking them side by side does not multiply output.\n\n" ..
    "Everything else burns something real: fuel, fluid, supplied heat or fusion plasma."
})

tip("solar-railway", {
  indent = 1,
  tag = "[item=sn-sunseed-locomotive]",
  trigger = {type = "research", technology = "sn-solar-railway"},
  title = "Trains that run on daylight",
  text = "Solar locomotives have no fuel slots and no connection to your factory grid. Only their fitted roof panels charge the locked onboard battery.\n\n" ..
    "Stop in daylight to recharge. At night both power and speed ceiling drop, and an empty battery means coasting. " ..
    "In a mixed consist the lowest solar speed cap applies to the whole train, so keep long hauls conventional until Advanced solar traction."
})

tip("field-crew", {
  indent = 1,
  tag = "[item=sn-field-controller]",
  trigger = {type = "research", technology = "sn-field-robotics"},
  title = "Construction without a robot network",
  text = "Carry a field controller and a crew flies out of your own inventory. There is no roboport, no logistic network and no power draw.\n\n" ..
    "Materials are reserved from your inventory when a worker launches and returned in full if the job is cancelled, blocked or the worker is destroyed in flight. " ..
    "CTRL + SHIFT + B pauses the crew: workers fly home with their cargo instead of being deleted."
})

tip("living-network", {
  indent = 1,
  tag = "[item=sn-planetary-beacon]",
  trigger = {type = "research", technology = "sn-planetary-coordination"},
  title = "Finishing the network",
  text = "Victory is a maintained state, not a launch.\n\n" ..
    "Every one of the five worlds must reach stage 5, and each needs a planetary beacon that has completed a coordination cycle within the last 90 seconds. " ..
    "Hold all five at once for ten uninterrupted minutes. Any break resets the timer, and the field station's network tab always names the exact world that is holding you back.\n\n" ..
    "Aim for 95 to 100 on every axis rather than exactly 90. Environmental drift will quietly break a build that sits on the threshold."
})

return T
