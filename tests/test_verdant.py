import math,json
from pathlib import Path
import pytest
from catalog import ROOT,MOD,load_catalog
from factorio_data import DataStage

@pytest.fixture(scope='module')
def verdant_data():
    path=ROOT/'.cache/factorio-data-2.0.77'
    if not path.exists():pytest.skip('Stable data checkout required')
    return DataStage(path)

def test_ik_keeps_leg_bones_constant_while_knees_bend_and_feet_lift():
    from explorer_model import explorer
    from gait import length,sub,THIGH,SHIN,knee_flexion
    for direction in (0,math.pi/2,math.pi,3*math.pi/2):
        flex=[];ankle=[]
        for frame in range(32):
            m=explorer(frame/32,'running',0,direction,direction)
            for side in (-1,1):
                hip=m.joints['hip-'+str(side)];knee=m.joints['knee-'+str(side)];foot=m.joints['ankle-'+str(side)]
                assert abs(length(sub(hip,knee))-THIGH)<1e-6
                assert abs(length(sub(knee,foot))-SHIN)<1e-6
                flex.append(knee_flexion(hip,knee,foot));ankle.append(foot[2])
                if m.foot_phases[side]['mode']=='stance':assert abs(foot[2]-.115)<1e-7
        assert max(flex)>75 and max(flex)-min(flex)>35
        assert max(ankle)-min(ankle)>.24

def test_stance_foot_motion_matches_the_authored_root_speed():
    from gait import foot_phase,STANCE,STEP_SPAN
    # While grounded, relative foot velocity exactly cancels constant root motion.
    for phase in (.05,.15,.30,.50):
        a=foot_phase(phase,-1);b=foot_phase(phase+.001,-1)
        speed=(b['along']-a['along'])/.001
        assert abs(speed+STEP_SPAN/STANCE)<1e-7
        assert a['lift']==0 and b['lift']==0

def test_visible_gloves_have_four_articulated_fingers_and_a_thumb():
    from explorer_model import explorer
    from gait import length,sub
    for pose in ('idle','running','idle_with_gun','mining_with_tool'):
        mesh=explorer(.25,pose,0,math.pi/2,math.pi/2)
        assert len(mesh.hands)==2
        for hand in mesh.hands.values():
            for finger in range(4):
                points=[hand[f'finger-{finger}-{i}'] for i in range(4)]
                assert sum(length(sub(a,b)) for a,b in zip(points,points[1:]))>.08
            assert all('thumb-'+str(i) in hand for i in range(3))
            assert length(sub(hand['palm'],hand['wrist']))>.06

def test_mining_animation_is_faster_without_changing_mining_mechanics(verdant_data):
    p=verdant_data.raw.character.character
    animation=p.animations[1].mining_with_tool
    assert animation.frame_count==20
    assert animation.frame_count/animation.animation_speed<.80*(16/.15)
    assert p.mining_speed==.5
    assert p.animations[1].running.frame_count==16
    assert abs(p.distance_per_frame-.088205645161)<1e-10


def test_complex_plants_are_larger_and_items_place_the_canonical_entities(verdant_data):
    data=verdant_data.raw
    expanded=0
    for m in load_catalog()['machines']:
        p=data[m.get('entity_type','assembling-machine')][m['entity_name']]
        assert data.item['sn-'+m['name']].place_result==m['entity_name']
        if m['footprint']>m['previous_footprint']:
            expanded+=1
            assert p.tile_width==m['footprint'] and p.tile_height==m['footprint']
            assert p.selection_box[2][1]==m['footprint']/2
            assert p.minable.results[1].name=='sn-'+m['name'] if p.minable.results else p.minable.result=='sn-'+m['name']
    assert expanded>=12
    assert data['assembling-machine']['sn-sanctuary-plant'].tile_width==7


def test_existing_compact_plants_keep_collision_ports_and_blueprint_items(verdant_data):
    ports=json.loads((ROOT/'docs/art/compact-fluid-ports.json').read_text())
    data=verdant_data.raw
    for m in load_catalog()['machines']:
        if m['footprint']==m['previous_footprint']:continue
        legacy=data['assembling-machine']['sn-'+m['name']]
        assert legacy and legacy.hidden_in_factoriopedia is True
        half=2.4 if m['previous_footprint']==5 else 1.2
        assert legacy.collision_box[2][1]==half
        assert legacy.placeable_by.item=='sn-'+m['name']
        for expected in ports[m['name']]:
            p=legacy.fluid_boxes[expected['box']].pipe_connections[1]
            assert list(p.position.values())==expected['position'] and p.direction==expected['direction']


def test_runtime_reindex_and_network_recognize_large_and_compact_beacons(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local s=game.surfaces[1]
      local large=mock.entity('sn-planetary-beacon-plant',s)
      local compact=mock.entity('sn-planetary-beacon',s,{x=20,y=0})
      local world=S.by_planet('nauvis')
      assert(world.beacon_ids[large.unit_number] and world.beacon_ids[compact.unit_number])
      local before=world.machine_count;mock.configure();assert(world.machine_count==before)
      assert(S.root().machines[large.unit_number] and S.root().machines[compact.unit_number])
    ''')


def test_larger_working_model_bounds_and_native_ports_match(verdant_data):
    from industrial_art import machine,rot
    ports=json.loads((ROOT/'docs/art/fluid-ports.json').read_text())
    for m in load_catalog()['machines']:
        if m['footprint']<=3:continue
        entity=verdant_data.raw['assembling-machine'][m['entity_name']]
        model=machine(m['name'],.25)
        assert len(model.port_anchors)==len(ports[m['name']])
        for port,anchor in zip(ports[m['name']],model.port_anchors):
            expected=entity.fluid_boxes[port['box']].pipe_connections[1]
            dx,dy={0:(0,-1),4:(1,0),8:(0,1),12:(-1,0)}[port['direction']]
            for q in range(4):
                actual=rot(anchor['position'],q*math.pi/2)
                wanted=rot((expected.position[1]+dx*.5,expected.position[2]+dy*.5,0),q*math.pi/2)
                assert all(abs(a-b)<1e-8 for a,b in zip(actual,wanted))
