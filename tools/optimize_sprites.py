#!/usr/bin/env python3
"""Shrink shipped PNGs without touching resolution, frame counts or geometry.

Measured on this mod's own atlases, the dominant cost is colour variety, not
pixel count: the renderer emits smooth 24-bit gradients that PNG's row
predictors cannot model, so each pixel costs real bytes. Two safe passes:

1. **Colour quantisation of RGB only.** The alpha channel is copied back
   verbatim, so antialiased silhouette edges and soft shadows are bit-exact.
   Collapsing alpha into a palette (ordinary ``pngquant``-style indexing) was
   rejected: it cut the sprites' 74 alpha levels to 6 and visibly hardened
   every edge.
2. **Lossless ``oxipng``** filter/deflate search over the result.

Both passes are guarded: a file is only rewritten when the candidate is
actually smaller and the alpha channel is unchanged. Non-integer downscaling is
never used - resampling a 7k-colour sheet by 1.5x pushed it to 40k colours and
made the file *three times larger*.

Usage::

    python tools/optimize_sprites.py            # optimise, in place
    python tools/optimize_sprites.py --check    # verify everything is optimised
"""
import argparse
import io
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import oxipng
from PIL import Image

from catalog import MOD, ROOT

Image.MAX_IMAGE_PIXELS = None

LEDGER = ROOT / 'docs/art/optimization.json'

# Colour budgets per class of art. Character and machine atlases are broad,
# smoothly shaded surfaces; icons and technology cards are small and flat, so
# they keep a wider palette where the saving would be marginal anyway.
BUDGETS = (
    ('graphics/entity/industry', 128),
    ('graphics/entity/nightglass', 128),
    ('graphics/entity/field-drones', 128),
    ('graphics/technology', 192),
    ('graphics/achievement', 192),
    ('graphics/icons', 192),
    ('graphics/menu', 192),
    ('graphics/entity', 128),
    ('graphics', 192),
)


def budget(relative):
    text = str(relative).replace('\\', '/')
    for prefix, colors in BUDGETS:
        if text.startswith(prefix):
            return colors
    return 192


def encode(image, level=3):
    """Deflate-optimise while keeping true RGBA.

    The mod's atlases must stay colour-type 6: several tests and the engine's
    own atlas builder expect four channels, and oxipng will happily rewrite a
    <=256-colour sheet as an indexed image unless indexing is disabled.
    """
    buffer = io.BytesIO()
    image.save(buffer, 'PNG', optimize=True, compress_level=9)
    return oxipng.optimize_from_memory(buffer.getvalue(), level=level,
                                       strip=oxipng.StripChunks.safe(),
                                       color_type_reduction=False,
                                       palette_reduction=False,
                                       bit_depth_reduction=False,
                                       grayscale_reduction=False)


def optimize_bytes(data, colors):
    """Return the smallest byte string that preserves alpha and resolution."""
    with Image.open(io.BytesIO(data)) as handle:
        source = handle.convert('RGBA')
    alpha = source.getchannel('A')
    best = min(encode(source), data, key=len)
    quantised = source.convert('RGB').quantize(
        colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    quantised.putalpha(alpha)
    candidate = encode(quantised)
    if len(candidate) < len(best):
        # Alpha must survive byte-for-byte, or soft edges would shift.
        with Image.open(io.BytesIO(candidate)) as handle:
            check = handle.convert('RGBA')
        if check.size == source.size and np.array_equal(np.asarray(check.getchannel('A')),
                                                        np.asarray(alpha)):
            best = candidate
    with Image.open(io.BytesIO(best)) as handle:
        assert handle.mode == 'RGBA', handle.mode
    return best


def process(path):
    path = Path(path)
    data = path.read_bytes()
    result = optimize_bytes(data, budget(path.relative_to(MOD)))
    if len(result) < len(data):
        path.write_bytes(result)
    return str(path.relative_to(ROOT)), len(data), min(len(result), len(data))


def targets():
    return sorted(p for p in (MOD / 'graphics').rglob('*.png'))


# Provenance ledgers record a sha256 per generated sprite. Optimising a sprite
# legitimately changes its bytes, so the digests are refreshed in place rather
# than by re-rendering the art (which would be identical pixels at a far higher
# cost). Shapes differ per ledger, so each is walked generically.
LEDGERS = ('docs/art/energy-manifest.json', 'docs/art/drone-manifest.json',
           'docs/art/icon-manifest.json', 'docs/art/achievement-manifest.json',
           'docs/art/lander-render.json', 'docs/art/character-render.json',
           'docs/art/review-manifest.json')


def digest(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve(name, ledger):
    """Ledgers store paths repo-relative, beside the ledger, or as a bare sprite
    filename belonging to the industry atlas folder."""
    for candidate in (ROOT / name, ledger.parent / name,
                      MOD / 'graphics/entity/industry' / name):
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def refresh_ledgers():
    """Re-hash every entry whose recorded digest no longer matches its file."""
    changed = 0
    for relative in LEDGERS:
        ledger = ROOT / relative
        if not ledger.exists():
            continue
        data = json.loads(ledger.read_text())

        def walk(node):
            nonlocal changed
            if isinstance(node, dict):
                for key, value in node.items():
                    if key in ('files', 'inputs') and isinstance(value, dict):
                        for name in list(value):
                            path = resolve(name, ledger)
                            if path and value[name] != (new := digest(path)):
                                value[name] = new
                                changed += 1
                    elif key == 'sha256' and isinstance(value, str):
                        pass
                    else:
                        walk(value)
                # A record shaped {"filename": ..., "sha256": ...}.
                if isinstance(node.get('sha256'), str):
                    name = node.get('filename') or node.get('path') or node.get('file')
                    path = resolve(name, ledger) if name else None
                    if path and node['sha256'] != (new := digest(path)):
                        node['sha256'] = new
                        changed += 1
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(data)
        if 'frame_rgba_sha256' in data:
            changed += relander(data)
        ledger.write_text(json.dumps(data, indent=2) + '\n')
    return changed


def relander(report):
    """The lander ledger also hashes each *composited* frame (static hull plus
    the cropped systems overlay). Those bytes change with the sprite, so they
    are rebuilt exactly the way the exporter and its test compose them."""
    import hashlib
    root = MOD / 'graphics/entity/industry'
    manifest = json.loads((ROOT / 'docs/art/sprite-manifest.json').read_text())
    spec = manifest['lander']
    crop = tuple(report['overlay_crop'][:2])
    hashes = []
    with Image.open(root / 'lander-still.png') as handle:
        hull = handle.convert('RGBA')
    with Image.open(root / 'lander.png') as handle:
        systems = handle.convert('RGBA')
    for i in range(spec['frame_count']):
        overlay = systems.crop((i * spec['width'], 0, (i + 1) * spec['width'], spec['height']))
        frame = hull.copy()
        frame.alpha_composite(overlay, crop)
        hashes.append(hashlib.sha256(frame.tobytes()).hexdigest())
    if report['frame_rgba_sha256'] == hashes:
        return 0
    report['frame_rgba_sha256'] = hashes
    return len(hashes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='fail if any shipped PNG could still be made smaller')
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()

    files = targets()
    if args.check:
        stale = []
        for path in files:
            data = path.read_bytes()
            if len(optimize_bytes(data, budget(path.relative_to(MOD)))) < len(data):
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            print('Unoptimised sprites:', *stale, sep='\n  ')
            return 1
        print(f'OPTIMIZED {len(files)} sprites already minimal')
        return 0

    before = after = 0
    records = {}
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for name, was, now in pool.map(process, files, chunksize=4):
            before += was
            after += now
            records[name] = now
            print(f'{name:70s} {was/1e3:9.1f} -> {now/1e3:9.1f} KB', flush=True)
    LEDGER.write_text(json.dumps({'total_bytes': after, 'files': records}, indent=2) + '\n')
    print(f'Refreshed {refresh_ledgers()} provenance digests')
    print(f'\nSPRITE_BYTES {before} -> {after} '
          f'({100 * (1 - after / before):.1f}% smaller, {(before - after)/1e6:.1f} MB saved)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
