local L={items={},recipes={},technologies={}}
local function item(kind,name,title,base,description)
 L.items[#L.items+1]={kind=kind,name=name,title=title,base=base,description=description}
end
item('inserter','vector-inserter','Vector servo inserter','bulk-inserter','A high-speed articulated transfer arm with a reinforced servo drive and configurable pickup and delivery vectors.')
item('inserter','canopy-inserter','Canopy stack inserter','stack-inserter','A high-capacity manipulator that stacks cargo on belts and transfers dense batches through an articulated servo assembly.')
item('transport-belt','vital-belt','Vital transport belt','turbo-transport-belt','A reinforced transport line with superconducting drive control and a nominal throughput of 90 items per second before belt stacking.')
item('underground-belt','vital-underground-belt','Vital underground belt','turbo-underground-belt','A sealed high-speed transfer tunnel connecting reinforced transport lines across sixteen tiles.')
item('splitter','vital-splitter','Vital distribution manifold','turbo-splitter','A high-speed distribution assembly with lane balancing, priority routing and item filtering.')
item('programmable-speaker','jukebox','Expedition jukebox','programmable-speaker','A rugged audio archive and playback console for expedition transmissions and recorded scores.')
local function recipe(name,title,time,ingredients,count,enabled)
 L.recipes[#L.recipes+1]={name=name,title=title,category='crafting',seconds=time,ingredients=ingredients,results={{'sn-'..name,count or 1}},enabled=enabled or false,logistics=true,icon=name}
end
recipe('vector-inserter','Assemble a vector servo inserter',8,{{'bulk-inserter',1},{'processing-unit',4},{'superconductor',2},{'carbon-fiber',4}})
recipe('canopy-inserter','Assemble a canopy stack inserter',12,{{'stack-inserter',1},{'quantum-processor',1},{'superconductor',4},{'sn-biodiversity-matrix',2}})
recipe('vital-belt','Assemble vital transport sections',3,{{'turbo-transport-belt',4},{'superconductor',1},{'carbon-fiber',2},{'sn-gaia-cell',1}},4)
recipe('vital-underground-belt','Assemble a sealed transfer tunnel',8,{{'turbo-underground-belt',2},{'sn-vital-belt',8},{'tungsten-plate',10},{'sn-gaia-cell',2}},2)
recipe('vital-splitter','Assemble a distribution manifold',10,{{'turbo-splitter',1},{'processing-unit',10},{'superconductor',4},{'sn-gaia-cell',2}})
recipe('jukebox','Assemble an expedition jukebox',5,{{'electronic-circuit',5},{'iron-plate',10},{'copper-cable',10}},1,true)
L.technologies={{name='living-logistics',title='Living-world logistics',prerequisites={'sn-planetary-coordination','stack-inserter','turbo-transport-belt'},
 science={{'automation-science-pack',1},{'logistic-science-pack',1},{'chemical-science-pack',1},{'production-science-pack',1},{'utility-science-pack',1},{'space-science-pack',1},{'sn-climate-science-pack',1}},count=750,seconds=30,
 unlocks={'vector-inserter','canopy-inserter','vital-belt','vital-underground-belt','vital-splitter'},description='Superconducting transport drives and high-capacity manipulators for a sustained interplanetary economy.'}}
return L
