-- Test-only real electric load, never included in the shipped mod archive.
data:extend({{
  type="electric-energy-interface",name="sn-engine-power-load",
  flags={"placeable-off-grid"},max_health=100,
  collision_box={{-.2,-.2},{.2,.2}},selection_box={{-.2,-.2},{.2,.2}},
  energy_source={type="electric",usage_priority="secondary-input",buffer_capacity="100MJ",input_flow_limit="1GW",output_flow_limit="0W"},
  energy_usage="1GW",energy_production="0W",gui_mode="none",
  picture={filename="__core__/graphics/empty.png",width=1,height=1}
}})
