"""Checks that mirror what the Factorio engine validates when it loads the mod.

The Lua tests confirm our prototypes say what we intend. These confirm the engine
will actually accept them. Every rule here corresponds to a real load failure:
a sprite rectangle that runs past the edge of its PNG, a filename that does not
exist, or a reference to a prototype that was never defined. None of those are
visible from the mod source alone, and each one aborts startup outright.
"""
import math
import re
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from factorio_data import DataStage  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
UPSTREAM = ROOT / '.cache/factorio-data-2.0.77'
MAX_TEXTURE = 8192


@pytest.fixture(scope='module')
def stage():
    if not UPSTREAM.exists():
        pytest.skip('Fetch Wube factorio-data 2.0.77; see docs/DEVELOPING.md.')
    return DataStage(UPSTREAM)


def ours(stage):
    """Every prototype this mod defines, as (kind, name, prototype)."""
    for kind in stage.raw:
        table = stage.raw[kind]
        if table is None or not hasattr(table, 'values'):
            continue
        for name in table:
            if str(name).startswith('sn-'):
                prototype = table[name]
                if hasattr(prototype, '__getitem__'):
                    yield kind, str(name), prototype


def walk(node, path, depth=0):
    """Yield every nested table, so sprites buried in layers are still reached."""
    if depth > 16:
        return
    yield path, node
    try:
        keys = list(node)
    except TypeError:
        return
    for key in keys:
        try:
            value = node[key]
        except Exception:  # noqa: BLE001 - lua tables raise assorted errors
            continue
        if hasattr(value, '__getitem__') and not isinstance(value, (str, int, float, bool)):
            yield from walk(value, f'{path}.{key}', depth + 1)


def resolve(filename):
    match = re.fullmatch(r'__([a-z0-9-]+)__/(.+)', filename)
    if not match:
        return None
    mod, relative = match.groups()
    if mod == 'second-nature':
        return ROOT / 'second-nature' / relative
    return UPSTREAM / mod / relative


def test_every_sprite_file_we_reference_exists(stage):
    missing = []
    for kind, name, prototype in ours(stage):
        for path, node in walk(prototype, f'{kind}/{name}'):
            try:
                filename = node['filename']
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(filename, str) or not filename.startswith('__'):
                continue
            # The pinned data repository ships no binaries, so only our own
            # files can be verified on disk.
            if not filename.startswith('__second-nature__/'):
                continue
            target = resolve(filename)
            if target is None or not target.exists():
                missing.append(f'{path}: {filename}')
    assert not missing, missing


def test_no_sprite_rectangle_runs_past_the_edge_of_its_image(stage):
    """The engine refuses a sprite whose declared rectangle is not inside the file:
    'The given sprite rectangle ... is outside the actual sprite size'."""
    sizes = {}
    problems = []
    checked = 0
    for kind, name, prototype in ours(stage):
        for path, node in walk(prototype, f'{kind}/{name}'):
            try:
                filename = node['filename']
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(filename, str) or not filename.startswith('__second-nature__/'):
                continue
            if not filename.endswith('.png') or node['stripes'] is not None:
                continue
            if filename not in sizes:
                target = resolve(filename)
                sizes[filename] = Image.open(target).size if target and target.exists() else None
            size = sizes[filename]
            if size is None:
                continue
            image_width, image_height = size
            width, height = node['width'], node['height']
            if width is None and node['size'] is not None:
                width = height = node['size']
            if not width or not height:
                continue
            checked += 1
            left, top = node['x'] or 0, node['y'] or 0
            frames = node['frame_count'] or 1
            directions = node['direction_count'] or 1
            cells = frames * directions
            columns = node['line_length'] or cells
            columns = min(columns, cells)
            rows = math.ceil(cells / columns)
            need_width = left + columns * width
            need_height = top + rows * height
            if need_width > image_width or need_height > image_height:
                problems.append(
                    f'{path}: {cells} cells of {width}x{height} as {columns}x{rows} '
                    f'need {need_width}x{need_height}, {filename} is {image_width}x{image_height}')
    assert checked > 300, checked
    assert not problems, problems


def test_no_image_we_ship_exceeds_the_engine_texture_limit(stage):
    oversize = []
    for image in sorted((ROOT / 'second-nature/graphics').rglob('*.png')):
        with Image.open(image) as opened:
            if max(opened.size) > MAX_TEXTURE:
                oversize.append(f'{image.relative_to(ROOT)}: {opened.size}')
    assert not oversize, oversize


def test_every_placeable_item_and_mining_result_names_a_real_prototype(stage):
    items = set()
    entities = set()
    for kind in stage.raw:
        table = stage.raw[kind]
        if table is None or not hasattr(table, 'values'):
            continue
        for name in table:
            prototype = table[name]
            if not hasattr(prototype, '__getitem__'):
                continue
            try:
                if prototype['stack_size'] is not None:
                    items.add(str(name))
                if prototype['collision_box'] is not None or prototype['selection_box'] is not None:
                    entities.add(str(name))
            except Exception:  # noqa: BLE001
                continue
    problems = []
    for kind, name, prototype in ours(stage):
        minable = prototype['minable']
        if minable is not None and minable['result'] is not None:
            if str(minable['result']) not in items:
                problems.append(f'{kind}/{name}: minable result {minable["result"]}')
        placeable = prototype['placeable_by']
        if placeable is not None and placeable['item'] is not None:
            if str(placeable['item']) not in items:
                problems.append(f'{kind}/{name}: placeable_by {placeable["item"]}')
        result = prototype['place_result']
        if result is not None and str(result) not in entities:
            problems.append(f'{kind}/{name}: place_result {result}')
    assert not problems, problems


def test_no_recipe_puts_a_fluid_in_an_item_only_category(stage):
    """The engine refuses a fluid in a hand-craftable category outright: "Recipe is
    in 'crafting' category but has a non-item ingredient 'lubricant' (fluid)".

    The rule is a property of the category itself, not of the machines that happen
    to support it: assembler 2 and 3 handle fluids and also accept plain 'crafting',
    so inferring capability from machines would wrongly clear 'crafting'. These are
    the vanilla categories a fluid may never appear in.
    """
    item_only = {'crafting', 'basic-crafting', 'advanced-crafting', 'smelting',
                 'centrifuging', 'crushing', 'electronics', 'pressing',
                 'organic-or-hand-crafting'}
    problems = []
    checked = 0
    for name in stage.raw['recipe']:
        recipe = stage.raw['recipe'][name]
        category = str(recipe['category'] or 'crafting')
        for field in ('ingredients', 'results'):
            node = recipe[field]
            if node is None:
                continue
            for entry in node.values():
                if not hasattr(entry, '__getitem__') or entry['type'] is None:
                    continue
                if str(entry['type']) != 'fluid':
                    continue
                checked += 1
                if category in item_only:
                    problems.append(f'{name}: {field} fluid {entry["name"]} in {category!r}')
    assert checked, 'No fluid recipes found, so this test would pass vacuously.'
    assert not problems, sorted(set(problems))
