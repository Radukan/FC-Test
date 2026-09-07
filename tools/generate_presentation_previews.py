#!/usr/bin/env python3
"""Source-art review sheets. These are not graphical-client screenshots."""
from pathlib import Path
import json,math,subprocess,io
from PIL import Image,ImageDraw,ImageFont
from catalog import ROOT,MOD

ART=ROOT/'docs/art'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def tile(image,spec,direction=0,frame=0):
    index=direction*spec['frame_count']+frame
    x=index%spec['line_length']*spec['width'];y=index//spec['line_length']*spec['height']
    return image.crop((x,y,x+spec['width'],y+spec['height']))

def generate():
    manifest=json.loads((ART/'sprite-manifest.json').read_text())
    def load(name):
        spec=manifest[name];return Image.open(MOD/spec['filename'].split('__second-nature__/')[1]),spec
    font=ImageFont.truetype(FONT,13)
    # Full frames retain the pivot, so the preview cannot disguise cropping or foot sliding.
    image,spec=load('explorer-0-running_with_gun')
    contact=Image.new('RGB',(6*210,3*270),(27,31,27));d=ImageDraw.Draw(contact)
    from character_layout import ARMED_ROWS
    directions=('N','NE','E','SE','S','SW','W','NW')
    for row,(aim,stride) in enumerate(ARMED_ROWS):
        frame=tile(image,spec,row,3);frame.thumbnail((200,232),Image.Resampling.LANCZOS)
        x=row%6*210;y=row//6*270;contact.paste(frame,(x+(210-frame.width)//2,y+5),frame)
        d.text((x+10,y+238),f'Row {row}: aim {directions[aim]}, stride {directions[stride]}',font=font,fill=(222,218,191))
    contact.save(ART/'character-aim-layout.jpg',quality=92,optimize=True)
    source,spec=load('explorer-0-mining_with_tool');frames=[]
    for f in range(spec['frame_count']):
        sheet=Image.new('RGB',(880,305),(27,31,27));draw=ImageDraw.Draw(sheet)
        for col,direction in enumerate((0,2,4,6)):
            frame=tile(source,spec,direction,f);frame.thumbnail((210,252),Image.Resampling.LANCZOS)
            sheet.paste(frame,(col*220+(220-frame.width)//2,4),frame)
            draw.text((col*220+15,264),f'Mining {directions[direction]}',font=font,fill=(222,218,191))
        draw.text((12,288),'Fixed pivot and complete tool/shadow canvas. Rendered assets, not gameplay.',font=font,fill=(171,177,155));frames.append(sheet)
    frames[0].save(ART/'mining-framing-preview.gif',save_all=True,append_images=frames[1:],duration=85,loop=0,optimize=True)
    selected=['air-scrubber-north','watershed-north','seed-disperser-north','planetary-beacon-north',
              'sentry-turret-fire','arc-turret-fire','lance-turret-fire','explorer-0-running']
    loaded=[load(name) for name in selected];frames=[]
    for f in range(12):
        sheet=Image.new('RGB',(880,500),(27,31,27));draw=ImageDraw.Draw(sheet)
        for i,(name,(source,spec)) in enumerate(zip(selected,loaded)):
            frame=tile(source,spec,0,f%spec['frame_count']);frame.thumbnail((205,210),Image.Resampling.LANCZOS)
            x=i%4*220;y=i//4*245;sheet.paste(frame,(x+(220-frame.width)//2,y+8),frame)
            draw.text((x+8,y+221),name.replace('-north','').replace('-fire',''),font=font,fill=(222,218,191))
        draw.text((12,484),'Original rendered sprite loops, not in-game footage.',font=font,fill=(171,177,155));frames.append(sheet)
    frames[0].save(ART/'industrial-animation-preview.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)
    print('Generated aiming, mining and industrial animation review sheets.')
if __name__=='__main__':generate()
