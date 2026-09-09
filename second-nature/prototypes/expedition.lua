local X = require("shared.expedition")
local H = require("prototypes.helpers")
local Art = require("prototypes.artwork")
data:extend({{type="ammo-category",name="sn-induction"},
  {type="equipment-grid",name="sn-expedition-grid",width=6,height=6,equipment_categories={"armor"}},
  {type="equipment-grid",name="sn-bastion-grid",width=10,height=10,equipment_categories={"armor"}}})
local function damage(node, value, kind)
  if type(node)~="table" then return end
  if node.damage then node.damage.amount=value;if kind then node.damage.type=kind end end
  for key,child in pairs(node) do if key~="damage" then damage(child,value,kind) end end
end
for index,x in ipairs(X.items) do
  if x.kind~="item" then
    local p=H.copy(x.kind,x.base)
    p.name,p.icon,p.icons,p.icon_size="sn-"..x.name,H.icon(x.name),nil,64
    p.localised_name={"item-name."..p.name};p.localised_description={"item-description."..p.name}
    p.factoriopedia_simulation=nil
    if x.kind=="gun" or x.kind=="ammo" or x.kind=="armor" or x.kind=="capsule" then
      p.subgroup,p.order="sn-defense",string.format("%02d",index)
    elseif x.kind=="energy-shield-equipment" then
      p.sprite={filename=H.icon(x.name),width=64,height=64,priority="medium"}
      p.max_shield_value=250
      p.energy_source={type="electric",buffer_capacity="500kJ",input_flow_limit="600kW",usage_priority="primary-input"}
      p.energy_per_shield="24kJ"
    else
      p.localised_name={"entity-name."..p.name};p.localised_description={"entity-description."..p.name}
      p.minable={mining_time=.5,result=p.name};p.placeable_by={item=p.name,count=1}
      p.next_upgrade,p.fast_replaceable_group=nil,nil
      if x.kind=="wall" then Art.wall(p,x.name) else Art.turret(p,x.name) end
    end
    if x.name=="carbine" then
      p.attack_parameters.range=22;p.attack_parameters.cooldown=7;p.attack_parameters.damage_modifier=1.15
    elseif x.name=="ballistic-magazine" then damage(p.ammo_type,6)
    elseif x.name=="field-armor" then
      p.resistances={{type="physical",decrease=4,percent=20},{type="acid",decrease=2,percent=25},{type="explosion",percent=25}}
    elseif x.name=="sentry-turret" then
      p.max_health=800;p.attack_parameters.range=23;p.attack_parameters.cooldown=8;p.attack_parameters.damage_modifier=1.1
    elseif x.name=="field-barricade" then
      p.max_health=750;p.resistances={{type="physical",decrease=4,percent=30},{type="acid",percent=65},{type="fire",percent=100},{type="explosion",decrease=10,percent=30}}
    elseif x.name=="induction-rifle" then
      p.attack_parameters.ammo_category="sn-induction";p.attack_parameters.range=29;p.attack_parameters.cooldown=16
      p.attack_parameters.damage_modifier=1;p.attack_parameters.movement_slow_down_factor=.35
    elseif x.name=="induction-cell" then
      p.ammo_category="sn-induction";p.magazine_size=10;damage(p.ammo_type,22,"electric")
    elseif x.name=="arc-turret" then
      p.max_health=1100;p.attack_parameters.range=29;p.attack_parameters.cooldown=30;p.attack_parameters.damage_modifier=3
      p.attack_parameters.ammo_type.energy_consumption="600kJ"
      p.attack_parameters.ammo_type.action.action_delivery.max_length=29
      p.energy_source={type="electric",buffer_capacity="12MJ",input_flow_limit="4MW",drain="30kW",usage_priority="primary-input"}
    elseif x.name=="composite-wall" then
      p.max_health=1800;p.resistances={{type="physical",decrease=10,percent=45},{type="acid",percent=85},{type="fire",percent=100},{type="explosion",decrease=20,percent=55},{type="laser",percent=65}}
    elseif x.name=="expedition-armor" then
      p.equipment_grid="sn-expedition-grid";p.inventory_size_bonus=20
      p.resistances={{type="physical",decrease=8,percent=35},{type="acid",decrease=4,percent=45},{type="fire",percent=70},{type="explosion",decrease=20,percent=40}}
    elseif x.name=="lance-rifle" then
      p.attack_parameters.range=48;p.attack_parameters.cooldown=105
    elseif x.name=="lance-cell" then damage(p.ammo_type,12000)
    elseif x.name=="lance-turret" then
      p.max_health=2600;p.attack_parameters.range=48;p.attack_parameters.cooldown=150
      p.attack_parameters.turn_range=.49;p.rotation_speed=.012
    elseif x.name=="bastion-armor" then
      p.equipment_grid="sn-bastion-grid";p.inventory_size_bonus=40
      p.resistances={{type="physical",decrease=15,percent=45},{type="acid",decrease=10,percent=60},{type="fire",percent=85},{type="explosion",decrease=40,percent=65},{type="electric",percent=40}}
    end
    data:extend({p})
    if x.kind=="wall" or x.kind=="ammo-turret" or x.kind=="electric-turret" or x.kind=="energy-shield-equipment" then
      local item={type="item",name=p.name,icon=H.icon(x.name),icon_size=64,subgroup="sn-defense",order=string.format("%02d",index),
        stack_size=x.kind=="wall" and 100 or 20,weight=50*kg,localised_name=p.localised_name,localised_description=p.localised_description,auto_recycle=false}
      if x.kind=="energy-shield-equipment" then item.place_as_equipment_result=p.name else item.place_result=p.name end
      data:extend({item})
    end
  end
end

-- Every early structural wood dependency has a mineral route, even with zero cargo.
-- Keep wood-processing / composting as optional biological routes, not fake metal-to-wood recipes.
local function replace_wood(name,replacement,ratio)
  local recipe=assert(data.raw.recipe[name],name)
  for _,i in ipairs(recipe.ingredients) do if i.name=="wood" then i.name=replacement;i.amount=i.amount*(ratio or 1) end end
end
replace_wood("small-electric-pole","iron-stick",2)
data.raw.recipe["small-electric-pole"].ingredients[#data.raw.recipe["small-electric-pole"].ingredients+1]={type="item",name="stone",amount=1}
data.raw.recipe["small-electric-pole"].enabled=true
replace_wood("wooden-chest","sn-alloy-stock",1)
replace_wood("shotgun","sn-alloy-stock",1)
replace_wood("combat-shotgun","sn-alloy-stock",1)
local pole=data.raw["electric-pole"]["small-electric-pole"]
pole.pictures=Art.sprite("field-pole-sheet")
pole.pictures.direction_count=4;pole.pictures.line_length=4
pole.icon=H.icon("field-pole");pole.icons=nil;pole.icon_size=64;pole.water_reflection=nil
pole.localised_name={"entity-name.sn-field-pole"}
-- Wire attachment points must follow OUR pole art. The inherited vanilla values
-- put copper at -2.578 while this crossarm sits at -1.9405, which left every
-- wire visibly floating half a tile above its insulator.
local PoleGeometry=require("shared.pole_geometry")
pole.connection_points={}
for index,entry in ipairs(PoleGeometry["field-pole"]) do
  pole.connection_points[index]={
    wire={copper=entry.wire.copper,red=entry.wire.red,green=entry.wire.green},
    shadow={copper=entry.shadow.copper,red=entry.shadow.red,green=entry.shadow.green}}
end
local chest=data.raw.container["wooden-chest"]
chest.picture=Art.sprite("field-crate-north");chest.icon=H.icon("field-crate");chest.icon_size=64;chest.icons=nil
chest.localised_name={"entity-name.sn-field-crate"}
for _,pair in ipairs({{"small-electric-pole","field-pole"},{"wooden-chest","field-crate"}}) do
  local item=data.raw.item[pair[1]];item.icon=H.icon(pair[2]);item.icons=nil;item.icon_size=64
  item.localised_name={"entity-name.sn-"..pair[2]}
  data.raw.recipe[pair[1]].localised_name=item.localised_name
end

if settings.startup["sn-expedition-character"].value then
  local character=data.raw.character.character
  character.icon=H.icon("warden");character.icon_size=64
  character.running_sound_animation_positions={1,9}
  character.distance_per_frame=0.088205645161
  for index,variation in ipairs(character.animations) do
    local tier=math.min(index-1,2)
    for _,pose in ipairs({"idle","idle_with_gun","running","running_with_gun","mining_with_tool"}) do
      variation[pose]=Art.animation("warden-"..tier.."-"..pose,pose=="mining_with_tool" and .26 or (pose:find("running") and .6 or .15))
    end
    variation.flipped_shadow_running_with_gun=nil
    variation.mining_with_tool_particles_animation_positions={11}
    if variation.take_off or variation.landing then
      variation.take_off=Art.animation("warden-2-idle");variation.landing=Art.animation("warden-2-idle")
      variation.idle_in_air=Art.animation("warden-2-idle")
      variation.idle_with_gun_in_air=Art.animation("warden-2-idle_with_gun")
      variation.flying=Art.animation("warden-2-running")
      variation.flying_with_gun=Art.animation("warden-2-running_with_gun")
    end
  end
  H.append(character.animations[2].armors,"sn-expedition-armor")
  H.append(character.animations[3].armors,"sn-bastion-armor")
  local corpse=data.raw["character-corpse"]["character-corpse"]
  corpse.pictures={}
  for i=0,2 do
    local picture=Art.animation("warden-"..i.."-corpse");picture.direction_count=nil
    corpse.pictures[#corpse.pictures+1]=picture
  end
  corpse.water_reflection=nil
  for name,value in pairs(corpse.armor_picture_mapping) do corpse.armor_picture_mapping[name]=math.min(value,3) end
  corpse.armor_picture_mapping["sn-field-armor"]=1
  corpse.armor_picture_mapping["sn-expedition-armor"]=2
  corpse.armor_picture_mapping["sn-bastion-armor"]=3
end
