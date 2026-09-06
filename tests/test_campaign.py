import pytest
from lupa.lua52 import LuaError


@pytest.mark.parametrize('entry', ['leaf', 'shortcut', 'key'])
def test_dashboard_reported_crash_all_entry_points(game_lua, entry):
    game_lua.globals().entry = entry
    game_lua.execute('''
      local p=mock.player(1)
      if entry=='leaf' then mock.event('on_gui_click',{player_index=1,element={valid=true,name='sn_open'}})
      elseif entry=='shortcut' then mock.event('on_lua_shortcut',{player_index=1,prototype_name='sn-dashboard'})
      else mock.handlers['sn-toggle-dashboard']({player_index=1}) end
      local frame=p.gui.screen.sn_dashboard
      assert(frame and frame.sn_tabs.sn_air.sn_content.sn_air_total)
      local function visit(e)
        if e.name~='' then assert(e.name:sub(1,3)=='sn_',e.name) end
        for _,child in ipairs(e.children) do visit(child) end
      end
      visit(frame)
      require('scripts.gui').toggle(p);assert(not p.gui.screen.sn_dashboard)
    ''')


@pytest.mark.parametrize('name', ['tabs', 'value', 'text', 'state', 'children', 'add'])
def test_gui_double_rejects_real_engine_reserved_names(game_lua, name):
    game_lua.globals().reserved = name
    with pytest.raises(LuaError, match='Invalid LuaGuiElement child name'):
        game_lua.execute("mock.player(1).gui.screen.add({type='label',name=reserved})")


def test_failed_dashboard_construction_does_not_kill_the_factory(game_lua):
    game_lua.execute('''
      local p=mock.player(1);p.gui.screen.add=function() error('deliberate presentation failure') end
      require('scripts.gui').toggle(p)
      assert(not p.gui.screen.sn_dashboard and not p.shortcut_toggled)
      assert(mock.logs[#mock.logs]:find('deliberate presentation failure'))
      assert(require('scripts.state').by_planet('nauvis').cycles==0)
    ''')


def prepare_landing(lua):
    lua.execute('''
      local S=require('scripts.state');S.root().campaign=nil
      mock.freeplay={}
      remote.add_interface('freeplay',{
        set_skip_intro=function(v) mock.freeplay.skip=v end,
        set_disable_crashsite=function(v) mock.freeplay.disabled=v end,
        set_created_items=function(v) mock.freeplay.items=v end,
        set_respawn_items=function(v) mock.freeplay.respawn=v end})
      require('scripts.campaign').init(true)
    ''')


def test_landing_is_shared_and_never_duplicates_on_join_or_update(game_lua):
    prepare_landing(game_lua)
    game_lua.execute('''
      local C=require('shared.constants');local S=require('scripts.state');local Campaign=require('scripts.campaign')
      local p=mock.player(1);Campaign.arrive(p);mock.run(60)
      local camp=S.root().campaign.camps[1];assert(camp and camp.ship.valid)
      assert(not camp.ship.minable and not camp.ship.destructible and not camp.rocket_launched)
      for _,item in ipairs(C.landing_cargo) do assert(camp.ship.inventory[item[1]]==item[2],item[1]) end
      local turrets=game.surfaces[1].find_entities_filtered({name='gun-turret'})
      assert(#turrets==2 and turrets[1].inventory['firearm-magazine']==75)
      assert(#game.surfaces[1].find_entities_filtered({name='stone-wall'})==10)
      assert(mock.freeplay.disabled and mock.freeplay.skip)
      camp.ship.inventory['iron-plate']=3
      local p2=mock.player(2);Campaign.arrive(p2);Campaign.arrive(p);mock.configure();mock.run(120)
      assert(#game.surfaces[1].find_entities_filtered({name='sn-lander'})==1)
      assert(camp.ship.inventory['iron-plate']==3)
      assert(S.root().campaign.arrivals[2].done)
    ''')


def test_arrival_pan_ends_and_only_a_nauvis_rocket_unlocks_salvage(game_lua):
    prepare_landing(game_lua)
    game_lua.execute('''
      local S=require('scripts.state');local Campaign=require('scripts.campaign');local p=mock.player(1)
      p.character={valid=true};Campaign.arrive(p);mock.run(60)
      assert(p.controller_type==defines.controllers.cutscene and p.gui.screen.sn_landing_skip)
      mock.run(240);assert(p.controller_type==defines.controllers.character and not p.gui.screen.sn_landing_skip)
      local camp=S.root().campaign.camps[1]
      local v=mock.surface('vulcanus',2);Campaign.rocket({rocket=mock.entity('rocket',v)})
      assert(not camp.rocket_launched and not camp.ship.minable)
      Campaign.rocket({rocket=mock.entity('rocket',game.surfaces[1])})
      assert(camp.rocket_launched and camp.ship.minable)
    ''')


def test_existing_save_does_not_get_replacement_landing_or_sterilization(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local Campaign=require('scripts.campaign');local surface=game.surfaces[1]
      game.tick=90000;mock.configure()
      local p=mock.player(1);Campaign.arrive(p);Campaign.tick()
      local tree=mock.entity('tree-04',surface,{x=5,y=5},mock.neutral,true)
      surface.tile_name='grass-1'
      Campaign.chunk(surface,{x=0,y=0},{{0,0},{32,32}})
      assert(tree.valid and #surface.changed_tiles==0 and surface.pollution==0)
      assert(not S.root().campaign.active and not next(S.root().campaign.camps))
    ''')


def test_fresh_chunks_are_barren_and_smog_is_seeded_exactly_once(game_lua):
    prepare_landing(game_lua)
    game_lua.execute('''
      local Campaign=require('scripts.campaign');local s=game.surfaces[1];s.tile_name='grass-1'
      local tree=mock.entity('tree-04',s,{x=5,y=5},mock.neutral,true)
      local fish=mock.entity('fish',s,{x=6,y=6},mock.neutral,true)
      local mine=mock.entity('sn-air-scrubber',s,{x=8,y=8})
      Campaign.chunk(s,{x=0,y=0},{{0,0},{32,32}})
      assert(not tree.valid and not fish.valid and mine.valid)
      assert(s.get_tile({x=1,y=1}).name=='dry-dirt' and #s.changed_tiles==1024 and s.pollution==80)
      Campaign.chunk(s,{x=0,y=0},{{0,0},{32,32}})
      assert(s.pollution==80 and #s.changed_tiles==1024)
      local gleba=mock.surface('gleba',4);gleba.tile_name='grass-1'
      local jungle=mock.entity('tree-04',gleba,{x=2,y=2},mock.neutral,true)
      Campaign.chunk(gleba,{x=0,y=0},{{0,0},{32,32}})
      assert(jungle.valid and #gleba.changed_tiles==0 and gleba.pollution==0)
    ''')


def test_dirty_local_air_blocks_living_bonuses_but_not_physical_batches(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local s=game.surfaces[1];local e=mock.entity('sn-soil-enricher',s)
      s.pollution=50;e.products_finished=1;mock.run(240)
      local w=S.by_planet('nauvis');assert(w.cycles==1 and w.values.soil==0)
      s.pollution=0;e.products_finished=2;mock.run(240)
      assert(w.cycles==2 and w.values.soil>0)
    ''')


def test_global_pollution_and_complete_hotspot_survey_gate_maturity(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local P=require('scripts.pollution');local M=require('shared.model')
      local s=game.surfaces[1];local w=S.by_planet('nauvis')
      P.track(w,0,0);P.track(w,1,0)
      s.total_pollution=4000;s.pollution=1;s.local_pollution['16:16']=120
      P.sample(w,s);assert(w.air.total==4000 and w.air.mean==2000 and not w.air.survey_complete)
      P.step(w,s);P.step(w,s);assert(w.air.peak==120 and w.air.dirty==1 and w.air.survey_complete)
      for axis in pairs(w.values) do w.values[axis]=100 end;w.toxicity=0;M.refresh(w);assert(not M.ready(w))
      s.total_pollution=0;s.pollution=0;s.local_pollution={};P.sample(w,s)
      assert(not M.ready(w),'stale hot survey must not be bypassed')
      P.step(w,s);P.step(w,s);assert(M.ready(w))
      P.track(w,2,0);M.refresh(w);assert(not M.ready(w),'new territory must be surveyed')
    ''')


def test_deleted_chunks_never_get_regenerated_by_the_succession_worker(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local P=require('scripts.pollution');local w=S.by_planet('nauvis');local s=game.surfaces[1]
      P.track(w,0,0);s.generated=false
      s.get_tile=function() error('must not inspect a deleted chunk') end
      s.get_pollution=function() error('must not sample a deleted chunk') end
      assert(P.step(w,s)==nil and #w.chunks==0)
    ''')


def test_local_overlay_is_private_bounded_and_does_not_generate_chunks(game_lua):
    game_lua.execute('''
      local G=require('scripts.gui');local S=require('scripts.state');local p=mock.player(1);G.welcome(p)
      G.toggle_overlay(p);local prefs=S.root().players[1];assert(prefs.air_overlay and #prefs.air_render==25)
      for _,r in ipairs(prefs.air_render) do assert(r.spec.players[1]==1 and r.spec.time_to_live==150) end
      G.toggle_overlay(p);assert(not prefs.air_overlay and #prefs.air_render==0)
      for _,r in ipairs(mock.renders) do assert(not r.valid) end
    ''')


def test_succession_and_polluted_water_are_reversible_and_bounded(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local T=require('scripts.terrain');local w=S.by_planet('nauvis');local s=game.surfaces[1]
      settings.global['sn-living-terrain'].value=true;w.stage=4
      local chunk={x=0,y=0,stripe=0};s.tile_name='water'
      T.succession(w,s,chunk,100);assert(#s.changed_tiles==128 and s.get_tile({0,4}).name=='water-green')
      chunk.stripe=0;T.succession(w,s,chunk,0);assert(s.get_tile({0,4}).name=='water')
      s.tiles={};s.tile_name='dirt-1';s.changed_tiles={};chunk.stripe=0
      local ore=mock.entity('ore',s,{x=8,y=5},mock.neutral,true);ore.type='resource'
      s.tiles['0:4']='concrete'
      T.succession(w,s,chunk,0)
      assert(#s.changed_tiles>0 and #s.changed_tiles<=128 and s.get_tile({0,4}).name=='concrete')
      assert(s.get_tile({8,5}).name=='dirt-1' and ore.valid)
    ''')


def test_smog_cancels_a_warned_raid_and_turns_back_a_tracked_wave(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local R=require('scripts.resistance');local s=game.surfaces[1]
      local e=mock.entity('sn-air-scrubber',s);local rec=S.root().machines[e.unit_number]
      local w=S.by_planet('nauvis');w.pressure=90;w.first_operation=1;game.tick=300;rec.last_effect=game.tick
      settings.global['sn-grace-minutes'].value=0
      mock.entity('biter-spawner',s,{x=150,y=0},mock.enemy,true)
      R.tick(w,s);assert(w.warning)
      s.pollution=200;game.tick=game.tick+60;R.tick(w,s);assert(not w.warning and #w.groups==0)
      s.pollution=0;w.next_raid_check=0;rec.last_effect=game.tick;R.tick(w,s);assert(w.warning)
      game.tick=w.warning.at;R.tick(w,s);assert(#w.groups==1)
      assert(w.groups[1].group.command.type==defines.command.attack and w.groups[1].group.command.target==e)
      s.pollution=200;R.tick(w,s)
      assert(w.groups[1].retreated and w.groups[1].group.command.type==defines.command.go_to_location)
      assert(w.groups[1].group.command.distraction==defines.distraction.none)
    ''')


def test_dirty_industry_is_never_selected_as_a_restoration_raid_target(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local R=require('scripts.resistance');local s=game.surfaces[1]
      local e=mock.entity('sn-forcing-tower',s);local w=S.by_planet('nauvis')
      game.tick=300;w.pressure=100;w.first_operation=1;settings.global['sn-grace-minutes'].value=0
      S.root().machines[e.unit_number].last_effect=game.tick
      mock.entity('biter-spawner',s,{x=150,y=0},mock.enemy,true)
      R.tick(w,s);assert(not w.warning)
    ''')


def make_ready(lua):
    lua.execute('''
      local S=require('scripts.state');local M=require('shared.model');local w=S.by_planet('nauvis')
      for axis in pairs(w.values) do w.values[axis]=100 end
      w.toxicity=0;w.air.total=0;w.air.peak=0;w.air.mean=0;w.air.measured=true;w.air.survey_complete=true
      M.refresh(w);w.clean_since=0;game.tick=8000
    ''')


def test_native_choice_is_confirmed_admin_only_in_multiplayer_and_irreversible(game_lua):
    make_ready(game_lua)
    game_lua.execute('''
      local G=require('scripts.gui');local S=require('scripts.state');local w=S.by_planet('nauvis');local p=mock.player(1)
      mock.multiplayer=true;p.admin=false;G.open(p)
      assert(not p.gui.screen.sn_dashboard.sn_tabs.sn_air.sn_content.sn_fate_actions.sn_choose_symbiosis.enabled)
      assert(not require('scripts.natives').choose(w,'eradication',p) and not w.native_outcome)
      p.admin=true;G.update(p)
      G.click({player_index=1,element={valid=true,name='sn_choose_symbiosis'}})
      assert(S.root().players[1].pending_fate=='symbiosis' and not w.native_outcome)
      G.click({player_index=1,element={valid=true,name='sn_confirm_fate'}})
      assert(w.native_outcome.mode=='symbiosis')
      assert(not require('scripts.natives').choose(w,'eradication',p))
    ''')


def test_symbiosis_changes_shape_preserves_other_worlds_and_does_not_ally_hostile_forces(game_lua):
    make_ready(game_lua)
    game_lua.execute('''
      local S=require('scripts.state');local N=require('scripts.natives');local w=S.by_planet('nauvis');local s=game.surfaces[1]
      local b=mock.entity('small-biter',s,{x=4,y=4},mock.enemy,true)
      local n=mock.entity('biter-spawner',s,{x=10,y=10},mock.enemy,true)
      local worm=mock.entity('small-worm-turret',s,{x=20,y=20},mock.enemy,true)
      local gleba=mock.surface('gleba',4);local other=mock.entity('small-biter',gleba,{x=4,y=4},mock.enemy,true)
      assert(N.choose(w,'symbiosis',mock.player(1)));N.chunk(w,s,{x=0,y=0})
      assert(not b.valid and not n.valid and not worm.valid and other.valid)
      assert(#s.find_entities_filtered({name='sn-bloomback'})==1 and #s.find_entities_filtered({name='sn-bloom-nest'})==2)
      local friend=game.forces['sn-symbiosis'];assert(friend and friend.get_friend(mock.player_force))
      assert(not mock.enemy.get_friend(mock.player_force))
      local processed=w.native_outcome.processed;N.chunk(w,s,{x=0,y=0});assert(w.native_outcome.processed==processed)
    ''')


def test_eradication_sweeps_are_bounded_and_future_chunks_inherit_the_choice(game_lua):
    make_ready(game_lua)
    game_lua.execute('''
      local S=require('scripts.state');local N=require('scripts.natives');local w=S.by_planet('nauvis');local s=game.surfaces[1]
      for i=1,80 do mock.entity('small-biter',s,{x=4,y=4},mock.enemy,true) end
      local owned=mock.entity('small-biter',s,{x=8,y=8},mock.player_force,true)
      assert(N.choose(w,'eradication',mock.player(1)))
      N.chunk(w,s,{x=0,y=0});assert(w.native_outcome.processed==32 and owned.valid)
      N.chunk(w,s,{x=0,y=0});N.chunk(w,s,{x=0,y=0});assert(w.native_outcome.processed==80)
      S.root().campaign.active=true
      local next_nest=mock.entity('biter-spawner',s,{x=40,y=10},mock.enemy,true)
      mock.event('on_chunk_generated',{surface=s,position={x=1,y=0},area={{32,0},{64,32}}})
      assert(not next_nest.valid and s.pollution==0 and w.native_outcome.processed==81)
    ''')


def test_new_survey_invalidates_readiness_without_waiting_for_a_model_tick(game_lua):
    make_ready(game_lua)
    game_lua.execute('''
      local S=require('scripts.state');local M=require('shared.model');local w=S.by_planet('nauvis')
      assert(M.ready(w));require('scripts.pollution').track(w,10,10)
      assert(not M.ready(w) and not require('scripts.natives').available(w))
    ''')


def test_calm_is_gradual_and_does_not_apply_when_the_startup_rule_is_disabled(game_lua):
    game_lua.execute('''
      local P=require('scripts.pollution');local s=game.surfaces[1]
      s.pollution=100;assert(P.calm(s,{0,0})==0.5)
      s.pollution=200;assert(P.calm(s,{0,0})==1)
      settings.startup['sn-biter-metabolism'].value=false;assert(P.calm(s,{0,0})==0)
    ''')


def test_two_clean_minutes_are_required_and_regression_restarts_the_hold(game_lua):
    make_ready(game_lua)
    game_lua.execute('''
      local S=require('scripts.state');local N=require('scripts.natives');local M=require('shared.model');local w=S.by_planet('nauvis')
      game.tick=7199;assert(not N.available(w));game.tick=7200;assert(N.available(w))
      w.air.total=501;M.refresh(w);N.tick(w);assert(not w.clean_since and not N.available(w))
      w.air.total=0;M.refresh(w);N.tick(w);assert(w.clean_since==game.tick and not N.available(w))
      game.tick=game.tick+7200;assert(N.available(w))
    ''')


def test_canceling_native_choice_never_changes_the_world(game_lua):
    make_ready(game_lua)
    game_lua.execute('''
      local G=require('scripts.gui');local S=require('scripts.state');local p=mock.player(1);G.open(p)
      G.click({player_index=1,element={valid=true,name='sn_choose_eradication'}})
      assert(S.root().players[1].pending_fate=='eradication')
      G.click({player_index=1,element={valid=true,name='sn_cancel_fate'}})
      assert(not S.by_planet('nauvis').native_outcome and not S.root().players[1].pending_fate)
    ''')


def test_mobile_natives_cannot_escape_resolution_by_outrunning_the_chunk_survey(game_lua):
    make_ready(game_lua)
    game_lua.execute('''
      local S=require('scripts.state');local N=require('scripts.natives');local s=game.surfaces[1];local w=S.by_planet('nauvis')
      local b=mock.entity('small-biter',s,{x=4,y=4},mock.enemy,true)
      assert(N.choose(w,'symbiosis',mock.player(1)))
      b.position={x=300,y=300};N.tick(w)
      assert(not b.valid and w.native_outcome.pending==0)
      assert(s.find_entities_filtered({name='sn-bloomback'})[1].position.x==300)
      local newborn=mock.entity('small-biter',s,{x=500,y=500},mock.enemy,true)
      mock.event('on_entity_spawned',{entity=newborn})
      assert(not newborn.valid and w.native_outcome.processed==2)
      local snapshot=remote.call('second_nature','get_world','nauvis')
      assert(snapshot.native_queue==nil and snapshot.native_outcome.pending==0)
    ''')


def test_local_gardens_cannot_spread_into_a_polluted_neighbor_chunk(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local T=require('scripts.terrain');local s=game.surfaces[1]
      local e=mock.entity('sn-seed-disperser',s);local rec=S.root().machines[e.unit_number];local w=S.by_planet('nauvis')
      settings.global['sn-living-terrain'].value=true;w.stage=4
      s.get_pollution=function(pos) return pos.x==0 and pos.y==0 and 0 or 100 end
      T.apply(rec,w,{terrain=true,trees=true},10)
      assert(#s.changed_tiles==0 and w.grown_trees==0)
    ''')


def test_pollution_index_ignores_engine_known_but_ungenerated_chunks(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local P=require('scripts.pollution');local s=game.surfaces[1];local w=S.by_planet('nauvis')
      s.chunks={{x=0,y=0},{x=1,y=0},{x=2,y=0}}
      s.is_chunk_generated=function(pos) return (pos.x or pos[1])~=1 end
      P.index(w,s);assert(#w.chunks==2 and not w.chunk_keys['1:0'])
      P.step(w,s);P.step(w,s);assert(w.air.survey_complete)
    ''')


def test_chunk_deletion_does_not_restart_a_large_survey(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local P=require('scripts.pollution');local s=game.surfaces[1];local w=S.by_planet('nauvis')
      for i=0,99 do P.track(w,i,0) end
      s.is_chunk_generated=function(pos) return (pos.x or pos[1])%3~=0 end
      for _=1,100 do P.step(w,s) end
      assert(#w.chunks==66 and w.air.survey_complete)
    ''')
