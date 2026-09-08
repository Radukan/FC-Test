-- Nightglass power and solar rail definitions. Watts and joules are explicit.
local E={plants={},trains={},items={},recipes={},technologies={},motor_interval=6}
E.plants={
 {name="micro-solar",title="Copperleaf solar rack",kind="solar-panel",size=2,watts=18000,health=250,
  description="A compact copper-backed photovoltaic rack. Passive, emission-free daytime electricity; it does not generate at night.",
  ingredients={{"iron-plate",4},{"copper-plate",6},{"sn-glass",4}}},
 {name="burner-set",title="Trailblazer burner set",kind="burner-generator",size=2,watts=180000,health=350,pollution=12,efficiency=.65,fuel="chemical",
  description="A small fuel-fired alternator for remote startup power. Burns chemical fuel, produces real pollution and stops when its fuel runs out.",
  ingredients={{"iron-plate",12},{"iron-gear-wheel",8},{"copper-cable",12},{"stone-furnace",1}}},
 {name="wind-turbine",title="Helical wind turbine",kind="electric-energy-interface",size=3,watts=120000,health=500,passive="wind",
  description="A helical atmospheric turbine. Emission-free, variable output depends on local wind and air pressure. It cannot operate in a vacuum.",
  ingredients={{"steel-plate",12},{"iron-gear-wheel",12},{"electronic-circuit",8},{"copper-cable",20}}},
 {name="biopellet-engine",title="Closed-loop biomass engine",kind="burner-generator",size=3,watts=500000,health=650,pollution=0,efficiency=.9,fuel="sn-grown-fuel",
  description="A sealed biomass engine with recirculating exhaust treatment. Burns prepared biopellets rather than coal; recover its mineral ash to keep it running. No direct pollution is emitted.",
  ingredients={{"steel-plate",25},{"engine-unit",8},{"electronic-circuit",15},{"sn-ceramic-membrane",10},{"sn-filter-cartridge",8}}},
 {name="geothermal-bore",title="Deep-loop geothermal plant",kind="electric-energy-interface",size=5,watts=1500000,health=1500,passive="geothermal",
  description="A deep closed-loop heat exchanger and turbine train. Steady, fuel-free, emission-free output varies with the planet's modeled geothermal resource; space platforms are unsupported.",
  ingredients={{"steel-plate",80},{"pumpjack",6},{"advanced-circuit",30},{"pipe",80},{"sn-thermal-buffer",20},{"sn-ceramic-membrane",25}}},
 {name="cogenerator",title="Residue-fired cogenerator",kind="burner-generator",size=4,watts=3000000,health=1200,pollution=35,efficiency=.7,fuel="chemical",
  description="A large fuel-fired industrial generator. High output from chemical fuels, with substantial real pollution and continuous fuel demand. It is a dirty alternative to the deep-loop plant.",
  ingredients={{"steel-plate",60},{"engine-unit",25},{"advanced-circuit",20},{"sn-thermal-buffer",10},{"pipe",30}}}
}
E.trains={
 {name="sunseed-locomotive",title="Sunseed solar shunter",tier=1,day_speed=.42,night_speed=.22,watts=180000,solar_watts=240000,battery_joules=24000000,night_power=.45,weight=1700,health=1000,
  description="A slow solar shunter with fixed roof panels and a 24 MJ onboard battery. No fuel slots or grid charging. Day limit about 91 km/h; night limit about 48 km/h, falling to unpowered coasting when depleted.",
  ingredients={{"locomotive",1},{"solar-panel",8},{"accumulator",6},{"electronic-circuit",20},{"sn-glass",20}}},
 {name="heliograph-locomotive",title="Heliograph solar locomotive",tier=2,day_speed=.68,night_speed=.42,watts=300000,solar_watts=420000,battery_joules=45000000,night_power=.5,weight=1900,health=1500,
  description="An improved solar freight locomotive with articulated panel shoulders and a 45 MJ battery. Solar-only traction; about 147 km/h by day and 91 km/h at night. Conventional locomotives remain faster.",
  ingredients={{"sn-sunseed-locomotive",1},{"solar-panel",12},{"accumulator",10},{"advanced-circuit",30},{"sn-thermal-buffer",10}}},
 {name="daybreak-locomotive",title="Daybreak solar express",tier=3,day_speed=.90,night_speed=.60,watts=450000,solar_watts=600000,battery_joules=72000000,night_power=.55,weight=2100,health=2200,
  description="A streamlined solar locomotive with dense roof arrays and a 72 MJ battery. About 194 km/h by day and 130 km/h at night, still below conventional train speeds. Panels are the only onboard energy source.",
  ingredients={{"sn-heliograph-locomotive",1},{"solar-panel",16},{"accumulator",16},{"processing-unit",30},{"low-density-structure",30},{"sn-biofilm",25}}}
}
local function recipe(name,title,ingredients,results,seconds)
 E.recipes[#E.recipes+1]={name=name,title=title,category="crafting",seconds=seconds or 10,ingredients=ingredients,results=results or {{"sn-"..name,1}},icon=name,power=true,recycle=false}
end
for _,p in ipairs(E.plants) do
 E.items[#E.items+1]={kind=p.kind,name=p.name,title=p.title,description=p.description}
 recipe(p.name,"Build "..p.title,p.ingredients,nil,p.size*5)
end
for _,t in ipairs(E.trains) do
 E.items[#E.items+1]={kind="locomotive",name=t.name,title=t.title,description=t.description}
 recipe(t.name,"Assemble "..t.title,t.ingredients,nil,20*t.tier)
end
E.items[#E.items+1]={kind="item",name="biopellet",title="Prepared biopellet",description="A sealed, dry biological fuel charge for closed-loop biomass engines. Eight megajoules of chemical energy; leaves recoverable mineral ash."}
E.items[#E.items+1]={kind="item",name="bio-ash",title="Biogenic mineral ash",description="Non-combustible mineral residue from a biopellet engine. Recover its nutrients rather than allowing the generator's residue inventory to fill."}
recipe("biopellet","Press a prepared biopellet",{{"sn-algal-biomass",6},{"sn-biochar",1}},nil,4)
recipe("ash-recovery","Recover ash nutrients",{{"sn-bio-ash",4},{"stone",2}},{{"sn-mineral-nutrients",1}},3)
E.recipes[#E.recipes].icon="bio-ash"
local function tech(name,title,pre,packs,count,unlocks,description)
 local science={};for _,p in ipairs(packs) do science[#science+1]={p,1} end
 E.technologies[#E.technologies+1]={name=name,title=title,prerequisites=pre,science=science,count=count,seconds=20,unlocks=unlocks,description=description}
end
local r,g,b,p,u,e="automation-science-pack","logistic-science-pack","chemical-science-pack","production-science-pack","utility-science-pack","sn-ecology-science-pack"
tech("practical-power","Practical field power",{"automation"},{r},20,{"micro-solar","burner-set"},"Small, contrasting power systems: clean daytime photovoltaic racks or fuel-fired startup generators.")
tech("wind-power","Atmospheric wind power",{"sn-practical-power","logistic-science-pack"},{r,g},60,{"wind-turbine"},"Harvest variable atmospheric wind. A passive alternative with no fuel consumption or direct emissions.")
tech("biomass-power","Closed-loop biomass power",{"sn-composting","sn-practical-power","sn-environmental-monitoring"},{r,g,e},80,{"biopellet","biopellet-engine","ash-recovery"},"Turn cultivated biomass into prepared fuel and recover its mineral residue in a closed-loop generator.")
tech("geothermal-power","Deep geothermal exchange",{"sn-thermal-engineering","production-science-pack"},{r,g,b,p,e},160,{"geothermal-bore"},"Large closed-loop wells supply steady clean power, with planet-dependent geothermal yield.")
tech("industrial-cogeneration","Industrial residue power",{"advanced-oil-processing","sn-thermal-engineering"},{r,g,b,e},150,{"cogenerator"},"A high-output, high-emission chemical-fuel generator for heavy industry. Fuel and pollution remain real costs.")
tech("solar-railway","Solar railway",{"railway","solar-energy","electric-energy-accumulators","sn-practical-power"},{r,g},80,{"sunseed-locomotive"},"Power a slow locomotive exclusively from installed roof panels and its onboard battery. Night operation is deliberately derated.")
tech("solar-railway-2","Solar freight engineering",{"sn-solar-railway","sn-thermal-engineering"},{r,g,b,e},150,{"heliograph-locomotive"},"Improve photovoltaic collection, battery capacity and traction while retaining solar-only power and lower night speeds.")
tech("solar-railway-3","Advanced solar traction",{"sn-solar-railway-2","production-science-pack","utility-science-pack"},{r,g,b,p,u,e},200,{"daybreak-locomotive"},"Dense solar arrays and a larger onboard store support faster clean rail, but not the speed of a conventional locomotive.")
E.by_plant={};E.by_train={}
for _,p in ipairs(E.plants) do E.by_plant["sn-"..p.name]=p end
for _,t in ipairs(E.trains) do E.by_train["sn-"..t.name]=t end
return E
