local H=require("prototypes.helpers")
local Art=require("prototypes.artwork")
local audio="__second-nature__/sound/"
local jukebox=H.copy("programmable-speaker","programmable-speaker")
jukebox.name,jukebox.icon,jukebox.icon_size="sn-jukebox",H.icon("jukebox"),64
jukebox.icons=nil;jukebox.localised_name={"entity-name.sn-jukebox"};jukebox.localised_description={"entity-description.sn-jukebox"}
jukebox.minable={mining_time=.3,result="sn-jukebox"};jukebox.max_health=350
jukebox.sprite=Art.sprite("jukebox-north");jukebox.maximum_polyphony=1
jukebox.energy_source={type="void"};jukebox.energy_usage_per_tick="1J"
jukebox.instruments={{name="sn-expedition-archive",notes={
  {name="sn-stop",sound={filename=audio.."voice/silence.ogg",volume=0}},
  {name="sn-after-the-ash",sound={filename=audio.."music/after-the-ash.ogg",volume=.8,category="ambient"}},
  {name="sn-living-world",sound={filename=audio.."music/we-need-a-living-world.ogg",volume=.75,category="ambient"}},
  {name="sn-transmission",sound={filename=audio.."music/landing-transmission.ogg",volume=.8,category="ambient"}}
}}}
data:extend({jukebox,{type="item",name="sn-jukebox",icon=H.icon("jukebox"),icon_size=64,subgroup="sn-logistics",order="z-audio",stack_size=20,place_result="sn-jukebox",
  localised_name=jukebox.localised_name,localised_description=jukebox.localised_description}})
-- A native hero track owns its complete voice-before-music sequence. It does not
-- depend on simulation ticks or queue fragments to keep spoken words together.
if settings.startup["sn-opening-audio"].value then
  local existing
  for _,track in pairs(data.raw["ambient-sound"]) do if track.planet=="nauvis" and track.track_type=="hero-track" then existing=track;break end end
  if existing then existing.sound={filename=audio.."music/landing-transmission.ogg",volume=.8};existing.variable_sound=nil
  else data:extend({{type="ambient-sound",name="sn-landing-transmission",track_type="hero-track",planet="nauvis",sound={filename=audio.."music/landing-transmission.ogg",volume=.8}}}) end
end
-- Zero random weight keeps the anthem available as a named track without making
-- it interrupt the normal ambient rotation. The physical jukebox can replay it.
data:extend({{type="ambient-sound",name="sn-living-world",track_type="main-track",planet="nauvis",weight=0,
  sound={filename=audio.."music/we-need-a-living-world.ogg",volume=.75}}})
