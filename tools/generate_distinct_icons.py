#!/usr/bin/env python3
"""Native 64px inventory icons with distinct objects, clear silhouettes and contrast.

This final pass owns item/building icons; run it AFTER world-sprite exporters.
No generic family icon is silently reused for a different catalog item.
"""
import hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter,ImageFont
from catalog import ROOT,MOD,load_catalog
from industrial_art import Mesh,render,rot,STEEL,WHITE,machine,turret,wall,equipment,logistics,lander
from icon_models import item,fluid,gear

ACCENTS={
 'algae-vat':(96,162,120),'composter':(173,141,82),'hydroponics-bay':(114,158,81),
 'electrolyzer':(107,151,182),'reclamation-plant':(144,167,151),'materials-kiln':(188,134,76),
 'pyrolyzer':(169,103,65),'air-scrubber':(99,166,169),'soil-enricher':(143,119,84),
 'seed-disperser':(187,174,94),'watershed':(106,164,187),'thermal-exchanger':(176,137,102),
 'detoxifier':(155,124,169),'pheromone-dampener':(151,129,184),'forcing-tower':(173,107,74),
 'basalt-conditioner':(166,135,106),'fulgoran-reclaimer':(173,119,115),'spore-tower':(126,174,124),
 'cryogenic-garden':(159,188,195),'sanctuary':(148,173,113),'planetary-beacon':(178,194,188),
 'ecology-monitor':(117,154,171)}


def upper_model(model,accent=None):
    out=Mesh()
    for vertices,c,glow in model.faces:
        if max(p[2] for p in vertices)<.61:continue
        if accent and c in (STEEL,WHITE):c=tuple(round(.40*a+.60*b) for a,b in zip(c,accent))
        out.face(vertices,c,glow)
    return out if out.faces else model


def render_icon(model,angle=math.pi*.78):
    # Frame the model itself, not its large world cast-shadow/plinth rectangle.
    rotated=Mesh();rotated.join(model,angle)
    points=[p for v,_,_ in rotated.faces for p in v]
    xs=[p[0] for p in points]
    ys=[math.sin(math.radians(48))*p[1]-math.cos(math.radians(48))*p[2] for p in points]
    ppu=min(210/max(.01,max(xs)-min(xs)),210/max(.01,max(ys)-min(ys)))
    centered=Mesh();centered.join(rotated,offset=(-(min(xs)+max(xs))/2,0,0))
    origin=.5-(min(ys)+max(ys))/2*ppu/256
    image=render(centered,256,256,ppu=ppu,origin=origin)
    alpha=image.getchannel('A').point(lambda a:255 if a==255 else 0)
    rgb=image.convert('RGB');rgb=ImageEnhance.Color(rgb).enhance(.9)
    rgb=ImageEnhance.Contrast(rgb).enhance(1.17);rgb=ImageEnhance.Brightness(rgb).enhance(1.20)
    image=rgb.convert('RGBA');image.putalpha(alpha)
    image=image.crop(alpha.getbbox());image.thumbnail((57,57),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(64,64));x=(64-image.width)//2;y=(64-image.height)//2
    shadow=Image.new('RGBA',(64,64));shadow.paste((0,0,0,95),(x+1,y+2,x+image.width+1,y+image.height+2),image.getchannel('A'))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(.7)));canvas.alpha_composite(image,(x,y))
    return canvas


def generate():
    k=load_catalog();models={};roles={}
    for x in k['items']:
        models[x['name']]=item(x['name']);roles[x['name']]='material / '+x.get('family','item')
    for x in k['fluids']:
        models[x['name']]=fluid(x['name']);roles[x['name']]='fluid'
    for x in k['machines']:
        models[x['name']]=upper_model(machine(x['name'],.125),ACCENTS[x['name']]);roles[x['name']]='process building'
    from energy_models import plant,locomotive
    for x in k['energy']['plants']:
        models[x['name']]=plant(x['name'],.125) if x['name']=='photonic-canopy' else upper_model(plant(x['name'],.125));roles[x['name']]=x['stage']+' power / '+x['mechanism']
    for x in k['energy']['trains']:
        models[x['name']]=locomotive(x['tier']);roles[x['name']]='solar rolling stock'
    for x in k['expedition']:
        name=x['name']
        if name in models:continue
        if x['kind'] in ('gun','ammo','armor','capsule','energy-shield-equipment','inserter','transport-belt','underground-belt','splitter'):
            models[name]=gear(name)
        elif x['kind'] in ('ammo-turret','electric-turret'):models[name]=upper_model(turret(name,0))
        elif x['kind']=='wall':models[name]=wall(0,name=='composite-wall')
        elif name=='field-drone':
            from generate_drone_assets import drone
            models[name]=drone(.125)
        elif name=='field-controller':
            from generate_drone_assets import controller
            models[name]=controller()
        elif name=='jukebox':models[name]=logistics('jukebox',.125)
        else:models[name]=item(name)
        roles[name]=x['kind']
    models['field-pole']=equipment('field-pole');roles['field-pole']='wood-free power pole'
    models['field-crate']=equipment('field-crate');roles['field-crate']='mineral crate'
    models['lander']=lander(0);roles['lander']='expedition craft'
    # Hidden rail components also remain readable in their locked equipment grid.
    for name,base in [('solar-drive-charge','induction-cell'),('solar-rail-battery','induction-cell'),('solar-rail-panels','glass')]:
        models[name]=gear(base) if base=='induction-cell' else Mesh();roles[name]='internal rail component'
        if name=='solar-rail-panels':
            from energy_models import solar
            solar(models[name],0,0,.18,.72,.60,.12)
    outputs={}
    for name,model in models.items():
        angle=-math.pi/5 if roles[name]=="process building" or " power / " in roles[name] else math.pi*.78
        icon=render_icon(model,angle)
        if name.startswith('solar-rail-') or name=='solar-drive-charge':
            # Different internal schematic markers; not just three identical cells.
            d=ImageDraw.Draw(icon)
            if name=='solar-drive-charge':d.polygon([(24,18),(38,18),(31,30),(41,30),(24,49),(29,34),(20,34)],fill=(229,187,92,255))
            elif name=='solar-rail-battery':d.rectangle((26,24,36,40),fill=(166,193,167,255))
        path=MOD/f'graphics/icons/{name}.png';icon.save(path,optimize=True)
        outputs[name]={'role':roles[name],'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    # Close-ups at both inventory resolutions make confusing pairs visible.
    names=sorted(outputs);cw,ch,cols=210,136,6
    sheet=Image.new('RGB',(cw*cols,80+ch*math.ceil(len(names)/cols)),(32,38,35));d=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
    d.text((20,20),'DISTINCT INVENTORY ART / 64 px and 32 px / original geometry',font=font,fill=(224,228,210))
    for i,name in enumerate(names):
        x=i%cols*cw;y=70+i//cols*ch
        with Image.open(MOD/f'graphics/icons/{name}.png') as im:
            sheet.paste(im,(x+24,y+8),im)
            small=im.resize((32,32),Image.Resampling.LANCZOS);sheet.paste(small,(x+106,y+25),small)
        for j,line in enumerate(__import__('textwrap').wrap(name,27)):d.text((x+10,y+84+j*15),line,font=font,fill=(209,218,200))
    sheet.save(ROOT/'docs/art/icon-review.jpg',quality=92,optimize=True)
    (ROOT/'docs/art/icon-manifest.json').write_text(json.dumps(outputs,indent=2)+'\n')
    print('DISTINCT_ICON_EXPORT',len(outputs),flush=True)


if __name__=='__main__':generate()
