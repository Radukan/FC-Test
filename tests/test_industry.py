"""Industry expansion: furnaces, assembly cells, ore concentration, mining,
pollution control and the field laboratory.

The design contract these tests defend is that nothing added here is a strict
upgrade of a vanilla machine. Every addition must trade something real, so a
player has a genuine reason to keep running stock furnaces, drills and
assemblers alongside ours.
"""
import json
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from catalog import load_catalog, load_module, plain  # noqa: E402
from factorio_data import DataStage  # noqa: E402

K = load_catalog()
INDUSTRY = plain(load_module('shared.industry'))
LAYOUTS = plain(load_module('shared.machine_layouts'))
AUDIO = plain(load_module('shared.audio_catalog'))
NEW = {m['name'] for m in INDUSTRY['machines']}


@pytest.fixture(scope='module')
def stage():
    return DataStage(ROOT / '.cache/factorio-data-2.0.77')


def machine(name):
    return next(m for m in K['machines'] if m['name'] == name)


def recipe(name):
    return K['by_recipe']['sn-' + name]


def watts(value):
    text = str(value)
    for suffix, factor in (('kW', 1e3), ('MW', 1e6), ('GW', 1e9)):
        if text.endswith(suffix):
            return float(text[:-len(suffix)]) * factor
    return float(text.rstrip('W'))


# ---------------------------------------------------------------------------
# Save compatibility
# ---------------------------------------------------------------------------

def test_new_machines_never_claim_a_legacy_footprint():
    """Only machines that actually grew after release may be `expanded`; a new
    building must not generate a hidden compact twin."""
    for name in NEW:
        layout = LAYOUTS[name]
        assert layout['previous_size'] == layout['size'], name
        assert layout['expanded'] is False, name
        assert layout['entity_name'] == 'sn-' + name, name


def test_pre_existing_machine_footprints_are_untouched():
    """Changing a footprint invalidates saved games and blueprints."""
    expected = {
        'algae-vat': (5, 3), 'composter': (3, 3), 'hydroponics-bay': (5, 3),
        'electrolyzer': (5, 3), 'reclamation-plant': (5, 3), 'materials-kiln': (5, 3),
        'pyrolyzer': (3, 3), 'air-scrubber': (3, 3), 'soil-enricher': (3, 3),
        'seed-disperser': (3, 3), 'watershed': (5, 3), 'thermal-exchanger': (5, 3),
        'detoxifier': (5, 3), 'pheromone-dampener': (3, 3), 'forcing-tower': (3, 3),
        'basalt-conditioner': (5, 3), 'fulgoran-reclaimer': (5, 3), 'spore-tower': (5, 3),
        'cryogenic-garden': (7, 5), 'sanctuary': (7, 3), 'planetary-beacon': (7, 5),
        'ecology-monitor': (1, 1),
    }
    for name, (size, previous) in expected.items():
        assert (LAYOUTS[name]['size'], LAYOUTS[name]['previous_size']) == (size, previous), name


# ---------------------------------------------------------------------------
# The complement-not-replace contract
# ---------------------------------------------------------------------------

def test_clean_machines_pay_for_low_emissions_and_dirty_ones_pay_in_pollution():
    """A clean furnace must not also be the fastest, and a dirty furnace must
    genuinely pollute rather than being a free win."""
    for name in ('crucible-furnace', 'oxy-smelter', 'arc-refinery'):
        assert machine(name)['pollution'] <= 0.5, name
    for name in ('blast-furnace', 'cupola-furnace', 'foundry-press'):
        assert machine(name)['pollution'] >= 10, name
    for name in ('blast-iron', 'blast-copper', 'dirty-steel', 'cupola-scrap'):
        r = recipe(name)
        assert r['emissions'] >= 6, name
        assert r['effects']['toxicity'] > 0, name


def test_clean_smelting_is_slower_per_plate_than_the_dirty_route():
    """Sealed smelting trades throughput for air quality. If it were also
    faster there would be no decision to make."""
    def rate(name, product):
        r = recipe(name)
        return sum(a for item, a, *_ in r['results'] if item == product) / r['seconds']

    assert rate('clean-iron-smelting', 'iron-plate') < rate('blast-iron', 'iron-plate')
    assert rate('clean-copper-smelting', 'copper-plate') < rate('blast-copper', 'copper-plate')
    assert rate('clean-steel', 'steel-plate') < rate('dirty-steel', 'steel-plate')


def test_green_mining_heads_are_never_faster_than_the_stock_drill(stage):
    """The reward for a zero-emission drill is clean air, not more ore."""
    stock = stage.raw['mining-drill']['electric-mining-drill']['mining_speed']
    for name in ('electric-auger', 'hydraulic-miner'):
        head = stage.raw['mining-drill']['sn-' + name]
        assert head['mining_speed'] <= stock, name
        emissions = head['energy_source']['emissions_per_minute']
        assert (emissions['pollution'] if emissions else 0) == 0, name
    deep = stage.raw['mining-drill']['sn-deep-core-drill']
    assert deep['mining_speed'] > stock
    assert deep['energy_source']['emissions_per_minute']['pollution'] > 0
    assert LAYOUTS['deep-core-drill']['size'] == 7


def test_field_laboratory_is_a_sidegrade_not_a_free_upgrade(stage):
    """Faster research, but it costs far more power than a stock lab."""
    stock = stage.raw['lab']['lab']
    ours = stage.raw['lab']['sn-field-laboratory']
    assert ours['researching_speed'] > stock['researching_speed']
    assert watts(ours['energy_usage']) > watts(stock['energy_usage'])
    # It must still accept every package the stock lab accepts, or it is a
    # downgrade disguised as an upgrade.
    assert set(plain(stock['inputs'])) <= set(plain(ours['inputs']))


def test_ore_concentration_is_a_multi_building_line_not_one_better_drill():
    """Richer ore has to cost factory space, water and three separate machines."""
    hosts = []
    for name in ('mill-iron-ore', 'flotation', 'dewater-concentrate'):
        category = recipe(name)['category']
        owners = [m['name'] for m in K['machines']
                  if category in ['sn-' + c for c in m['categories']]]
        assert owners, name
        hosts.append(owners[0])
        r = recipe(name)
        fluids = [e for e in list(r['ingredients']) + list(r['results']) if len(e) > 2]
        assert fluids, name
    assert len(set(hosts)) == 3, hosts


def test_concentrate_route_beats_raw_ore_but_needs_oxygen_and_more_steps():
    """The payoff must be real, otherwise nobody builds the line."""
    raw, rich = recipe('clean-iron-smelting'), recipe('concentrate-iron')
    raw_per_ore = (sum(a for i, a, *_ in raw['results'] if i == 'iron-plate') /
                   sum(a for i, a, *_ in raw['ingredients'] if i == 'iron-ore'))
    # 5 raw ore -> 4 concentrate, so one concentrate embodies 1.25 ore.
    rich_plates = sum(a for i, a, *_ in rich['results'] if i == 'iron-plate')
    assert rich_plates / (2 * 1.25) > raw_per_ore
    assert any(i == 'sn-oxygen' for i, *_ in rich['ingredients'])


def test_pollution_control_buildings_are_expensive_and_produce_real_residue():
    """Strong cleanup is fine; free cleanup is not."""
    for name, floor in (('smog-precipitation', 100), ('direct-air-capture', 400)):
        r = recipe(name)
        assert r['effects']['pollution'] <= -floor, name
        assert r['operation'] is True and r['domain'] is True, name
        assert len(list(r['ingredients'])) >= 2, name
        assert len(list(r['results'])) >= 2, name
    tower = machine('carbon-capture-tower')
    assert tower['energy'] == '5MW' and tower['fixed'] == 'direct-air-capture'


# ---------------------------------------------------------------------------
# Prototype integrity
# ---------------------------------------------------------------------------

def test_every_new_machine_builds_a_real_prototype_and_item(stage):
    for name in NEW:
        kind = machine(name).get('entity_type') or 'assembling-machine'
        proto = stage.raw[kind]['sn-' + name]
        assert proto is not None, name
        assert proto['placeable_by']['item'] == 'sn-' + name, name
        assert stage.raw['item']['sn-' + name]['place_result'] == 'sn-' + name, name


def test_new_recipe_categories_are_reachable_from_some_machine():
    owned = set()
    for m in K['machines']:
        owned.update('sn-' + c for c in m['categories'])
    for r in INDUSTRY['recipes']:
        if r['category'].startswith('sn-'):
            assert r['category'] in owned, r['name']


def test_new_machines_have_enough_fluid_boxes_for_their_recipes(stage):
    for r in INDUSTRY['recipes']:
        if not r['category'].startswith('sn-'):
            continue
        need_in = sum(1 for e in r['ingredients'] if len(e) > 2)
        need_out = sum(1 for e in r['results'] if len(e) > 2)
        for m in K['machines']:
            if r['category'] not in ['sn-' + c for c in m['categories']]:
                continue
            boxes = list(plain(stage.raw['assembling-machine'][m['entity_name']]['fluid_boxes']) or [])
            ins = sum(b['production_type'] in ('input', 'input-output') for b in boxes)
            outs = sum(b['production_type'] in ('output', 'input-output') for b in boxes)
            assert ins >= need_in, (r['name'], m['name'])
            assert outs >= need_out, (r['name'], m['name'])


def test_every_new_technology_has_reachable_prerequisites(stage):
    known = {'sn-' + t['name'] for t in K['technologies']}
    for t in INDUSTRY['technologies']:
        for pre in t['prerequisites']:
            assert pre in known or stage.raw['technology'][pre] is not None, (t['name'], pre)
        assert t['unlocks'], t['name']


def test_new_technology_unlocks_name_real_recipes():
    recipes = {r['name'] for r in K['recipes']}
    for t in INDUSTRY['technologies']:
        for unlock in t['unlocks']:
            assert unlock in recipes, (t['name'], unlock)


def test_audio_layer_keys_reference_entities_that_actually_exist():
    """A `-plant` suffix typo would silently leave a machine mute."""
    valid = {layout['entity_name'] for layout in LAYOUTS.values()}
    for name, layer in AUDIO['entities'].items():
        assert name in valid, name
        assert layer in AUDIO['layers'], layer


def test_new_machine_models_fit_their_sprite_canvas():
    from industrial_art import machine as build
    from sprite_bounds import assert_sprite_fits
    for name in sorted(NEW):
        view = machine(name)['art_view']
        for direction in range(4):
            for frame in range(8):
                assert_sprite_fits(build(name, frame / 8), view,
                                   direction * math.pi / 2, (name, direction, frame))


def test_fluid_port_contract_covers_every_machine():
    ports = json.loads((ROOT / 'docs/art/fluid-ports.json').read_text())
    for m in K['machines']:
        assert m['name'] in ports, m['name']


def test_every_machine_is_built_to_its_declared_footprint(stage):
    """The sprite, the fluid ports and the description all describe the size in
    machine_layouts, so the bounding box has to match it. Inheriting the base
    prototype's box instead leaves ports hanging outside the entity, which the
    engine rejects outright with a PipeConnectionDefinition error."""
    for m in K['machines']:
        layout = LAYOUTS[m['name']]
        kind = m.get('entity_type') or 'assembling-machine'
        proto = stage.raw[kind][layout['entity_name']]
        if proto is None:
            continue
        size = layout['size']
        left_top, right_bottom = proto['selection_box'][1], proto['selection_box'][2]
        assert right_bottom[1] - left_top[1] == size, (m['name'], size)
        assert right_bottom[2] - left_top[2] == size, (m['name'], size)
        assert proto['tile_width'] == size and proto['tile_height'] == size, m['name']


def test_every_fluid_port_sits_inside_its_entity(stage):
    """A pipe connection outside the collision box is a hard prototype error."""
    checked = 0
    for m in K['machines']:
        layout = LAYOUTS[m['name']]
        kind = m.get('entity_type') or 'assembling-machine'
        proto = stage.raw[kind][layout['entity_name']]
        if proto is None or proto['fluid_boxes'] is None:
            continue
        box = proto['collision_box']
        for fluid_box in proto['fluid_boxes'].values():
            if fluid_box['pipe_connections'] is None:
                continue
            for connection in fluid_box['pipe_connections'].values():
                position = connection['position']
                if position is None:
                    continue
                checked += 1
                assert box[1][1] <= position[1] <= box[2][1], (m['name'], position[1])
                assert box[1][2] <= position[2] <= box[2][2], (m['name'], position[2])
    assert checked


def test_no_sound_accent_points_at_a_missing_working_visualisation(stage):
    """Sound accents address working visualisations by name. Our drills replace the
    inherited art, which drops those layers, and an accent left pointing at one that
    no longer exists is a hard prototype error rather than a silent miss: the big
    mining drill this machine is copied from cues a sound off "drill-animation".
    """
    drills = 0
    for m in K['machines']:
        layout = LAYOUTS[m['name']]
        kind = m.get('entity_type') or 'assembling-machine'
        proto = stage.raw[kind][layout['entity_name']]
        if proto is None:
            continue
        available = set()
        for holder in (proto, proto['graphics_set']):
            if holder is None or holder['working_visualisations'] is None:
                continue
            for visualisation in holder['working_visualisations'].values():
                if visualisation['name'] is not None:
                    available.add(str(visualisation['name']))
        sound = proto['working_sound']
        if sound is not None and sound['sound_accents'] is not None:
            for accent in sound['sound_accents'].values():
                target = accent['play_for_working_visualisation']
                assert target is None or str(target) in available, \
                    (m['name'], str(target), sorted(available))
        if kind == 'mining-drill':
            drills += 1
            # Our drills draw none of the inherited layers, so no accent may survive.
            assert sound is None or sound['sound_accents'] is None, m['name']
    assert drills == 3, drills


def test_mining_heads_drop_ore_outside_their_own_body(stage):
    """vector_to_place_result is inherited from the base drill, which may have a
    smaller body than ours. On a larger head the inherited vector lands inside the
    machine, where no belt or chest can reach the ore."""
    drills = 0
    for m in K['machines']:
        if (m.get('entity_type') or 'assembling-machine') != 'mining-drill':
            continue
        layout = LAYOUTS[m['name']]
        proto = stage.raw['mining-drill'][layout['entity_name']]
        vector = proto['vector_to_place_result']
        assert vector is not None, m['name']
        drills += 1
        assert abs(vector[2]) > layout['size'] / 2, (m['name'], vector[2], layout['size'])
        assert vector[1] == 0, m['name']
    assert drills == 3, drills
