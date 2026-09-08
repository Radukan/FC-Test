-- Personal construction assistants, deliberately outside LuaLogisticNetwork.
local D = {
  item = "sn-field-drone", controller = "sn-field-controller", entity = "sn-field-drone-worker",
  technology = "sn-field-robotics", range = 18, speed = .035,
  step_ticks = 1, scan_ticks = 30, work_ticks = 90, lifetime_ticks = 3600,
  default_limit = 64, maximum_limit = 128, global_limit = 512,
  scan_limit = 128, queue_limit = 256, dispatch_budget = 8, cargo_slots = 96, directions = 16,
  items = {}, recipes = {}, technologies = {},
  planner_shortcuts={"undo","redo","copy","cut","paste","import-string","give-blueprint","give-blueprint-book","give-deconstruction-planner","give-upgrade-planner"}
}
D.items = {
  {kind="item",name="field-drone",title="Wind-up construction drone",description="A spring-driven rotorcraft that builds, dismantles and upgrades nearby planner targets from its operator's inventory. Carry drones, a field controller and materials after research. New crews run automatically; The upper-left controller button or Ctrl + Shift + B pauses/resumes them; recalled workers fly back to their operator. No armor, power supply or logistics network is needed."},
  {kind="item",name="field-controller",title="Field drone controller",description="Carry this with wind-up drones and materials in the character inventory. The crew starts automatically after Field construction robotics. The controller-only button at the upper left, or Ctrl + Shift + B, opens the monitor and pauses/resumes work. No equipment grid, power or roboport connection is required."}
}
D.recipes = {
  {name="field-drone",title="Assemble a wind-up construction drone",category="crafting",seconds=2,
   ingredients={{"iron-plate",2},{"iron-gear-wheel",1},{"electronic-circuit",1},{"copper-cable",2}},
   results={{"sn-field-drone",1}},icon="field-drone",logistics=true,recycle=false},
  {name="field-controller",title="Build a field drone controller",category="crafting",seconds=5,
   ingredients={{"iron-plate",8},{"iron-gear-wheel",6},{"electronic-circuit",5},{"copper-cable",6}},
   results={{"sn-field-controller",1}},icon="field-controller",logistics=true,recycle=false}
}
D.technologies = {
  {name="field-robotics",title="Field construction robotics",prerequisites={"automation"},
   science={{"automation-science-pack",1}},count=20,seconds=15,
   unlocks={"field-drone","field-controller"},
   description="Compact spring-driven construction assistants for local blueprint work. A carried controller winds and directs a large, slow crew without batteries, an equipment grid, roboports or logistic deliveries."}
}
D.technologies[#D.technologies+1]={name="field-robotics-2",title="Field crew tuning 1",prerequisites={D.technology},
  science={{"automation-science-pack",1}},count=40,seconds=15,unlocks={},
  effects={{type="nothing",effect_description={"sn-drones.tuning-1"}}},
  description="Improve the field sequencer: 22-tile reach, 20% faster flight and shorter on-site work cycles. Native robots and other equipment are unchanged."}
D.technologies[#D.technologies+1]={name="field-robotics-3",title="Field crew tuning 2",prerequisites={"sn-field-robotics-2","logistic-science-pack"},
  science={{"automation-science-pack",1},{"logistic-science-pack",1}},count=60,seconds=15,unlocks={},
  effects={{type="nothing",effect_description={"sn-drones.tuning-2"}}},
  description="Refine the field drive and job sequencer: 26-tile reach, 3-tile-per-second flight and one-second work cycles. No logistics network or power supply is introduced."}
return D
