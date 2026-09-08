#!/usr/bin/env python3
"""Author the Nightglass power plant / solar rolling-stock sprites and research cards."""
import hashlib,json,math
from PIL import Image,ImageDraw
from lupa.lua52 import LuaRuntime
from catalog import ROOT,MOD,plain,load_catalog
from industrial_art import render
from energy_models import plant,locomotive
from sprite_bounds import assert_sprite_fits


def catalog():
    return load_catalog()['energy']


def save(image,path):
    path.parent.mkdir(parents=True,exist_ok=True);image.save(path,optimize=True)


def icon(image,path):
    box=image.getchannel('A').point(lambda a:255 if a>150 else 0).getbbox()
    image=image.crop(box);image.thumbnail((58,58),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(64,64));out.alpha_composite(image,((64-image.width)//2,(64-image.height)//2));save(out,path)


def cropped_sheet(images,key,columns,scale,origin,ppu,split=False):
    box=[images[0].width,images[0].height,0,0]
    for im in images:
        b=im.getbbox();box=[min(box[0],b[0]),min(box[1],b[1]),max(box[2],b[2]),max(box[3],b[3])]
    crop=[max(0,box[0]-12),max(0,box[1]-12),min(images[0].width,box[2]+12),min(images[0].height,box[3]+12)]
    w,h=crop[2]-crop[0],crop[3]-crop[1]
    sheet=Image.new('RGBA',(w*columns,h*math.ceil(len(images)/columns)))
    for i,im in enumerate(images):sheet.paste(im.crop(crop),((i%columns)*w,(i//columns)*h))
    assert max(sheet.size)<=8192,(key,sheet.size)
    path=MOD/f'graphics/entity/nightglass/{key}.png';save(sheet,path)
    spec={'filename':f'__second-nature__/graphics/entity/nightglass/{key}.png','width':w,'height':h,
          'scale':scale,'shift':[round((crop[0]+w/2-images[0].width/2)*scale/32,7),round((crop[1]+h/2-images[0].height*origin)*scale/32,7)],
          'line_length':columns,'apply_projection':False}
    return spec


def generate():
    data=catalog();specs={};previews={}
    for p in data['plants']:
        for q,direction in enumerate(('north','east','south','west')):
            images=[]
            for f in range(8):
                model=plant(p['name'],f/8)
                assert_sprite_fits(model,{'width':1024,'height':1024,'ppu':64,'origin':.5},q*math.pi/2,(p['name'],q,f))
                images.append(render(model,1024,1024,ppu=64,origin=.5,angle=q*math.pi/2,map_aligned=True))
            key=p['name']+'-'+direction
            specs[key]=cropped_sheet(images,key,8,.5,.5,64)
            specs[key].update(frame_count=8,direction_count=1)
            if q==0:
                previews[p['name']]=images[0]
                icon(images[0],MOD/f'graphics/icons/{p["name"]}.png')
        print('POWER ART',p['name'],flush=True)
    for t in data['trains']:
        bodies=[];shadows=[];model=locomotive(t['tier'])
        for d in range(64):
            angle=d*math.tau/64
            assert_sprite_fits(model,{'width':384,'height':384,'ppu':48,'origin':.5},angle,(t['name'],d))
            image=render(model,384,384,ppu=48,origin=.5,angle=angle,map_aligned=True)
            a=image.getchannel('A')
            bodies.append(Image.composite(image,Image.new('RGBA',image.size),a.point(lambda v:255 if v==255 else 0)))
            shadows.append(Image.composite(image,Image.new('RGBA',image.size),a.point(lambda v:255 if 0<v<255 else 0)))
            if d==16:previews[t['name']]=image
        for suffix,images in (('',bodies),('-shadow',shadows)):
            key=t['name']+suffix
            specs[key]=cropped_sheet(images,key,8,32/48,.5,48)
            specs[key].update(direction_count=64,usage='train')
            if suffix:specs[key]['draw_as_shadow']=True
        icon(previews[t['name']],MOD/f'graphics/icons/{t["name"]}.png')
        print('SOLAR RAIL ART',t['name'],flush=True)
    # Fuel and fitted grid-component icons are original model details, not copied stock art.
    from industrial_art import Mesh,STEEL,DARK,COPPER,GOLD
    for key,color in [('producer-gas',(159,109,55)),('biogas',(76,153,90)),('synthetic-gas',(66,124,165)),('biopellet',(85,121,64)),('bio-ash',(137,130,112)),('solar-rail-panels',(45,82,120)),('solar-rail-battery',(123,133,147)),('solar-drive-charge',(66,135,158))]:
        m=Mesh();m.box((0,0,.25),(.7,.48,.45),color,.1)
        for x in (-.23,0,.23):m.box((x,0,.49),(.05,.42,.035),GOLD,.01)
        image=render(m,128,128,origin=.6);icon(image,MOD/f'graphics/icons/{key}.png')
    mapping={'practical-power':'burner-set','wind-power':'wind-turbine','biomass-power':'biopellet-engine','geothermal-power':'geothermal-bore','industrial-cogeneration':'cogenerator',
             'river-power':'river-turbine','compact-steam':'steam-piston','producer-gas-power':'producer-gas-engine',
             'solar-concentration':'solar-tower','biogas-power':'biogas-turbine','heat-recovery-power':'heat-recovery-turbine',
             'photonic-power':'photonic-canopy','planetary-thermal-power':'planetary-thermal-tap','combined-cycle-power':'combined-cycle',
             'biofuel-cell-power':'biofuel-cell','modular-fission-power':'salt-reactor','plasma-conversion-power':'plasma-generator',
             'solar-railway':'sunseed-locomotive','solar-railway-2':'heliograph-locomotive','solar-railway-3':'daybreak-locomotive'}
    for name,key in mapping.items():
        card=Image.new('RGBA',(256,256));d=ImageDraw.Draw(card)
        points=[(128+120*math.cos(i*math.tau/6-math.pi/2),128+120*math.sin(i*math.tau/6-math.pi/2)) for i in range(6)]
        d.polygon(points,fill=(26,35,38,255),outline=(157,169,122,255),width=4)
        im=previews[key].crop(previews[key].getbbox());im.thumbnail((186,174),Image.Resampling.LANCZOS)
        card.alpha_composite(im,((256-im.width)//2,36+(174-im.height)//2));save(card,MOD/f'graphics/technology/{name}.png')
    def lua(v):
        if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
        if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
        return json.dumps(v)
    (MOD/'shared/energy_art.lua').write_text('-- Generated by tools/generate_energy_assets.py. Original authored models.\nreturn '+lua(specs)+'\n')
    files=list((MOD/'graphics/entity/nightglass').glob('*.png'))
    report={'specs':specs,'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (ROOT/'docs/art/energy-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print('NIGHTGLASS_ASSETS_COMPLETE',flush=True)


if __name__=='__main__':generate()
