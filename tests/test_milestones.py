"""Milestones, the in-game field guide and the working-sound pass.

Achievement and tip prototypes are checked against the real pinned game data;
awards are checked against the runtime doubles. Nothing here asserts that the
graphical achievement window looks a particular way.
"""
import hashlib
import json
import re

import pytest
from PIL import Image, ImageChops, ImageStat

from catalog import ROOT, MOD, load_catalog, load_module
from factorio_data import DataStage


@pytest.fixture(scope='module')
def stage():
    path = ROOT / '.cache/factorio-data-2.0.77'
    if not path.exists():
        pytest.skip('Pinned stable data checkout required; see docs/DEVELOPING.md.')
    return DataStage(path, True)


MILESTONES = load_module('shared.achievements')
TIPS = load_module('shared.tips')
AUDIO = load_module('shared.audio_catalog')

# Types the engine evaluates on its own. Scripts cannot unlock any of these.
ENGINE_TYPES = {
    'build-entity-achievement', 'produce-achievement', 'research-with-science-pack-achievement',
    'dont-build-entity-achievement', 'dont-use-entity-in-energy-production-achievement',
    'use-entity-in-energy-production-achievement',
}


def test_every_milestone_is_declared_once_with_a_stable_unique_order():
    names = [x['name'] for x in MILESTONES['all']]
    assert len(names) == len(set(names)), 'Duplicate milestone name'
    orders = [x['order'] for x in MILESTONES['all']]
    assert len(orders) == len(set(orders)), 'Duplicate milestone order'
    for entry in MILESTONES['all']:
        assert re.fullmatch(r'[a-z][a-z0-9-]+', entry['name']), entry['name']
        assert len(entry['description']) > 40, entry['name']
        assert entry['title'][0].isupper()


def test_only_plain_achievements_are_script_unlockable():
    """A script can only unlock type "achievement"; anything else silently fails."""
    for entry in MILESTONES['script']:
        assert entry.get('script') is True
    for entry in MILESTONES['engine']:
        assert entry['kind'] in ENGINE_TYPES, entry['kind']
        assert not entry.get('script')
    runtime = (MOD / 'scripts/achievements.lua').read_text()
    # The runtime must never try to award an engine-evaluated milestone.
    for entry in MILESTONES['engine']:
        assert '"' + entry['name'] + '"' not in runtime, entry['name']


def test_every_script_milestone_is_actually_reachable_from_the_runtime():
    """A medal nobody can win is a bug, not content."""
    sources = '\n'.join(p.read_text() for p in sorted((MOD / 'scripts').glob('*.lua')))
    for entry in MILESTONES['script']:
        assert '"' + entry['name'] + '"' in sources, f"Unreachable milestone {entry['name']}"


def test_achievement_and_tip_prototypes_exist_with_real_icons(stage):
    for entry in MILESTONES['all']:
        name = 'sn-' + entry['name']
        kind = 'achievement' if entry.get('script') else entry['kind']
        proto = stage.raw[kind][name]
        assert proto is not None, (kind, name)
        assert proto['icon_size'] == 128
        path = MOD / proto['icon'].removeprefix('__second-nature__/')
        with Image.open(path) as image:
            assert image.size == (128, 128) and image.mode == 'RGBA'
        assert stage.raw['sprite']['sn-medal-' + entry['name']] is not None
    assert stage.raw['tips-and-tricks-item-category'][TIPS['category']] is not None
    for entry in TIPS['items']:
        proto = stage.raw['tips-and-tricks-item']['sn-' + entry['name']]
        assert proto is not None, entry['name']
        assert proto['category'] == TIPS['category']


def test_mod_tips_add_a_new_category_without_touching_stock_entries(stage):
    """No stock Factorio tip may be replaced, recategorized or hidden."""
    ours = {'sn-' + x['name'] for x in TIPS['items']}
    for name, proto in stage.raw['tips-and-tricks-item'].items():
        if name in ours:
            continue
        assert proto['category'] != TIPS['category'], name
    assert stage.raw['tips-and-tricks-item-category'][TIPS['category']]['order'] == TIPS['category_order']


def test_achievement_conditions_reference_prototypes_that_exist(stage):
    def exists(name):
        for kind in ('assembling-machine', 'electric-energy-interface', 'solar-panel', 'generator',
                     'burner-generator', 'reactor', 'fusion-generator', 'item', 'tool'):
            if stage.raw[kind] is not None and stage.raw[kind][name] is not None:
                return True
        return False

    for entry in MILESTONES['engine']:
        for key in ('to_build', 'item_product', 'science_pack', 'entity', 'dont_build', 'excluded', 'included'):
            value = entry['fields'].get(key)
            if value is None:
                continue
            for name in (value if isinstance(value, list) else [value]):
                assert exists(name), (entry['name'], key, name)


def test_medallion_art_is_individual_and_matches_its_ledger():
    manifest = json.loads((ROOT / 'docs/art/achievement-manifest.json').read_text())
    assert set(manifest) == {x['name'] for x in MILESTONES['all']}
    seen = {}
    for name, spec in manifest.items():
        path = ROOT / spec['file']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == spec['sha256'], ('Stale achievement art', name)
        assert digest not in seen, (name, seen.get(digest))
        seen[digest] = name


@pytest.mark.parametrize('pair', [
    ('a-living-world', 'second-nature'), ('root-systems', 'new-growth'),
    ('deep-green', 'first-breath'), ('network-nodes', 'field-stations'),
    ('coordination-cells', 'matrix-gardener'), ('quiet-eden', 'common-ground'),
])
def test_related_medallions_stay_distinguishable_at_list_size(pair):
    """The achievement list draws these small; near-identical plates are useless."""
    def small(name):
        with Image.open(ROOT / f'docs/../second-nature/graphics/achievement/{name}.png') as image:
            image = image.resize((48, 48), Image.Resampling.LANCZOS)
            background = Image.new('RGBA', image.size, (46, 46, 43, 255))
            background.alpha_composite(image)
            return background.convert('RGB')
    difference = ImageStat.Stat(ImageChops.difference(small(pair[0]), small(pair[1]))).mean
    assert sum(difference) / 3 > 6, (pair, difference)


def test_no_generating_plant_or_working_building_is_silent(stage):
    """A machine that visibly runs but makes no sound reads as broken."""
    catalog = load_catalog()
    kinds = ('assembling-machine', 'solar-panel', 'electric-energy-interface', 'burner-generator',
             'generator', 'reactor', 'fusion-generator', 'constant-combinator')

    def find(name):
        for kind in kinds:
            proto = stage.raw[kind][name] if stage.raw[kind] is not None else None
            if proto is not None:
                return proto
        raise AssertionError('Missing prototype ' + name)

    for plant in catalog['energy']['plants']:
        assert find('sn-' + plant['name'])['working_sound'] is not None, plant['name']
    for machine in catalog['machines']:
        assert find(machine['entity_name'])['working_sound'] is not None, machine['name']


def test_every_working_sound_file_is_a_real_upstream_asset(stage):
    """Referenced audio must exist in the pinned game data, not be invented."""
    referenced = set()
    for path in (stage.upstream / 'base').rglob('*.lua'):
        referenced.update(re.findall(r'"(__(?:base|space-age)__/sound/[^"]+\.ogg)"', path.read_text(errors='replace')))
    for path in (stage.upstream / 'space-age').rglob('*.lua'):
        referenced.update(re.findall(r'"(__(?:base|space-age)__/sound/[^"]+\.ogg)"', path.read_text(errors='replace')))
    ours = {layer['file'] for layer in AUDIO['layers'].values()}
    assert ours, 'No audio layers declared'
    for name in sorted(ours):
        assert name in referenced, f'{name} is not referenced by any upstream prototype'


def test_inventory_handling_sounds_cover_every_carried_item(stage):
    """Stock items click when moved. Ours used the bare engine default."""
    silent = []
    for kind in ('item', 'tool', 'ammo', 'armor', 'capsule', 'gun', 'item-with-entity-data'):
        collection = stage.raw[kind]
        if collection is None:
            continue
        for name, proto in collection.items():
            if not str(name).startswith('sn-') or proto['hidden']:
                continue
            if proto['inventory_move_sound'] is None:
                silent.append(str(name))
    assert not silent, silent


def test_awards_are_per_force_recorded_once_and_pushed_to_every_member(game_lua):
    game_lua.execute('''
      local A=require('scripts.achievements');local S=require('scripts.state')
      local first=mock.player(1);local other=mock.force(4,'other');local guest=mock.player(2,other)
      assert(A.award(mock.player_force,'first-breath'))
      assert(not A.award(mock.player_force,'first-breath'),'awarded twice')
      assert(first.achievements['sn-first-breath'])
      assert(not guest.achievements['sn-first-breath'],'leaked to another force')
      assert(A.earned(1,'first-breath') and not A.earned(4,'first-breath'))
      local earned,total=A.count(1);assert(earned==1 and total>=10)
      assert(not A.award(mock.player_force,'not-a-real-milestone'))
    ''')


def test_a_player_who_was_offline_receives_the_award_on_join(game_lua):
    game_lua.execute('''
      local A=require('scripts.achievements')
      A.award(mock.player_force,'root-systems')
      local latecomer=mock.player(3)
      assert(not latecomer.achievements['sn-root-systems'])
      mock.event('on_player_joined_game',{player_index=3})
      assert(latecomer.achievements['sn-root-systems'],'offline award was lost')
    ''')


def test_planetary_milestones_go_to_the_forces_that_did_the_work(game_lua):
    game_lua.execute('''
      local A=require('scripts.achievements');local S=require('scripts.state');local M=require('shared.model')
      local worker=mock.player(1);local bystander_force=mock.force(4,'bystander');mock.player(2,bystander_force)
      mock.entity('sn-air-scrubber',game.surfaces[1])
      local world=S.by_planet('nauvis');world.contributions[1]=12
      for axis in pairs(world.values) do world.values[axis]=45 end
      world.toxicity=20;M.refresh(world);assert(world.stage>=1)
      A.world_tick(world)
      assert(A.earned(1,'first-breath'))
      assert(not A.earned(4,'first-breath'),'credited a force that never worked here')
    ''')


def test_field_station_milestone_requires_real_work_on_all_five_worlds(game_lua):
    game_lua.execute('''
      local C=require('shared.constants');local A=require('scripts.achievements');local S=require('scripts.state')
      mock.player(1)
      for i,planet in ipairs(C.planets) do
        local surface=i==1 and game.surfaces[1] or mock.surface(planet,i)
        mock.entity('sn-air-scrubber',surface)
        local world=S.by_planet(planet)
        if i<#C.planets then world.contributions[1]=3 end
      end
      A.network_tick();assert(not A.earned(1,'field-stations'),'awarded with a missing world')
      S.by_planet(C.planets[#C.planets]).contributions[1]=3
      A.network_tick();assert(A.earned(1,'field-stations'))
    ''')


def test_merging_forces_keeps_the_earliest_award_and_never_duplicates(game_lua):
    game_lua.execute('''
      local A=require('scripts.achievements');local S=require('scripts.state')
      local absorbed=mock.force(4,'absorbed');local player=mock.player(1)
      game.tick=500;A.award(absorbed,'signal-restored')
      game.tick=900;A.award(mock.player_force,'first-breath')
      mock.event('on_forces_merged',{source_index=4,destination=mock.player_force})
      assert(A.earned(1,'signal-restored') and A.earned(1,'first-breath'))
      assert(not S.root().achievements.forces[4])
      assert(S.root().achievements.forces[1]['signal-restored']==500,'lost the original award time')
      assert(player.achievements['sn-signal-restored'],'merged award was not pushed to members')
    ''')


def test_victory_and_expedition_hooks_award_their_milestones(game_lua):
    game_lua.execute('''
      local C=require('shared.constants');local S=require('scripts.state');local N=require('scripts.network')
      local M=require('shared.model');local A=require('scripts.achievements')
      mock.player(1);game.tick=10000;mock.player_force.technologies['sn-living-worlds'].researched=true
      for i,planet in ipairs(C.planets) do
        local surface=i==1 and game.surfaces[1] or mock.surface(planet,i)
        local beacon=mock.entity('sn-planetary-beacon',surface)
        S.root().machines[beacon.unit_number].last_effect=game.tick
        local world=S.by_planet(planet)
        for axis in pairs(world.values) do world.values[axis]=99 end
        world.toxicity=0;M.refresh(world)
      end
      N.tick(C.victory_ticks);assert(A.earned(1,'second-nature'))
    ''')


def test_the_milestone_tab_lists_every_medal_and_marks_only_earned_ones(game_lua):
    game_lua.execute('''
      local A=require('scripts.achievements');local G=require('scripts.gui');local Defs=require('shared.achievements')
      local player=mock.player(1)
      A.award(mock.player_force,'first-breath')
      G.open(player)
      local pane=player.gui.screen.sn_dashboard.sn_tabs.sn_milestones.sn_content
      for _,entry in ipairs(Defs.script) do assert(pane['sn_medal_'..entry.name],'missing row '..entry.name) end
      assert(pane.sn_medal_first_breath==nil,'names must keep their catalog spelling')
      assert(pane['sn_medal_first-breath'].sn_badge.style.draw_grayscale_picture==false)
      assert(pane['sn_medal_terraformer'].sn_badge.style.draw_grayscale_picture==true)
      G.close(player)
    ''')
