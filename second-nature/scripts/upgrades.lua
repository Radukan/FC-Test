local S = require("scripts.state")
local U = {}
function U.refresh(force)
  local root = S.root();root.efficiency = root.efficiency or {}
  local bonus = 1
  for level,value in ipairs({1.15,1.30,1.45}) do
    local technology = force.technologies["sn-restoration-efficiency-" .. level]
    if technology and technology.researched then bonus = value end
  end
  root.efficiency[force.index] = bonus
end
function U.bonus(force)
  local root = S.root()
  if not root.efficiency or not root.efficiency[force.index] then U.refresh(force) end
  return root.efficiency[force.index]
end
return U
