-- Six meaningfully different power systems in each progression stage.
-- Existing 0.7 entity footprints are retained; large output also has real costs.
local P={plants={},fluids={},recipes={},technologies={}}
local function plant(name,title,stage,kind,size,watts,mechanism,ingredients,description,extra)
  local p={name=name,title=title,stage=stage,kind=kind,size=size,watts=watts,mechanism=mechanism,
    health=stage=="early" and 500 or (stage=="mid" and 1200 or 2200),ingredients=ingredients,description=description}
  for k,v in pairs(extra or {}) do p[k]=v end
  P.plants[#P.plants+1]=p
end
-- EARLY / red and green. A practical factory can use a few units rather than
-- hundreds of trickle generators; variable/shoreline/fuel constraints still matter.
plant("micro-solar","Copperleaf photovoltaic bank","early","solar-panel",2,120000,"photovoltaic",
 {{"iron-plate",20},{"copper-plate",25},{"sn-glass",20},{"electronic-circuit",10}},
 "A dense copper-backed photovoltaic bank. 120 kW peak with no direct emissions, but no night output. Its improved cells cost substantially more than a small starter rack.")
plant("burner-set","Trailblazer burner alternator","early","burner-generator",2,600000,"direct-combustion",
 {{"iron-plate",25},{"iron-gear-wheel",15},{"copper-cable",25},{"stone-furnace",2}},
 "Compact 600 kW chemical-fuel generation. Low conversion efficiency and substantial pollution trade fuel economy for a simple, scalable start.",
 {pollution=18,efficiency=.55,fuel="chemical"})
plant("wind-turbine","Helical wind turbine","early","electric-energy-interface",3,400000,"wind",
 {{"steel-plate",20},{"iron-gear-wheel",20},{"electronic-circuit",15},{"copper-cable",30}},
 "Up to 400 kW from atmospheric wind. Output varies with wind, pressure and weather; no fuel or direct emissions. Nearby turbines share the same weather.",{passive="wind"})
plant("river-turbine","River paddle station","early","electric-energy-interface",3,350000,"hydro",
 {{"iron-plate",40},{"iron-gear-wheel",25},{"pipe",10},{"electronic-circuit",10}},
 "A 350 kW shoreline paddle generator. Requires at least four natural water tiles within four tiles of its center; landfill can stop it. Fuel-free but geographically constrained.",{passive="hydro"})
plant("steam-piston","Twin-cylinder steam engine","early","generator",3,1800000,"low-temperature-steam",
 {{"steam-engine",2},{"steel-plate",12},{"iron-gear-wheel",15}},
 "A compact 1.8 MW twin-cylinder set using 165 C steam. It does not create heat: boiler fuel and water supply remain necessary. Direct emissions are zero; the heat source determines cleanliness.",
 {fluid="steam",temperature=165,fluid_per_tick=1,efficiency=1,pollution=0})
plant("producer-gas-engine","Producer-gas alternator","early","generator",3,1200000,"coal-gasification",
 {{"steel-plate",20},{"engine-unit",6},{"pipe",20},{"electronic-circuit",12}},
 "A 1.2 MW gas engine using coal-derived producer gas. Conversion losses, water, chemical processing and real emissions distinguish it from direct solid-fuel generation.",
 {fluid="sn-producer-gas",temperature=25,fluid_per_tick=.05,efficiency=.8,pollution=20,burns_fluid=true})
-- MID / blue and ecology. Existing hardware keeps its collision box on upgrade.
plant("biopellet-engine","Closed-loop biomass engine","mid","burner-generator",3,3000000,"solid-biomass",
 {{"steel-plate",60},{"engine-unit",20},{"advanced-circuit",20},{"sn-ceramic-membrane",25},{"sn-filter-cartridge",20}},
 "A sealed 3 MW biopellet engine. Zero direct emissions, but cultivated fuel and ash removal require a real production chain. It cannot substitute coal for its prepared biological fuel.",
 {pollution=0,efficiency=.9,fuel="sn-grown-fuel"})
plant("geothermal-bore","Deep-loop geothermal plant","mid","electric-energy-interface",5,8000000,"geothermal",
 {{"steel-plate",180},{"pumpjack",12},{"advanced-circuit",80},{"pipe",120},{"sn-thermal-buffer",40},{"sn-ceramic-membrane",40}},
 "A deep thermal wellfield rated up to 8 MW. Planetary yield varies. Bores in the same 32 x 32 tile region share that region's thermal budget, so stacking them does not multiply free output.",
 {passive="geothermal",region_size=32})
plant("cogenerator","Residue-fired cogenerator","mid","burner-generator",4,12000000,"industrial-solid-fuel",
 {{"steel-plate",150},{"engine-unit",50},{"advanced-circuit",60},{"sn-thermal-buffer",25},{"pipe",60}},
 "A 12 MW chemical-fuel industrial generator. High throughput is paid for with continuous bulk fuel and 80 pollution per minute at full activity. Existing compact footprints remain unchanged.",
 {pollution=80,efficiency=.72,fuel="chemical"})
plant("solar-tower","Heliostat power tower","mid","solar-panel",7,1800000,"concentrated-solar",
 {{"sn-micro-solar",20},{"steel-plate",100},{"advanced-circuit",40},{"sn-glass",120},{"sn-thermal-buffer",20}},
 "A 1.8 MW daylight receiver surrounded by heliostats. High capital cost buys denser solar output; storage or other generation is still required at night.")
plant("biogas-turbine","Anaerobic biogas turbine","mid","generator",5,6000000,"anaerobic-gas",
 {{"steel-plate",80},{"engine-unit",25},{"advanced-circuit",30},{"pipe",60},{"sn-biofilm",30}},
 "A 6 MW turbine burning gas from cultivated biomass and compost. Zero direct emissions, with substantial biological feedstock, processing and pipe throughput requirements.",
 {fluid="sn-biogas",temperature=25,fluid_per_tick=.45,efficiency=.9,pollution=0,burns_fluid=true})
plant("heat-recovery-turbine","High-pressure recovery turbine","mid","generator",5,18000000,"high-temperature-steam",
 {{"steam-turbine",3},{"steel-plate",60},{"advanced-circuit",20},{"sn-ceramic-membrane",25}},
 "An 18 MW generator using 500 C steam. Heat must come from real boilers/reactors; no heat or steam is created by the turbine. High output means high steam flow.",
 {fluid="steam",temperature=500,fluid_per_tick=3.10,efficiency=1,pollution=0})
-- LATE / production, utility and Space Age specialties.
plant("photonic-canopy","Photonic solar canopy","late","solar-panel",9,12000000,"photonic-solar",
 {{"solar-panel",200},{"low-density-structure",120},{"processing-unit",80},{"superconductor",40},{"sn-glass",200}},
 "A 12 MW high-density photovoltaic canopy. Expensive panels and interplanetary conductors replace large fields of small solar units. Output remains daylight-only.")
plant("planetary-thermal-tap","Planetary thermal tap","late","electric-energy-interface",9,30000000,"deep-crust-thermal",
 {{"sn-geothermal-bore",2},{"tungsten-plate",150},{"processing-unit",80},{"sn-thermal-buffer",80},{"sn-ceramic-membrane",80}},
 "A 30 MW deep-crust thermal installation. Planet-dependent, always available, but taps share a 32 x 32 region's finite output rather than multiplying power when stacked.",
 {passive="geothermal",region_size=32})
plant("combined-cycle","Catalytic combined-cycle plant","late","generator",7,60000000,"synthetic-gas-combined-cycle",
 {{"sn-producer-gas-engine",4},{"steel-plate",250},{"processing-unit",80},{"engine-unit",80},{"pipe",150},{"sn-ceramic-membrane",60}},
 "A 60 MW synthetic-gas plant. Better conversion efficiency and lower emissions per megawatt still require a large chemical-fuel supply. Fuel remains a substantial operating cost.",
 {fluid="sn-synthetic-gas",temperature=25,fluid_per_tick=.60,efficiency=.85,pollution=65,burns_fluid=true})
plant("biofuel-cell","Solid-oxide biogas cellbank","late","generator",6,24000000,"electrochemical-biomass",
 {{"sn-biogas-turbine",2},{"processing-unit",60},{"superconductor",30},{"sn-ceramic-membrane",120},{"sn-biofilm",60}},
 "A 24 MW electrochemical cellbank using clean biogas. No direct pollution, but the biological gas supply and high-grade membranes are real costs. Higher efficiency does not create extra fuel energy.",
 {fluid="sn-biogas",temperature=25,fluid_per_tick=1.6,efficiency=1,pollution=0,burns_fluid=true})
plant("salt-reactor","Lead-cooled modular reactor","late","reactor",5,80000000,"fission-heat",
 {{"nuclear-reactor",2},{"heat-pipe",50},{"processing-unit",60},{"sn-thermal-buffer",50},{"sn-ceramic-membrane",60}},
 "An 80 MW thermal fission unit with load-following fuel use and no neighbour bonus. Requires uranium fuel, spent-cell handling, heat exchangers, water and turbines; its rating is heat, not free electricity.",
 {heat=true,pollution=0})
plant("plasma-generator","Magnetoplasma generator","late","fusion-generator",5,150000000,"fusion-plasma-conversion",
 {{"fusion-generator",3},{"superconductor",40},{"quantum-processor",10},{"sn-ceramic-membrane",100}},
 "A 150 MW plasma converter. It needs real fusion plasma and a clear hot-fluoroketone output. Three conventional converters and advanced materials buy density, not additional energy from the plasma.",
 {width=3,height=5,pollution=0})
P.fluids={
 {name="producer-gas",title="Producer gas",color={.56,.42,.25},fuel_value="500kJ",description="Coal-derived combustible gas. Its production loses part of the coal's energy and consumes water; used by producer-gas alternators."},
 {name="biogas",title="Refined biogas",color={.40,.64,.29},fuel_value="250kJ",description="Combustible gas from cultivated biomass and compost. Used in biological turbines and solid-oxide cellbanks."},
 {name="synthetic-gas",title="Catalytic synthesis gas",color={.32,.49,.66},fuel_value="2MJ",description="A processed chemical fuel gas made from solid fuel, oxygen and water. Its declared energy is below that of its fuel feedstock."}
}
P.recipes={
 {name="producer-gas",title="Gasify coal",category="chemistry",seconds=4,ingredients={{"coal",4},{"water",20,"fluid"}},results={{"sn-producer-gas",24,"fluid"}},icon="producer-gas",power=true,recycle=false},
 {name="biogas",title="Digest cultivated biomass",category="chemistry",seconds=8,ingredients={{"sn-algal-biomass",12},{"sn-compost",2},{"water",30,"fluid"}},results={{"sn-biogas",40,"fluid"}},icon="biogas",power=true,recycle=false},
 {name="synthetic-gas",title="Refine synthesis gas",category="chemistry",seconds=20,ingredients={{"solid-fuel",8},{"sn-oxygen",50,"fluid"},{"water",20,"fluid"}},results={{"sn-synthetic-gas",40,"fluid"}},icon="synthetic-gas",power=true,recycle=false}
}
return P
