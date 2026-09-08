-- Accounting doubles; actual native solar charging/rail movement are engine probes.
local E=require('shared.energy')
local old=mock.entity
function mock.rail(name,position)
  local e=old(name,game.surfaces[1],position or {x=0,y=0},mock.player_force,true)
  e.type='locomotive'
  e.train={valid=true,id=e.unit_number,speed=0,manual_mode=true}
  local grid={valid=true,equipment={}}
  grid.put=function(spec)
    local tier=tonumber(spec.name:match('(%d+)$'));local def=E.trains[tier]
    local eq={valid=true,name=spec.name,energy=0,max_energy=spec.name:find('battery') and def.battery_joules or 0}
    grid.equipment[#grid.equipment+1]=eq;return eq
  end
  e.grid=grid
  e.burner=setmetatable({heat=0,remaining_burning_fuel=0},{
    __index=function(t,k) if k=='currently_burning' then return rawget(t,'_fuel') end end,
    __newindex=function(t,k,v)
      if k=='currently_burning' then rawset(t,'_fuel',v);if not v then rawset(t,'remaining_burning_fuel',0) end
      else rawset(t,k,v) end
    end})
  return e
end
function mock.battery(e)
  for _,eq in ipairs(e.grid.equipment) do if eq.name:find('battery') then return eq end end
end
mock.surface_defaults=function(surface)
  surface.darkness=0;surface.wind_speed=.015
  surface.get_property=function(name) return surface.properties[name] or (name=='pressure' and 1000 or 0) end
end
mock.surface_defaults(game.surfaces[1])
