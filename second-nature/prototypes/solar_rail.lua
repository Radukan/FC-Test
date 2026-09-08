local E=require("shared.energy")
local A=require("shared.energy_art")
local H=require("prototypes.helpers")
data:extend({{type="equipment-category",name="sn-solar-rail"},{type="fuel-category",name="sn-solar-traction"},
 {type="item",name="sn-solar-drive-charge",icon=H.icon("solar-drive-charge"),icon_size=64,stack_size=1,
  hidden=true,hidden_in_factoriopedia=true,fuel_category="sn-solar-traction",fuel_value="1GJ",auto_recycle=false,
  fuel_acceleration_multiplier=1,fuel_top_speed_multiplier=1,localised_name={"sn-energy.internal-charge"}}})
for _,t in ipairs(E.trains) do
  local name="sn-"..t.name;local panel="sn-solar-rail-panel-"..t.tier;local battery="sn-solar-rail-battery-"..t.tier
  data:extend({{type="equipment-grid",name="sn-solar-rail-grid-"..t.tier,width=3,height=2,locked=true,equipment_categories={"sn-solar-rail"}}})
  local pv=H.copy("solar-panel-equipment","solar-panel-equipment")
  pv.name=panel;pv.take_result=panel;pv.power=t.solar_watts.."W"
  pv.categories={"sn-solar-rail"};pv.shape={width=2,height=2,type="full"}
  pv.sprite={filename=H.icon("solar-rail-panels"),width=64,height=64,scale=1}
  pv.localised_name={"sn-energy.installed-panels"}
  local store=H.copy("battery-equipment","battery-equipment")
  store.name=battery;store.take_result=battery;store.categories={"sn-solar-rail"}
  store.shape={width=1,height=2,type="full"}
  store.energy_source={type="electric",buffer_capacity=t.battery_joules.."J",usage_priority="tertiary"}
  store.sprite={filename=H.icon("solar-rail-battery"),width=64,height=64,scale=.5}
  store.localised_name={"sn-energy.installed-battery"}
  data:extend({pv,store,
    {type="item",name=panel,icon=H.icon("solar-rail-panels"),icon_size=64,stack_size=1,hidden=true,hidden_in_factoriopedia=true,
      placed_as_equipment_result=panel,auto_recycle=false,localised_name=pv.localised_name},
    {type="item",name=battery,icon=H.icon("solar-rail-battery"),icon_size=64,stack_size=1,hidden=true,hidden_in_factoriopedia=true,
      placed_as_equipment_result=battery,auto_recycle=false,localised_name=store.localised_name}})
  local loco=H.copy("locomotive","locomotive")
  loco.name=name;loco.icon=H.icon(t.name);loco.icon_size=64;loco.icons=nil
  loco.localised_name={"entity-name."..name};loco.localised_description={"entity-description."..name}
  loco.minable={mining_time=.8,result=name};loco.placeable_by={item=name,count=1}
  loco.max_speed=t.day_speed;loco.max_power=t.watts.."W";loco.weight=t.weight;loco.max_health=t.health
  loco.equipment_grid="sn-solar-rail-grid-"..t.tier
  -- No item fuel can enter. The runtime only transfers metered battery joules
  -- into the engine's internal traction buffer; no free fuel stack is created.
  loco.energy_source={type="burner",fuel_categories={"sn-solar-traction"},fuel_inventory_size=0,burnt_inventory_size=0,effectivity=1}
  loco.pictures={rotated={layers={table.deepcopy(A[t.name]),table.deepcopy(A[t.name.."-shadow"])}}}
  loco.wheels,loco.front_light_pictures,loco.corpse,loco.factoriopedia_simulation=nil,nil,nil,nil
  loco.allow_manual_color=false;loco.default_copy_color_from_train_stop=false
  loco.icons_positioning=nil
  local item=H.copy("item-with-entity-data","locomotive")
  item.name=name;item.icon=H.icon(t.name);item.icon_size=64;item.icons=nil
  item.place_result=name;item.subgroup="sn-energy";item.order="b-"..t.tier;item.stack_size=5
  item.localised_name=loco.localised_name;item.localised_description=loco.localised_description
  data:extend({loco,item})
end
