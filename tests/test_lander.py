"""Geometry, exact compositing and save-safe runtime checks for the shuttle refit."""
import hashlib
import json

from PIL import Image
import pytest

from catalog import ROOT, MOD, plain
from factorio_data import DataStage
from lander_model import lander, layout
from sprite_bounds import assert_sprite_fits

ART = ROOT / 'docs/art'


@pytest.fixture(scope='module')
def lander_data():
    path = ROOT / '.cache/factorio-data-2.0.77'
    if not path.exists():
        pytest.skip('Pinned stable data is required')
    return DataStage(path)


def test_refit_preserves_native_container_geometry_inventory_and_identity(lander_data):
    p = lander_data.raw.container['sn-lander']
    contract = layout()
    assert plain(p.collision_box) == contract['collision_box'] == [[-4.7, -2.8], [4.7, 2.8]]
    assert plain(p.selection_box) == contract['selection_box'] == [[-5, -3.1], [5, 3.1]]
    assert p.inventory_size == 48 and p.max_health == 5000
    assert p.minable is None and p.corpse is None
    assert 'not-deconstructable' in list(p.flags.values())
    assert 'not-blueprintable' in list(p.flags.values())
    assert p.picture.apply_projection is False
    assert lander_data.raw.animation['sn-lander-idle'].animation_speed == contract['animation_speed']


@pytest.mark.parametrize('phase', [0, .125, .375, .75])
def test_tapered_ship_and_landing_gear_fit_the_existing_camp_and_full_canvas(phase):
    mesh = lander(phase)
    assert_sprite_fits(mesh, layout()['view'], context=('lander', phase), margin=12)
    assert len(mesh.faces) > 10000
    assert len(mesh.contacts) == 4
    assert mesh.anchors['nose'][0] < mesh.anchors['cockpit'][0] < mesh.anchors['seed-vault'][0]
    for side in (-1, 1):
        assert mesh.anchors['engine-' + str(side)][0] > mesh.anchors['seed-vault'][0]
    for vertices, _, _ in mesh.faces:
        for x, y, z in vertices:
            assert -4.7 <= x <= 4.7 and -2.8 <= y <= 2.8 and z >= -1e-8


def test_sparse_standby_overlay_reconstructs_all_reference_frames_without_double_shadows():
    manifest = json.loads((ART / 'sprite-manifest.json').read_text())
    report = json.loads((ART / 'lander-render.json').read_text())
    base, spec = manifest['lander-still'], manifest['lander']
    root = MOD / 'graphics/entity/industry'
    hull = Image.open(root / 'lander-still.png').convert('RGBA')
    systems = Image.open(root / 'lander.png').convert('RGBA')
    assert report['view'] == layout()['view']
    assert report['art_revision'] == layout()['art_revision']
    for name, expected in report['files'].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected
    assert not any(systems.getchannel('A').histogram()[1:255]), 'No second translucent hull or shadow'
    assert 0 < report['moving_pixels'] < hull.width * hull.height * .02
    assert spec['width'] * spec['height'] < base['width'] * base['height'] / 8
    for axis, (large, small) in enumerate(((base['width'], spec['width']), (base['height'], spec['height']))):
        offset = (large - small) / 2 + (spec['shift'][axis] - base['shift'][axis]) * 32 / base['scale']
        assert abs(offset - report['overlay_crop'][axis]) < .001, 'Runtime pivot must match the authoring crop'
    frames = set()
    for i in range(spec['frame_count']):
        overlay = systems.crop((i * spec['width'], 0, (i + 1) * spec['width'], spec['height']))
        frame = hull.copy()
        frame.alpha_composite(overlay, tuple(report['overlay_crop'][:2]))
        digest = hashlib.sha256(frame.tobytes()).hexdigest()
        assert digest == report['frame_rgba_sha256'][i]
        frames.add(digest)
        bbox = frame.getchannel('A').point(lambda a: 255 if a > 16 else 0).getbbox()
        assert min(bbox[0], bbox[1], frame.width - bbox[2], frame.height - bbox[3]) >= 12
    assert len(frames) == spec['frame_count'] == 8


def test_existing_camp_rebuilds_only_the_render_object_once(game_lua):
    game_lua.execute('''
      local S=require('scripts.state');local A=require('scripts.artwork')
      local L=require('shared.lander_layout');local Campaign=require('scripts.campaign')
      local ship=mock.entity('sn-lander',game.surfaces[1],{x=7,y=-12})
      ship.inventory['iron-plate']=3
      local original=rendering.draw_animation({animation='sn-lander-idle',target={entity=ship},surface=ship.surface})
      local camp={ship=ship,animation=original,rocket_launched=true,position={x=7,y=-12}}
      S.root().campaign.camps[1]=camp
      local before=#mock.renders
      mock.configure()
      assert(not original.valid and camp.animation.valid and camp.animation~=original)
      assert(camp.art_revision==L.art_revision and #mock.renders==before+1)
      assert(camp.animation.spec.animation_speed==L.animation_speed)
      assert(camp.ship==ship and ship.position.x==7 and ship.position.y==-12)
      assert(ship.inventory['iron-plate']==3 and camp.rocket_launched)
      assert(not ship.minable and not ship.destructible)
      local current=camp.animation
      mock.configure();A.lander(camp)
      assert(camp.animation==current and #mock.renders==before+1)
      assert(Campaign.land(mock.player_force,ship.surface)==camp and ship.inventory['iron-plate']==3)
      current.destroy();A.lander(camp)
      assert(camp.animation.valid and camp.animation~=current and #mock.renders==before+2)
    ''')


def test_invalid_or_missing_ship_never_gets_recreated_or_refilled(game_lua):
    game_lua.execute('''
      local A=require('scripts.artwork');local count=#mock.renders
      A.lander({});A.lander({ship={valid=false}})
      assert(#mock.renders==count)
    ''')
