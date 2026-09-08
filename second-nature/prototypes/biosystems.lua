local H=require("prototypes.helpers")
local function bind_sticker(name,slow,ticks)
  return {type="sticker",name=name,flags={"not-on-map"},duration_in_ticks=ticks,target_movement_modifier=slow,
    animation={filename="__second-nature__/graphics/entity/industry/root-binding.png",width=96,height=96,frame_count=4,line_length=4,
      animation_speed=.12,scale=.5,draw_as_glow=true},render_layer="object"}
end
data:extend({bind_sticker("sn-mycelial-binding",.58,240),bind_sticker("sn-resonance-daze",.72,120)})
local seed=data.raw.ammo["sn-mycelial-magazine"]
seed.ammo_type={action={type="direct",action_delivery={type="instant",target_effects={
  {type="damage",damage={amount=7,type="physical"}},
  {type="damage",damage={amount=3,type="poison"}},
  {type="create-sticker",sticker="sn-mycelial-binding"},
  {type="create-explosion",entity_name="explosion-hit",only_when_visible=true}}}}}
local beam=H.copy("beam","laser-beam")
beam.name="sn-resonance-beam"
H.tint_sprites(beam,{.45,1,.65})
beam.action={type="direct",action_delivery={type="instant",target_effects={
  {type="damage",damage={amount=9,type="electric"}},
  {type="create-sticker",sticker="sn-resonance-daze"}}}}
data:extend({beam})
local diffuser=data.raw["electric-turret"]["sn-arc-turret"]
diffuser.attack_parameters.ammo_type.action.action_delivery.beam=beam.name
diffuser.attack_parameters.damage_modifier=2
-- Pressure rounds bind a small amount of real airborne contamination at impact.
-- This credits no fitness or science and never manufactures pollution to remove.
local lance=data.raw.ammo["sn-lance-cell"]
lance.ammo_type.action.action_delivery.target_effects={
  {type="damage",damage={amount=8500,type="physical"}},
  {type="create-sticker",sticker="sn-resonance-daze"},
  {type="script",effect_id="sn-pressure-cleanup"}}
