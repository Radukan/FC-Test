"""Power pole wires must terminate on the insulators that are actually drawn.

Version 0.9 reused the vanilla connection points with our own pole art. Vanilla
attaches copper at y = -2.578; our crossarm sits at y = -1.9405, so every wire
in the game floated roughly 0.58 tiles above the pole it was supposedly bolted
to. These tests pin the geometry to the mesh it is derived from.
"""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from catalog import load_module, plain  # noqa: E402
from factorio_data import DataStage  # noqa: E402
from pole_geometry import connection_points, sprite_top_tile, to_lua  # noqa: E402
from industrial_art import equipment  # noqa: E402

GEOMETRY = plain(load_module('shared.pole_geometry'))['field-pole']


@pytest.fixture(scope='module')
def stage():
    return DataStage(ROOT / '.cache/factorio-data-2.0.77')


def test_generated_table_is_in_sync_with_the_mesh():
    """The checked-in Lua must be exactly what the generator produces now."""
    current = (ROOT / 'second-nature/shared/pole_geometry.lua').read_text()
    assert current == to_lua(), 'run tools/pole_geometry.py'


def test_copper_attaches_to_the_drawn_crossarm_not_vanilla_geometry(stage):
    pole = stage.raw['electric-pole']['small-electric-pole']
    points = list(plain(pole['connection_points']))
    assert len(points) == 4
    for entry in points:
        copper = list(entry['wire']['copper'])
        assert copper[1] == pytest.approx(-1.9405, abs=1e-3), copper
        # The old vanilla value is exactly what this test exists to prevent.
        assert copper[1] != pytest.approx(-2.578, abs=1e-3)


def test_wire_points_sit_on_the_pole_sprite_not_above_it():
    """Attachment points must lie within the drawn pole, not float above it.

    `sprite_top_tile` reports the apex of the north-facing mesh. Rotating the
    crossarm pushes its far insulator further up the screen, so the bound is the
    apex minus the arm's own half-span, not the apex itself.
    """
    top = sprite_top_tile(equipment('field-pole'))
    reach = 0.53 * abs(GEOMETRY[1]['wire']['red'][1] - GEOMETRY[1]['wire']['green'][1]) / 1.06
    for entry in GEOMETRY:
        for colour in ('copper', 'red', 'green'):
            y = entry['wire'][colour][1]
            # Screen y grows downwards, so 'below the apex' means a larger y.
            assert y >= top[1] - reach - 1e-6, (colour, y, top)
            # It must still be up on the arm, and never below the pole's base.
            assert -2.5 < y < 0, (colour, y)
    # Copper is the load-bearing case: it is dead centre and must be on the apex.
    for entry in GEOMETRY:
        assert entry['wire']['copper'][1] == pytest.approx(-1.9405, abs=1e-3)


def test_signal_wires_separate_across_the_crossarm_in_every_rotation():
    """Red and green must never coincide, or the two wires overlap on screen."""
    for index, entry in enumerate(GEOMETRY):
        red, green = entry['wire']['red'], entry['wire']['green']
        separation = max(abs(red[0] - green[0]), abs(red[1] - green[1]))
        assert separation > .3, (index, red, green)
        if index % 2 == 0:
            # North/south: the arm is broadside, so the wires split across x.
            assert abs(red[0] - green[0]) == pytest.approx(1.06, abs=1e-3)
        else:
            # East/west: the same arm is end-on, so they split in depth.
            assert abs(red[1] - green[1]) == pytest.approx(.7877, abs=1e-3)


def test_shadow_points_are_offset_from_their_wire_points():
    """A shadow drawn at the wire position would sit in mid-air."""
    for entry in GEOMETRY:
        for colour in ('copper', 'red', 'green'):
            wire, shadow = entry['wire'][colour], entry['shadow'][colour]
            assert (abs(wire[0] - shadow[0]) > .5 or abs(wire[1] - shadow[1]) > .5), colour


def test_generator_is_reproducible():
    """Two runs must produce identical bytes, or CI's freshness check flaps."""
    assert to_lua() == to_lua()
    first = connection_points('field-pole')
    second = connection_points('field-pole')
    assert first == second
