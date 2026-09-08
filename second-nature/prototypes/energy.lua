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
  local n="sn-"..p.name;local width,height=p.width or p.size,p.height or p.size
  local entity={type=p.kind,name=n,icon=H.icon(p.name),icon_size=64,
    flags={"placeable-neutral","player-creation"},max_health=p.health,
    minable={mining_time=.6,result=n},placeable_by={item=n,count=1},
    collision_box={{-width/2+.18,-height/2+.18},{width/2-.18,height/2-.18}},
    selection_box={{-width/2,-height/2},{width/2,height/2}},
    tile_width=width,tile_height=height,drawing_box_vertical_extension=3,
    localised_name={"entity-name."..n},localised_description={"entity-description."..n}}
  if p.kind=="solar-panel" then
    entity.energy_source={type="electric",usage_priority="solar"}
    entity.production=p.watts.."W";entity.picture=picture(p.name.."-north")
  elseif p.kind=="burner-generator" then
    entity.max_power_output=p.watts.."W"
    entity.energy_source={type="electric",usage_priority="secondary-output",buffer_capacity=p.watts*2 .."J",output_flow_limit=p.watts.."W"}
    entity.burner={type="burner",fuel_categories={p.fuel},effectivity=p.efficiency,
      fuel_inventory_size=3,burnt_inventory_size=p.fuel=="sn-grown-fuel" and 1 or 0,
      emissions_per_minute={pollution=p.pollution}}
    if p.pollution>0 then entity.burner.smoke={{name="smoke",position={0,-.3},frequency=6,deviation={.15,.15},height=2}} end
    entity.animation={}
    for _,d in ipairs({"north","east","south","west"}) do entity.animation[d]=animation(p.name.."-"..d) end
  elseif p.kind=="generator" then
    entity.energy_source={type="electric",usage_priority="secondary-output",emissions_per_minute={pollution=p.pollution or 0}}
    entity.effectivity=p.efficiency;entity.fluid_usage_per_tick=p.fluid_per_tick
    entity.maximum_temperature=p.temperature;entity.max_power_output=p.watts.."W"
    entity.burns_fluid=p.burns_fluid or false;entity.scale_fluid_usage=true;entity.destroy_non_fuel_fluid=false
    entity.fluid_box={volume=400,production_type="input",filter=p.fluid,
      pipe_connections={{flow_direction="input",direction=defines.direction.north,position={0,-height/2+.5}},
                        {flow_direction="input",direction=defines.direction.south,position={0,height/2-.5}}}}
    entity.vertical_animation=animation(p.name.."-north");entity.horizontal_animation=animation(p.name.."-east")
    if (p.pollution or 0)>0 then entity.smoke={{name="smoke",position={0,-.3},frequency=4,height=2}} end
  elseif p.kind=="reactor" then
    local base=H.copy("reactor","nuclear-reactor")
    for k,v in pairs(entity) do base[k]=v end;entity=base
    entity.consumption=p.watts.."W";entity.neighbour_bonus=0;entity.scale_energy_usage=true
    entity.energy_source.emissions_per_minute={pollution=0}
    entity.picture=picture(p.name.."-north")
    entity.working_light_picture,entity.lower_layer_picture,entity.heat_lower_layer_picture=nil,nil,nil
    entity.connection_patches_connected,entity.connection_patches_disconnected=nil,nil
    entity.heat_connection_patches_connected,entity.heat_connection_patches_disconnected=nil,nil
    entity.factoriopedia_simulation=nil
  elseif p.kind=="fusion-generator" then
    local base=H.copy("fusion-generator","fusion-generator")
    -- Preserve the native 3 x 5 port geometry and connection categories.
    for k,v in pairs(entity) do base[k]=v end;entity=base
    entity.energy_source.output_flow_limit=p.watts.."W"
    entity.max_fluid_usage=data.raw["fusion-generator"]["fusion-generator"].max_fluid_usage*3
    entity.effectivity=1;entity.next_upgrade=nil;entity.factoriopedia_simulation=nil
    entity.graphics_set={}
    for _,d in ipairs({"north","east","south","west"}) do
      local native=data.raw["fusion-generator"]["fusion-generator"].graphics_set[d.."_graphics_set"]
      entity.graphics_set[d.."_graphics_set"]={animation=animation(p.name.."-"..d),fluid_input_graphics=table.deepcopy(native.fluid_input_graphics)}
    end
  else
    entity.energy_source={type="electric",usage_priority="primary-output",buffer_capacity=p.watts*2 .."J",input_flow_limit="0W",output_flow_limit=p.watts.."W"}
    entity.energy_production="0W";entity.energy_usage="0W";entity.gui_mode="none"
    entity.continuous_animation=true;entity.animations={}
    for _,d in ipairs({"north","east","south","west"}) do entity.animations[d]=animation(p.name.."-"..d) end
    entity.surface_conditions={{property="pressure",min=300}}
  end
  data:extend({entity,{type="item",name=n,icon=H.icon(p.name),icon_size=64,stack_size=20,
    subgroup="sn-energy",order=p.stage.."-"..string.format("%02d",index),place_result=n,weight=p.size*20*kg,
    localised_name=entity.localised_name,localised_description=entity.localised_description}})
end
data:extend({
 {type="item",name="sn-biopellet",icon=H.icon("biopellet"),icon_size=64,stack_size=100,subgroup="sn-energy",order="fuel-a",weight=2*kg,
  fuel_category="sn-grown-fuel",fuel_value="8MJ",burnt_result="sn-bio-ash",auto_recycle=false,
  localised_name={"item-name.sn-biopellet"},localised_description={"item-description.sn-biopellet"}},
 {type="item",name="sn-bio-ash",icon=H.icon("bio-ash"),icon_size=64,stack_size=100,subgroup="sn-energy",order="fuel-b",weight=1*kg,
  auto_recycle=false,localised_name={"item-name.sn-bio-ash"},localised_description={"item-description.sn-bio-ash"}}
})
