local E=require("shared.energy")
local A=require("shared.energy_art")
local H=require("prototypes.helpers")
local function animation(key)
  local a=table.deepcopy(assert(A[key],key));a.animation_speed=.15;a.direction_count=nil;return a
end
local function picture(key)
  local a=animation(key);a.animation_speed,a.frame_count,a.line_length,a.apply_projection=nil,nil,nil,nil;return a
end
data:extend({{type="fuel-category",name="sn-grown-fuel"}})
for index,p in ipairs(E.plants) do
  local n="sn-"..p.name;local half=p.size/2
  local entity={type=p.kind,name=n,icon=H.icon(p.name),icon_size=64,
    flags={"placeable-neutral","player-creation"},max_health=p.health,
    minable={mining_time=.6,result=n},placeable_by={item=n,count=1},
    collision_box={{-half+.18,-half+.18},{half-.18,half-.18}},selection_box={{-half,-half},{half,half}},
    tile_width=p.size,tile_height=p.size,drawing_box_vertical_extension=3,
    localised_name={"entity-name."..n},localised_description={"entity-description."..n}}
  if p.kind=="solar-panel" then
    entity.energy_source={type="electric",usage_priority="solar"}
    entity.production=p.watts.."W";entity.picture=picture(p.name.."-north")
  elseif p.kind=="burner-generator" then
    entity.max_power_output=p.watts.."W"
    entity.energy_source={type="electric",usage_priority="secondary-output",buffer_capacity=p.watts*2 .."J",output_flow_limit=p.watts.."W"}
    entity.burner={type="burner",fuel_categories={p.fuel},effectivity=p.efficiency,
      fuel_inventory_size=2,burnt_inventory_size=p.fuel=="sn-grown-fuel" and 1 or 0,
      emissions_per_minute={pollution=p.pollution}}
    if p.pollution>0 then entity.burner.smoke={{name="smoke",position={0,-.3},frequency=6,deviation={.15,.15},height=2}} end
    entity.animation={}
    for _,d in ipairs({"north","east","south","west"}) do entity.animation[d]=animation(p.name.."-"..d) end
  else
    entity.energy_source={type="electric",usage_priority="primary-output",buffer_capacity=p.watts*2 .."J",input_flow_limit="0W",output_flow_limit=p.watts.."W"}
    entity.energy_production="0W";entity.energy_usage="0W";entity.gui_mode="none"
    entity.continuous_animation=true;entity.animations={}
    for _,d in ipairs({"north","east","south","west"}) do entity.animations[d]=animation(p.name.."-"..d) end
    entity.surface_conditions={{property="pressure",min=300}}
  end
  data:extend({entity,{type="item",name=n,icon=H.icon(p.name),icon_size=64,stack_size=20,
    subgroup="sn-energy",order=string.format("a-%02d",index),place_result=n,weight=p.size*20*kg,
    localised_name=entity.localised_name,localised_description=entity.localised_description}})
end
data:extend({
 {type="item",name="sn-biopellet",icon=H.icon("biopellet"),icon_size=64,stack_size=100,subgroup="sn-energy",order="c-a",weight=2*kg,
  fuel_category="sn-grown-fuel",fuel_value="8MJ",burnt_result="sn-bio-ash",auto_recycle=false,
  localised_name={"item-name.sn-biopellet"},localised_description={"item-description.sn-biopellet"}},
 {type="item",name="sn-bio-ash",icon=H.icon("bio-ash"),icon_size=64,stack_size=100,subgroup="sn-energy",order="c-b",weight=1*kg,
  auto_recycle=false,localised_name={"item-name.sn-bio-ash"},localised_description={"item-description.sn-bio-ash"}}
})
