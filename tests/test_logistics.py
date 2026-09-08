import pytest
from pathlib import Path
from catalog import ROOT
from factorio_data import DataStage

@pytest.fixture(scope='module')
def advanced_data():
    path=ROOT/'.cache/factorio-data-2.0.77'
    if not path.exists():pytest.skip('Pinned stable data required')
    return DataStage(path)

def test_all_inserters_support_native_custom_vectors(advanced_data):
    for name,p in advanced_data.raw.inserter.items():assert p.allow_custom_vectors is True,name

def test_endgame_belt_family_has_matched_speed_and_correct_links(advanced_data):
    data=advanced_data.raw
    a=data['transport-belt']['sn-vital-belt'];b=data['underground-belt']['sn-vital-underground-belt'];c=data.splitter['sn-vital-splitter']
    assert a.speed==b.speed==c.speed==.1875
    assert a.related_underground_belt==b.name and c.related_transport_belt==a.name
    assert b.max_distance==16
    assert data.inserter['sn-vector-inserter'].rotation_speed>data.inserter['bulk-inserter'].rotation_speed
    assert data.inserter['sn-canopy-inserter'].max_belt_stack_size==4

def test_biosystem_defenses_have_distinct_native_effects(advanced_data):
    data=advanced_data.raw
    assert data.ammo['sn-mycelial-magazine'].ammo_category=='bullet'
    effects=data.ammo['sn-mycelial-magazine'].ammo_type.action.action_delivery.target_effects
    assert any(e.type=='create-sticker' and e.sticker=='sn-mycelial-binding' for e in effects.values())
    assert data.sticker['sn-mycelial-binding'].target_movement_modifier<1
    assert data['electric-turret']['sn-arc-turret'].attack_parameters.ammo_type.action.action_delivery.beam=='sn-resonance-beam'
    effects=data.ammo['sn-lance-cell'].ammo_type.action.action_delivery.target_effects
    assert any(e.type=='script' and e.effect_id=='sn-pressure-cleanup' for e in effects.values())

@pytest.mark.parametrize('kind',['pickup','drop'])
def test_inserter_grid_enforces_two_tiles_on_both_axes(game_lua,kind):
    game_lua.globals().kind=kind
    game_lua.execute('''
      local I=require('scripts.inserters');local p=mock.player(1);local e=mock.entity('inserter',game.surfaces[1],{x=10.5,y=20.5})
      assert(I.set(p,e,kind,2,-2))
      local v=kind=='pickup' and e.pickup_position or e.drop_position
      assert(v.x==12.5 and v.y==18.5)
      assert(not I.set(p,e,kind,3,0) and not I.set(p,e,kind,0,-3))
      assert(not I.set(p,e,kind,0,0) and not I.set(p,e,kind,.5,1))
      assert(not I.set(p,e,kind,0/0,1))
    ''')

def test_vector_editor_preserves_ownership_and_distinct_endpoints(game_lua):
    game_lua.execute('''
      local I=require('scripts.inserters');local p=mock.player(1);local e=mock.entity('inserter',game.surfaces[1])
      assert(not I.set(p,e,'pickup',0,1))
      e.force=mock.enemy;assert(not I.set(p,e,'drop',2,0));e.force=p.force
      I.open(p,e,false);local f=p.gui.screen.sn_inserter_editor;assert(f)
      local b=f.sn_vector_grids.sn_pickup_column.sn_pickup_grid['sn_vector_pickup_2_-2']
      I.click({player_index=1,element=b});assert(e.pickup_position.x==2 and e.pickup_position.y==-2)
      I.reset(p,e);assert(e.pickup_position.y==-1 and e.drop_position.y==1.2)
      settings.startup['sn-inserter-vectors'].value=false;assert(not I.set(p,e,'pickup',2,0))
    ''')

def test_native_jukebox_can_replace_and_stop_a_track(game_lua):
    game_lua.execute('''
      local J=require('scripts.jukebox');local p=mock.player(1);local e=mock.entity('sn-jukebox',game.surfaces[1])
      assert(J.play(p,e,2,false));assert(e.played.instrument==1 and e.played.note==3 and e.played.stop)
      assert(e.parameters.playback_mode=='local' and not e.parameters.allow_polyphony)
      assert(J.play(p,e,0,false) and e.played.note==1)
      mock.multiplayer=true;p.admin=false;assert(not J.play(p,e,2,true))
      p.admin=true;assert(J.play(p,e,2,true) and e.parameters.playback_mode=='surface')
      e.force=mock.enemy;assert(not J.play(p,e,1,false))
    ''')

def test_lore_panel_is_not_duplicated_on_reconnect(game_lua):
    game_lua.execute('''
      local J=require('scripts.jukebox');local p=mock.player(1)
      J.transmission(p);local f=p.gui.left.sn_transmission;assert(f)
      J.transmission(p);assert(p.gui.left.sn_transmission==f)
      J.click({player_index=1,element={valid=true,name='sn_transmission_close'}})
      assert(not p.gui.left.sn_transmission)
      J.transmission(p);assert(not p.gui.left.sn_transmission)
    ''')

def test_pressure_capture_is_bounded_by_actual_pollution(game_lua):
    game_lua.execute('''
      local s=game.surfaces[1];local w=require('scripts.state').by_planet('nauvis');local cycles=w.cycles
      s.pollution=2
      mock.event('on_script_trigger_effect',{effect_id='sn-pressure-cleanup',surface_index=1,target_position={x=0,y=0}})
      assert(s.pollution==0 and w.removed_pollution==2 and w.cycles==cycles)
      mock.event('on_script_trigger_effect',{effect_id='sn-pressure-cleanup',surface_index=1,target_position={x=0,y=0}})
      assert(w.removed_pollution==2)
    ''')


def test_fluid_port_art_and_prototypes_use_one_coordinate_contract(advanced_data):
    import json,math
    from catalog import load_catalog
    from industrial_art import machine,rot
    ports=json.loads((ROOT/'docs/art/fluid-ports.json').read_text())
    vectors={0:(0,-1),4:(1,0),8:(0,1),12:(-1,0)}
    for definition in load_catalog()['machines']:
        name=definition['name']
        if definition.get('entity_type')=='constant-combinator':continue
        p=advanced_data.raw['assembling-machine'][definition['entity_name']]
        mesh=machine(name,0)
        assert len(mesh.port_anchors)==len(ports[name])
        for source,anchor in zip(ports[name],mesh.port_anchors):
            connection=p.fluid_boxes[source['box']].pipe_connections[1]
            assert list(connection.position.values())==source['position']
            assert connection.direction==source['direction']
            assert p.fluid_boxes[source['box']].pipe_picture is None
            dx,dy=vectors[source['direction']]
            expected=(source['position'][0]+dx*.5,source['position'][1]+dy*.5,0)
            for quarter in range(4):
                tip=rot(anchor['position'],quarter*math.pi/2);match=rot(expected,quarter*math.pi/2)
                assert all(abs(a-b)<1e-9 for a,b in zip(tip,match))
                assert tip[2]==0,'connector tip must project to the actual pipe boundary'


def test_point_not_flat_head_leads_the_mining_impact():
    import math
    from explorer_model import explorer
    for facing in range(8):
        m=explorer(.5,'mining_with_tool',0,facing*math.pi/4,facing*math.pi/4)
        tip=m.anchors['tool_tip'];neck=m.anchors['tool_neck']
        assert tip[2]<neck[2] and tip[2]<.3
        assert sum((a-b)**2 for a,b in zip(tip,neck))>.04


def test_opening_is_one_complete_native_hero_track_and_replayable_archive(advanced_data):
    data=advanced_data.raw
    hero=data['ambient-sound']['sn-landing-transmission']
    assert hero.track_type=='hero-track' and hero.planet=='nauvis'
    assert hero.sound.filename.endswith('landing-transmission.ogg')
    assert data['ambient-sound']['sn-living-world'].weight==0
    jukebox=data['programmable-speaker']['sn-jukebox']
    assert len(jukebox.instruments[1].notes)==4 and jukebox.maximum_polyphony==1
    assert jukebox.instruments[1].notes[3].sound.filename.endswith('we-need-a-living-world.ogg')


def test_arrival_audio_contains_complete_voice_then_song_and_saved_lyrics():
    import json,struct,hashlib
    from catalog import MOD
    report=json.loads((ROOT/'docs/art/living-world-score.json').read_text())
    assert report['intro_seconds']>30 and report['song_seconds']==160
    assert report['suite_seconds']>report['intro_seconds']+report['song_seconds']
    assert 'not singing' in report['vocals']
    assert 'humanity' in ' '.join(report['lyrics'].values()).lower()
    assert 'green and lush' in report['lyrics']['chorus'].lower()
    for name,expected in [('we-need-a-living-world.ogg',report['song_seconds']),('landing-transmission.ogg',report['suite_seconds'])]:
        data=(MOD/'sound/music'/name).read_bytes();assert data[:4]==b'OggS'
        first=27+data[26];assert data[first:first+7]==b'\x01vorbis'
        rate=struct.unpack_from('<I',data,first+12)[0];assert rate==32000 and data[first+11]==2
        position=0;granule=0
        while position<len(data):
            assert data[position:position+4]==b'OggS'
            count=data[position+26];header=27+count
            value=struct.unpack_from('<Q',data,position+6)[0]
            if value<2**63:granule=max(granule,value)
            position+=header+sum(data[position+27:position+header])
        assert abs(granule/rate-expected)<.05
        assert hashlib.sha256(data).hexdigest()==report['sha256'][name]
