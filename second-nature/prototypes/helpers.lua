local H = {}
function H.icon(name) return "__second-nature__/graphics/icons/" .. name .. ".png" end
function H.copy(kind, name) return table.deepcopy(assert(data.raw[kind] and data.raw[kind][name], "Second Nature requires " .. kind .. "/" .. name)) end
function H.contains(list, value)
  for _, entry in ipairs(list or {}) do if entry == value then return true end end
  return false
end
function H.append(list, value) if not H.contains(list, value) then list[#list + 1] = value end end
function H.tint_sprites(node, color)
  if type(node) ~= "table" then return end
  if (node.filename or node.filenames or node.stripes) and not node.draw_as_shadow and not node.draw_as_light then
    local old = node.tint or {1, 1, 1, 1}
    node.tint = {r = (old.r or old[1] or 1) * color[1], g = (old.g or old[2] or 1) * color[2], b = (old.b or old[3] or 1) * color[3], a = old.a or old[4] or 1}
  end
  for key, child in pairs(node) do if key ~= "tint" then H.tint_sprites(child, color) end end
end
function H.conditions(r)
  local C = require("shared.constants")
  local conditions = {}
  if r.domain or r.planet or r.stage then conditions[#conditions + 1] = {property = "sn-restoration-domain", min = 1, max = 1} end
  if r.planet then
    local id = C.profiles[r.planet].id
    conditions[#conditions + 1] = {property = "sn-planet-identity", min = id, max = id}
  end
  if r.stage then conditions[#conditions + 1] = {property = "sn-ecological-stage", min = r.stage, max = 5} end
  return #conditions > 0 and conditions or nil
end
return H
