-- Canonical placement footprints. Compact prototypes retain their old dimensions
-- for saved entities/blueprints; new inventory placement uses the larger plants.
local sizes = {
  ["algae-vat"]=5, ["composter"]=3, ["hydroponics-bay"]=5, ["electrolyzer"]=5,
  ["reclamation-plant"]=5, ["materials-kiln"]=5, ["pyrolyzer"]=3,
  ["air-scrubber"]=3, ["soil-enricher"]=3, ["seed-disperser"]=3, ["watershed"]=5,
  ["thermal-exchanger"]=5, ["detoxifier"]=5, ["pheromone-dampener"]=3,
  ["forcing-tower"]=3, ["basalt-conditioner"]=5, ["fulgoran-reclaimer"]=5,
  ["spore-tower"]=5, ["cryogenic-garden"]=7, ["sanctuary"]=7,
  ["planetary-beacon"]=7, ["ecology-monitor"]=1
}
local layouts={}
for name,size in pairs(sizes) do
  local previous=(name=="cryogenic-garden" or name=="planetary-beacon") and 5 or (name=="ecology-monitor" and 1 or 3)
  local large=size>previous
  layouts[name]={size=size,previous_size=previous,expanded=large,
    entity_name="sn-"..name..(large and "-plant" or ""),art_name=name..(large and "-plant" or ""),
    frame_size=size==7 and 640 or (size==5 and 448 or (size==1 and 160 or 320)),origin=size==7 and .57 or .60}
end
return layouts
