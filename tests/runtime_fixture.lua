-- Deterministic, deliberately small API test doubles. These do not simulate the
-- engine's electric networks, graphics, entity collision or actual recipe execution.
local C=require('shared.constants');local K=require('shared.catalog')
local function deepcopy(t)
  if type(t)~='table' then return t end
  local r={};for k,v in pairs(t) do r[k]=deepcopy(v) end;return r
end
table.deepcopy=nil
package.preload["util"]=function() table.deepcopy=deepcopy;return {table={deepcopy=deepcopy}} end
mock={handlers={},nth={},commands={},messages={},logs={},renders={},next_id=100,next_registration=0,entities={},surface_calls={}}
storage={};defines={events={},command={attack_area=1,attack=2,go_to_location=3,stop=4},distraction={by_enemy=1,none=0},controllers={character=1,cutscene=2}}
local event_names={'on_entity_spawned','on_chunk_generated','on_force_created','on_biter_base_built','on_rocket_launched','on_cutscene_cancelled','on_pre_player_mined_item','on_robot_pre_mined','on_entity_died','script_raised_destroy','on_built_entity','on_robot_built_entity','script_raised_built','script_raised_revive','on_space_platform_built_entity','on_entity_cloned','on_object_destroyed','on_surface_created','on_surface_deleted','on_surface_cleared','on_forces_merged','on_player_created','on_player_joined_game','on_player_removed','on_gui_click','on_gui_selection_state_changed','on_gui_closed','on_lua_shortcut','on_runtime_mod_setting_changed'}
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
settings={startup={['sn-overhaul-progression']={value=true},['sn-desolate-start']={value=true},['sn-legacy-smog']={value=80},['sn-biter-metabolism']={value=true},['sn-menu-background']={value=true}},global={}}
for name,value in pairs({['sn-native-fate']='choose',['sn-restoration-speed']=1,['sn-native-resistance']='balanced',['sn-grace-minutes']=20,['sn-living-terrain']=false,['sn-tree-growth']=false,['sn-network-victory']=true}) do settings.global[name]={value=value} end
settings.get_player_settings=function() return {['sn-show-welcome']={value=true}} end
prototypes={entity={}}
for _,name in ipairs({'sn-bloomback','sn-bloom-nest','sn-lander','tree-04','tree-08-brown','tree-02-red','tree-09','small-biter','small-spitter','sn-rootbreaker','sn-canopy-breaker','sn-blight-spitter','small-wriggler-pentapod','small-strafer-pentapod','small-stomper-pentapod','medium-stomper-pentapod','medium-strafer-pentapod','big-stomper-pentapod','big-strafer-pentapod'}) do prototypes.entity[name]={} end
log=function(message) mock.logs[#mock.logs+1]=message end
rendering={}
rendering.draw_sprite=function(spec)
  assert(spec.target_offset==nil,'removed rendering API')
  assert(spec.target.entity and spec.target.entity.valid)
  local r={valid=true,spec=spec};r.destroy=function() r.valid=false end
  mock.renders[#mock.renders+1]=r;return r
end
rendering.draw_rectangle=function(spec) local r={valid=true,spec=spec};r.destroy=function() r.valid=false end;mock.renders[#mock.renders+1]=r;return r end
rendering.clear=function() for _,r in ipairs(mock.renders) do r.valid=false end end
mock.forces_by_name={}
game={tick=0,surfaces={},players={},connected_players={},forces=setmetatable({},{__index=function(_,key) return mock.forces_by_name[key] end}),map_settings={pollution={enabled=true}}}
game.is_multiplayer=function() return mock.multiplayer or false end
game.print=function(m) mock.messages[#mock.messages+1]=m end
game.get_player=function(index) return game.players[index] end
game.reset_game_state=function() mock.reset_count=(mock.reset_count or 0)+1 end
game.set_game_state=function(state) mock.victory=state end
function mock.force(index,name)
  local f={index=index,name=name,technologies={['sn-living-worlds']={researched=false}},cease_fire=false,friend=false}
  f.print=function(m) mock.messages[#mock.messages+1]=m end
  f.friends={};f.ceases={}
  local function key(other) return type(other)=='table' and other.name or other end
  f.get_cease_fire=function(other) return f.cease_fire or f.ceases[key(other)] or false end
  f.get_friend=function(other) return f.friend or f.friends[key(other)] or false end
  f.set_friend=function(other,value) f.friends[key(other)]=value end
  f.set_cease_fire=function(other,value) f.ceases[key(other)]=value end
  f.get_spawn_position=function() return {x=0,y=0} end
  f.chart=function(_,area) f.charted=area end
  f.get_evolution_factor=function() return 0.4 end
  game.forces[index]=f;mock.forces_by_name[name]=f;return f
end
game.create_force=function(name) return mock.force(#game.forces+1,name) end
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
  s.chunks={};s.tiles={};s.local_pollution={}
  local function xy(pos) return pos.x or pos[1],pos.y or pos[2] end
  local function key(pos) local x,y=xy(pos);return math.floor(x)..':'..math.floor(y) end
  s.get_chunks=function() local i=0;return function() i=i+1;return s.chunks[i] end end
  s.get_pollution=function(pos) return s.local_pollution[key(pos)] or s.pollution end
  s.get_total_pollution=function() return s.total_pollution or s.pollution end
  s.request_to_generate_chunks=function() end;s.force_generate_chunk_requests=function() end
  s.destroy_decoratives=function() end
  s.find_tiles_filtered=function(filter)
    local tiles={};local a=filter.area;local l=a.left_top or a[1];local r=a.right_bottom or a[2]
    local lx,ly=xy(l);local rx,ry=xy(r)
    for x=lx,rx-1 do for y=ly,ry-1 do local t=s.get_tile({x=x,y=y});if matches(t.name,filter.name) then tiles[#tiles+1]=t end end end
    return tiles
  end
  s.pollute=function(_,amount,source) s.pollution=s.pollution+amount;assert(s.pollution>=-0.0001);s.pollution_source=source end
  s.is_chunk_generated=function() return s.generated end
  s.get_tile=function(pos) local x,y=xy(pos);return {name=s.tiles[key(pos)] or s.tile_name,hidden_tile=s.hidden_tile,position={x=x,y=y}} end
  s.set_tiles=function(tiles,correct,entities,decoratives,raise)
    assert(correct==false and entities==false and decoratives==false and raise==false)
    for _,t in ipairs(tiles) do s.changed_tiles[#s.changed_tiles+1]=t;s.tiles[key(t.position)]=t.name end
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
  game.surfaces[index]=s;if mock.handlers[defines.events.on_surface_created] then mock.event('on_surface_created',{surface_index=index}) end;return s
end
function mock.entity(name,surface,pos,force,no_event)
  mock.next_id=mock.next_id+1
  if type(force)=='string' then force=mock.forces_by_name[force] or mock.neutral end
  local def=K.by_machine[name]
  local kind=def and (def.entity_type or 'assembling-machine') or (name:find('spawner') and 'unit-spawner' or (name:find('tree') and 'tree' or 'unit'))
  if name=='sn-lander' then kind='container' elseif name=='gun-turret' then kind='ammo-turret' elseif name=='stone-wall' then kind='wall' elseif name=='fish' then kind='fish' elseif name=='sn-bloom-nest' then kind='simple-entity-with-owner' elseif name:find('worm') then kind='turret' end
  local e={name=name,type=kind,surface=surface,position=pos or {x=0,y=0},force=force or mock.player_force,valid=true,unit_number=mock.next_id,products_finished=0,
    _recipe=def and def.fixed and ('sn-'..def.fixed) or nil,commandable={}}
  e.inventory={};e.insert=function(stack) e.inventory[stack.name]=(e.inventory[stack.name] or 0)+stack.count;return stack.count end
  e.commandable.set_command=function(command) e.command=command end
  e.get_recipe=function() assert(e.type=='assembling-machine','Entity is not crafting-machine');return e._recipe and {name=e._recipe} or nil end
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
mock.gui_reserved = {}
function mock.gui(spec,parent)
  assert(not (spec.name and mock.gui_reserved[spec.name]), "Invalid LuaGuiElement child name: " .. tostring(spec.name))
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
    position={x=0,y=0},controller_type=defines.controllers.character,gui={screen=mock.gui({type='screen'}),top=mock.gui({type='flow'})},admin=true}
  p.set_shortcut_toggled=function(name,value) p.shortcut_toggled=value end
  p.set_controller=function(spec) p.controller_type=spec.type;p.cutscene=spec end
  p.exit_cutscene=function() p.controller_type=defines.controllers.character end
  p.print=function(m) mock.messages[#mock.messages+1]=m end
  game.players[index]=p;return p
end
mock.surface('nauvis',1)
