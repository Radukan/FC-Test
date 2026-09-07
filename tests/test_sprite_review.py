"""Guard the actual exported pixels, their ground pivots and the current previews."""
import hashlib
import json
import math
import re

from PIL import Image

from catalog import ROOT, MOD, load_catalog
from industrial_art import machine
from sprite_bounds import assert_sprite_fits

ART = ROOT / 'docs/art'


def test_machine_canvases_include_model_and_cast_shadow_in_all_rotations():
    for entry in load_catalog()['machines']:
        for phase in (0, .25, .5, .75):
            model = machine(entry['name'], phase)
            for quarter in range(4):
                assert_sprite_fits(model, entry['art_view'], quarter * math.pi / 2,
                                   (entry['name'], phase, quarter))


def test_machine_sheets_do_not_clip_alpha_or_shift_native_ground_and_pipe_anchors():
    manifest = json.loads((ART / 'sprite-manifest.json').read_text())
    for entry in load_catalog()['machines']:
        view = entry['art_view']
        for direction in ('north', 'east', 'south', 'west'):
            name = entry['art_name'] + '-' + direction
            spec = manifest[name]
            assert (spec['width'], spec['height']) == (view['width'], view['height']), name
            assert spec['apply_projection'] is False
            assert view['ppu'] * spec['scale'] == 32
            assert spec['shift'][0] == 0
            anchor = (spec['height'] * view['origin'] - spec['height'] / 2) * spec['scale'] + spec['shift'][1] * 32
            assert abs(anchor) < .0001, (name, anchor)
            with Image.open(MOD / spec['filename'].split('__second-nature__/')[1]) as image:
                for frame in range(spec['frame_count']):
                    alpha = image.crop((frame * spec['width'], 0, (frame + 1) * spec['width'], spec['height'])).getchannel('A')
                    bounds = alpha.point(lambda a: 255 if a > 16 else 0).getbbox()
                    assert bounds and min(bounds[0], bounds[1], spec['width'] - bounds[2], spec['height'] - bounds[3]) >= 2, (name, frame, bounds)


def test_catalog_document_uses_the_real_new_and_legacy_footprints():
    text = (ROOT / 'docs/CATALOG.md').read_text()
    for m in load_catalog()['machines']:
        row = f"| {m['title']} | {m['footprint']} x {m['footprint']} | {m['previous_footprint']} x {m['previous_footprint']} |"
        assert row in text


def test_review_ledger_matches_the_current_assets_and_canonical_building_keys():
    report = json.loads((ART / 'review-manifest.json').read_text())
    assert report['version'] == json.loads((MOD / 'info.json').read_text())['version']
    assert len(report['inputs']) >= 35
    for path, expected in report['inputs'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, ('Stale preview input', path)
    for name, expected in report['outputs'].items():
        assert hashlib.sha256((ART / name).read_bytes()).hexdigest() == expected, ('Stale preview output', name)
    for m in load_catalog()['machines']:
        assert report['canonical_machines'][m['name']] == {'art_name': m['art_name'], 'footprint': m['footprint']}
        assert f"second-nature/graphics/entity/industry/{m['art_name']}-north.png" in report['inputs']


def test_animation_reviews_have_complete_cycles_and_declared_authored_timing():
    from gait import MINING_SPEED
    from lander_model import layout
    expected = {
        'mining-framing-preview.gif': (20, 20 / (60 * MINING_SPEED) * 1000),
        'lander-standby.gif': (8, 8 / (60 * layout()['animation_speed']) * 1000),
        'locomotion-review.gif': (16, 16 * 80),  # Deliberately slowed source review.
        'industrial-animation-preview.gif': (8, 8 * 100),
    }
    for name, (count, milliseconds) in expected.items():
        with Image.open(ART / name) as gif:
            assert gif.n_frames == count, name
            duration = 0
            for i in range(gif.n_frames):
                gif.seek(i)
                duration += gif.info['duration']
            assert abs(duration - milliseconds) <= 10, (name, duration, milliseconds)


def test_readme_art_links_resolve_in_the_source_checkout():
    text = (ROOT / 'README.md').read_text()
    paths = re.findall(r'\]\((docs/art/[^)]+)\)', text)
    assert len(paths) >= 4
    for path in paths:
        assert (ROOT / path).is_file(), path
