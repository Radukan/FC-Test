import hashlib
import json
from pathlib import Path

import pytest
from PIL import Image
from catalog import ROOT, MOD, plain
from factorio_data import DataStage


@pytest.fixture
def drone_lua(game_lua):
    game_lua.execute((ROOT/'tests/drone_fixture.lua').read_text())
    game_lua.execute('''
      D=require('scripts.field_drones');S=require('scripts.state')
      function enable(p)
        assert(D.set_enabled(p,true));S.root().field_drones.owners[p.index].cell=10
      end
    ''')
    return game_lua


@pytest.fixture(scope='module')
def drone_data():
    path=ROOT/'.cache/factorio-data-2.0.77'
    if not path.exists():pytest.skip('Pinned stable prototype data required')
    return DataStage(path)


def test_cheap_red_science_construction_has_no_network_or_roboport_prototype(drone_data):
    data=drone_data.raw
    tech=data.technology['sn-field-robotics']
    assert list(tech.prerequisites.values())==['automation']
    assert tech.unit.count==20 and tech.unit.time==15
    ingredients=plain(tech.unit.ingredients)
    assert ingredients==[['automation-science-pack',1]]
    for name in ('sn-field-drone','sn-field-controller'):
        item=data.item[name]
        assert item and item.place_result is None and item.placed_as_equipment_result is None
        recipe=data.recipe[name]
        assert recipe.enabled is False and recipe.allow_quality is False
        assert all(i.name in {'iron-plate','iron-gear-wheel','electronic-circuit','copper-cable'} for i in recipe.ingredients.values())
        assert data['construction-robot'][name] is None and data['logistic-robot'][name] is None
    assert data.item['sn-field-drone'].stack_size==200
    assert data['simple-entity-with-owner']['sn-field-drone-worker']
    assert data['simple-entity-with-owner']['sn-field-drone-worker'].minable is None


def test_drone_sprite_specs_and_assets_are_complete_and_original():
    report=json.loads((ROOT/'docs/art/drone-manifest.json').read_text())
    for name,digest in report['files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    for spec in report['specs'].values():
        image=Image.open(MOD/spec['filename'].split('__second-nature__/')[1])
        assert image.size==(spec['width']*8,spec['height']) and image.mode=='RGBA'
        assert spec['apply_projection'] is False
        frames=set()
        for i in range(8):
            frame=image.crop((i*spec['width'],0,(i+1)*spec['width'],spec['height']))
            frames.add(hashlib.sha256(frame.tobytes()).hexdigest())
            box=frame.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()
            assert min(box[0],box[1],spec['width']-box[2],spec['height']-box[3])>=2
        assert len(frames)>1


def test_real_material_is_reserved_at_launch_and_not_built_instantly(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);local ghost=mock.ghost(p,'stone-wall',{x=5,y=2})
      enable(p);mock.drone_steps(30)
      assert(S.root().field_drones.active==1 and ghost.valid and #mock.revivals==0)
      assert(p.inventory.get_item_count('stone-wall')==0 and p.inventory.get_item_count('sn-field-drone')==0)
      local worker=next(S.root().field_drones.workers)
      local r=S.root().field_drones.workers[worker]
      assert(r.cargo.get_item_count('stone-wall')==1 and r.entity.logistic_network==nil)
      mock.drone_steps(1200)
      assert(not ghost.valid and #mock.revivals==1)
      assert(p.inventory.get_item_count('stone-wall')==0 and p.inventory.get_item_count('sn-field-drone')==1)
      assert(not r.cargo.valid and S.root().field_drones.active==0 and not next(S.root().field_drones.claims))
    ''')


def test_requires_research_controller_character_and_actual_materials(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);local ghost=mock.ghost(p,'stone-wall',{x=3,y=3})
      p.force.technologies['sn-field-robotics'].researched=false;assert(not D.set_enabled(p,true))
      p.force.technologies['sn-field-robotics'].researched=true
      p.inventory.remove({name='sn-field-controller',count=1});assert(not D.set_enabled(p,true))
      p.inventory.insert({name='sn-field-controller',count=1})
      p.controller_type=defines.controllers.remote;assert(not D.set_enabled(p,true))
      p.controller_type=defines.controllers.character;p.surface.platform={};assert(not D.set_enabled(p,true));p.surface.platform=nil
      p.inventory.remove({name='stone-wall',count=1});enable(p);mock.drone_steps(1200)
      assert(ghost.valid and S.root().field_drones.active==0 and p.inventory.get_item_count('sn-field-drone')==1)
    ''')


def test_multiple_operators_cannot_double_claim_or_pay_for_one_ghost(drone_lua):
    drone_lua.execute('''
      local a=mock.drone_player(1);local b=mock.drone_player(2)
      local ghost=mock.ghost(a,'stone-wall',{x=5,y=2});enable(a);enable(b)
      mock.drone_steps(1200)
      assert(#mock.revivals==1 and not ghost.valid)
      assert(a.inventory.get_item_count('stone-wall')+b.inventory.get_item_count('stone-wall')==1)
      assert(a.inventory.get_item_count('sn-field-drone')+b.inventory.get_item_count('sn-field-drone')==2)
    ''')


def test_cancelled_ghost_returns_both_reserved_items_exactly_once(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);local ghost=mock.ghost(p,'stone-wall',{x=8,y=2})
      enable(p);mock.drone_steps(30);assert(S.root().field_drones.active==1)
      ghost.valid=false;mock.drone_steps(1200);D.cancel(1);D.cancel(1)
      assert(#mock.revivals==0 and p.inventory.get_item_count('stone-wall')==1 and p.inventory.get_item_count('sn-field-drone')==1)
      assert(S.root().field_drones.active==0)
    ''')


@pytest.mark.parametrize('cause',['blocked','revive_error'])
def test_failed_revival_refunds_instead_of_creating_free_entities(drone_lua,cause):
    drone_lua.execute(f'''
      local p=mock.drone_player(1);local ghost=mock.ghost(p,'stone-wall',{{x=3,y=2}})
      ghost.{cause}=true;enable(p);mock.drone_steps(420);D.set_enabled(p,false)
      assert(ghost.valid and #mock.revivals==0 and S.root().field_drones.active==0)
      assert(p.inventory.get_item_count('stone-wall')==1 and p.inventory.get_item_count('sn-field-drone')==1)
    ''')


def test_inventory_overflow_spills_exact_reserved_quality_instead_of_losing_it(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1,1,1,'rare');local g=mock.ghost(p,'stone-wall',{x=5,y=2},'rare')
      enable(p);mock.drone_steps(30)
      p.inventory.insert({name='iron-plate',count=8000})
      D.set_enabled(p,false)
      assert(mock.spill_count('sn-field-drone','rare')==1 and mock.spill_count('stone-wall','rare')==1)
      assert(S.root().field_drones.active==0 and #mock.revivals==0)
    ''')


def test_matching_quality_is_required_and_specialized_packed_items_are_left_alone(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1,2,2);local rare=mock.ghost(p,'stone-wall',{x=3,y=2},'rare')
      local special=mock.ghost(p,'packed-vehicle',{x=4,y=2})
      p.inventory.insert({name='packed-vehicle',count=1})
      enable(p);mock.drone_steps(900)
      assert(rare.valid and special.valid and #mock.revivals==0)
      p.inventory.insert({name='stone-wall',quality='rare',count=1});mock.drone_steps(1200)
      assert(not rare.valid and special.valid and #mock.revivals==1)
      assert(mock.revivals[1].quality=='rare' and p.inventory.get_item_count('stone-wall')==2)
      assert(p.inventory.get_item_count('packed-vehicle')==1)
    ''')


def test_tile_ghosts_consume_the_real_tile_item(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);p.inventory.insert({name='stone-brick',count=1})
      local ghost=mock.ghost(p,'stone-path',{x=2.5,y=2.5},nil,true)
      enable(p);mock.drone_steps(1200)
      assert(not ghost.valid and #mock.revivals==1 and mock.revivals[1].tile)
      assert(p.inventory.get_item_count('stone-brick')==0 and p.inventory.get_item_count('sn-field-drone')==1)
    ''')


def test_no_foreign_out_of_range_or_loose_item_work(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1,4,4)
      local foreign=mock.ghost(p,'stone-wall',{x=2,y=2});foreign.force=mock.enemy
      local far=mock.ghost(p,'stone-wall',{x=25,y=25})
      local blocked=mock.ghost(p,'stone-wall',{x=4,y=2})
      local dropped=mock.entity('item-on-ground',p.surface,{x=4,y=2},mock.neutral,true);dropped.type='item-entity'
      enable(p);mock.drone_steps(1200)
      assert(foreign.valid and far.valid and blocked.valid and dropped.valid and #mock.revivals==0)
      assert(p.inventory.get_item_count('stone-wall')==4)
      dropped.valid=false;mock.drone_steps(1200)
      assert(not blocked.valid and foreign.valid and far.valid and #mock.revivals==1)
    ''')


@pytest.mark.parametrize('event',['on_pre_player_died','on_player_left_game','on_player_changed_surface','on_player_controller_changed','on_player_changed_force'])
def test_owner_transitions_recall_reservations_without_duplication(drone_lua,event):
    drone_lua.execute(f'''
      local p=mock.drone_player(1);mock.ghost(p,'stone-wall',{{x=6,y=2}})
      enable(p);mock.drone_steps(30);assert(S.root().field_drones.active==1)
      mock.event('{event}',{{player_index=1}})
      assert(S.root().field_drones.active==0 and p.inventory.get_item_count('sn-field-drone')==1 and p.inventory.get_item_count('stone-wall')==1)
    ''')


def test_destroyed_drone_is_lost_but_unspent_material_is_recoverable(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);mock.ghost(p,'stone-wall',{x=6,y=2})
      enable(p);mock.drone_steps(30)
      local _,r=next(S.root().field_drones.workers)
      mock.event('on_entity_died',{entity=r.entity});r.entity.valid=false
      mock.drone_steps(60)
      assert(S.root().field_drones.active==0 and p.inventory.get_item_count('sn-field-drone')==0)
      assert(mock.spill_count('stone-wall')==1 and mock.spill_count('sn-field-drone')==0)
    ''')


def test_configuration_preserves_active_escrow_and_does_not_grant_another_drone(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);mock.ghost(p,'stone-wall',{x=6,y=2})
      enable(p);mock.drone_steps(30)
      local id,r=next(S.root().field_drones.workers);local cargo=r.cargo
      mock.configure();mock.configure()
      assert(S.root().field_drones.workers[id].cargo==cargo and cargo.valid and S.root().field_drones.active==1)
      mock.drone_steps(1200)
      assert(#mock.revivals==1 and p.inventory.get_item_count('sn-field-drone')==1 and not cargo.valid)
    ''')


def test_dense_blueprint_uses_a_large_crew_but_dispatch_work_is_bounded(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1,100,100)
      for x=1,8 do for y=1,8 do mock.ghost(p,'stone-wall',{x=x,y=y}) end end
      enable(p);mock.drone_steps(30)
      assert(S.root().field_drones.active==8,'one dispatch step is bounded')
      mock.drone_steps(42)
      assert(S.root().field_drones.active==64,'queue should support a full large crew')
      settings.get_player_settings=function() return {['sn-field-drone-limit']={value=1}} end
      mock.drone_steps(6);assert(S.root().field_drones.active==1)
      D.set_enabled(p,false)
      assert(p.inventory.get_item_count('sn-field-drone')==100 and p.inventory.get_item_count('stone-wall')==100)
    ''')


def test_gui_toggle_is_namespaced_and_closing_it_does_not_recall_the_crew(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);mock.ghost(p,'stone-wall',{x=6,y=2})
      mock.handlers['sn-toggle-field-drones']({player_index=1})
      assert(p.gui.left.sn_field_drones and D.status(p).enabled)
      S.root().field_drones.owners[1].cell=10;mock.drone_steps(30)
      local close=p.gui.left.sn_field_drones.sn_drone_buttons.sn_drone_close
      mock.event('on_gui_click',{player_index=1,element=close})
      assert(not p.gui.left.sn_field_drones and D.status(p).enabled and S.root().field_drones.active==1)
      mock.handlers['sn-toggle-field-drones']({player_index=1})
      assert(p.gui.left.sn_field_drones and not D.status(p).enabled and S.root().field_drones.active==0)
    ''')


def test_build_permissions_are_enforced(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1)
      p.permission_group={allows_action=function() return false end}
      assert(not D.set_enabled(p,true) and D.status(p).reason=='permission')
      p.permission_group={allows_action=function(action) return action~=defines.input_action.build_terrain end}
      p.inventory.insert({name='stone-brick',count=1})
      local tile=mock.ghost(p,'stone-path',{x=2.5,y=2.5},nil,true)
      enable(p);mock.drone_steps(900)
      assert(tile.valid and p.inventory.get_item_count('stone-brick')==1)
    ''')


def test_return_restores_both_render_layers_after_a_render_clear(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);mock.ghost(p,'stone-wall',{x=8,y=2})
      enable(p);mock.drone_steps(30);local _,rec=next(S.root().field_drones.workers)
      assert(rec.visual.spec.render_layer=='air-object' and rec.shadow.spec.render_layer=='ground-patch-higher')
      local old_body,old_shadow=rec.visual,rec.shadow
      rendering.clear();mock.drone_steps(3)
      assert(not old_body.valid and not old_shadow.valid and rec.visual.valid and rec.shadow.valid)
      D.set_enabled(p,false);assert(not rec.visual.valid and not rec.shadow.valid and not rec.cargo.valid)
    ''')


def test_unreachable_teleport_and_surface_cleanup_return_the_reservation(drone_lua):
    drone_lua.execute('''
      local p=mock.drone_player(1);mock.ghost(p,'stone-wall',{x=8,y=2})
      enable(p);mock.drone_steps(30);local _,rec=next(S.root().field_drones.workers)
      rec.entity.teleport_blocked=true;mock.drone_steps(3)
      assert(S.root().field_drones.active==0 and p.inventory.get_item_count('sn-field-drone')==1)
      S.root().field_drones.owners[1].cell=10;game.tick=60;D.step_player(p)
      assert(S.root().field_drones.active==1)
      mock.event('on_pre_surface_cleared',{surface_index=p.surface.index})
      assert(S.root().field_drones.active==0 and p.inventory.get_item_count('stone-wall')==1)
    ''')
