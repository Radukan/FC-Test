-- Canonical placement footprints. Compact prototypes retain their old dimensions
-- for saved entities/blueprints; new inventory placement uses the larger plants.
--
-- `previous` is only set for machines that shipped at a smaller size in an
-- earlier version. Anything introduced at its current size has previous == size,
-- so it is never flagged `expanded` and never gets a hidden compact twin.
local sizes = {
  ["algae-vat"]=5, ["composter"]=3, ["hydroponics-bay"]=5, ["electrolyzer"]=5,
  ["reclamation-plant"]=5, ["materials-kiln"]=5, ["pyrolyzer"]=3,
  ["air-scrubber"]=3, ["soil-enricher"]=3, ["seed-disperser"]=3, ["watershed"]=5,
  ["thermal-exchanger"]=5, ["detoxifier"]=5, ["pheromone-dampener"]=3,
  ["forcing-tower"]=3, ["basalt-conditioner"]=5, ["fulgoran-reclaimer"]=5,
  ["spore-tower"]=5, ["cryogenic-garden"]=7, ["sanctuary"]=7,
  ["planetary-beacon"]=7, ["ecology-monitor"]=1,
  -- Industry expansion. All introduced at their current footprint.
  ["crucible-furnace"]=3, ["oxy-smelter"]=5, ["arc-refinery"]=5,
  ["blast-furnace"]=5, ["cupola-furnace"]=3,
  ["biopolymer-assembler"]=3, ["precision-assembler"]=3, ["foundry-press"]=5,
  ["ore-mill"]=5, ["flotation-cell"]=5, ["dewatering-press"]=3,
  ["electric-auger"]=3, ["hydraulic-miner"]=3, ["deep-core-drill"]=7,
  ["smog-precipitator"]=5, ["carbon-capture-tower"]=7, ["field-laboratory"]=3
}
-- Machines that grew after release keep their original collision footprint on
-- a hidden compact prototype so saved games and blueprints stay valid.
local previous = {
  ["algae-vat"]=3, ["hydroponics-bay"]=3, ["electrolyzer"]=3, ["reclamation-plant"]=3,
  ["materials-kiln"]=3, ["watershed"]=3, ["thermal-exchanger"]=3, ["detoxifier"]=3,
  ["basalt-conditioner"]=3, ["fulgoran-reclaimer"]=3, ["spore-tower"]=3,
  ["cryogenic-garden"]=5, ["sanctuary"]=3, ["planetary-beacon"]=5
}
local layouts={}
for name,size in pairs(sizes) do
  local was=previous[name] or size
  local large=size>was
  layouts[name]={size=size,previous_size=was,expanded=large,
    entity_name="sn-"..name..(large and "-plant" or ""),art_name=name..(large and "-plant" or ""),
    -- Extra space below the ground pivot contains complete cast shadows in
    -- every rotation. A changed canvas must never shift a native pipe seam.
    frame_width=size==7 and 640 or (size==5 and 448 or (size==1 and 160 or 320)),
    frame_height=size==7 and 640 or (size==5 and 512 or (size==1 and 192 or 384)),
    origin=size==7 and .57 or (size==5 and .525 or .50)}
end
return layouts
