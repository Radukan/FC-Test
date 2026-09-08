#!/usr/bin/env python3
"""Research cards and medical icon drawn from the new original industrial art."""
from pathlib import Path
import math,json
from PIL import Image, ImageDraw
from catalog import MOD,load_catalog
from industrial_art import Mesh,render,STEEL,EDGE,WHITE,RED

def generate():
    model=Mesh();model.box((0,0,.26),(.9,.66,.5),WHITE)
    model.box((0,0,.52),(.6,.13,.03),RED);model.box((0,0,.52),(.13,.5,.03),RED)
    image=render(model,128,128,origin=.6);bbox=image.getbbox();im=image.crop(bbox);im.thumbnail((58,58),Image.Resampling.LANCZOS)
    output=Image.new('RGBA',(64,64));output.alpha_composite(im,((64-im.width)//2,(64-im.height)//2));output.save(MOD/'graphics/icons/field-dressing.png')
    mapping={'biofoundations':'algae-vat','composting':'composter','environmental-monitoring':'ecology-monitor','atmospheric-engineering':'air-scrubber',
      'water-cycle':'watershed','reforestation':'seed-disperser','dirty-shortcuts':'pyrolyzer','thermal-engineering':'thermal-exchanger',
      'closed-loops':'reclamation-plant','clean-chemistry':'electrolyzer','planetary-ecology':'ecology-monitor',
      'vulcanus-restoration':'basalt-conditioner','fulgora-remediation':'fulgoran-reclaimer','gleba-symbiosis':'spore-tower',
      'habitat-engineering':'sanctuary','climate-science':'thermal-exchanger','aquilo-habitats':'cryogenic-garden',
      'planetary-coordination':'planetary-beacon','living-worlds':'planetary-beacon','ecological-research':'sanctuary',
      'expedition-defense':'sentry-turret','induction-defense':'arc-turret','bastion-defense':'lance-turret'}
    manifest=json.loads((MOD.parent/'docs/art/sprite-manifest.json').read_text())
    catalog=load_catalog();art_names={m['name']:m['art_name'] for m in catalog['machines']}
    for t in catalog['technologies']:
        if t['name'].startswith('field-robotics') or t['name'] in {x['name'] for x in catalog.get('energy',{}).get('technologies',[])}:continue  # Owned by generate_drone_assets.py.
        card=Image.new('RGBA',(256,256));d=ImageDraw.Draw(card)
        points=[(128+119*math.cos(i*math.tau/6-math.pi/2),128+119*math.sin(i*math.tau/6-math.pi/2)) for i in range(6)]
        d.polygon(points,fill=(28,38,43,250),outline=(208,145,63,255),width=4)
        for y in range(32,220,16):d.line((38,y,216,y),fill=(42,54,59,200),width=1)
        name=mapping.get(t['name'],'ecology-monitor');name=art_names.get(name,name)
        image=Image.open(MOD/f'graphics/entity/industry/{name}-north.png') if (MOD/f'graphics/entity/industry/{name}-north.png').exists() else Image.open(MOD/f'graphics/icons/{name}.png')
        spec=manifest.get(name+'-north')
        if spec:image=image.crop((0,0,spec['width'],spec['height']))
        image=image.crop(image.getbbox());image.thumbnail((182,172),Image.Resampling.LANCZOS)
        card.alpha_composite(image,((256-image.width)//2,36+(170-image.height)//2))
        for i in range(3):d.ellipse((98+i*24,216,110+i*24,224),fill=(70,185,172,255))
        card.save(MOD/f'graphics/technology/{t["name"]}.png',optimize=True)
    print('Generated industrial research cards and field dressing icon.')
if __name__=='__main__':generate()
