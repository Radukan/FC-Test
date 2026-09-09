#!/usr/bin/env python3
"""Derive electric-pole wire connection points from the actual pole meshes.

Vanilla poles declare where their copper/red/green wires attach. Our poles are
procedurally modelled, so those numbers have to come from the same geometry the
sprite is rendered from, or the wires visibly float in the air above the
insulators. Version 0.9 shipped a copper attachment at -2.578 tiles while the
sprite's crossarm sits at -1.9405, leaving about 0.58 tiles of gap.

The generated table is written to `second-nature/shared/pole_geometry.lua` and
consumed by `prototypes/expedition.lua`. Keep this the single source of truth:
regenerate rather than hand-editing the Lua.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from industrial_art import equipment  # noqa: E402

# The renderer's fixed camera. Screen Y combines depth and height, so a point at
# model (x, y, z) lands on the ground plane at tile (x, sin(E)*y - cos(E)*z).
ELEVATION = math.radians(48)
SIN_E, COS_E = math.sin(ELEVATION), math.cos(ELEVATION)

# Shadows are cast along this direction and flattened onto z = 0.
LIGHT = (-.65, -.78, 1.35)


def _tile(point):
    x, y, z = point
    return (round(x, 4), round(SIN_E * y - COS_E * z, 4))


def _shadow_tile(point):
    """Where the same point's shadow falls, in tile coordinates."""
    x, y, z = point
    t = z / LIGHT[2]
    return _tile((x - LIGHT[0] * t, y - LIGHT[1] * t, 0))


def sprite_top_tile(model):
    """Highest point of the mesh, in tile coordinates. Used as a sanity bound."""
    best = None
    for face, _, _ in model.faces:
        for vertex in face:
            tile = _tile(vertex)
            if best is None or tile[1] < best[1]:
                best = tile
    return best


def _insulators(model):
    """The three insulator caps on top of the crossarm.

    These are the parts a wire visibly terminates on, so they -- not the mast
    or the arm beam -- define the attachment points. They are the only geometry
    in the top band that is clustered into separate columns in x, so find the
    top band and group its vertices by x.
    """
    highest = max(z for face, _, _ in model.faces for _, _, z in face)
    # Only the caps themselves. A looser band also catches the crossarm beam and
    # the mast tips, which drags the computed centres off the insulator columns.
    band = [v for face, _, _ in model.faces for v in face if v[2] >= highest - .06]
    assert band, 'pole mesh has no top band'

    # Split the band into columns wherever there is a real gap along x, then take
    # each column's midpoint. A low-polygon cylinder does not place vertices
    # symmetrically, so averaging them would bias the centre off the true axis.
    clusters = []
    for vertex in sorted(band, key=lambda v: v[0]):
        if clusters and vertex[0] - clusters[-1][-1][0] <= .20:
            clusters[-1].append(vertex)
        else:
            clusters.append([vertex])
    merged = []
    for group in clusters:
        xs = [p[0] for p in group]
        ys = [p[1] for p in group]
        merged.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2,
                       max(p[2] for p in group)))
    assert len(merged) >= 3, 'expected three insulator caps, found %d' % len(merged)
    # Outermost pair carries the signal wires; the middle one carries copper.
    left, right = merged[0], merged[-1]
    middle = min(merged, key=lambda p: abs(p[0]))
    return middle, left, right


def connection_points(name='field-pole'):
    """Four rotations of copper/red/green attachment points plus shadow copies."""
    model = equipment(name)
    middle, left, right = _insulators(model)
    cx, cy, cz = middle
    # Signal wires land on the outer insulator caps.
    reach = (right[0] - left[0]) * .5

    points = []
    for direction in range(4):
        angle = direction * math.pi / 2
        cos_a, sin_a = math.cos(angle), math.sin(angle)

        def place(dx, dy):
            x = cx + dx * cos_a - dy * sin_a
            y = cy + dx * sin_a + dy * cos_a
            return (x, y, cz)

        copper = place(0, 0)
        # The signal wires always sit at the two ends of the physical crossarm.
        # Rotating that offset is what makes an east/west pole, seen end-on,
        # separate its wires in screen depth rather than across the screen.
        red, green = place(-reach, 0), place(reach, 0)

        points.append({
            'wire': {'copper': _tile(copper), 'red': _tile(red), 'green': _tile(green)},
            'shadow': {'copper': _shadow_tile(copper), 'red': _shadow_tile(red),
                       'green': _shadow_tile(green)},
        })
    return points


def _number(value):
    # Normalise negative zero so the generated file is stable across platforms.
    if abs(value) < 5e-5:
        return '0'
    return ('%.4f' % value).rstrip('0').rstrip('.')


def _lua_pair(pair):
    return '{%s, %s}' % (_number(pair[0]), _number(pair[1]))


def to_lua(names=('field-pole',)):
    lines = [
        '-- Generated by tools/pole_geometry.py. Do not edit by hand.',
        '--',
        '-- Wire attachment points measured from the pole meshes themselves, so',
        '-- copper and signal wires terminate on the drawn insulators instead of',
        '-- floating above them. Regenerate after changing the pole model.',
        'return {',
    ]
    for name in names:
        lines.append('  ["%s"] = {' % name)
        for entry in connection_points(name):
            wire, shadow = entry['wire'], entry['shadow']
            lines.append('    {')
            lines.append('      wire = {copper = %s, red = %s, green = %s},' % (
                _lua_pair(wire['copper']), _lua_pair(wire['red']), _lua_pair(wire['green'])))
            lines.append('      shadow = {copper = %s, red = %s, green = %s}' % (
                _lua_pair(shadow['copper']), _lua_pair(shadow['red']), _lua_pair(shadow['green'])))
            lines.append('    },')
        lines.append('  },')
    lines.append('}')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    target = ROOT / 'second-nature/shared/pole_geometry.lua'
    # Never write this file with a shell redirect: the freshness test compares
    # exact bytes and a trailing blank line fails it.
    target.write_text(to_lua())
    print('Wrote', target.relative_to(ROOT))
