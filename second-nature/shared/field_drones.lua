-- Personal construction assistants, deliberately outside LuaLogisticNetwork.
local D = {
  item = "sn-field-drone", controller = "sn-field-controller", entity = "sn-field-drone-worker",
  technology = "sn-field-robotics", range = 18, speed = .035,
  step_ticks = 3, scan_ticks = 30, work_ticks = 90, lifetime_ticks = 3600,
  default_limit = 64, maximum_limit = 128, global_limit = 512,
  scan_limit = 128, queue_limit = 256, dispatch_budget = 8, cargo_slots = 4,
  items = {}, recipes = {}, technologies = {}
}
D.items = {
  {kind="item",name="field-drone",title="Wind-up construction drone",description="A light spring-driven rotorcraft with a folding gripper and a single construction cradle. A field controller dispatches it from its operator's inventory; it has no roboport docking or logistics interface."},
  {kind="item",name="field-controller",title="Field drone controller",description="A hand-cranked spring winder and short-range construction sequencer. It directs nearby wind-up drones using supplies carried by its operator, without an armor grid or a logistics network."}
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
return D
