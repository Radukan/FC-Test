#!/usr/bin/env python3
"""Review actual exported assets without re-rendering meshes. Not game footage.

Uses canonical catalog art keys, never obsolete compact aliases. Animation panels
keep a fixed full-frame crop throughout the loop. A fingerprint ledger prevents
stale art previews from being presented as current work.
"""
import hashlib
import json
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont
from catalog import ROOT, MOD, load_catalog

ART = ROOT / 'docs/art'
BACKGROUND = (22, 31, 30)
PANEL = (30, 40, 37)
CREAM = (227, 224, 203)
MUTED = (161, 177, 157)
ACCENT = (186, 191, 131)
INPUTS = {}
MANIFEST = {}


def font(size=14, bold=False):
    path = '/usr/share/fonts/truetype/dejavu/DejaVuSans' + ('-Bold' if bold else '') + '.ttf'
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


def load(name):
    spec = MANIFEST[name]
    path = MOD / spec['filename'].split('__second-nature__/')[1]
    INPUTS[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return Image.open(path), spec


def tile(image, spec, direction=0, frame=0):
    index = direction * spec['frame_count'] + frame
    x = index % spec['line_length'] * spec['width']
    y = index // spec['line_length'] * spec['height']
    return image.crop((x, y, x + spec['width'], y + spec['height']))


def fit_sprite(sheet, image, box, trim=False):
    """Static contact cards may trim alpha; animated panels never trim per frame."""
    if trim:
        bounds = image.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
        image = image.crop(bounds)
    else:
        image = image.copy()
    image.thumbnail((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    x = box[0] + (box[2] - box[0] - image.width) // 2
    y = box[1] + (box[3] - box[1] - image.height) // 2
    sheet.paste(image, (x, y), image)


def header(sheet, title, subtitle):
    d = ImageDraw.Draw(sheet)
    d.text((28, 20), title, font=font(25, True), fill=CREAM)
    d.text((28, 58), subtitle, font=font(13), fill=MUTED)
    d.line((28, 86, sheet.width - 28, 86), fill=(67, 83, 68))


def durations(count, frame_ms):
    # GIF delays are integral centiseconds. Distribute rounding, don't speed up
    # every mining frame by flooring 64.10 ms to 60 ms.
    return [round((i + 1) * frame_ms / 10) * 10 - round(i * frame_ms / 10) * 10 for i in range(count)]


def save_gif(frames, name, duration):
    palette = frames[0].quantize(colors=256)
    converted = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    converted[0].save(ART / name, save_all=True, append_images=converted[1:],
                      duration=duration, loop=0, optimize=False, disposal=1)


def lander_frames():
    hull, _ = load('lander-still')
    systems, spec = load('lander')
    report_path = ART / 'lander-render.json'
    report = json.loads(report_path.read_text())
    INPUTS[str(report_path.relative_to(ROOT))] = hashlib.sha256(report_path.read_bytes()).hexdigest()
    frames = []
    for i in range(spec['frame_count']):
        full = hull.copy()
        full.alpha_composite(tile(systems, spec, frame=i), tuple(report['overlay_crop'][:2]))
        frames.append(full)
    hull.close()
    systems.close()
    return frames


def contact_sheet(catalog):
    entries = [(m['title'], m['art_name'] + '-north', f"{m['footprint']} x {m['footprint']} tiles")
               for m in catalog['machines']]
    entries += [
        ('Wayfarer expedition lander', 'lander-still', 'Permanent camp / preserved footprint'),
        ('Rootweaver emplacement', 'sentry-turret-fire', 'Mycelial defense'),
        ('Resonance diffuser', 'arc-turret-fire', 'Electrical / pheromonal defense'),
        ('Atmospheric pressure lance', 'lance-turret-fire', 'Line weapon'),
        ('Riveted power pole', 'field-pole-north', 'Mineral-built infrastructure'),
        ('Mineral-frame crate', 'field-crate-north', 'Wood-free storage'),
        ('Vector servo inserter', 'vector-inserter-north', 'Precision logistics'),
        ('Canopy stack inserter', 'canopy-inserter-north', 'Endgame stacked cargo'),
        ('Vital distribution manifold', 'vital-splitter-north', 'Matched 90-item/s belt family'),
        ('Expedition jukebox', 'jukebox-north', 'Local archive playback'),
        ('Explorer / field gear', 'explorer-0-idle', 'Authored adult character'),
        ('Explorer / modular gear', 'explorer-1-idle', 'Articulated rig'),
        ('Explorer / bastion gear', 'explorer-2-idle', 'Third armor appearance'),
    ]
    cw, ch, columns = 300, 310, 4
    sheet = Image.new('RGB', (cw * columns, 110 + ch * math.ceil(len(entries) / columns)), BACKGROUND)
    header(sheet, 'SECOND NATURE / VERDANT WORKS', 'Current exported sprites. New-build footprints. Source-art inspection, not game screenshots.')
    d = ImageDraw.Draw(sheet)
    for i, (label, name, caption) in enumerate(entries):
        x, y = i % columns * cw, 100 + i // columns * ch
        d.rounded_rectangle((x + 10, y + 8, x + cw - 10, y + ch - 8), radius=7, fill=PANEL)
        source, spec = load(name)
        frame = tile(source, spec, direction=4 if name.startswith('explorer') else 0)
        fit_sprite(sheet, frame, (x + 18, y + 18, x + cw - 18, y + 242), trim=True)
        source.close()
        d.text((x + 22, y + 253), label, font=font(13, True), fill=CREAM)
        d.text((x + 22, y + 277), caption, font=font(11), fill=MUTED)
    sheet.save(ART / 'ironbound-contact-sheet.jpg', quality=92, optimize=True)


def character_reviews():
    from character_layout import ARMED_ROWS
    from gait import MINING_SPEED
    directions = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW')
    image, spec = load('explorer-0-running_with_gun')
    contact = Image.new('RGB', (6 * 220, 3 * 305 + 105), BACKGROUND)
    header(contact, 'ARMED LOCOMOTION / 18 NATIVE ROWS', 'Aim and stride are independent; the engine mirrors the remaining facings. Full fixed-pivot frames.')
    d = ImageDraw.Draw(contact)
    for row, (aim, stride) in enumerate(ARMED_ROWS):
        x, y = row % 6 * 220, 100 + row // 6 * 305
        fit_sprite(contact, tile(image, spec, row, 12), (x + 6, y + 4, x + 214, y + 259))
        d.text((x + 12, y + 268), f'Row {row}: aim {directions[aim]} / stride {directions[stride]}', font=font(11), fill=CREAM)
    contact.save(ART / 'character-aim-layout.jpg', quality=92, optimize=True)

    running, rspec = load('explorer-0-running')
    frames = []
    for f in range(rspec['frame_count']):
        sheet = Image.new('RGB', (4 * 310, 474), BACKGROUND)
        header(sheet, 'THE EXPLORER / ARTICULATED LOCOMOTION', 'Slowed source review: planted stance, raised swing, bent knees and gloved hands. Native movement is distance-driven.')
        d = ImageDraw.Draw(sheet)
        for i, (source, s, row, label) in enumerate([
                (running, rspec, 2, 'Profile / east'), (running, rspec, 4, 'Front / south'),
                (running, rspec, 1, 'Three-quarter / northeast'), (image, spec, 7, 'Armed / aim east, stride north')]):
            x = i * 310
            fit_sprite(sheet, tile(source, s, row, f), (x + 5, 93, x + 305, 420))
            d.text((x + 15, 434), label, font=font(13), fill=CREAM)
        frames.append(sheet)
    save_gif(frames, 'locomotion-review.gif', 80)
    image.close()
    running.close()

    source, spec = load('explorer-0-mining_with_tool')
    frames = []
    for f in range(spec['frame_count']):
        sheet = Image.new('RGB', (4 * 310, 492), BACKGROUND)
        header(sheet, 'MINING / THE POINT LEADS THE STRIKE', 'Twenty authored frames at 0.26 animation speed. Complete tool/shadow canvas; unchanged gameplay mining speed.')
        d = ImageDraw.Draw(sheet)
        for i, direction in enumerate((0, 2, 4, 6)):
            x = i * 310
            fit_sprite(sheet, tile(source, spec, direction, f), (x + 5, 90, x + 305, 435))
            d.text((x + 15, 451), 'Mining / ' + directions[direction], font=font(13), fill=CREAM)
        frames.append(sheet)
    save_gif(frames, 'mining-framing-preview.gif', durations(spec['frame_count'], 1000 / (60 * MINING_SPEED)))
    source.close()


def industrial_review(catalog):
    names = ('algae-vat', 'hydroponics-bay', 'electrolyzer', 'reclamation-plant',
             'materials-kiln', 'watershed', 'sanctuary', 'planetary-beacon')
    by_name = {m['name']: m for m in catalog['machines']}
    loaded = [(by_name[name], *load(by_name[name]['art_name'] + '-north')) for name in names]
    frames = []
    for f in range(8):
        sheet = Image.new('RGB', (4 * 280, 688), BACKGROUND)
        header(sheet, 'PROCESS ARCHITECTURES / THE LIVING FACTORY', 'Fermentation trains, greenhouse terraces, membrane banks and habitat courts. Slowed source loops, not gameplay.')
        d = ImageDraw.Draw(sheet)
        for i, (m, source, spec) in enumerate(loaded):
            x, y = i % 4 * 280, 98 + i // 4 * 290
            fit_sprite(sheet, tile(source, spec, frame=f), (x + 6, y, x + 274, y + 240))
            d.text((x + 12, y + 244), m['title'], font=font(12, True), fill=CREAM)
            d.text((x + 12, y + 266), f"{m['footprint']} x {m['footprint']} / new construction", font=font(11), fill=MUTED)
        frames.append(sheet)
    save_gif(frames, 'industrial-animation-preview.gif', 100)
    for _, source, _ in loaded:
        source.close()


def ship_review():
    frames = lander_frames()
    sheet = Image.new('RGB', (1280, 924), BACKGROUND)
    d = ImageDraw.Draw(sheet)
    d.text((42, 28), 'SECOND NATURE / VERDANT WORKS', font=font(15, True), fill=ACCENT)
    d.text((38, 58), 'WAYFARER', font=font(57, True), fill=CREAM)
    d.text((42, 136), 'An expedition craft. Not a crash site.', font=font(21), fill=MUTED)
    d.line((42, 180, 1238, 180), fill=(65, 82, 65))
    fit_sprite(sheet, frames[0], (24, 198, 916, 817), trim=True)
    notes = [
        ('01 / FLIGHT DECK', 'Tapered steel and ceramic hull. Sloped, divided cockpit glazing.'),
        ('02 / PROPULSION', 'Twin engine pods, cold exhaust bells, lift ducts and swept stabilizers.'),
        ('03 / LIVING CARGO', 'Sealed seed canisters, copper service loops and folded solar cells.'),
        ('04 / GROUND SYSTEMS', 'Splayed hydraulic struts, maintenance hatches and a cargo ramp.'),
    ]
    for i, (title, text) in enumerate(notes):
        y = 232 + i * 138
        d.text((936, y), title, font=font(15, True), fill=ACCENT)
        for j, line in enumerate(textwrap.wrap(text, 32)):
            d.text((936, y + 30 + j * 22), line, font=font(15), fill=CREAM)
    d.line((42, 834, 1238, 834), fill=(65, 82, 65))
    d.text((42, 856), 'PRESERVED / collision footprint, 48 cargo slots, permanent protection and existing save identity.', font=font(15), fill=CREAM)
    d.text((42, 889), 'Original authored sprite composite. Source-art preview, not a graphical Factorio screenshot.', font=font(13), fill=MUTED)
    sheet.save(ART / 'lander-review.jpg', quality=94, optimize=True)

    animation = []
    for frame in frames:
        sheet = Image.new('RGB', (1024, 766), BACKGROUND)
        header(sheet, 'WAYFARER / STANDBY SYSTEMS', 'One static hull and ground shadow. Only fan wells and navigation lights are overlaid.')
        fit_sprite(sheet, frame, (32, 100, 992, 727), trim=True)
        ImageDraw.Draw(sheet).text((28, 739), 'Native authored standby rate / source sprites, not in-game footage.', font=font(13), fill=MUTED)
        animation.append(sheet)
    # No need for the optional renderer to read the shared view/speed contract.
    from lander_model import layout
    save_gif(animation, 'lander-standby.gif', durations(len(frames), 1000 / (60 * layout()['animation_speed'])))


def generate():
    global MANIFEST
    INPUTS.clear()
    MANIFEST = json.loads((ART / 'sprite-manifest.json').read_text())
    catalog = load_catalog()
    contact_sheet(catalog)
    character_reviews()
    industrial_review(catalog)
    ship_review()
    outputs = ('ironbound-contact-sheet.jpg', 'character-aim-layout.jpg', 'locomotion-review.gif',
               'mining-framing-preview.gif', 'industrial-animation-preview.gif', 'lander-review.jpg', 'lander-standby.gif')
    report = {
        'description': 'Current source-art review ledger. These files are not game screenshots or gameplay certification.',
        'version': json.loads((MOD / 'info.json').read_text())['version'],
        'inputs': dict(sorted(INPUTS.items())),
        'outputs': {name: hashlib.sha256((ART / name).read_bytes()).hexdigest() for name in outputs},
        'canonical_machines': {m['name']: {'art_name': m['art_name'], 'footprint': m['footprint']} for m in catalog['machines']},
    }
    (ART / 'review-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Generated current contact, aim, locomotion, mining, process and ship reviews.')


if __name__ == '__main__':
    generate()
