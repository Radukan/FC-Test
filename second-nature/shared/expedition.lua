-- Stable expedition equipment. Actual combat uses native ammo/energy/armor mechanics.
local X = {items = {}, recipes = {}, technologies = {}}
local function item(kind,name,title,base,description)
  X.items[#X.items+1] = {kind=kind,name=name,title=title,base=base,description=description}
end
item("item","alloy-stock","Mineral-composite stock",nil,"An iron-reinforced mineral composite used for structural frames, storage casings and firearm stocks.")
item("gun","carbine","Expedition carbine","submachine-gun","A compact automatic carbine chambered for standard ballistic magazines.")
item("ammo","ballistic-magazine","Expedition magazine","firearm-magazine","Ten copper-jacketed cartridges for automatic weapons and sentry turrets.")
item("capsule","field-dressing","Sterile field dressing","raw-fish","A sterile biofilm dressing that accelerates wound closure and restores health.")
item("armor","field-armor","Expedition field armor","light-armor","A fitted expedition suit with reinforced impact panels and chemical-resistant outer layers.")
item("ammo-turret","sentry-turret","Riveted sentry turret","gun-turret","A belt-fed automatic sentry mounted in a reinforced, rotating armored housing.")
item("wall","field-barricade","Riveted field barricade","stone-wall","A riveted, stone-filled barrier that absorbs impacts and resists corrosive attack.")
item("gun","induction-rifle","Induction rifle","submachine-gun","A battery-fed precision rifle that discharges concentrated electrical energy into its target.")
item("ammo","induction-cell","Induction cell","firearm-magazine","A sealed power cell providing ten electrical discharges for an induction rifle.")
item("electric-turret","arc-turret","Capacitor arc turret","laser-turret","A capacitor-fed electrical turret with a high-capacity buffer and a sustained demand for power.")
item("wall","composite-wall","Composite bastion wall","stone-wall","A layered steel and biological-composite barrier with strong impact and acid resistance.")
item("armor","expedition-armor","Powered expedition armor","modular-armor","Powered modular armor with a six-by-six equipment grid and expanded carrying capacity.")
item("gun","lance-rifle","Heavy lance rifle","railgun","A magnetic accelerator that drives dense projectiles through armored targets along a straight firing line.")
item("ammo","lance-cell","Dense-core lance round","railgun-ammo","A dense-core rail projectile capable of penetrating multiple targets along its firing line.")
item("ammo-turret","lance-turret","Bastion lance turret","railgun-turret","A reinforced magnetic accelerator for long-range defense against heavily armored targets. Requires charged power reserves and rail ammunition.")
item("armor","bastion-armor","Bastion expedition armor","power-armor-mk2","Heavy powered armor with a ten-by-ten equipment grid, reinforced plating and expanded carrying capacity.")
item("energy-shield-equipment","ecoshield-equipment","Biosphere shield module","energy-shield-mk2-equipment","A powered field generator that absorbs incoming damage and recharges from the equipment grid.")
local function recipe(name,title,seconds,ingredients,amount,enabled)
  X.recipes[#X.recipes+1]={name=name,title=title,category="crafting",seconds=seconds,ingredients=ingredients,
    results={{"sn-"..name,amount or 1}},enabled=enabled or false,defense=true,icon=name}
end
recipe("alloy-stock","Form mineral-composite stocks",1,{{"iron-plate",2},{"stone",2}},2,true)
recipe("ballistic-magazine","Assemble expedition magazines",2,{{"iron-plate",4},{"copper-plate",1}},1,true)
recipe("field-dressing","Prepare sterile field dressings",3,{{"sn-biofilm",2},{"sn-glass",1}},2)
recipe("carbine","Build an expedition carbine",6,{{"iron-plate",12},{"iron-gear-wheel",8},{"sn-alloy-stock",4},{"copper-plate",5}})
recipe("field-armor","Build an expedition field suit",8,{{"iron-plate",30},{"copper-plate",10},{"sn-alloy-stock",6}})
recipe("sentry-turret","Build a riveted sentry",12,{{"iron-plate",25},{"iron-gear-wheel",15},{"electronic-circuit",8},{"sn-alloy-stock",8}})
recipe("field-barricade","Pack riveted field barricades",4,{{"iron-plate",4},{"stone",10}},2,true)
recipe("induction-rifle","Build an induction rifle",15,{{"steel-plate",20},{"advanced-circuit",10},{"battery",12},{"sn-alloy-stock",8}})
recipe("induction-cell","Assemble induction cells",5,{{"battery",2},{"copper-plate",3},{"electronic-circuit",1}})
recipe("arc-turret","Build a capacitor arc turret",20,{{"steel-plate",35},{"advanced-circuit",15},{"battery",30},{"sn-ceramic-membrane",10}})
recipe("composite-wall","Build composite bastion walls",6,{{"sn-field-barricade",2},{"steel-plate",4},{"sn-biofilm",4},{"stone-brick",5}},2)
recipe("expedition-armor","Build powered expedition armor",30,{{"steel-plate",40},{"advanced-circuit",30},{"battery",30},{"sn-biofilm",20}})
recipe("lance-rifle","Build a heavy lance rifle",45,{{"railgun",1},{"tungsten-plate",30},{"supercapacitor",10},{"sn-biodiversity-matrix",5}})
recipe("lance-cell","Assemble dense-core lance rounds",10,{{"railgun-ammo",1},{"tungsten-carbide",4},{"superconductor",2}})
recipe("lance-turret","Build a bastion lance turret",60,{{"railgun-turret",1},{"tungsten-plate",60},{"supercapacitor",20},{"quantum-processor",5},{"sn-biodiversity-matrix",10}})
recipe("bastion-armor","Build bastion expedition armor",60,{{"power-armor-mk2",1},{"tungsten-plate",40},{"quantum-processor",10},{"sn-biodiversity-matrix",20}})
recipe("ecoshield-equipment","Build a biosphere shield module",30,{{"energy-shield-mk2-equipment",2},{"supercapacitor",10},{"sn-biodiversity-matrix",5}})
local function tech(name,title,prerequisites,packs,count,unlocks,description,effects)
  local ingredients={};for _,pack in ipairs(packs) do ingredients[#ingredients+1]={pack,1} end
  X.technologies[#X.technologies+1]={name=name,title=title,prerequisites=prerequisites,science=ingredients,count=count,
    unlocks=unlocks or {},description=description,seconds=30,effects=effects}
end
local r="automation-science-pack";local g="logistic-science-pack";local b="chemical-science-pack"
local e="sn-ecology-science-pack";local c="sn-climate-science-pack"
tech("expedition-defense","Frontier defense",{"military","steel-processing"},{r},80,
  {"carbine","field-armor","sentry-turret","field-dressing"},"Replace expedition losses with wood-free arms, armor and sentries. Basic magazines and barricades can already be crafted by hand.")
tech("induction-defense","Electrical defense doctrine",{"laser-turret","sn-thermal-engineering"},{r,g,b,"military-science-pack",e},250,
  {"induction-rifle","induction-cell","arc-turret","composite-wall","expedition-armor"},"Battery-fed rifles, electrical perimeter turrets and modular protection. Stronger defenses need a stronger energy economy.")
tech("bastion-defense","Bastion defense doctrine",{"railgun","sn-planetary-coordination"},{r,g,b,"military-science-pack","utility-science-pack","space-science-pack","cryogenic-science-pack",c},600,
  {"lance-rifle","lance-cell","lance-turret","bastion-armor","ecoshield-equipment"},"Late-game magnetic lances and powered protection. Expensive ammunition, charging and friendly firing lanes remain real constraints.")
for level,bonus in ipairs({15,30,45}) do
  local prerequisites=level==1 and {"sn-atmospheric-engineering"} or {"sn-restoration-efficiency-"..(level-1),level==2 and "sn-thermal-engineering" or "sn-climate-science"}
  local packs=level==1 and {r,g,e} or (level==2 and {r,g,b,e} or {r,g,b,"space-science-pack",e,c})
  tech("restoration-efficiency-"..level,"Ecological process optimization "..level,prerequisites,packs,({150,350,700})[level],{},
    "Improve your productive clean installations, pollution capture and recently supported terrain recovery. Bonuses are bounded: total +"..bonus.."%, not instant greening or faster research clocks.",
    {{type="nothing",effect_description={"sn-expedition.efficiency-effect",tostring(bonus)}}})
end
return X
