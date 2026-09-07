"""The Wayfarer: an intact, grounded industrial restoration shuttle.

Original authored geometry. Longitudinal X axis, nose to the left; no square
building plinth. Everything physical fits the existing 9.4 x 5.6 tile collision
contract. Solar cells and a sealed seed vault are equipment, not free production.
"""
import math
from functools import lru_cache

from industrial_art import (
    Mesh, DARK, STEEL, EDGE, COPPER, GOLD, TEAL, TAU,
    add, sub, mul, color, hose, fan,
)
from catalog import MOD, plain

HULL = (151, 153, 131)
CERAMIC = (191, 187, 158)
SAGE = (99, 124, 96)
HEAT = (56, 53, 45)
GLASS = (33, 80, 91)
SOLAR = (33, 52, 65)


@lru_cache(maxsize=1)
def layout():
    from lupa.lua52 import LuaRuntime
    lua = LuaRuntime(unpack_returned_tuples=True)
    return plain(lua.execute((MOD / 'shared/lander_layout.lua').read_text()))


def tapered_body(mesh, stations, sides=32, palette=None):
    """Loft elliptical cross-sections (x, half-width, half-height, center-z)."""
    rings = []
    for x, width, height, z in stations:
        rings.append([(x, width * math.sin(i * TAU / sides),
                       z + height * math.cos(i * TAU / sides)) for i in range(sides)])
    palette = palette or (CERAMIC, HULL, SAGE, HEAT)
    for row, (a, b) in enumerate(zip(rings, rings[1:])):
        for i in range(sides):
            elevation = math.cos((i + .5) * TAU / sides)
            c = palette[0 if elevation > .80 else 1 if elevation > .30 else 2 if elevation > -.35 else 3]
            mesh.face([a[i], b[i], b[(i + 1) % sides], a[(i + 1) % sides]], color(c, 1 - .025 * (row % 3)))
    mesh.face(list(reversed(rings[0])), HEAT)
    mesh.face(rings[-1], HEAT)
    return rings


def plate(mesh, outline, thickness, paint):
    mesh.face(outline, paint)
    lower = [add(p, (0, 0, -thickness)) for p in outline]
    mesh.face(list(reversed(lower)), HEAT)
    for i in range(len(outline)):
        j = (i + 1) % len(outline)
        mesh.face([outline[i], outline[j], lower[j], lower[i]], STEEL)


def seam(mesh, points, radius=.013, paint=HEAT):
    hose(mesh, points, radius, paint)


def bolt(mesh, point, radius=.035):
    x, y, z = point
    mesh.cyl(x, y, z, radius, .018, EDGE, 6)
    mesh.box((x, y, z + .022), (radius * 1.1, .010, .008), DARK, 0)


def stencil(mesh, text, at, step=.032):
    # A tiny physical maintenance stencil, on a horizontal upper hull plate.
    glyphs = {
        'S': ['111', '100', '111', '001', '111'],
        'N': ['101', '111', '111', '111', '101'],
        '0': ['111', '101', '101', '101', '111'],
        '1': ['010', '110', '010', '010', '111'],
        '-': ['000', '000', '111', '000', '000'],
    }
    for k, letter in enumerate(text):
        for j, line in enumerate(glyphs[letter]):
            for i, pixel in enumerate(line):
                if pixel != '1':
                    continue
                x, y, z = add(at, ((k * 4 + i) * step, j * step, 0))
                mesh.face([(x, y, z), (x + step * .82, y, z),
                           (x + step * .82, y + step * .82, z), (x, y + step * .82, z)], CERAMIC)


def cockpit(mesh):
    # A raised, multi-pane flight deck with a sloping windscreen and an open face.
    front = [(-3.32, -.49, 1.66), (-3.32, .49, 1.66)]
    brow = [(-2.53, -.72, 2.19), (-2.53, .72, 2.19)]
    back = [(-1.46, -.60, 2.08), (-1.46, .60, 2.08)]
    sill = [(-1.20, -.92, 1.55), (-1.20, .92, 1.55)]
    mesh.face([front[0], front[1], brow[1], brow[0]], GLASS)
    mesh.face([brow[0], brow[1], back[1], back[0]], (45, 94, 102))
    for side in (0, 1):
        mesh.face([front[side], brow[side], back[side], sill[side]], GLASS)
        seam(mesh, [front[side], brow[side], back[side], sill[side]], .040, CERAMIC)
        seam(mesh, [front[side], sill[side]], .045, SAGE)
        middle = add(mul(brow[side], .48), mul(back[side], .52))
        bottom = add(mul(front[side], .48), mul(sill[side], .52))
        seam(mesh, [middle, bottom], .028, EDGE)
        # Quiet reflected sky streaks follow the actual sloped glass.
        a = add(mul(front[side], .30), mul(brow[side], .70))
        b = add(mul(sill[side], .30), mul(back[side], .70))
        seam(mesh, [add(a, (0, .008 if side else -.008, .008)),
                    add(b, (0, .008 if side else -.008, .008))], .013, (81, 135, 137))
    for pair in (front, brow, back):
        seam(mesh, pair, .035, EDGE)
    seam(mesh, [(-3.32, 0, 1.67), (-2.53, 0, 2.20), (-1.46, 0, 2.09)], .032, CERAMIC)
    mesh.face([back[0], back[1], sill[1], sill[0]], SAGE)
    for side in (-1, 1):
        mesh.tube((-3.43, side * .42, 1.26), (-3.47, side * .42, 1.26), .11, HEAT, 16)
        mesh.ball((-3.49, side * .42, 1.27), .075, (178, 162, 106), stretch=(.30, 1, .65))
    mesh.anchors['cockpit'] = (-2.45, 0, 2.20)


def landing_gear(mesh):
    contacts = []
    for x in (-2.60, 2.56):
        for side in (-1, 1):
            y = side * 2.30
            mesh.box((x, y, .085), (.83, .62, .17), HEAT, .18)
            mesh.box((x, y, .18), (.68, .48, .055), STEEL, .14)
            contact = (x, y, .02)
            contacts.append(contact)
            root = (x * .86, side * 1.13, .85)
            knee = (x * 1.01, side * 1.92, .44)
            foot = (x, y, .25)
            mesh.tube(root, knee, .13, SAGE, 16)
            mesh.tube(knee, foot, .082, EDGE, 16)
            mesh.ball(knee, .155, HEAT, stretch=(1, .85, 1))
            mesh.tube(add(root, (.28, 0, .05)), add(foot, (.19, 0, 0)), .060, COPPER, 12)
            seam(mesh, [add(root, (-.16, 0, .08)), add(knee, (-.12, 0, .03)),
                        add(foot, (-.10, 0, .02))], .025, DARK)
            for dx in (-.24, .24):
                bolt(mesh, (x + dx, y, .217))
    mesh.contacts = contacts


def engine_pod(mesh, side, t):
    y, z = side * 1.83, 1.14
    pod = Mesh()
    tapered_body(pod, [(-.55, .31, .34, z), (-.22, .51, .49, z),
                       (.48, .57, .57, z), (1.64, .53, .52, z),
                       (2.72, .43, .41, z), (3.10, .32, .31, z)],
                 palette=(CERAMIC, SAGE, STEEL, HEAT))
    mesh.join(pod, offset=(0, y, 0))
    for x, radius in ((-.22, .51), (1.63, .53), (2.72, .43)):
        mesh.tube((x - .038, y, z), (x + .038, y, z), radius + .018, EDGE, 32)
    # A flared, dark, cold exhaust bell. No flame on a parked lander.
    for x, r in ((3.02, .32), (3.18, .37), (3.37, .46)):
        mesh.tube((x, y, z), (x + .10, y, z), r, HEAT, 32)
    mesh.tube((3.46, y, z), (3.50, y, z), .47, COPPER, 32)
    mesh.tube((3.505, y, z), (3.52, y, z), .405, DARK, 32)
    for i in range(16):
        a = i * TAU / 16
        mesh.tube((2.83, y + .34 * math.sin(a), z + .34 * math.cos(a)),
                  (3.47, y + .455 * math.sin(a), z + .455 * math.cos(a)), .022, STEEL, 6)
    # Horizontal lift-fan wells and a protective rim stay fixed; only the blades turn.
    fan(mesh, .63, y, 1.69, .46, t if side < 0 else -t)
    mesh.ring((.63, y, 1.865), .43, .037, DARK)
    for i in range(6):
        x = 1.27 + i * .17
        mesh.box((x, y, 1.685 - i * .018), (.065, .62, .05), HEAT, .015)
    seam(mesh, [(-.22, y - side * .28, 1.51), (.14, y - side * .36, 1.61),
                (1.18, y - side * .35, 1.60), (1.68, y - side * .31, 1.45)], .055, COPPER)
    # Swept vertical stabilizers, not another vertical cylindrical building tank.
    outline = [(1.89, y, 1.58), (2.70, y, 2.73), (3.35, y, 2.65), (3.11, y, 1.51)]
    for offset in (-.045, .045):
        mesh.face([add(p, (0, offset, 0)) for p in outline], SAGE if offset * side > 0 else HULL)
    for i in range(4):
        a, b = outline[i], outline[(i + 1) % 4]
        mesh.face([add(a, (0, -.045, 0)), add(b, (0, -.045, 0)),
                   add(b, (0, .045, 0)), add(a, (0, .045, 0))], EDGE)
    seam(mesh, [add(outline[1], (0, side * .051, -.10)),
                add(outline[2], (0, side * .051, -.10))], .04, GOLD)
    mesh.anchors['engine-' + str(side)] = (3.52, y, z)
    mesh.anchors['fan-' + str(side)] = (.63, y, 1.9)


def cargo_ramp(mesh):
    # A short starboard cargo stair stays inside the historical collision rectangle.
    left, right = -1.33, -.47
    top, bottom = (1.04, .97), (2.62, .10)
    plate(mesh, [(left, top[0], top[1]), (right, top[0], top[1]),
                 (right, bottom[0], bottom[1]), (left, bottom[0], bottom[1])], .07, HEAT)
    for i in range(9):
        t = i / 8
        y = top[0] * (1 - t) + bottom[0] * t
        z = top[1] * (1 - t) + bottom[1] * t
        mesh.box(((left + right) / 2, y, z + .035), (.83, .095, .045), EDGE, .012)
        for j in range(4):
            mesh.box((left + .12 + j * .20, y, z + .062), (.083, .06, .010), DARK, .003)
    for x in (left - .045, right + .045):
        seam(mesh, [(x, top[0], top[1] + .42), (x, 2.28, .71), (x, 2.52, .48)], .033, EDGE)
        for y, z in ((1.11, .93), (2.28, .29)):
            mesh.tube((x, y, z), (x, y, z + .42), .028, STEEL, 8)
    mesh.box((-.90, 1.07, 1.20), (.87, .10, .48), DARK, .11)
    for x in (left + .08, right - .08):
        mesh.box((x, 1.134, 1.26), (.058, .026, .32), GOLD, .01)
    mesh.anchors['ramp'] = (-.90, 2.62, .10)


def lander(t=0):
    mesh = Mesh()
    mesh.anchors = {'nose': (-4.43, 0, .91)}
    mesh.surface_finish = 'hull'
    landing_gear(mesh)
    stations = [(-4.43, .045, .08, .91), (-4.16, .38, .23, .96),
                (-3.57, .76, .41, 1.05), (-2.79, 1.01, .60, 1.13),
                (-1.35, 1.14, .71, 1.13), (.25, 1.20, .73, 1.12),
                (1.53, 1.12, .67, 1.10), (2.68, .91, .55, 1.08),
                (3.40, .59, .36, 1.05)]
    rings = tapered_body(mesh, stations)
    # Hull panel joints track the taper; they are not a repeated box-grid texture.
    for ring in rings[2:-1]:
        seam(mesh, ring[:18], .012, HEAT)
        seam(mesh, ring[18:] + ring[:1], .012, HEAT)
        for i in (2, 7, 25, 30):
            bolt(mesh, add(ring[i], (0, 0, .012)), .027)
    cockpit(mesh)
    for side in (-1, 1):
        outline = [(-1.12, side * .88, .91), (.57, side * 2.53, .82),
                   (2.95, side * 2.49, .76), (3.11, side * .83, .92)]
        plate(mesh, outline, .16, SAGE)
        seam(mesh, outline[:2], .045, EDGE)
        plate(mesh, [(1.02, side * 2.35, .835), (2.76, side * 2.33, .79),
                     (2.91, side * 1.04, .93), (1.14, side * 1.08, .94)], .018, HULL)
        engine_pod(mesh, side, t)
        # Folded photovoltaic strips on the shoulders, with individual cell busbars.
        mesh.box((.54, side * 1.02, 1.565), (1.90, .28, .065), EDGE, .05)
        for i in range(10):
            x = -.29 + i * .184
            mesh.box((x, side * 1.02, 1.608), (.165, .23, .015), SOLAR, .008)
            mesh.box((x, side * 1.02, 1.619), (.008, .21, .005), (105, 135, 133), 0)
        # Navigation lights are on opaque wing plating, so overlay compositing is exact.
        nav = color((104, 160, 134) if side < 0 else (176, 93, 53), .72 + .28 * math.cos(t * TAU) ** 2)
        mesh.box((.78, side * 2.37, .89), (.18, .12, .045), DARK, .03)
        mesh.ball((.78, side * 2.37, .929), .052, nav, stretch=(1.3, .6, .4), glow=True)
    # Service spine, sealed gene-bank containers and accessible dorsal hatches.
    for x, width, z in ((-.76, .60, 1.867), (.03, .70, 1.882), (1.95, .56, 1.737)):
        mesh.box((x, 0, z), (width, .72, .055), HEAT, .13)
        mesh.box((x, 0, z + .041), (width - .09, .62, .04), HULL, .12)
        mesh.tube((x - .10, -.18, z + .077), (x + .10, -.18, z + .077), .022, EDGE, 8)
        for dx in (-width * .33, width * .33):
            bolt(mesh, (x + dx, .23, z + .066), .025)
    mesh.box((.90, 0, 1.862), (.75, .88, .12), HEAT, .14)
    for y in (-.23, 0, .23):
        mesh.tube((.60, y, 1.986), (1.15, y, 1.986), .102, SAGE, 18)
        for x in (.61, 1.11):
            mesh.tube((x, y, 1.986), (x + .05, y, 1.986), .118, EDGE, 18)
        mesh.tube((.82, y, 1.986), (.93, y, 1.986), .108, (45, 103, 98), 18)
    mesh.anchors['seed-vault'] = (.89, 0, 2.11)
    mesh.box((-.72, .46, 1.77), (.75, .22, .026), SAGE, .03)
    stencil(mesh, 'SN-01', (-1.01, .389, 1.794), .032)
    for side in (-1, 1):
        seam(mesh, [(-1.24, side * .76, 1.58), (-.98, side * .87, 1.59),
                    (.18, side * .91, 1.55), (1.53, side * .74, 1.54)], .040, COPPER)
        for i in range(5):
            x = 1.70 + i * .17
            mesh.box((x, side * .43, 1.704 - i * .046), (.065, .37, .065), HEAT, .015)
    # Rear communications spine with a folded high-gain dish and pressure housings.
    mesh.cyl(2.55, 0, 1.61, .24, .12, HEAT, 20)
    mesh.tube((2.55, 0, 1.74), (2.71, 0, 2.20), .055, EDGE, 12)
    mesh.ball((2.70, 0, 2.18), .26, CERAMIC, stretch=(.24, 1, .85))
    mesh.tube((2.57, 0, 2.17), (2.26, 0, 2.17), .026, COPPER, 8)
    for y in (-.42, .42):
        mesh.tube((3.12, y, 1.46), (3.70, y, 1.46), .098, HEAT, 14)
        mesh.tube((3.64, y, 1.46), (3.73, y, 1.46), .134, EDGE, 14)
    cargo_ramp(mesh)
    return mesh
