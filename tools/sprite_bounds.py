"""Pure-Python geometry/framing checks; no optional raster dependencies required."""
import math


def projected_bounds(mesh, view, angle=0):
    """Map-aligned mesh plus the rasterizer's directional ground shadow."""
    c, s = math.cos(angle), math.sin(angle)
    elevation = math.cos(math.radians(48))
    ox, oy, ppu = view['width'] / 2, view['height'] * view['origin'], view['ppu']
    left = top = math.inf
    right = bottom = -math.inf
    for vertices, _, _ in mesh.faces:
        for x, y, z in vertices:
            x, y = x * c - y * s, x * s + y * c
            px = ox + x * ppu
            py = oy + (y - z * elevation) * ppu
            sx = ox + (x + z * .65 / 1.35) * ppu
            sy = oy + (y + z * .78 / 1.35) * ppu
            left, top = min(left, px, sx), min(top, py, sy)
            right, bottom = max(right, px, sx), max(bottom, py, sy)
    return left, top, right, bottom


def assert_sprite_fits(mesh, view, angle=0, context=None, margin=8):
    bounds = projected_bounds(mesh, view, angle)
    assert min(bounds[0], bounds[1], view['width'] - bounds[2],
               view['height'] - bounds[3]) >= margin, (context, bounds, view)
    return bounds
