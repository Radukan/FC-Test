"""Render true 2x-detail explorer frames, trim common padding and tile safe pages.

Each pose has a fixed crop and compensated native pivot. Stripes keep every
input texture below 8192 pixels without downscaling or losing native directions.
"""
import hashlib
import json
import math
import re
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
from catalog import ROOT,MOD
from character_layout import frame_spec,pose_angles,assert_frame_fits
from industrial_art import render
from explorer_model import explorer

CACHE=ROOT/'.cache/character-hd'


def frame(task):
    tier,pose,direction,index,count=task
    move,aim=pose_angles(pose,direction);m=explorer(index/count,pose,tier,move,aim)
    assert_frame_fits(m,(tier,pose,direction,index))
    view=frame_spec(pose)
    im=render(m,view['width'],view['height'],ppu=view['ppu'],origin=view['origin'],map_aligned=True)
    # Suppress sub-visible RGB noise, not geometry or alpha. One intensity bit
    # avoids oversized high-entropy atlases at the new 160-texel model density.
    r,g,b,a=im.split();lut=[v&254 for v in range(256)]
    im=Image.merge('RGBA',(r.point(lut),g.point(lut),b.point(lut),a))
    path=CACHE/f'{tier}-{pose}-{direction:02}-{index:02}.png'
    im.save(path,compress_level=2)
    return str(path),im.getbbox()


def export_pose(tier,pose,count,directions,manifest,save,jobs=2):
    CACHE.mkdir(parents=True,exist_ok=True)
    view=frame_spec(pose)
    tasks=[(tier,pose,d,i,count) for d in range(directions) for i in range(count)]
    records=[];bounds=[view['width'],view['height'],0,0]
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        for path,b in pool.map(frame,tasks,chunksize=1):
            records.append(path)
            bounds=[min(bounds[0],b[0]),min(bounds[1],b[1]),max(bounds[2],b[2]),max(bounds[3],b[3])]
    margin=16
    crop=[max(0,math.floor((bounds[0]-margin)/2)*2),max(0,math.floor((bounds[1]-margin)/2)*2),
          min(view['width'],math.ceil((bounds[2]+margin)/2)*2),min(view['height'],math.ceil((bounds[3]+margin)/2)*2)]
    width,height=crop[2]-crop[0],crop[3]-crop[1]
    columns=max(n for n in range(1,count+1) if count%n==0 and n*width<=8192)
    rows_per_direction=count//columns
    per_page=max(1,min(directions,8192//(height*rows_per_direction)))
    assert height*rows_per_direction<=8192
    name=f'explorer-{tier}-{pose}';folder=MOD/'graphics/entity/industry'
    chunks=[];used=[]
    for page,start in enumerate(range(0,directions,per_page)):
        number=min(per_page,directions-start);rows=number*rows_per_direction
        atlas=Image.new('RGBA',(width*columns,height*rows))
        for offset in range(number*count):
            with Image.open(records[start*count+offset]) as im:
                atlas.paste(im.crop(crop),((offset%columns)*width,(offset//columns)*height))
        filename=name+(f'-{page+1}' if per_page<directions else '')+'.png'
        path=folder/filename;save(atlas,path);used.append(path)
        chunks.append({'filename':'__second-nature__/graphics/entity/industry/'+filename,
                       'width_in_frames':columns,'height_in_frames':rows,'x':0,'y':0})
    spec={'width':width,'height':height,'frame_count':count,'direction_count':directions,
          'line_length':columns,'scale':view['scale'],'apply_projection':False,
          'shift':[round((crop[0]+width/2-view['width']/2)*view['scale']/32,7),
                   round((crop[1]+height/2-view['height']*view['origin'])*view['scale']/32,7)]}
    if len(chunks)==1:spec['filename']=chunks[0]['filename']
    else:spec['stripes']=chunks
    manifest[name]=spec
    # Remove only obsolete pages belonging to this exact generated pose.
    for old in folder.glob(name+'*.png'):
        if re.fullmatch(re.escape(name)+r'(?:-\d+)?\.png',old.name) and old not in used:old.unlink()
    report_path=ROOT/'docs/art/character-render.json'
    report=json.loads(report_path.read_text()) if report_path.exists() else {}
    report[name]={'view':view,'crop':crop,'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in used}}
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    with Image.open(records[0]) as im:preview=im.copy()
    with Image.open(records[4*count]) as im:front=im.copy()
    for p in records:__import__('pathlib').Path(p).unlink()
    print('CHARACTER_HD',tier,pose,width,height,'pages',len(chunks),flush=True)
    return preview,front
