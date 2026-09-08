"""Export one hull/shadow plus an opaque, tightly cropped moving-system overlay.

Rendering a complete ship again over the container used to double its soft
shadow. The overlay now replaces only opaque pixels that actually change. Every
composited frame is checked against the corresponding complete reference render.
"""
import hashlib
import json
import math

import numpy as np
from PIL import Image

from catalog import MOD, ROOT
from industrial_art import render
from lander_model import lander, layout


def export_lander(manifest, save, icon):
    contract = layout()
    view = contract['view']
    width, height, count = view['width'], view['height'], view['frames']
    frames = []
    for frame in range(count):
        frames.append(render(lander(frame / count), width, height, ppu=view['ppu'],
                             origin=view['origin'], map_aligned=True))
        print(f'LANDER frame {frame + 1}/{count}', flush=True)
    pixels = np.stack([np.asarray(frame) for frame in frames])
    changed = np.any(pixels != pixels[0], axis=(0, 3))
    opaque = np.all(pixels[:, :, :, 3] == 255, axis=0)
    assert np.any(changed), 'Standby systems must actually animate'
    assert not np.any(changed & ~opaque), 'Moving systems must not change the hull silhouette or ground shadow'
    mask = Image.fromarray(changed.astype('uint8') * 255, 'L')
    box = mask.getbbox()
    crop = (max(0, math.floor((box[0] - 4) / 2) * 2),
            max(0, math.floor((box[1] - 4) / 2) * 2),
            min(width, math.ceil((box[2] + 4) / 2) * 2),
            min(height, math.ceil((box[3] + 4) / 2) * 2))
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]
    atlas = Image.new('RGBA', (cw * count, ch))
    hashes = []
    for i, full in enumerate(frames):
        overlay = Image.composite(full, Image.new('RGBA', full.size), mask).crop(crop)
        atlas.paste(overlay, (i * cw, 0))
        composite = frames[0].copy()
        composite.alpha_composite(overlay, crop[:2])
        assert composite.tobytes() == full.tobytes(), f'Overlay mismatch in frame {i}'
        hashes.append(hashlib.sha256(full.tobytes()).hexdigest())

    out = MOD / 'graphics/entity/industry'
    save(frames[0], out / 'lander-still.png')
    save(atlas, out / 'lander.png')
    icon(frames[0], 'lander')
    common = {'direction_count': 1, 'scale': view['scale'], 'apply_projection': False}
    manifest['lander-still'] = dict(common,
        filename='__second-nature__/graphics/entity/industry/lander-still.png',
        width=width, height=height, frame_count=1, line_length=1,
        shift=[0, round((.5 - view['origin']) * height * view['scale'] / 32, 6)])
    manifest['lander'] = dict(common,
        filename='__second-nature__/graphics/entity/industry/lander.png',
        width=cw, height=ch, frame_count=count, line_length=count,
        shift=[round((crop[0] + cw / 2 - width / 2) * view['scale'] / 32, 6),
               round((crop[1] + ch / 2 - height * view['origin']) * view['scale'] / 32, 6)])
    report = {
        'description': 'Exact reconstruction from one static hull/shadow and a cropped opaque systems overlay. Offline renders, not gameplay.',
        'art_revision': contract['art_revision'],
        'view': view,
        'overlay_crop': list(crop),
        'moving_pixels': int(np.count_nonzero(changed)),
        'frame_rgba_sha256': hashes,
        'files': {name: hashlib.sha256((out / name).read_bytes()).hexdigest()
                  for name in ('lander-still.png', 'lander.png')},
    }
    (ROOT / 'docs/art/lander-render.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'LANDER overlay {cw} x {ch}; one unchanged hull and ground shadow', flush=True)
    return frames[0]
