-- Deterministic, deliberately small API test doubles. These do not simulate the
-- engine's electric networks, graphics, entity collision or actual recipe execution.
local C=require('shared.constants');local K=require('shared.catalog')
function table.deepcopy(t)
  if type(t)~='table' then return t end
  local r={};for k,v in pairs(t) do r[k]=table.deepcopy(v) end;return r
end
mock={handlers={},nth={},commands={},messages={},logs={},renders={},next_id=100,next_registration=0,entities={},surface_calls={}}
storage={};defines={events={},command={attack_area=1},distraction={by_enemy=1}}
local event_names={'on_pre_player_mined_item','on_robot_pre_mined','on_entity_died','script_raised_destroy','on_built_entity','on_robot_built_entity','script_raised_built','script_raised_revive','on_space_platform_built_entity','on_entity_cloned','on_object_destroyed','on_surface_created','on_surface_deleted','on_surface_cleared','on_forces_merged','on_player_created','on_player_joined_game','on_player_removed','on_gui_click','on_gui_selection_state_changed','on_gui_closed','on_lua_shortcut','on_runtime_mod_setting_changed'}
for i,name in ipairs(event_names) do defines.events[name]=i end
script={mod_name='second-nature'}
script.on_init=function(fn) mock.init=fn end
script.on_configuration_changed=function(fn) mock.configure=fn end
script.on_nth_tick=function(n,fn) mock.nth[n]=fn end
script.on_event=function(event,fn)
  if type(event)=='table' then for _,e in ipairs(event) do mock.handlers[e]=fn end else mock.handlers[event]=fn end
end
script.register_on_object_destroyed=function(entity)
  if not entity._registration then mock.next_registration=mock.next_registration+1;entity._registration=mock.next_registration end
  return entity._registration
end
commands={add_command=function(name,desc,fn) mock.commands[name]=fn end}
remote={interfaces={}}
remote.add_interface=function(name,methods) remote.interfaces[name]=methods end
remote.call=function(name,method,...) return remote.interfaces[name][method](...) end
mock.escape_disabled=false
remote.add_interface('space_finish_script',{get_no_victory=function() return mock.escape_disabled end,set_no_victory=function(v) mock.escape_disabled=v end})
settings={startup={['sn-overhaul-progression']={value=true}},global={}}
for name,value in pairs({['sn-restoration-speed']=1,['sn-native-resistance']='balanced',['sn-grace-minutes']=20,['sn-living-terrain']=false,['sn-tree-growth']=false,['sn-network-victory']=true}) do settings.global[name]={value=value} end
settings.get_player_settings=function() return {['sn-show-welcome']={value=true}} end
prototypes={entity={}}
for _,name in ipairs({'tree-04','tree-08-brown','tree-02-red','tree-09','small-biter','small-spitter','sn-rootbreaker','sn-canopy-breaker','sn-blight-spitter','small-wriggler-pentapod','small-strafer-pentapod','small-stomper-pentapod','medium-stomper-pentapod','medium-strafer-pentapod','big-stomper-pentapod','big-strafer-pentapod'}) do prototypes.entity[name]={} end
log=function(message) mock.logs[#mock.logs+1]=message end
rendering={}
rendering.draw_sprite=function(spec)
  assert(spec.target_offset==nil,'removed rendering API')
  assert(spec.target.entity and spec.target.entity.valid)
  local r={valid=true,spec=spec};r.destroy=function() r.valid=false end
  mock.renders[#mock.renders+1]=r;return r
end
rendering.clear=function() for _,r in ipairs(mock.renders) do r.valid=false end end
game={tick=0,surfaces={},players={},connected_players={},forces={}}
game.print=function(m) mock.messages[#mock.messages+1]=m end
game.get_player=function(index) return game.players[index] end
game.reset_game_state=function() mock.reset_count=(mock.reset_count or 0)+1 end
game.set_game_state=function(state) mock.victory=state end
function mock.force(index,name)
  local f={index=index,name=name,technologies={['sn-living-worlds']={researched=false}},cease_fire=false,friend=false}
  f.print=function(m) mock.messages[#mock.messages+1]=m end
  f.get_cease_fire=function() return f.cease_fire end;f.get_friend=function() return f.friend end
  f.get_evolution_factor=function() return 0.4 end
  game.forces[index]=f;return f
end
mock.player_force=mock.force(1,'player');mock.enemy=mock.force(2,'enemy');mock.neutral=mock.force(3,'neutral')
local function matches(value,wanted)
  if wanted==nil then return true end
  if type(wanted)=='table' and wanted.name then return value==wanted.name end
  if type(wanted)=='table' then for _,v in ipairs(wanted) do if v==value then return true end end;return false end
  return value==wanted
end
function mock.surface(name,index)
  local s={name=name,index=index,valid=true,planet=C.profiles[name] and {name=name} or nil,properties={},entities={},pollution=0,peaceful_mode=false,
    tile_name='dirt-1',generated=true,changed_tiles={},query_calls=0,pollutant_type=C.profiles[name] and {name=name=='gleba' and 'spores' or 'pollution'} or nil}
  s.set_property=function(key,value) s.properties[key]=value end
  s.get_pollution=function() return s.pollution end
  s.pollute=function(_,amount,source) s.pollution=s.pollution+amount;assert(s.pollution>=-0.0001);s.pollution_source=source end
  s.is_chunk_generated=function() return s.generated end
  s.get_tile=function() return {name=s.tile_name,hidden_tile=s.hidden_tile} end
  s.set_tiles=function(tiles,correct,entities,decoratives,raise)
    assert(correct==false and entities==false and decoratives==false and raise==false)
    for _,t in ipairs(tiles) do s.changed_tiles[#s.changed_tiles+1]=t end
  end
  s.find_entities_filtered=function(filter)
    s.query_calls=s.query_calls+1
    if s.blocked and filter.area then return {{type='resource'}} end
    local found={}
    for _,e in ipairs(s.entities) do
      local in_range=true
      if filter.position then in_range=(e.position.x-filter.position.x)^2+(e.position.y-filter.position.y)^2<=(filter.radius or 1)^2 end
      if filter.area then local a=filter.area;in_range=e.position.x>=a[1][1] and e.position.x<=a[2][1] and e.position.y>=a[1][2] and e.position.y<=a[2][2] end
      if e.valid and in_range and matches(e.name,filter.name) and matches(e.type,filter.type) and matches(e.force.name,filter.force) then
        found[#found+1]=e;if filter.limit and #found>=filter.limit then break end
      end
    end
    return found
  end
  s.count_entities_filtered=function(filter) return #s.find_entities_filtered(filter) end
  s.can_place_entity=function() return not s.blocked end
  s.find_non_colliding_position=function(_,pos) return {x=pos.x+3,y=pos.y+3} end
  s.create_entity=function(spec) return mock.entity(spec.name,s,spec.position,spec.force,true) end
  s.create_unit_group=function(spec)
    local g={valid=true,members={},position=spec.position,force=spec.force}
    g.add_member=function(e) g.members[#g.members+1]=e;e.commandable.parent_group=g end
    g.set_command=function(command) g.command=command end;g.start_moving=function() g.moving=true end
    g.destroy=function() g.valid=false end;return g
  end
  game.surfaces[index]=s;return s
end
function mock.entity(name,surface,pos,force,no_event)
  mock.next_id=mock.next_id+1
  if type(force)=='string' then force=force=='enemy' and mock.enemy or mock.neutral end
  local def=K.by_machine[name]
  local kind=def and (def.entity_type or 'assembling-machine') or (name:find('spawner') and 'unit-spawner' or (name:find('tree') and 'tree' or 'unit'))
  local e={name=name,type=kind,surface=surface,position=pos or {x=0,y=0},force=force or mock.player_force,valid=true,unit_number=mock.next_id,products_finished=0,
    _recipe=def and def.fixed and ('sn-'..def.fixed) or nil,commandable={}}
  e.get_recipe=function() return e._recipe and {name=e._recipe} or nil end
  local behavior={sections={}}
  behavior.get_section=function(i) return behavior.sections[i] end
  behavior.add_section=function()
    local section={valid=true,is_manual=true,group='',filters={}}
    behavior.sections[#behavior.sections+1]=section;return section
  end
  e.get_or_create_control_behavior=function() return behavior end
  e.destroy=function() e.valid=false;local handler=mock.handlers[defines.events.on_object_destroyed];if handler and e._registration then handler({registration_number=e._registration}) end end
  surface.entities[#surface.entities+1]=e;mock.entities[e.unit_number]=e
  if not no_event and mock.handlers[defines.events.on_built_entity] then mock.handlers[defines.events.on_built_entity]({entity=e}) end
  return e
end
function mock.event(name,event) return mock.handlers[defines.events[name]](event) end
function mock.run(ticks)
  for _=1,ticks do
    game.tick=game.tick+1
    for _,interval in ipairs({15,60,120}) do if game.tick%interval==0 and mock.nth[interval] then mock.nth[interval]({tick=game.tick}) end end
  end
end
function mock.gui(spec,parent)
  local g={valid=true,name=spec.name or '',type=spec.type,parent=parent,children={},style={},caption=spec.caption,value=spec.value,selected_index=spec.selected_index}
  if parent then parent.children[#parent.children+1]=g;if g.name~='' then parent[g.name]=g end end
  g.add=function(child) return mock.gui(child,g) end
  g.add_tab=function() end
  g.destroy=function() g.valid=false;if parent and parent[g.name]==g then parent[g.name]=nil end end
  return g
end
package.preload['mod-gui']=function() return {button_style='slot_button',get_button_flow=function(p) return p.gui.top end} end
function mock.player(index)
  local p={index=index,force=mock.player_force,surface=game.surfaces[1],display_resolution={width=1920,height=1080},display_scale=1,
    gui={screen=mock.gui({type='screen'}),top=mock.gui({type='flow'})},admin=true}
  p.set_shortcut_toggled=function(_,value) p.shortcut_toggled=value end
  p.print=function(m) mock.messages[#mock.messages+1]=m end
  game.players[index]=p;return p
end
mock.surface('nauvis',1)
