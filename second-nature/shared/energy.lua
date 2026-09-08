-- Nightglass power and solar rail definitions. Watts and joules are explicit.
local E={plants={},trains={},items={},recipes={},technologies={},motor_interval=6}
local Power=require("shared.power_catalog")
E.plants=Power.plants
E.fluids=Power.fluids
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
for _,r in ipairs(Power.recipes) do E.recipes[#E.recipes+1]=r end
local r,g,b,p,u,e="automation-science-pack","logistic-science-pack","chemical-science-pack","production-science-pack","utility-science-pack","sn-ecology-science-pack"
tech("practical-power","Practical field power",{"automation"},{r},20,{"micro-solar","burner-set"},"Small, contrasting power systems: clean daytime photovoltaic racks or fuel-fired startup generators.")
tech("wind-power","Atmospheric wind power",{"sn-practical-power","logistic-science-pack"},{r,g},60,{"wind-turbine"},"Harvest variable atmospheric wind. A passive alternative with no fuel consumption or direct emissions.")
tech("biomass-power","Closed-loop biomass power",{"sn-composting","sn-practical-power","sn-environmental-monitoring"},{r,g,e},80,{"biopellet","biopellet-engine","ash-recovery"},"Turn cultivated biomass into prepared fuel and recover its mineral residue in a closed-loop generator.")
tech("geothermal-power","Deep geothermal exchange",{"sn-thermal-engineering","advanced-material-processing-2"},{r,g,b,e},200,{"geothermal-bore"},"Large closed-loop wells supply steady clean power, with planet-dependent geothermal yield.")
tech("industrial-cogeneration","Industrial residue power",{"advanced-oil-processing","sn-thermal-engineering"},{r,g,b,e},150,{"cogenerator"},"A high-output, high-emission chemical-fuel generator for heavy industry. Fuel and pollution remain real costs.")
tech("river-power","Shoreline mechanics",{"sn-practical-power","logistics"},{r},35,{"river-turbine"},"A fuel-free paddle station trades fuel logistics for a maintained natural-water shoreline.")
tech("compact-steam","Compact steam engineering",{"sn-practical-power","steel-processing"},{r},40,{"steam-piston"},"Denser piston generation from real 165 C steam; boilers and water remain necessary.")
tech("producer-gas-power","Coal gasification power",{"oil-processing","sn-practical-power"},{r,g},60,{"producer-gas","producer-gas-engine"},"Gasification and pipe logistics improve fuel handling without inventing energy or removing emissions.")
tech("solar-concentration","Solar concentration",{"solar-energy","advanced-material-processing-2"},{r,g,b},160,{"solar-tower"},"Concentrated daylight generation with large capital cost and no hidden night output.")
tech("biogas-power","Anaerobic power",{"sn-biomass-power","chemical-science-pack"},{r,g,b,e},160,{"biogas","biogas-turbine"},"Cultivated gas supports a larger clean power chain at the cost of substantial feedstock throughput.")
tech("heat-recovery-power","High-pressure power conversion",{"nuclear-power","sn-thermal-engineering"},{r,g,b,e},160,{"heat-recovery-turbine"},"High-flow conversion of externally produced 500 C steam into electricity.")
tech("photonic-power","Photonic power fields",{"sn-solar-concentration","electromagnetic-plant","utility-science-pack"},{r,g,b,p,u,e},240,{"photonic-canopy"},"Dense solar canopies exchange advanced material cost for fewer generating entities and less occupied land.")
tech("planetary-thermal-power","Planetary thermal extraction",{"sn-geothermal-power","tungsten-steel","utility-science-pack"},{r,g,b,p,u,e},260,{"planetary-thermal-tap"},"Deep thermal taps increase each region's renewable budget without allowing unlimited stacked bore output.")
tech("combined-cycle-power","Catalytic combined cycles",{"sn-industrial-cogeneration","production-science-pack","utility-science-pack"},{r,g,b,p,u,e},220,{"synthetic-gas","combined-cycle"},"High-density chemical generation remains bound by fuel calorific value, processing and real pollution.")
tech("biofuel-cell-power","Solid-oxide biological cells",{"sn-biogas-power","electromagnetic-plant","utility-science-pack"},{r,g,b,p,u,e},220,{"biofuel-cell"},"Electrochemical biogas conversion raises density and efficiency without creating fuel energy.")
tech("modular-fission-power","Load-following fission",{"nuclear-power","sn-geothermal-power","utility-science-pack"},{r,g,b,p,u,e},220,{"salt-reactor"},"A load-following reactor sacrifices neighbour bonuses for compact, controllable thermal output.")
tech("plasma-conversion-power","Magnetoplasma conversion",{"fusion-reactor","sn-climate-science"},{r,g,b,p,u,"cryogenic-science-pack",e},300,{"plasma-generator"},"High-throughput conversion of real fusion plasma. Fuel, startup power, coolant and heat rejection remain part of the fusion system.")
tech("solar-railway","Solar railway",{"railway","solar-energy","electric-energy-accumulators","sn-practical-power"},{r,g},80,{"sunseed-locomotive"},"Power a slow locomotive exclusively from installed roof panels and its onboard battery. Night operation is deliberately derated.")
tech("solar-railway-2","Solar freight engineering",{"sn-solar-railway","sn-thermal-engineering"},{r,g,b,e},150,{"heliograph-locomotive"},"Improve photovoltaic collection, battery capacity and traction while retaining solar-only power and lower night speeds.")
tech("solar-railway-3","Advanced solar traction",{"sn-solar-railway-2","production-science-pack","utility-science-pack"},{r,g,b,p,u,e},200,{"daybreak-locomotive"},"Dense solar arrays and a larger onboard store support faster clean rail, but not the speed of a conventional locomotive.")
E.by_plant={};E.by_train={}
for _,p in ipairs(E.plants) do E.by_plant["sn-"..p.name]=p end
for _,t in ipairs(E.trains) do E.by_train["sn-"..t.name]=t end
return E
