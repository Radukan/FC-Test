#!/usr/bin/env python3
"""Render original industrial sprites/animations. Requires requirements-art.txt.
Everything is procedural authored geometry; no Wube sprite/model is copied.
"""
from pathlib import Path
import json, math, argparse
from PIL import Image, ImageDraw, ImageFont
from catalog import MOD, ROOT, load_catalog
from industrial_art import *
import character_layout as character
import gait

OUT=MOD/'graphics/entity/industry'
DIRECTIONS=('north','east','south','west')
manifest_path=ROOT/"docs/art/sprite-manifest.json"
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

def save(image,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.stem+".tmp.png");image.save(temporary,optimize=True);temporary.replace(path)

def icon(image,name):
    bbox=image.getchannel('A').point(lambda a:255 if a>140 else 0).getbbox()
    if not bbox:return
    im=image.crop(bbox);im.thumbnail((58,58),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(64,64));canvas.alpha_composite(im,((64-im.width)//2,(64-im.height)//2))
    save(canvas,MOD/'graphics/icons'/f'{name}.png')

def spec(name,width,height=None,frames=8,directions=1,origin=.7,scale=.5):
    height=height or width
    return {'filename':f'__second-nature__/graphics/entity/industry/{name}.png','width':width,'height':height,
            'frame_count':frames,'line_length':frames,'direction_count':directions,'scale':scale,
            'shift':[0,round((.5-origin)*height*scale/32,6)]}

def animate(name,maker,width=320,height=None,frames=8,directions=1,origin=.7,ppu=64,angles=None,map_aligned=False):
    height=height or width
    columns=8 if frames==1 and directions>8 else (16 if directions>=32 else (10 if frames==20 and width*frames>8192 else frames))
    atlas=Image.new('RGBA',(width*columns,height*math.ceil(frames*directions/columns)))
    preview=None
    for direction in range(directions):
        angle=angles[direction] if angles is not None else direction*TAU/directions
        for frame in range(frames):
            image=render(maker(frame/frames,direction),width,height,angle=angle,origin=origin,ppu=ppu,map_aligned=map_aligned)
            index=direction*frames+frame
            atlas.alpha_composite(image,((index%columns)*width,(index//columns)*height))
            if preview is None:preview=image
    save(atlas,OUT/f'{name}.png')
    manifest[name]=spec(name,width,height,frames,directions,origin)
    manifest[name]['line_length']=columns
    if map_aligned:manifest[name]['apply_projection']=False
    return preview

def corpse(tier):
    m=explorer(0,'idle',tier,move_angle=math.pi/2)
    result=Mesh()
    # Lie on the ground, preserving armor appearance and actual corpse inventory.
    for vertices,c,g in m.faces:
        result.face([(x,(z-1.0)*.9,y+.28) for x,y,z in vertices],c,g)
    return result

def render_all(only=None):
    OUT.mkdir(parents=True,exist_ok=True)
    catalog=load_catalog();previews=[]
    for entry in catalog['machines']:
        name=entry['name']
        if only and name not in only:continue
        size={1:160,3:320,5:448,7:640}[entry['footprint']]
        art_name=entry['art_name']
        origin=.57 if entry['footprint']==7 else .6
        for index,direction in enumerate(DIRECTIONS):
            preview=animate(art_name+'-'+direction,lambda t,_:machine(name,t),size,frames=8,angles=[index*math.pi/2],origin=origin,map_aligned=True)
            if index==0:previews.append((entry['title'],preview));icon(preview,name)
        print('BUILDING',name,flush=True)
    if not only or 'lander' in only:
        preview=animate('lander',lambda t,_:lander(t),768,640,frames=8,angles=[math.pi])
        previews.append(('Intact expedition lander',preview));icon(preview,'lander')
        # Container picture is a single frame; runtime overlay supplies the animated lamps/rotors.
        save(preview,OUT/'lander-still.png');manifest['lander-still']=spec('lander-still',768,640,1)
        print('LANDER',flush=True)
    for name in ('sentry-turret','arc-turret','lance-turret'):
        if only and name not in only:continue
        size=320 if name=='lance-turret' else 192
        preview=animate(name+'-idle',lambda t,d:turret(name,0,angle=d*TAU/64),size,frames=1,directions=64,angles=[0]*64)
        animate(name+'-fire',lambda t,d:turret(name,t,angle=d*TAU/64),size,frames=4,directions=64,angles=[0]*64)
        icon(preview,name);previews.append((name.replace('-',' ').title(),preview));print('DEFENSE',name,flush=True)
    for advanced in (False,True):
        name='composite-wall' if advanced else 'field-barricade'
        if only and name not in only:continue
        for key,mask in {'single':0,'straight_vertical':5,'straight_horizontal':10,'corner_right_down':6,
                         'corner_left_down':12,'t_up':14,'ending_right':2,'ending_left':8,
                         'filling':15,'water_connection_patch':4,'gate_connection_patch':4}.items():
            preview=animate(name+'-'+key,lambda t,d:wall(mask,advanced),128,frames=1,origin=.76)
            if key=='single':icon(preview,name);previews.append((name.replace('-',' ').title(),preview))
        print('WALL',name,flush=True)
    for name in ('field-pole','field-crate'):
        if only and name not in only:continue
        for index,direction in enumerate(DIRECTIONS):
            preview=animate(name+'-'+direction,lambda t,d:equipment(name),128,256 if name=='field-pole' else 128,
                            frames=1,angles=[index*math.pi/2],origin=.82 if name=='field-pole' else .7)
            if index==0:icon(preview,name);previews.append((name.replace('-',' ').title(),preview))
    if not only or 'field-pole' in only:
        sheet=Image.new('RGBA',(512,256))
        for i,d in enumerate(DIRECTIONS):sheet.alpha_composite(Image.open(OUT/f'field-pole-{d}.png'),(i*128,0))
        save(sheet,OUT/'field-pole-sheet.png')
        manifest['field-pole-sheet']=dict(manifest['field-pole-north'],filename='__second-nature__/graphics/entity/industry/field-pole-sheet.png',direction_count=4,line_length=4)
    for name,size,frames in [('vector-inserter',128,1),('canopy-inserter',128,1),('vital-splitter',192,8),('jukebox',192,8)]:
        if only and name not in only:continue
        for i,direction in enumerate(DIRECTIONS):
            preview=animate(name+'-'+direction,lambda t,_:logistics(name,t),size,frames=frames,angles=[i*math.pi/2],origin=.60,map_aligned=True)
            if i==0:icon(preview,name);previews.append((name.replace('-',' ').title(),preview))
        print('LOGISTICS',name,flush=True)
    if not only:
        for name in ('vital-belt','vital-underground-belt'):
            icon(render(logistics(name),160,128,origin=.6,map_aligned=True),name)
        model=Mesh();model.cyl(0,0,0,.24,.62,STEEL)
        for i in range(4):model.ball((-.14+i*.09,0,.60),.075,GREEN,stretch=(.7,.7,2.1))
        icon(render(model,128,128,origin=.64), 'mycelial-magazine')
        sticker=Image.new('RGBA',(96*4,96))
        for frame in range(4):
            draw=ImageDraw.Draw(sticker);x=frame*96
            for i in range(5):
                a=i*TAU/5+frame*.06
                points=[(x+48+math.cos(a+j*.24)*r,48+math.sin(a+j*.24)*r*.62) for j,r in enumerate((4,13,22,29,35))]
                draw.line(points,fill=(98,176,98,180),width=3)
        save(sticker,OUT/'root-binding.png')
    if not only or 'explorer' in only:
        for tier in range(3):
            for pose,frames,count in [('idle',4,8),('idle_with_gun',4,8),('running',gait.RUN_FRAMES,8),('mining_with_tool',gait.MINING_FRAMES,8),('running_with_gun',gait.RUN_FRAMES,18)]:
                def actor(t,d):
                    move,aim=character.pose_angles(pose,d)
                    model=explorer(t,pose,tier,move_angle=move,aim_angle=aim)
                    character.assert_frame_fits(model,(tier,pose,d,t))
                    return model
                view=character.frame_spec(pose)
                preview=animate(f'explorer-{tier}-{pose}',actor,view['width'],view['height'],frames=frames,directions=count,
                    angles=[0]*count,origin=view['origin'],ppu=view['ppu'],map_aligned=True)
                if pose=='idle':icon(preview,'explorer' if tier==0 else f'explorer-{tier}');previews.append((f'Explorer / armor {tier}',preview))
            preview=animate(f'explorer-{tier}-corpse',lambda t,d:corpse(tier),256,192,frames=2,origin=.5,ppu=70)
            print('EXPLORER',tier,flush=True)
        # Small animated status beacon for the constant combinator, not an invented craft.
    if not only:
        overlay=Image.new('RGBA',(32*8,32))
        for frame in range(8):
            d=ImageDraw.Draw(overlay);light=int(100+120*(.5+.5*math.sin(frame*TAU/8)))
            d.ellipse((frame*32+10,10,frame*32+22,22),fill=(42,light,190,220))
        save(overlay,OUT/'status-light.png');manifest['status-light']=spec('status-light',32,frames=8,origin=.5)
        # Weapon/armor icons use original procedural geometry, never cloned stock icons.
        for name,tier in [('carbine',0),('induction-rifle',1),('lance-rifle',2),('field-armor',0),('expedition-armor',1),('bastion-armor',2)]:
            if 'armor' in name:im=render(explorer(0,'idle',tier,move_angle=math.pi),character.WIDTH,character.HEIGHT,ppu=character.PIXELS_PER_UNIT,origin=character.ORIGIN,map_aligned=True)
            else:
                model=Mesh();model.box((0,0,.2),(.28,1.25,.25),STEEL)
                model.box((0,.6,.2),(.38,.55,.31),GOLD if tier==0 else (TEAL if tier==1 else WHITE))
                model.tube((0,-.4,.23),(0,-1.5-tier*.25,.23),.055+ tier*.016,DARK)
                for i in range(4):model.box((0,-.1-i*.24,.25),(.38,.09,.27),EDGE)
                model.box((0,.15,.02),(.2,.3,.33),COPPER)
                im=render(model,192,144,ppu=64,origin=.55,angle=-math.pi/4)
            icon(im,name)
        for name,c in [('alloy-stock',GOLD),('ballistic-magazine',COPPER),('induction-cell',TEAL),('lance-cell',BLUE),('ecoshield-equipment',GREEN)]:
            model=equipment('cell');model.box((0,0,.45),(.65,.34,.18),c)
            icon(render(model,128,128,origin=.65),name)
    # Machine specs can be imported without loading the renderer at runtime.
    if True:
        def lua(v):
            if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
            if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
            return json.dumps(v)
        (MOD/'shared/art.lua').write_text('-- Generated by tools/generate_industrial_assets.py. Original authored geometry.\nreturn '+lua(manifest)+'\n')
        (ROOT/'docs/art').mkdir(parents=True,exist_ok=True)
        (ROOT/'docs/art/sprite-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        cols=5;cellw,cellh=236,248;rows=math.ceil(len(previews)/cols)
        sheet=Image.new('RGB',(cols*cellw,rows*cellh),(22,29,32));draw=ImageDraw.Draw(sheet)
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
        for i,(label,image) in enumerate(previews):
            x=i%cols*cellw;y=i//cols*cellh
            thumb=image.copy();thumb.thumbnail((220,210),Image.Resampling.LANCZOS)
            sheet.paste(thumb,(x+(cellw-thumb.width)//2,y+8+(205-thumb.height)//2),thumb)
            draw.text((x+12,y+221),label,fill=(219,226,220),font=font)
        if not only:sheet.save(ROOT/'docs/art/ironbound-contact-sheet.jpg',quality=91,optimize=True)
    print('SPRITE_EXPORT_COMPLETE',len(manifest),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='*');args=parser.parse_args()
    render_all(set(args.only) if args.only else None)
