from pathlib import Path
import pytest
from catalog import ROOT, MOD, load_catalog, plain
from factorio_data import DataStage


@pytest.fixture(scope='module')
def expedition_data():
    path=ROOT/'.cache/factorio-data-2.0.77'
    if not path.exists():pytest.skip('Pinned stable data is required')
    return DataStage(path)


def test_all_early_structural_wood_dependencies_have_mineral_routes(expedition_data):
    data=expedition_data.raw
    for name in ('small-electric-pole','wooden-chest','shotgun','combat-shotgun','sn-seed-mix'):
        assert all(i.name!='wood' for i in data.recipe[name].ingredients.values()),name
    assert data.recipe['small-electric-pole'].enabled is True
    assert data.recipe['sn-alloy-stock'].enabled is True
    assert {i.name for i in data.recipe['sn-alloy-stock'].ingredients.values()}=={'iron-plate','stone'}
    assert data.recipe['sn-ballistic-magazine'].enabled is True
    assert any(i.name=='wood' for i in data.recipe['sn-wood-compost'].ingredients.values()),'optional wood recovery is not banned'


def test_all_introduced_building_primary_art_is_original(expedition_data):
    def filenames(node):
        if not hasattr(node,'items'):return
        for k,v in node.items():
            if k=='filename':yield v
            else:yield from filenames(v)
    data=expedition_data.raw
    for machine in load_catalog()['machines']:
        entity=data[machine.get('entity_type','assembling-machine')]['sn-'+machine['name']]
        paths=list(filenames(entity.graphics_set or entity.sprites))
        assert paths and all(path.startswith('__second-nature__/graphics/entity/industry/') for path in paths)
    for kind,name in [('ammo-turret','sn-sentry-turret'),('electric-turret','sn-arc-turret'),('ammo-turret','sn-lance-turret')]:
        p=data[kind][name]
        assert p.attacking_animation.frame_count==4 and p.attacking_animation.direction_count==64
        assert p.graphics_set is not None and len(p.graphics_set)==0
    assert data.container['sn-lander'].minable is None
    assert '__second-nature__' in data.container['sn-lander'].picture.filename


def test_explorer_covers_armor_tool_and_armed_locomotion_variations(expedition_data):
    char=expedition_data.raw.character.character
    for variation in char.animations.values():
        for pose in ('idle','idle_with_gun','running','running_with_gun','mining_with_tool'):
            assert variation[pose].filename.startswith('__second-nature__/')
        assert variation.running_with_gun.direction_count==18
        assert variation.running.frame_count==12
        assert variation.flipped_shadow_running_with_gun is None
    assert 'sn-expedition-armor' in list(char.animations[2].armors.values())
    assert 'sn-bastion-armor' in list(char.animations[3].armors.values())
    assert expedition_data.raw['character-corpse']['character-corpse'].armor_picture_mapping['sn-bastion-armor']==3


def test_weapons_and_defenses_have_ammo_energy_and_progression_contracts(expedition_data):
    data=expedition_data.raw
    assert data.gun['sn-carbine'].attack_parameters.ammo_category=='bullet'
    assert data['ammo-turret']['sn-sentry-turret'].attack_parameters.ammo_category=='bullet'
    assert data.gun['sn-induction-rifle'].attack_parameters.ammo_category==data.ammo['sn-induction-cell'].ammo_category
    assert data['electric-turret']['sn-arc-turret'].energy_source.input_flow_limit=='4MW'
    assert data['ammo-turret']['sn-lance-turret'].energy_source is not None
    assert data['ammo-turret']['sn-lance-turret'].energy_per_shot is not None
    assert data.armor['sn-expedition-armor'].equipment_grid=='sn-expedition-grid'
    assert data['equipment-grid']['sn-expedition-grid'].width==6
    assert data['equipment-grid']['sn-bastion-grid'].width==10
    assert data.capsule['sn-field-dressing'] is not None
    assert len(data.technology['sn-restoration-efficiency-3'].prerequisites)>0
    assert data.technology['sn-restoration-efficiency-3'].max_level is None
    assert data.technology['sn-restoration-efficiency-3'].effects[1].effect_description[2]=='45'


def test_full_recovery_is_not_a_fast_or_instant_paintbrush(lua):
    lua.execute('''
      local H=require('shared.succession');local M=require('shared.model');local w=M.new('nauvis')
      for k in pairs(w.values) do w.values[k]=100 end
      local c={cover=0,stress=0}
      H.advance(c,w,0,10000,1,false);assert(c.cover<.06,'offline time must not instantly grow a forest')
      for i=2,18 do H.advance(c,w,0,10,1,false) end
      assert(c.cover>.99 and c.cover<=1)
    ''')


def test_heavy_pollution_reverses_mature_habitat_gradually(lua):
    lua.execute('''
      local H=require('shared.succession');local M=require('shared.model');local w=M.new('nauvis')
      for k in pairs(w.values) do w.values[k]=100 end
      local c={cover=1,stress=0}
      H.advance(c,w,250,1,1,false);assert(c.cover>.99 and c.stress<.1)
      for i=1,14 do H.advance(c,w,250,10,1,false) end
      assert(c.cover==0 and c.stress==1)
      H.advance(c,w,0,10,1,false);assert(c.cover<.06,'cleanup cannot instantly undo prolonged damage')
    ''')


def test_optimization_is_bounded_and_never_accelerates_damage(lua):
    lua.execute('''
      local H=require('shared.succession');local M=require('shared.model');local w=M.new('nauvis')
      for k in pairs(w.values) do w.values[k]=100 end
      local a={cover=0,stress=0};local b={cover=0,stress=0}
      H.advance(a,w,0,10,1,false);H.advance(b,w,0,10,999,false)
      assert(math.abs(b.cover/a.cover-1.45)<.00001)
      a={cover=1,stress=1};b={cover=1,stress=1}
      H.advance(a,w,250,10,1,false);H.advance(b,w,250,10,1.45,false)
      assert(a.cover==b.cover)
    ''')


def test_upgrades_are_force_specific_and_reversal_updates_the_cache(game_lua):
    game_lua.execute('''
      local U=require('scripts.upgrades');local f=mock.player_force
      f.technologies['sn-restoration-efficiency-1']={researched=true}
      f.technologies['sn-restoration-efficiency-2']={researched=true}
      f.technologies['sn-restoration-efficiency-3']={researched=true}
      mock.event('on_research_finished',{research={force=f}});assert(U.bonus(f)==1.45)
      local other=mock.force(4,'other');assert(U.bonus(other)==1)
      f.technologies['sn-restoration-efficiency-3'].researched=false
      mock.event('on_research_reversed',{research={force=f}});assert(U.bonus(f)==1.30)
    ''')


def test_slow_capture_and_research_work_on_real_completion_deltas(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local U=require('scripts.upgrades');local s=game.surfaces[1]
      local e=mock.entity('sn-air-scrubber',s);s.pollution=100;e.products_finished=1;mock.run(240)
      assert(s.pollution==90 and S.by_planet('nauvis').cycles==1)
      mock.player_force.technologies['sn-restoration-efficiency-3']={researched=true};U.refresh(mock.player_force)
      e.products_finished=2;mock.run(240);assert(math.abs(s.pollution-75.5)<.00001)
    ''')


def test_visual_toggle_does_not_disable_the_habitat_simulation(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local T=require('scripts.terrain');local s=game.surfaces[1];local w=S.by_planet('nauvis')
      for k in pairs(w.values) do w.values[k]=100 end;w.stage=4
      local chunk={x=0,y=0,cover=0,stress=0,ecology_tick=0,land=true,trees={}}
      settings.global['sn-living-terrain'].value=false;game.tick=10*3600
      T.succession(w,s,chunk,0)
      assert(chunk.cover>0 and chunk.cover<.06 and #s.changed_tiles==0)
    ''')


def test_landscape_maturity_is_a_real_final_gate(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local M=require('shared.model');local w=S.by_planet('nauvis')
      for k in pairs(w.values) do w.values[k]=100 end;w.toxicity=0
      w.landscape={mean=.79,measured=true};M.refresh(w);assert(w.stage==4 and not M.ready(w))
      w.landscape.mean=.8;M.refresh(w);assert(M.ready(w))
    ''')


def test_withering_removes_only_tracked_restoration_trees(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local T=require('scripts.terrain');local s=game.surfaces[1];local w=S.by_planet('nauvis')
      local ours=mock.entity('tree-04',s,{x=10,y=10},mock.neutral,true)
      local player_tree=mock.entity('tree-04',s,{x=20,y=20},mock.neutral,true)
      local c={x=0,y=0,cover=.2,stress=1,ecology_tick=0,land=true,trees={ours},stripe=0}
      settings.global['sn-living-terrain'].value=true;game.tick=60
      T.succession(w,s,c,250)
      assert(not ours.valid and player_tree.valid and w.withered_trees==1)
    ''')


def test_pole_direction_count_matches_its_wire_positions(expedition_data):
    p=expedition_data.raw['electric-pole']['small-electric-pole']
    assert p.pictures.direction_count==len(p.connection_points)


def test_mod_owned_withered_trees_can_recover_without_touching_other_trees(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local T=require('scripts.terrain');local s=game.surfaces[1];local w=S.by_planet('nauvis')
      for k in pairs(w.values) do w.values[k]=100 end;w.stage=4
      local stump=mock.entity('dead-dry-hairy-tree',s,{x=10,y=10},mock.neutral,true)
      local other=mock.entity('tree-04',s,{x=25,y=25},mock.neutral,true)
      local c={x=0,y=0,cover=.9,stress=0,ecology_tick=36000,land=true,trees={},dead_trees={stump},stripe=0}
      settings.global['sn-living-terrain'].value=true;settings.global['sn-tree-growth'].value=true;game.tick=36000
      T.succession(w,s,c,0)
      assert(not stump.valid and other.valid and #c.trees==1 and #c.dead_trees==0)
    ''')
