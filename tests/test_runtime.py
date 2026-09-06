import pytest


def test_install_and_recipe_accounting_without_free_idle_progress(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local s=game.surfaces[1]
      local e=mock.entity('sn-air-scrubber',s);s.pollution=25
      local initial=S.by_planet('nauvis').values.atmosphere
      mock.run(480)
      assert(S.by_planet('nauvis').values.atmosphere==initial)
      e.products_finished=1;mock.run(240)
      local w=S.by_planet('nauvis')
      assert(w.cycles==1 and w.values.atmosphere>initial)
      assert(s.pollution==0 and w.removed_pollution==25)
      mock.run(480);assert(w.cycles==1)
      assert(w.contributions[1]==1)
    ''')


def test_deconstruction_removes_last_bucket_slot_and_registration(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local e=mock.entity('sn-air-scrubber',game.surfaces[1]);local r=S.root().machines[e.unit_number]
      e.destroy();assert(#S.root().buckets[r.bucket]==0)
      assert(not S.root().machines[e.unit_number] and not S.root().registrations[r.registration])
      mock.run(480);assert(S.by_planet('nauvis').machine_count==0)
    ''')


def test_dense_bucket_swap_does_not_skip_or_duplicate_machines(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local entities={}
      for i=1,80 do entities[i]=mock.entity('sn-air-scrubber',game.surfaces[1],{x=i*4,y=0}) end
      for i=1,80,3 do entities[i].destroy() end
      local count=0
      for _,e in ipairs(entities) do if e.valid then e.products_finished=1;count=count+1 end end
      mock.run(480);assert(S.by_planet('nauvis').cycles==count)
      assert(S.by_planet('nauvis').machine_count==count)
      for b,list in ipairs(S.root().buckets) do for slot,id in ipairs(list) do
        assert(S.root().machines[id].bucket==b and S.root().machines[id].slot==slot)
      end end
    ''')


def test_duplicate_build_clone_and_configuration_are_idempotent(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local e=mock.entity('sn-air-scrubber',game.surfaces[1])
      e.products_finished=7;mock.run(240)
      local before=S.by_planet('nauvis').cycles
      mock.event('script_raised_built',{entity=e});mock.configure();mock.run(240)
      assert(S.by_planet('nauvis').cycles==before and S.by_planet('nauvis').machine_count==1)
      local clone=mock.entity('sn-air-scrubber',game.surfaces[1],{x=10,y=0},nil,true);clone.products_finished=7
      mock.event('on_entity_cloned',{destination=clone});mock.run(240)
      assert(S.by_planet('nauvis').cycles==before)
      clone.products_finished=8;mock.run(240);assert(S.by_planet('nauvis').cycles==before+1)
    ''')


def test_unsupported_surfaces_are_not_terraformed(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local space=mock.surface('platform-7',7)
      local e=mock.entity('sn-air-scrubber',space);e.products_finished=100;mock.run(240)
      assert(not S.root().worlds[7] and not S.root().machines[e.unit_number])
    ''')


def test_teleport_rebases_production_to_destination_planet(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local e=mock.entity('sn-air-scrubber',game.surfaces[1])
      e.products_finished=2;mock.run(240)
      local f=mock.surface('fulgora',3);e.surface=f;e.products_finished=4;mock.run(240)
      assert(S.by_planet('fulgora').cycles==0)
      e.products_finished=5;mock.run(240)
      assert(S.by_planet('fulgora').cycles==1 and S.by_planet('nauvis').cycles==2)
    ''')


def test_specialty_recipe_injection_cannot_award_wrong_planet_progress(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local e=mock.entity('sn-basalt-conditioner',game.surfaces[1])
      e.products_finished=99;mock.run(240);assert(S.by_planet('nauvis').cycles==0)
    ''')


def test_monitor_uses_quality_aware_dense_section_and_force_local_state(game_lua):
    game_lua.execute('''
      local e=mock.entity('sn-ecology-monitor',game.surfaces[1]);mock.run(240)
      local s=e.get_or_create_control_behavior().get_section(1)
      assert(#s.filters==9 and s.group=='')
      assert(s.filters[1].value.name=='sn-atmosphere' and s.filters[1].value.quality=='normal')
      assert(s.filters[1].min==35 and s.filters[1].index==nil)
      mock.run(240);assert(#e.get_or_create_control_behavior().sections==1)
    ''')


def test_surface_deletion_and_force_merge_preserve_invariants(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local f=mock.surface('fulgora',3);local e=mock.entity('sn-air-scrubber',f)
      local w=S.by_planet('fulgora');w.contributions[1]=5;w.contributions[4]=8
      local dst=mock.force(4,'new-force');mock.event('on_forces_merged',{source_index=1,destination=dst})
      assert(w.contributions[4]==13 and not w.contributions[1])
      mock.event('on_surface_deleted',{surface_index=3})
      assert(not S.by_planet('fulgora') and not S.root().machines[e.unit_number])
      mock.run(480)
    ''')


def test_resistance_requires_existing_distant_nest_and_warns_before_spawning(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local R=require('scripts.resistance');local s=game.surfaces[1]
      settings.global['sn-grace-minutes'].value=0
      local e=mock.entity('sn-seed-disperser',s);local rec=S.root().machines[e.unit_number]
      local w=S.by_planet('nauvis');w.first_operation=1;w.pressure=70;game.tick=300;rec.last_effect=game.tick
      R.tick(w,s);assert(not w.warning and #w.groups==0)
      local near=mock.entity('biter-spawner',s,{x=30,y=0},mock.enemy,true)
      w.next_raid_check=0;R.tick(w,s);assert(not w.warning)
      local nest=mock.entity('biter-spawner',s,{x=140,y=0},mock.enemy,true)
      w.next_raid_check=0;R.tick(w,s);assert(w.warning and #w.groups==0)
      game.tick=w.warning.at;R.tick(w,s)
      assert(#w.groups==1 and #w.groups[1].group.members<=40)
      assert(w.groups[1].group.command.destination.x==0 and w.groups[1].group.moving)
      assert(w.next_raid_check>=game.tick+8*60*60)
    ''')


@pytest.mark.parametrize('mode',['off','peaceful','no-nest','destroy-target','destroy-nest','cease-fire'])
def test_resistance_cancellation_is_safe(game_lua,mode):
    game_lua.globals().test_mode=mode
    game_lua.execute('''
      local S=require('scripts.state');local R=require('scripts.resistance');local s=game.surfaces[1]
      settings.global['sn-grace-minutes'].value=0;game.tick=300
      local e=mock.entity('sn-seed-disperser',s);local rec=S.root().machines[e.unit_number];rec.last_effect=game.tick
      local w=S.by_planet('nauvis');w.first_operation=1;w.pressure=70
      local n=mock.entity('biter-spawner',s,{x=150,y=0},mock.enemy,true);R.tick(w,s);assert(w.warning)
      if test_mode=='off' then settings.global['sn-native-resistance'].value='off'
      elseif test_mode=='peaceful' then s.peaceful_mode=true
      elseif test_mode=='destroy-target' then e.destroy()
      elseif test_mode=='cease-fire' then mock.player_force.cease_fire=true
      else n.destroy() end
      game.tick=game.tick+2700;R.tick(w,s);assert(#w.groups==0 and not w.warning)
    ''')


def test_raid_recruits_existing_commandables_without_old_unit_group_api(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local R=require('scripts.resistance');local s=game.surfaces[1];game.tick=300
      settings.global['sn-grace-minutes'].value=0
      local e=mock.entity('sn-seed-disperser',s);S.root().machines[e.unit_number].last_effect=game.tick
      local w=S.by_planet('nauvis');w.first_operation=1;w.pressure=70
      mock.entity('biter-spawner',s,{x=150,y=0},mock.enemy,true)
      local u=mock.entity('small-biter',s,{x=151,y=0},mock.enemy,true)
      setmetatable(u,{__index=function(_,key) if key=='unit_group' then error('removed API') end end})
      R.tick(w,s);game.tick=w.warning.at;R.tick(w,s)
      assert(u.commandable.parent_group==w.groups[1].group)
    ''')


@pytest.mark.parametrize('tile',['water','deepwater','lava','oil-ocean-deep','ice-platform','foundation','concrete','artificial-yumako-soil','natural-jellynut-soil'])
def test_terrain_never_replaces_protected_tiles(game_lua,tile):
    game_lua.globals().test_tile=tile
    game_lua.execute('''
      local S=require('scripts.state');local T=require('scripts.terrain');local s=game.surfaces[1]
      settings.global['sn-living-terrain'].value=true;s.tile_name=test_tile
      local e=mock.entity('sn-soil-enricher',s);local w=S.by_planet('nauvis');w.stage=3
      T.apply(S.root().machines[e.unit_number],w,{terrain=true,trees=true},100)
      assert(#s.changed_tiles==0 and w.grown_trees==0)
    ''')


def test_terrain_is_bounded_and_respects_resources_hidden_tiles_and_generation(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local T=require('scripts.terrain');local s=game.surfaces[1]
      settings.global['sn-living-terrain'].value=true
      local e=mock.entity('sn-soil-enricher',s);local w=S.by_planet('nauvis');w.stage=3;local rec=S.root().machines[e.unit_number]
      s.blocked=true;T.apply(rec,w,{terrain=true},100);assert(#s.changed_tiles==0)
      s.blocked=false;s.hidden_tile='water';T.apply(rec,w,{terrain=true},100);assert(#s.changed_tiles==0)
      s.hidden_tile=nil;s.generated=false;T.apply(rec,w,{terrain=true},100);assert(#s.changed_tiles==0)
      s.generated=true
      for i=1,100 do T.apply(rec,w,{terrain=true},100) end
      assert(#s.changed_tiles>0 and #s.changed_tiles<=20 and S.root().visual_budget==0)
    ''')


def test_aquilo_uses_entity_anchored_gardens_without_tile_replacement(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local T=require('scripts.terrain');local s=mock.surface('aquilo',5)
      settings.global['sn-living-terrain'].value=true
      local e=mock.entity('sn-cryogenic-garden',s);local w=S.by_planet('aquilo');w.stage=2;local rec=S.root().machines[e.unit_number]
      T.apply(rec,w,{garden=true,terrain=true},10);T.apply(rec,w,{garden=true,terrain=true},10)
      assert(#mock.renders==1 and #s.changed_tiles==0 and rec.garden.valid)
      e.destroy();assert(not mock.renders[1].valid)
    ''')


def test_network_is_force_specific_and_requires_recent_actual_beacon_cycles(game_lua):
    game_lua.execute('''
      local C=require('shared.constants');local S=require('scripts.state');local N=require('scripts.network');local M=require('shared.model')
      mock.player_force.technologies['sn-living-worlds'].researched=true;game.tick=10000
      local second=mock.force(4,'second');second.technologies['sn-living-worlds'].researched=true
      for i,planet in ipairs(C.planets) do
        local surface=i==1 and game.surfaces[1] or mock.surface(planet,i)
        local beacon=mock.entity('sn-planetary-beacon',surface);local w=S.by_planet(planet)
        for axis in pairs(w.values) do w.values[axis]=95 end;w.toxicity=2;M.refresh(w)
        S.root().machines[beacon.unit_number].last_effect=game.tick
      end
      assert(N.status(mock.player_force));assert(not N.status(second))
      N.tick(1200);assert(S.root().networks[1].held==1200)
      game.tick=game.tick+C.beacon_freshness+1;N.tick(60)
      assert(S.root().networks[1].held==0 and not N.status(mock.player_force))
    ''')


def test_victory_hold_is_continuous_and_awarded_exactly_once(game_lua):
    game_lua.execute('''
      local C=require('shared.constants');local S=require('scripts.state');local N=require('scripts.network');local M=require('shared.model')
      game.tick=10000;mock.player_force.technologies['sn-living-worlds'].researched=true
      for i,planet in ipairs(C.planets) do
        local surface=i==1 and game.surfaces[1] or mock.surface(planet,i)
        local e=mock.entity('sn-planetary-beacon',surface);S.root().machines[e.unit_number].last_effect=game.tick
        local w=S.by_planet(planet);for axis in pairs(w.values) do w.values[axis]=99 end;w.toxicity=0;M.refresh(w)
      end
      N.tick(C.victory_ticks-1);assert(not mock.victory)
      N.tick(1);assert(mock.victory.player_won and mock.victory.can_continue and mock.victory.victorious_force.index==1)
      N.tick(60);assert(mock.reset_count==1)
    ''')


def test_stock_victory_setting_is_restored_not_blindly_enabled(game_lua):
    game_lua.execute('''
      local N=require('scripts.network');assert(mock.escape_disabled)
      settings.global['sn-network-victory'].value=false;N.configure_victory();assert(not mock.escape_disabled)
      mock.escape_disabled=true;settings.global['sn-network-victory'].value=true;N.configure_victory()
      settings.global['sn-network-victory'].value=false;N.configure_victory();assert(mock.escape_disabled)
    ''')


def test_dashboard_builds_updates_switches_tabs_and_closes(game_lua):
    game_lua.execute('''
      local G=require('scripts.gui');local p=mock.player(1);G.welcome(p);G.open(p)
      local f=p.gui.screen.sn_dashboard;assert(f and p.shortcut_toggled)
      assert(f.tabs.overview.content.body.visible)
      local selector=f.tabs.overview.content.selector.sn_planet;selector.selected_index=5
      G.selection({player_index=1,element=selector});assert(f.tabs.overview.content.uncharted.visible)
      local guide=f.tabs.guide.content.sn_guide;guide.selected_index=3;G.selection({player_index=1,element=guide})
      G.click({player_index=1,element={valid=true,name='sn_select_nauvis'}})
      assert(f.tabs.overview.content.body.visible and f.tabs.selected_tab_index==1)
      G.close(p);assert(not p.gui.screen.sn_dashboard and not p.shortcut_toggled)
    ''')


def test_remote_reports_are_copies_not_mutation_backdoors(game_lua):
    game_lua.execute('''
      local snap=remote.call('second_nature','get_world','nauvis');snap.values.atmosphere=100
      assert(remote.call('second_nature','get_world','nauvis').values.atmosphere==35)
      assert(not remote.call('second_nature','get_world','aquilo'))
    ''')


def test_switching_dirty_recipes_cannot_launder_toxic_debt(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local s=game.surfaces[1]
      local e=mock.entity('sn-pyrolyzer',s)
      e._recipe='sn-coal-activation';e.products_finished=1;mock.run(240)
      local w=S.by_planet('nauvis');assert(w.cycles==1 and w.toxicity>30)
      local before=w.toxicity;e._recipe=nil;e.products_finished=2;mock.run(240)
      assert(w.cycles==2 and w.toxicity>before)
    ''')


@pytest.mark.parametrize('event',['on_pre_player_mined_item','on_robot_pre_mined','on_entity_died','script_raised_destroy'])
def test_pending_completed_work_is_flushed_before_entity_removal(game_lua,event):
    game_lua.globals().test_event=event
    game_lua.execute('''
      local S=require('scripts.state');local e=mock.entity('sn-air-scrubber',game.surfaces[1])
      e.products_finished=1
      mock.event(test_event,{entity=e});e.destroy()
      assert(S.by_planet('nauvis').cycles==1)
      mock.run(240);assert(S.by_planet('nauvis').cycles==1)
    ''')


def test_legacy_surface_without_pollutant_never_calls_pollution_api(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local surface=game.surfaces[1]
      surface.pollutant_type=nil
      surface.get_pollution=function() error('no pollutant on legacy/scenario surface') end
      surface.pollute=function() error('no pollutant on legacy/scenario surface') end
      local e=mock.entity('sn-air-scrubber',surface);e.products_finished=1
      mock.run(240);assert(S.by_planet('nauvis').cycles==1)
      local dirty=mock.entity('sn-forcing-tower',surface);dirty.products_finished=1
      mock.run(240);assert(S.by_planet('nauvis').cycles==2)
    ''')
