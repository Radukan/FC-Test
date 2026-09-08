local L=require("shared.logistics")
local H=require("prototypes.helpers")
local Art=require("prototypes.artwork")
for index,x in ipairs(L.items) do
  if x.kind~="programmable-speaker" then
    local p=H.copy(x.kind,x.base)
    p.name,p.icon,p.icon_size,p.icons="sn-"..x.name,H.icon(x.name),64,nil
    p.localised_name={"entity-name."..p.name};p.localised_description={"entity-description."..p.name}
    p.minable={mining_time=.2,result=p.name};p.placeable_by={item=p.name,count=1}
    p.next_upgrade,p.factoriopedia_simulation=nil,nil
    if x.kind=="inserter" then
      p.allow_custom_vectors=true;p.extension_speed=.18;p.rotation_speed=.075
      p.energy_per_movement="12kJ";p.energy_per_rotation="12kJ"
      p.energy_source={type="electric",usage_priority="secondary-input",drain="2kW",buffer_capacity="200kJ",input_flow_limit="200kW"}
      p.max_health=250
      p.platform_picture=Art.four_way(x.name,false)
      H.tint_sprites(p.hand_base_picture,{.75,1,.88});H.tint_sprites(p.hand_open_picture,{.75,1,.88});H.tint_sprites(p.hand_closed_picture,{.75,1,.88})
      p.hand_base_frozen,p.hand_open_frozen,p.hand_closed_frozen,p.platform_frozen=nil,nil,nil,nil
    else
      p.speed=.1875;p.max_health=350
      -- Native tread geometry retains exact lane/corner/stack alignment.
      H.tint_sprites(p.belt_animation_set,{.77,1,.92})
      if x.kind=="transport-belt" then p.related_underground_belt="sn-vital-underground-belt"
      elseif x.kind=="underground-belt" then p.max_distance=16;H.tint_sprites(p.structure,{.8,1,.9})
      elseif x.kind=="splitter" then
        p.related_transport_belt="sn-vital-belt";p.structure=Art.four_way(x.name,true);p.structure_patch=nil;p.frozen_patch=nil
      end
    end
    data:extend({p,{type="item",name=p.name,icon=H.icon(x.name),icon_size=64,subgroup="sn-logistics",order=tostring(index),stack_size=100,
      weight=x.kind=="inserter" and 20*kg or 10*kg,place_result=p.name,localised_name=p.localised_name,localised_description=p.localised_description}})
  end
end
