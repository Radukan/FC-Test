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
from atlas_io import Atlas, paths as atlas_paths

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
    if 'stripes' in spec:
        for path in atlas_paths(spec):INPUTS[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        return Atlas(spec),spec
    path = MOD / spec['filename'].split('__second-nature__/')[1]
    INPUTS[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return Image.open(path), spec


def tile(image, spec, direction=0, frame=0):
    if isinstance(image,Atlas):return image.frame(direction,frame)
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
    entries += [(p['title'],p['name']+'-north',f"{p['size']} x {p['size']} / power") for p in catalog.get('energy',{}).get('plants',[])]
    entries += [(t['title'],t['name'],f"Solar only / {t['battery_joules']/1e6:.0f} MJ") for t in catalog.get('energy',{}).get('trains',[])]
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
        ('Wind-up construction drone', 'field-drone-flying', 'Inventory-fed / no network'),
        ('Field drone controller', 'field-controller-icon', 'Auto-enabled / Ctrl + Shift + B'),
        ('Warden / field gear', 'warden-0-idle', 'Sealed restoration warden'),
        ('Warden / modular gear', 'warden-1-idle', 'Articulated rig'),
        ('Warden / bastion gear', 'warden-2-idle', 'Third armor appearance'),
    ]
    cw, ch, columns = 300, 310, 4
    sheet = Image.new('RGB', (cw * columns, 110 + ch * math.ceil(len(entries) / columns)), BACKGROUND)
    header(sheet, 'SECOND NATURE / NIGHTGLASS', 'Current exported sprites. New-build footprints. Source-art inspection, not game screenshots.')
    d = ImageDraw.Draw(sheet)
    for i, (label, name, caption) in enumerate(entries):
        x, y = i % columns * cw, 100 + i // columns * ch
        d.rounded_rectangle((x + 10, y + 8, x + cw - 10, y + ch - 8), radius=7, fill=PANEL)
        source, spec = load(name)
        frame = tile(source, spec, direction=4 if name.startswith('warden') else 0)
        fit_sprite(sheet, frame, (x + 18, y + 18, x + cw - 18, y + 242), trim=True)
        source.close()
        d.text((x + 22, y + 253), label, font=font(13, True), fill=CREAM)
        d.text((x + 22, y + 277), caption, font=font(11), fill=MUTED)
    sheet.save(ART / 'ironbound-contact-sheet.jpg', quality=92, optimize=True)


def character_reviews():
    from character_layout import ARMED_ROWS
    from gait import MINING_SPEED
    directions = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW')
    image, spec = load('warden-0-running_with_gun')
    contact = Image.new('RGB', (6 * 220, 3 * 305 + 105), BACKGROUND)
    header(contact, 'ARMED LOCOMOTION / 18 NATIVE ROWS', 'Aim and stride are independent; the engine mirrors the remaining facings. Full fixed-pivot frames.')
    d = ImageDraw.Draw(contact)
    for row, (aim, stride) in enumerate(ARMED_ROWS):
        x, y = row % 6 * 220, 100 + row // 6 * 305
        fit_sprite(contact, tile(image, spec, row, 12), (x + 6, y + 4, x + 214, y + 259))
        d.text((x + 12, y + 268), f'Row {row}: aim {directions[aim]} / stride {directions[stride]}', font=font(11), fill=CREAM)
    contact.save(ART / 'character-aim-layout.jpg', quality=92, optimize=True)

    running, rspec = load('warden-0-running')
    frames = []
    for f in range(rspec['frame_count']):
        sheet = Image.new('RGB', (4 * 310, 474), BACKGROUND)
        header(sheet, 'THE EXPLORER / ARTICULATED LOCOMOTION', 'Slowed source review: hip/shoulder counter-rotation, independent head bob, weight transfer and grounded feet.')
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

    source, spec = load('warden-0-mining_with_tool')
    frames = []
    for f in range(spec['frame_count']):
        sheet = Image.new('RGB', (4 * 310, 492), BACKGROUND)
        header(sheet, 'MINING / RIGHT HAND AT 48% OF THE SHAFT', 'Right grip near the midpoint; lower left-hand support. Rounded boots, weighted impact, unchanged mining speed.')
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
    d.text((42, 28), 'SECOND NATURE / NIGHTGLASS', font=font(15, True), fill=ACCENT)
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


def field_crew_review():
    source, spec = load('field-drone-flying')
    shadow, shadow_spec = load('field-drone-flying-shadow')
    working, work_spec = load('field-drone-working')
    work_shadow, ws_spec = load('field-drone-working-shadow')
    frames = []
    for f in range(64):
        sheet = Image.new('RGB', (880, 510), BACKGROUND)
        header(sheet, 'FIELD DRONES / DIRECTIONAL 3D MOTION', 'Source-sprite motion study, not gameplay footage. In-game positions update every tick.')
        d = ImageDraw.Draw(sheet)
        for y in range(128,450,28):d.line((30,y,850,y),fill=(35,48,41))
        for x in range(30,851,28):d.line((x,128,x,450),fill=(35,48,41))
        phase=f/64*math.tau
        for i, (body, bs, ground, gs) in enumerate([(source,spec,shadow,shadow_spec),(working,work_spec,work_shadow,ws_spec)]):
            a=phase+i*math.pi
            x=440+255*math.cos(a);y=285+92*math.sin(a)
            vx=-255*math.sin(a);vy=92*math.cos(a)
            heading=round((math.atan2(vx,-vy)/math.tau)%1*bs['direction_count'])%bs['direction_count']
            image=tile(ground,gs,heading,f%8);image.alpha_composite(tile(body,bs,heading,f%8))
            sheet.paste(image,(round(x-image.width/2),round(y-image.height*.52)),image)
        d.text((30,468),'AUTO-ENABLED WITH KIT  |  Ctrl + Shift + B: pause / resume and monitor',font=font(15),fill=CREAM)
        frames.append(sheet)
    save_gif(frames, 'field-drone-preview.gif', 50)
    for image in (source, shadow, working, work_shadow):image.close()

    sheet=Image.new('RGB',(1200,870),BACKGROUND)
    header(sheet,'FIELD CREW / SECOND NATURE '+json.loads((MOD/'info.json').read_text())['version'],'Auto-enabled inventory crews, planner work, directional 3D drone sprites and a sealed warden silhouette.')
    d=ImageDraw.Draw(sheet)
    for i in range(3):
        d.rounded_rectangle((22+i*395,110,392+i*395,775),radius=9,fill=PANEL)
    tech, ts=load('field-robotics-card')
    fit_sprite(sheet,tile(tech,ts),(62,175,350,490))
    tech.close()
    running, rs=load('warden-0-running')
    for i,frame in enumerate((4,12)):
        fit_sprite(sheet,tile(running,rs,4,frame),(430+i*165,184,580+i*165,493),trim=True)
    running.close()
    mining, ms=load('warden-0-mining_with_tool')
    for i,frame in enumerate((5,10)):
        fit_sprite(sheet,tile(mining,ms,2,frame),(825+i*165,172,975+i*165,505),trim=True)
    mining.close()
    columns=[
        ('01 / EARLY CONSTRUCTION',['AUTO-ENABLED with carried kit','Ctrl + Shift + B: pause / resume','Build, deconstruct and upgrade','16 directional 3D sprite views','No armor, power or logistics']),
        ('02 / REFINED EXPLORER',['Tapered, tear-shaped chest profile','Reduced projection and upper bulk','Rounded boot outline and toe cap','Coordinated hips, shoulders, head','Subtle protective-clothing motion']),
        ('03 / WEIGHTED TOOL WORK',['Right palm at 48% of the shaft','Both hands remain on the shaft','Measured wind-up and fast impact','Torso drive and planted stance','Unchanged mining productivity'])]
    for i,(title,lines) in enumerate(columns):
        x=42+i*395
        d.text((x,137),title,font=font(15,True),fill=ACCENT)
        for j,line in enumerate(lines):d.text((x,545+j*36),line,font=font(14),fill=CREAM)
    d.text((30,799),'Personal inventory / blueprint and planner tools / real material accounting / no logistics-network connection',font=font(15),fill=CREAM)
    d.text((30,838),'Exported sprites and poses, not graphical Factorio footage. See the field-crew contract and verification ledger.',font=font(12),fill=MUTED)
    sheet.save(ART/'field-crew-review.jpg',quality=94,optimize=True)


def nightglass_review(catalog):
    energy=catalog['energy'];stages=('early','mid','late')
    sheet=Image.new('RGB',(1500,1240),BACKGROUND);d=ImageDraw.Draw(sheet)
    header(sheet,'NIGHTGLASS FOUNDRY / SECOND NATURE '+json.loads((MOD/'info.json').read_text())['version'],
           'Sealed restoration warden, readable inventory icons, visible crew recall and six power systems per stage. Source-art review, not gameplay.')
    for i in range(3):d.rounded_rectangle((24+i*494,112,496+i*494,641),radius=8,fill=PANEL)
    d.text((44,132),'A HUMAN GOTH EXPLORER',font=font(18,True),fill=ACCENT)
    actor,spec=load('warden-0-idle');fit_sprite(sheet,tile(actor,spec,4,0),(65,166,460,567),trim=True);actor.close()
    d.text((44,587),'Softer face, skin and shoulder contours',font=font(15),fill=CREAM)
    d.text((44,612),'Original adult design / Morticia-inspired styling',font=font(13),fill=MUTED)
    d.text((538,132),'DISTINCT INVENTORY OBJECTS',font=font(18,True),fill=ACCENT)
    names=('silica','glass','biochar','activated-carbon','filter-cartridge','spent-filter','ceramic-membrane','biofilm',
           'field-pole','field-crate','field-armor','bastion-armor','vector-inserter','canopy-inserter','biogas','hydrogen')
    for i,name in enumerate(names):
        path=MOD/f'graphics/icons/{name}.png';INPUTS[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        im=Image.open(path);x=560+(i%4)*106;y=186+(i//4)*91;sheet.paste(im,(x,y),im);im.close()
    d.text((538,587),'Native 64 px art, reviewed again at 32 px',font=font(15),fill=CREAM)
    d.text((538,612),'Different shapes, contrast and purposeful color',font=font(13),fill=MUTED)
    d.text((1032,132),'CONTROL + RECALL',font=font(18,True),fill=ACCENT)
    path=MOD/'graphics/icons/field-controller.png';im=Image.open(path);sheet.paste(im,(1216,206),im);im.close()
    for j,line in enumerate(['Upper-left mod-button area','Visible only with a carried controller','Click or Ctrl + Shift + B','Pausing makes workers fly home','No instant remote refund/despawn']):
        d.text((1032,315+j*43),line,font=font(15),fill=CREAM)
    d.text((1032,587),'Iron sticks and power poles are starter crafts',font=font(14),fill=ACCENT)
    d.text((30,674),'18 POWER SYSTEMS / SIX DIFFERENT OPTIONS IN EACH STAGE',font=font(22,True),fill=CREAM)
    for col,stage in enumerate(stages):
        x=24+col*494;d.text((x+18,720),stage.upper(),font=font(17,True),fill=ACCENT)
        for row,p in enumerate(x for x in energy['plants'] if x['stage']==stage):
            y=758+row*72
            path=MOD/f'graphics/icons/{p["name"]}.png';INPUTS[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
            with Image.open(path) as im:sheet.paste(im,(x+7,y-6),im)
            label=p['title']
            for j,line in enumerate(textwrap.wrap(label,34)):d.text((x+83,y+2+j*20),line,font=font(14,True),fill=CREAM)
            rating=f"{p['watts']/1000000:g} MW" if p['watts']>=1000000 else f"{p['watts']/1000:g} kW"
            if p.get('heat'):rating+=' thermal'
            d.text((x+83,y+43),rating+' / '+p['mechanism'],font=font(11),fill=MUTED)
    d.text((30,1206),'Ratings are constrained by sunlight, wind, shoreline, regional heat, fuel or supplied thermal/plasma energy. No source creates free fuel.',font=font(13),fill=MUTED)
    sheet.save(ART/'nightglass-review.jpg',quality=93,optimize=True)

    frames=[];loaded=[(p,*load(p['name']+'-north')) for p in energy['plants']]
    for f in range(8):
        board=Image.new('RGB',(1800,1030),BACKGROUND)
        header(board,'POWER ARCHITECTURES / EARLY, MID, LATE','Six distinct systems per row. Source animation study; operational rates are checked by the engine harness.')
        draw=ImageDraw.Draw(board)
        for i,(p,image,spec) in enumerate(loaded):
            x=(i%6)*300;y=100+(i//6)*305
            fit_sprite(board,tile(image,spec,frame=f),(x+7,y+3,x+293,y+247))
            for j,line in enumerate(textwrap.wrap(p['title'],30)):draw.text((x+14,y+250+j*19),line,font=font(12,True),fill=CREAM)
        frames.append(board)
    save_gif(frames,'power-options-preview.gif',100)
    for _,image,_ in loaded:image.close()


def generate():
    global MANIFEST
    INPUTS.clear()
    MANIFEST = json.loads((ART / 'sprite-manifest.json').read_text())
    drone = json.loads((ART/'drone-manifest.json').read_text())
    for key,spec in drone['specs'].items():MANIFEST['field-drone-'+key]=spec
    for key,path,size in [('field-controller-icon','graphics/icons/field-controller.png',64),('field-robotics-card','graphics/technology/field-robotics.png',256)]:
        MANIFEST[key]={'filename':'__second-nature__/'+path,'width':size,'height':size,'frame_count':1,'line_length':1,'direction_count':1}
    energy_art=json.loads((ART/'energy-manifest.json').read_text())
    for key,spec in energy_art['specs'].items():MANIFEST[key]=dict(spec,frame_count=spec.get('frame_count',1))
    catalog = load_catalog()
    contact_sheet(catalog)
    character_reviews()
    industrial_review(catalog)
    ship_review()
    field_crew_review()
    nightglass_review(catalog)
    outputs = ('ironbound-contact-sheet.jpg', 'character-aim-layout.jpg', 'locomotion-review.gif',
               'mining-framing-preview.gif', 'industrial-animation-preview.gif', 'lander-review.jpg', 'lander-standby.gif', 'field-crew-review.jpg', 'field-drone-preview.gif','nightglass-review.jpg','power-options-preview.gif')
    report = {
        'description': 'Current source-art review ledger. These files are not game screenshots or gameplay certification.',
        'version': json.loads((MOD / 'info.json').read_text())['version'],
        'inputs': dict(sorted(INPUTS.items())),
        'outputs': {name: hashlib.sha256((ART / name).read_bytes()).hexdigest() for name in outputs},
        'canonical_machines': {m['name']: {'art_name': m['art_name'], 'footprint': m['footprint']} for m in catalog['machines']},
    }
    (ART / 'review-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Generated current contact, aim, locomotion, mining, process, ship and field-crew reviews.')


if __name__ == '__main__':
    generate()
