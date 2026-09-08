local C = require("shared.constants")
local Pollution = require("scripts.pollution")
local Telemetry = {}
function Telemetry.update(entity, world)
  local behavior = entity.get_or_create_control_behavior()
  if not behavior then return end
  -- The first section is reserved. Do not use a named group: that would synchronize
  -- distinct monitors across planets through Factorio's shared logistic groups.
  local section = behavior.get_section(1) or behavior.add_section()
  if not section then return end
  if not section.is_manual then return end
  if section.group ~= "" then section.group = "" end
  section.active = true
  section.multiplier = 1
  local values = {}
  for _, axis in ipairs(C.axes) do values[#values + 1] = {name = axis, value = math.floor(world.values[axis])} end
  values[#values + 1] = {name = "toxicity", value = math.ceil(world.toxicity)}
  values[#values + 1] = {name = "pressure", value = math.ceil(world.pressure)}
  values[#values + 1] = {name = "stability", value = math.floor(world.score)}
  values[#values + 1] = {name = "stage", value = world.stage}
  values[#values + 1] = {name = "smog-total", value = math.min(2147483647, math.ceil(world.air and world.air.total or 0))}
  values[#values + 1] = {name = "smog-local", value = math.min(2147483647, math.ceil(Pollution.local_amount(entity.surface, entity.position)))}
  local filters = {}
  for index, signal in ipairs(values) do
    filters[#filters + 1] = {value = {type = "virtual", name = "sn-" .. signal.name, quality = "normal"}, min = signal.value}
  end
  section.filters = filters
end
return Telemetry
