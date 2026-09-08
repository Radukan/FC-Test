#!/usr/bin/env python3
"""Original friendly fauna sprites. The illustrated menu background is a separately authored image."""
from pathlib import Path
import math
from PIL import Image
from generate_assets import Art, PAL, DARK, LIGHT, GOLD, fade, mix
from catalog import MOD


def bloomback(frame=0):
    a = Art((96, 96), scale=3)
    a.ellipse((19, 57, 77, 79), (0, 0, 0, 65))
    for side in (-1, 1):
        for leg in range(3):
            y = 37 + leg * 11
            step = math.sin((frame / 4 + leg / 3 + (side + 1) / 4) * math.tau) * 3
            a.line([(48 + side * 17, y), (48 + side * 28, y + step), (48 + side * 31, y + 7 + step)], (40, 91, 86), 5)
            a.ellipse((45 + side * 31, y + 3 + step, 51 + side * 31, y + 9 + step), (106, 182, 135), DARK)
    a.ellipse((22, 25, 74, 74), (29, 82, 77), DARK, 2)
    a.ellipse((24, 24, 72, 69), (66, 143, 119))
    a.ellipse((27, 24, 69, 64), (122, 185, 126))
    a.poly([(48, 26), (31, 34), (29, 49), (44, 65), (48, 57)], (141, 206, 148), (39, 108, 95), 1.4)
    a.poly([(48, 26), (65, 34), (67, 49), (52, 65), (48, 57)], (91, 180, 150), (39, 108, 95), 1.4)
    a.line([(48, 27), (48, 61)], (221, 223, 154), 1.4)
    for y in (36, 44, 52):
        a.line([(48, y + 3), (35, y - 4)], (182, 222, 151), 1)
        a.line([(48, y + 3), (61, y - 4)], (157, 214, 173), 1)
    for x in (39, 57):
        a.line([(x, 23), (x - 4, 11), (x + 1, 7)], (60, 133, 110), 2)
        a.ellipse((x - 2, 3, x + 5, 10), (222, 218, 146), (78, 135, 108), 1)
    a.ellipse((33, 14, 63, 35), (80, 169, 157), DARK, 1.3)
    for x in (39, 54):
        a.ellipse((x - 3, 18, x + 4, 27), (233, 238, 209))
        a.ellipse((x, 21, x + 3, 26), (27, 66, 64))
        a.ellipse((x, 20, x + 1.3, 22), (255, 255, 235))
    a.arc((43, 23, 54, 31), 20, 160, (38, 108, 99), 1)
    # A soft flowering carapace, not the hostile spiked biter silhouette.
    for i in range(5):
        t = i * math.tau / 5
        x, y = 48 + math.cos(t) * 6, 42 + math.sin(t) * 6
        a.ellipse((x - 4, y - 5, x + 4, y + 5), (236, 218, 147), (180, 166, 98), .6)
    a.ellipse((44, 38, 52, 46), (219, 163, 88), (134, 119, 59), .8)
    return a.image.resize((96, 96), Image.Resampling.LANCZOS)


def generate():
    folder = MOD / 'graphics/entity'
    folder.mkdir(parents=True, exist_ok=True)
    atlas = Image.new('RGBA', (384, 768))
    for direction in range(8):
        for frame in range(4):
            image = bloomback(frame).rotate(-direction * 45, resample=Image.Resampling.BICUBIC)
            atlas.alpha_composite(image, (frame * 96, direction * 96))
    atlas.save(folder / 'bloomback.png', optimize=True)
    bloomback().resize((64, 64), Image.Resampling.LANCZOS).save(MOD / 'graphics/icons/bloomback.png', optimize=True)
    a = Art((256, 192), scale=2)
    a.ellipse((15, 66, 245, 180), (0, 0, 0, 65))
    for i in range(7):
        a.ellipse((19 + i, 43 + i, 236 - i, 169 - i), mix((36, 73, 69), (100, 143, 92), i / 6))
    for i in range(24):
        t = i * math.tau / 24
        x, y = 128 + math.cos(t) * 94, 106 + math.sin(t) * 48
        a.ellipse((x - 12, y - 6, x + 12, y + 7), (125, 144, 116), (48, 85, 74), 1)
    for i in range(13):
        x, y = 48 + (i * 43) % 166, 65 + (i * 23) % 77
        a.line([(x, y + 17), (x, y - 17)], (53, 122, 97), 3)
        a.leaf(x - 6, y + 4, .9, (79, 163, 124))
        a.leaf(x + 7, y - 6, 1.1, (137, 193, 121))
        for j in range(5):
            t = j * math.tau / 5
            bx, by = x + math.cos(t) * 8, y - 16 + math.sin(t) * 6
            a.ellipse((bx - 5, by - 5, bx + 5, by + 5), (204, 228, 179), (112, 167, 135), .7)
        a.ellipse((x - 3, y - 19, x + 3, y - 13), (234, 185, 101))
    a.save(folder / 'bloom-nest.png')
    print('Generated Bloomback: 8 directions × 4 walking frames, icon and symbiotic bloom nest.')

if __name__ == '__main__':
    generate()
