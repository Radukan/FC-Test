#!/usr/bin/env python3
"""Original wind-up field drone and controller art. No native robot sprites copied."""
import hashlib
import json
import math
from PIL import Image, ImageDraw
from catalog import ROOT, MOD
from sprite_bounds import assert_sprite_fits
from industrial_art import Mesh, render, fan, hose, STEEL, DARK, EDGE, GOLD, COPPER, TEAL, TAU


def drone(t=0, working=False):
    m=Mesh();z=.70+.018*math.sin(t*TAU)
    m.cyl(0,0,z,.23,.18,STEEL,28)
    m.ball((0,-.025,z+.13),.215,STEEL,stretch=(1,.88,.71))
    m.box((0,-.168,z+.17),(.23,.10,.11),DARK,.04)
    m.box((0,-.224,z+.18),(.165,.025,.073),(75,145,149),.02)
    for side in (-1,1):
        m.box((side*.20,.015,z+.08),(.08,.22,.085),GOLD,.024)
        m.tube((side*.14,.12,z+.03),(side*.19,.21,z-.04),.026,COPPER,10)
        m.ball((side*.19,.21,z-.04),.035,EDGE)
    z+=.055
    m.cyl(0,0,z+.18,.19,.035,GOLD,28)
    m.ring((0,0,z+.22),.12,.020,COPPER)
    for i in range(5):
        a=t*TAU+i*TAU/5
        m.tube((0,0,z+.235),(.11*math.cos(a),.11*math.sin(a),z+.235),.012,EDGE,6)
    for side in (-1,1):
        x=side*.45
        m.tube((side*.15,0,z+.08),(x,0,z+.16),.047,EDGE,12)
        hose(m,[(side*.17,.08,z+.12),(x,.10,z+.15),(x,.05,z+.26)],.020,COPPER)
        fan(m,x,0,z+.10,.245,side*t)
        m.ring((x,0,z+.29),.25,.018,STEEL)
        m.tube((side*.13,-.09,z),(side*.16,-.15,.35),.029,DARK,10)
        claw=side*(.13 if not working else .10+.025*math.sin(t*TAU))
        m.tube((side*.16,-.15,.35),(claw,-.19,.22),.028,EDGE,10)
        m.tube((claw,-.19,.22),(claw*.55,-.19,.21),.024,COPPER,10)
    m.box((0,.02,z-.10),(.27,.21,.16),DARK,.05)
    m.box((0,-.18,z+.065),(.15,.055,.09),DARK,.02)
    m.ball((0,-.218,z+.07),.038,TEAL,stretch=(1,.45,.65),glow=True)
    if working:
        m.ball((0,-.20,.21),.026+.009*math.sin(t*TAU),(221,183,100),glow=True)
    return m


def controller():
    m=Mesh();m.box((0,0,.17),(.74,.56,.33),STEEL,.13)
    m.box((0,-.03,.35),(.52,.39,.05),DARK,.07)
    m.box((-.05,-.06,.385),(.29,.20,.03),TEAL,.04)
    m.cyl(.39,0,.12,.065,.30,EDGE,12)
    m.tube((.39,0,.43),(.39,.25,.43),.035,COPPER,12)
    m.cyl(.39,.25,.43,.045,.11,DARK,12)
    for i in range(3):m.cyl(.18,-.13+i*.10,.38,.025,.025,GOLD,10)
    return m


def icon(image, path):
    im=image.crop(image.getbbox());im.thumbnail((58,58),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(64,64));canvas.alpha_composite(im,((64-im.width)//2,(64-im.height)//2))
    canvas.save(path,optimize=True)


def generate():
    out=MOD/'graphics/entity/field-drones';out.mkdir(parents=True,exist_ok=True)
    specs={};previews=[];directions=16
    view={'width':176,'height':192,'ppu':56,'origin':.52,'scale':32/56}
    for name,working in [('flying',False),('working',True)]:
        atlas=Image.new('RGBA',(176*8,192*directions));shadows=Image.new('RGBA',atlas.size)
        for direction in range(directions):
            for i in range(8):
                model=drone(i/8,working);angle=direction*TAU/directions
                assert_sprite_fits(model,view,angle,(name,direction,i))
                im=render(model,176,192,ppu=56,origin=.52,angle=angle,map_aligned=True)
                alpha=im.getchannel('A')
                body_mask=alpha.point(lambda a:255 if a==255 else 0)
                shadow_mask=alpha.point(lambda a:255 if 0<a<255 else 0)
                body=Image.composite(im,Image.new('RGBA',im.size),body_mask)
                shadow=Image.composite(im,Image.new('RGBA',im.size),shadow_mask)
                combined=shadow.copy();combined.alpha_composite(body)
                assert combined.tobytes()==im.tobytes()
                atlas.alpha_composite(body,(i*176,direction*192));shadows.alpha_composite(shadow,(i*176,direction*192))
                if i==0 and direction==2:previews.append(im)
        atlas.save(out/f'{name}.png',optimize=True)
        shadows.save(out/f'{name}-shadow.png',optimize=True)
        specs[name]={'filename':f'__second-nature__/graphics/entity/field-drones/{name}.png',
                     'width':176,'height':192,'frame_count':8,'line_length':8,'direction_count':directions,
                     'scale':32/56,'shift':[0,round((.5-.52)*192/56,7)],'apply_projection':False}
        specs[name+'-shadow']=dict(specs[name],filename=f'__second-nature__/graphics/entity/field-drones/{name}-shadow.png')
    icon(previews[0],MOD/'graphics/icons/field-drone.png')
    icon(render(controller(),128,128,origin=.6),MOD/'graphics/icons/field-controller.png')
    card=Image.new('RGBA',(256,256));d=ImageDraw.Draw(card)
    points=[(128+119*math.cos(i*TAU/6-math.pi/2),128+119*math.sin(i*TAU/6-math.pi/2)) for i in range(6)]
    d.polygon(points,fill=(28,38,43,250),outline=(208,145,63,255),width=4)
    hero=render(drone(.125,True),384,320,ppu=140,origin=.5,map_aligned=True)
    hero=hero.crop(hero.getbbox());hero.thumbnail((188,176),Image.Resampling.LANCZOS)
    card.alpha_composite(hero,((256-hero.width)//2,34+(176-hero.height)//2))
    for i in range(3):d.ellipse((98+i*24,216,110+i*24,224),fill=(70,185,172,255))
    card.save(MOD/'graphics/technology/field-robotics.png',optimize=True)
    for name,accent in [('field-robotics-2',(113,190,174,255)),('field-robotics-3',(211,197,125,255))]:
        tier=card.copy();d=ImageDraw.Draw(tier);d.ellipse((184,168,230,214),fill=accent,outline=(28,38,43,255),width=3)
        d.text((201,183),name[-1],fill=(20,30,28,255))
        tier.save(MOD/f'graphics/technology/{name}.png',optimize=True)
    def lua(v):
        if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
        if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
        return json.dumps(v)
    (MOD/'shared/drone_art.lua').write_text('-- Generated by tools/generate_drone_assets.py. Original authored geometry.\nreturn '+lua(specs)+'\n')
    report={'specs':specs,'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted(out.glob('*.png'))+[MOD/'graphics/icons/field-drone.png',MOD/'graphics/icons/field-controller.png',MOD/'graphics/technology/field-robotics.png',MOD/'graphics/technology/field-robotics-2.png',MOD/'graphics/technology/field-robotics-3.png']}}
    (ROOT/'docs/art/drone-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print('FIELD_DRONE_ART_COMPLETE')


if __name__=='__main__':generate()
