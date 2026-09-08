#!/usr/bin/env python3
"""Render original 128 px achievement medallions from the shared milestone list.

Each medallion is drawn from primitives, never traced from a game asset. The
emblem inside every ring is unique so the achievement window stays readable at
its real display size, and a fingerprint ledger keeps the shipped PNGs honest.
"""
import hashlib
import json
import math

from PIL import Image, ImageDraw, ImageFilter

from catalog import ROOT, MOD, load_module
from generate_assets import Art, PAL, DARK, GOLD, LIGHT, fade, mix

SIZE = 128
OUT = MOD / 'graphics/achievement'

# Ring colour per milestone family, so a glance separates progress from mastery.
FAMILY = {
    'first-breath': 'atmosphere', 'root-systems': 'soil', 'a-living-world': 'biodiversity',
    'new-growth': 'biodiversity', 'terraformer': 'soil', 'deep-green': 'atmosphere',
    'signal-restored': 'temperature', 'common-ground': 'biodiversity', 'quiet-eden': 'toxicity',
    'hold-the-line': 'pressure', 'field-stations': 'water', 'second-nature': 'stage',
    'first-gust': 'atmosphere', 'network-nodes': 'stability', 'coordination-cells': 'stage',
    'matrix-gardener': 'biodiversity', 'read-the-world': 'temperature', 'no-shortcuts': 'water',
    'nightglass-grid': 'stability',
}


def plate(colour):
    """A struck metal disc with a bevel and a coloured inner ring."""
    a = Art((SIZE, SIZE), 2)
    shadow = Image.new('RGBA', a.image.size)
    ImageDraw.Draw(shadow).ellipse(a.box((10, 14, 118, 122)), fill=(0, 0, 0, 120))
    a.image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(6)))
    a.ellipse((6, 6, 122, 122), (38, 50, 46, 255), fade(colour, .55), 3)
    a.ellipse((12, 12, 116, 116), (26, 37, 35, 255), fade(GOLD, .8), 1.5)
    a.ellipse((17, 17, 111, 111), (21, 31, 30, 255))
    for step in range(36):
        angle = step * math.tau / 36
        x, y = 64 + 52 * math.cos(angle), 64 + 52 * math.sin(angle)
        a.ellipse((x - 1.2, y - 1.2, x + 1.2, y + 1.2), fade(colour, .75 if step % 3 else 1.0))
    return a


def horizon(a, colour, height=78):
    """The recurring planetary curve that ties the whole set together."""
    a.arc((14, height - 44, 114, height + 56), 188, 352, fade(colour, .85), 2.5)
    a.poly([(22, height + 4), (64, height - 13), (106, height + 4), (106, height + 16), (22, height + 16)],
           (30, 46, 42, 255))


def emblem(a, name, colour):
    if name == 'first-breath':
        for i in range(3):
            a.arc((26 + i * 5, 30 + i * 11, 102 - i * 5, 60 + i * 11), 190, 350, mix(colour, LIGHT, i * .25), 3)
        a.leaf(64, 88, 1.5, PAL['biodiversity'])
    elif name == 'root-systems':
        # Soil band with a rooted stem: the roots are the subject, not the canopy.
        a.poly([(20, 82), (108, 82), (108, 104), (20, 104)], mix(colour, DARK, .35), None)
        a.line([(64, 84), (64, 44)], (126, 102, 70, 255), 4)
        a.leaf(78, 44, 1.5, PAL['biodiversity'])
        a.leaf(48, 58, 1.1, mix(PAL['biodiversity'], LIGHT, .35))
        for side in (-1, 1):
            for i in range(3):
                a.line([(64, 84), (64 + side * (9 + i * 8), 92 + i * 4), (64 + side * (15 + i * 12), 101 + i * 2)],
                       mix(colour, LIGHT, .35 - i * .1), 2)
    elif name == 'a-living-world':
        a.ellipse((30, 30, 98, 98), (34, 68, 58, 255), fade(colour, .8), 2)
        a.arc((30, 30, 98, 98), 20, 160, LIGHT, 2)
        for x, y, s in [(50, 62, 1.0), (74, 56, 1.3), (62, 80, .9)]:
            a.leaf(x, y, s, PAL['biodiversity'])
    elif name == 'new-growth':
        horizon(a, colour)
        for x, s in [(40, .9), (64, 1.35), (88, 1.0)]:
            a.line([(x, 82), (x, 82 - 22 * s)], (104, 84, 58, 255), 3)
            a.leaf(x + 7 * s, 62 - 12 * s, s, PAL['biodiversity'])
            a.leaf(x - 9 * s, 70 - 8 * s, s * .8, mix(PAL['biodiversity'], LIGHT, .3))
    elif name == 'terraformer':
        for row, y in enumerate((50, 66, 82)):
            a.poly([(20, y), (64, y - 15), (108, y), (64, y + 15)],
                   mix((116, 92, 68), PAL['biodiversity'], .45 - row * .2), DARK, 1)
        a.leaf(64, 46, 1.2, PAL['biodiversity'])
    elif name == 'deep-green':
        # A filter column pulling a plume down and out of the air.
        a.rect((46, 30, 82, 100), (40, 56, 53, 255), fade(colour, .85), 2, r=5)
        a.rect((41, 30, 87, 39), GOLD, DARK, 1.5, r=2)
        a.rect((41, 91, 87, 100), GOLD, DARK, 1.5, r=2)
        for i in range(4):
            a.line([(52, 46 + i * 12), (76, 46 + i * 12)], fade(colour, .9 - i * .12), 2.5)
        for i, (x, y) in enumerate(((26, 44), (26, 62), (102, 52), (102, 70))):
            a.arc((x - 16, y - 12, x + 16, y + 12), 200 if x < 64 else 340, 340 if x < 64 else 200,
                  fade(colour, .7 - i * .1), 2)
        a.leaf(64, 112, 1.1, PAL['biodiversity'])
    elif name == 'signal-restored':
        a.poly([(64, 26), (76, 60), (76, 86), (52, 86), (52, 60)], (176, 184, 168, 255), DARK, 1.5)
        a.poly([(52, 86), (46, 100), (64, 92), (82, 100), (76, 86)], fade(colour, .8), DARK, 1)
        a.line([(64, 40), (64, 68)], colour, 2)
        for i in range(3):
            a.arc((36 - i * 8, 12 - i * 8, 92 + i * 8, 68 + i * 8), 235, 305, mix(colour, LIGHT, i * .3), 2)
    elif name == 'common-ground':
        a.ellipse((26, 44, 76, 94), (0, 0, 0, 0), PAL['biodiversity'], 3)
        a.ellipse((52, 44, 102, 94), (0, 0, 0, 0), fade(colour, .85), 3)
        a.leaf(64, 68, 1.1, mix(PAL['biodiversity'], LIGHT, .35))
    elif name == 'quiet-eden':
        horizon(a, colour, 82)
        a.ellipse((44, 30, 84, 70), (30, 44, 44, 255), fade(colour, .7), 2)
        a.line([(50, 36), (78, 64)], fade(colour, .9), 3)
        a.line([(78, 36), (50, 64)], fade(colour, .9), 3)
        a.leaf(94, 78, .9, PAL['biodiversity'])
    elif name == 'hold-the-line':
        a.poly([(64, 24), (100, 40), (100, 74), (64, 104), (28, 74), (28, 40)],
               (44, 62, 58, 255), fade(colour, .9), 3)
        a.line([(40, 58), (88, 58)], GOLD, 3); a.line([(40, 74), (88, 74)], GOLD, 3)
        a.leaf(64, 56, 1.2, PAL['biodiversity'])
    elif name == 'field-stations':
        for i in range(5):
            angle = i * math.tau / 5 - math.pi / 2
            x, y = 64 + 32 * math.cos(angle), 64 + 32 * math.sin(angle)
            a.line([(64, 64), (x, y)], fade(colour, .55), 1.5)
            a.ellipse((x - 8, y - 8, x + 8, y + 8), fade(colour, .85), DARK, 1.5)
        a.ellipse((54, 54, 74, 74), (30, 48, 44, 255), GOLD, 1.5)
        a.leaf(64, 66, .8, PAL['biodiversity'])
    elif name == 'second-nature':
        a.ellipse((28, 28, 100, 100), (30, 58, 52, 255), fade(colour, .8), 2.5)
        for i in range(5):
            angle = i * math.tau / 5 - math.pi / 2
            x, y = 64 + 44 * math.cos(angle), 64 + 44 * math.sin(angle)
            a.ellipse((x - 5, y - 5, x + 5, y + 5), GOLD, DARK, 1)
        a.line([(64, 88), (64, 54), (72, 44)], LIGHT, 3)
        a.leaf(74, 52, 1.2, PAL['biodiversity']); a.leaf(52, 70, .9, mix(PAL['biodiversity'], LIGHT, .3))
    elif name == 'first-gust':
        a.line([(64, 96), (64, 50)], (168, 176, 162, 255), 4)
        for i in range(3):
            angle = i * math.tau / 3 - math.pi / 2
            a.poly([(64, 50), (64 + 34 * math.cos(angle), 50 + 34 * math.sin(angle)),
                    (64 + 26 * math.cos(angle + .5), 50 + 26 * math.sin(angle + .5))], fade(colour, .9), DARK, 1)
        a.ellipse((58, 44, 70, 56), GOLD, DARK, 1)
        for i in range(2):
            a.arc((14, 24 + i * 62, 60, 50 + i * 62), 200, 340, fade(colour, .6), 2)
    elif name == 'network-nodes':
        for i in range(5):
            angle = i * math.tau / 5 - math.pi / 2
            x, y = 64 + 33 * math.cos(angle), 64 + 33 * math.sin(angle)
            nx, ny = 64 + 33 * math.cos(angle + math.tau / 5), 64 + 33 * math.sin(angle + math.tau / 5)
            a.line([(x, y), (nx, ny)], fade(colour, .55), 1.5)
            a.poly([(x, y - 10), (x + 8, y + 6), (x - 8, y + 6)], fade(colour, .9), DARK, 1)
        a.ellipse((57, 57, 71, 71), GOLD, DARK, 1.5)
    elif name == 'coordination-cells':
        for row in range(2):
            for col in range(3):
                x, y = 36 + col * 28, 48 + row * 30
                pts = [(x + 12 * math.cos(k * math.tau / 6), y + 12 * math.sin(k * math.tau / 6)) for k in range(6)]
                a.poly(pts, fade(colour, .55 + row * .2), fade(GOLD, .9), 1.2)
                a.ellipse((x - 3, y - 3, x + 3, y + 3), LIGHT)
    elif name == 'matrix-gardener':
        for row in range(3):
            for col in range(3):
                x, y = 40 + col * 24, 40 + row * 24
                a.ellipse((x - 8, y - 8, x + 8, y + 8), fade(PAL['biodiversity'], .35 + .2 * ((row + col) % 3)),
                          fade(colour, .8), 1)
        a.leaf(64, 64, 1.3, LIGHT)
    elif name == 'read-the-world':
        a.rect((26, 32, 102, 96), (36, 50, 47, 255), fade(colour, .85), 2, r=6)
        for i in range(4):
            a.line([(34, 46 + i * 13), (94, 46 + i * 13)], fade(GOLD, .7 - i * .1), 1.5)
        a.line([(34, 84), (50, 66), (62, 76), (78, 50), (94, 58)], PAL['biodiversity'], 3)
        a.leaf(94, 50, .8, PAL['biodiversity'])
    elif name == 'no-shortcuts':
        a.ellipse((30, 30, 98, 98), (0, 0, 0, 0), fade(colour, .9), 3)
        a.line([(40, 40), (88, 88)], fade(colour, .9), 3)
        a.poly([(64, 44), (78, 74), (50, 74)], (92, 78, 62, 255), DARK, 1.5)
        a.line([(64, 44), (64, 26)], fade((120, 120, 120), 1), 2)
        a.leaf(88, 44, 1.0, PAL['biodiversity'])
    elif name == 'nightglass-grid':
        horizon(a, colour, 88)
        for x in (38, 64, 90):
            a.poly([(x - 13, 74), (x + 13, 62), (x + 13, 70), (x - 13, 82)], fade(colour, .8), DARK, 1)
            a.line([(x, 78), (x, 90)], (150, 158, 146, 255), 2)
        a.ellipse((54, 24, 74, 44), GOLD, DARK, 1.5)
        for i in range(6):
            angle = i * math.tau / 6
            a.line([(64 + 14 * math.cos(angle), 34 + 14 * math.sin(angle)),
                    (64 + 21 * math.cos(angle), 34 + 21 * math.sin(angle))], fade(GOLD, .8), 1.5)
    else:
        raise KeyError(name)


def generate():
    milestones = load_module('shared.achievements')
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for entry in milestones['all']:
        name = entry['name']
        colour = PAL[FAMILY[name]]
        art = plate(colour)
        emblem(art, name, colour)
        path = OUT / (name + '.png')
        art.save(path, (SIZE, SIZE))
        manifest[name] = {
            'kind': 'script' if entry.get('script') else entry['kind'],
            'file': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    # One sheet so the whole set can be judged together at real display size.
    names = sorted(manifest)
    columns = 5
    rows = math.ceil(len(names) / columns)
    sheet = Image.new('RGB', (columns * 150, 60 + rows * 168), (26, 34, 32))
    draw = ImageDraw.Draw(sheet)
    from PIL import ImageFont
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    draw.text((18, 20), 'SECOND NATURE / ACHIEVEMENT MEDALLIONS / 128 px, original geometry',
              font=font, fill=(226, 230, 210))
    for index, name in enumerate(names):
        x, y = index % columns * 150 + 11, 56 + index // columns * 168
        with Image.open(OUT / (name + '.png')) as image:
            sheet.paste(image, (x, y), image)
        for line, part in enumerate(__import__('textwrap').wrap(name, 20)):
            draw.text((x, y + 132 + line * 15), part, font=font, fill=(206, 216, 198))
    sheet.save(ROOT / 'docs/art/achievement-review.jpg', quality=92, optimize=True)
    (ROOT / 'docs/art/achievement-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('ACHIEVEMENT_ART', len(manifest), flush=True)


if __name__ == '__main__':
    generate()
