"""Depth-aware sprite rasterizer with self-shadowing and procedural surface wear.
The material is anchored in model space so fixed machinery does not shimmer.
This is an offline CPU art tool, not a runtime shader or an imported game asset.
"""
import math
import numpy as np
from PIL import Image,ImageDraw,ImageFilter

ELEVATION=math.radians(48)

def unit(v):
    v=np.asarray(v,dtype=float);return v/max(1e-12,np.linalg.norm(v))

def rotz(points,a):
    c,s=math.cos(a),math.sin(a);p=np.asarray(points,dtype=float)
    return p@np.array([[c,s,0],[-s,c,0],[0,0,1]])

def project(points,width,height,ppu,origin,map_aligned=False):
    p=np.asarray(points);ground=1.0 if map_aligned else math.sin(ELEVATION)
    return np.column_stack((width/2+p[:,0]*ppu,height*origin+(ground*p[:,1]-math.cos(ELEVATION)*p[:,2])*ppu,
      p[:,1]*math.cos(ELEVATION)+p[:,2]*math.sin(ELEVATION)))

def noise(p,scale=1):
    q=p*scale;cells=np.floor(q);f=q-cells;f=f*f*(3-2*f);result=np.zeros(len(p))
    for x in (0,1):
      for y in (0,1):
       for z in (0,1):
        cell=cells+np.array([x,y,z]);n=np.sin(cell@np.array([127.1,311.7,74.7]))*43758.5453;n-=np.floor(n)
        weight=(f[:,0] if x else 1-f[:,0])*(f[:,1] if y else 1-f[:,1])*(f[:,2] if z else 1-f[:,2])
        result+=weight*n
    return result

def triangles(vertices):
    for i in range(1,len(vertices)-1):yield (0,i,i+1)

def raster_triangle(p,width,height):
    pa,pb,pc=p
    xmin=max(0,int(math.floor(min(pa[0],pb[0],pc[0]))));xmax=min(width-1,int(math.ceil(max(pa[0],pb[0],pc[0]))))
    ymin=max(0,int(math.floor(min(pa[1],pb[1],pc[1]))));ymax=min(height-1,int(math.ceil(max(pa[1],pb[1],pc[1]))))
    if xmin>xmax or ymin>ymax:return None
    den=(pb[1]-pc[1])*(pa[0]-pc[0])+(pc[0]-pb[0])*(pa[1]-pc[1])
    if abs(den)<1e-8:return None
    yy,xx=np.ogrid[ymin:ymax+1,xmin:xmax+1];xx=xx+.5;yy=yy+.5
    a=((pb[1]-pc[1])*(xx-pc[0])+(pc[0]-pb[0])*(yy-pc[1]))/den
    b=((pc[1]-pa[1])*(xx-pc[0])+(pa[0]-pc[0])*(yy-pc[1]))/den
    c=1-a-b;mask=(a>=-1e-6)&(b>=-1e-6)&(c>=-1e-6)
    return (slice(ymin,ymax+1),slice(xmin,xmax+1)),a,b,c,mask

def render(mesh,width=320,height=None,ppu=64,angle=0,aa=2,origin=.70,map_aligned=False):
    height=height or width;w,h=width*aa,height*aa;scale=ppu*aa
    faces=[]
    smooth_colors=set(getattr(mesh,"smooth_colors",()))
    smooth_normals={}
    camera=np.array([0,math.cos(ELEVATION),math.sin(ELEVATION)])
    for vertices,color,glow in mesh.faces:
        model=np.asarray(vertices,dtype=float);world=rotz(model,angle)
        normal=unit(np.cross(world[1]-world[0],world[2]-world[0]))
        if tuple(color) in smooth_colors:
            for vertex in world:
                key=(tuple(color),tuple(np.round(vertex,7)))
                smooth_normals[key]=smooth_normals.get(key,np.zeros(3))+normal
        if np.dot(normal,camera)<0:normal=-normal
        faces.append((model,world,np.asarray(color)/255,glow,normal))
    smooth_normals={key:unit(value) for key,value in smooth_normals.items()}
    from raster_kernel import gbuffer,shadow_depth
    tri_world=[];tri_local=[];tri_colors=[];tri_normals=[];tri_glows=[];tri_screen=[]
    for model,world,c,glow,n in faces:
        screen=project(world,w,h,scale,origin,map_aligned)
        for inds in triangles(world):
            ids=list(inds);tri_world.append(world[ids]);tri_local.append(model[ids]);tri_screen.append(screen[ids])
            normals=[]
            color_key=tuple(np.rint(c*255).astype(int))
            for vertex in world[ids]:
                value=smooth_normals.get((color_key,tuple(np.round(vertex,7))),n)
                normals.append(value if np.dot(value,camera)>=0 else -value)
            tri_colors.append(c);tri_normals.append(normals);tri_glows.append(float(bool(glow)))
    worlds=np.asarray(tri_world);locals=np.asarray(tri_local);screens=np.asarray(tri_screen)
    buffer=gbuffer(screens,worlds,locals,np.asarray(tri_normals),np.asarray(tri_colors),np.asarray(tri_glows),w,h)
    depth=buffer[:,:,0];pos=buffer[:,:,1:4];uv=buffer[:,:,4:7];normals=buffer[:,:,7:10];albedo=buffer[:,:,10:13];emissive=buffer[:,:,13]>0
    valid=depth>-1e8
    # A directional shadow map supplies real contact/self shadows between components.
    light=unit((-.65,-.78,1.35));lr=unit(np.cross(light,(0,0,1)));lu=unit(np.cross(lr,light))
    points=np.concatenate([f[1] for f in faces]);lp=np.column_stack((points@lr,points@lu,points@light))
    lo=np.min(lp[:,:2],axis=0)-.12;hi=np.max(lp[:,:2],axis=0)+.12
    shadow_size=min(768,max(320,width*2));ss=(shadow_size-1)/(hi-lo)
    projected_light=np.empty_like(worlds)
    projected_light[:,:,0]=(worlds@lr-lo[0])*ss[0]
    projected_light[:,:,1]=(worlds@lu-lo[1])*ss[1]
    projected_light[:,:,2]=worlds@light
    shadow=shadow_depth(projected_light,shadow_size,shadow_size)
    xyz=pos[valid].astype(float);surface=uv[valid].astype(float);normal=normals[valid].astype(float)
    color=albedo[valid].astype(float);glow=emissive[valid]
    lx=np.rint((xyz@lr-lo[0])*ss[0]).astype(int);ly=np.rint((xyz@lu-lo[1])*ss[1]).astype(int);lz=xyz@light
    visibility=np.zeros(len(xyz))
    for dx,dy in ((0,0),(-1,0),(1,0),(0,-1),(0,1)):
        z=shadow[np.clip(ly+dy,0,shadow_size-1),np.clip(lx+dx,0,shadow_size-1)]
        visibility+=(lz>=z-.022)/5
    coarse=noise(surface,3.6);fine=noise(surface,55)
    # Earthy steel, worn paint, oxidized seams and fabric retain each building's colors.
    skin=(color[:,0]>.53)&(color[:,1]>.30)&(color[:,1]<.60)&(color[:,2]<.48)&(color[:,0]>color[:,1]*1.25)
    paint=(np.max(color,axis=1)-np.min(color,axis=1))>.21
    goth=getattr(mesh,'surface_finish',None)=='goth'
    if goth:skin=skin | ((np.min(color,axis=1)>.65) & ((np.max(color,axis=1)-np.min(color,axis=1))<.16))
    metal=~skin&~glow
    grime=(.96+.025*coarse) if goth else (.86+.19*coarse+.05*fine)
    color*=np.where(skin, .97+.05*fine, grime)[:,None]
    rust=np.clip((.29-coarse)*1.1,0,.25)*metal*(~paint)
    color=color*(1-rust[:,None])+np.array([.33,.18,.075])*rust[:,None]
    scratches=np.clip((fine-.78)*.18,0,.045)*metal*(0.15 if goth else 1)
    color+=scratches[:,None]
    # Low-amplitude procedural normals add grain without moving the texture through time.
    bump=np.column_stack((np.sin(surface[:,0]*89+surface[:,2]*21),np.sin(surface[:,1]*83+surface[:,2]*31),np.zeros(len(surface))))
    if getattr(mesh, 'surface_finish', None) in ('hull', 'cloth', 'goth'):
        # Non-periodic, model-anchored cast-metal grain; avoid a woven/checker
        # pattern on the shuttle's broad ceramic and painted hull surfaces.
        bump=np.column_stack((noise(surface+np.array([7.1,2.3,4.7]),32)-.5,
                              noise(surface+np.array([1.9,8.2,3.6]),32)-.5,
                              noise(surface+np.array([4.6,1.7,9.2]),32)-.5))
    bump-=normal*np.sum(normal*bump,axis=1)[:,None]
    normal+=bump*np.where(skin,.006 if goth else .012,.025 if goth else .065)[:,None];normal/=np.maximum(1e-6,np.linalg.norm(normal,axis=1))[:,None]
    ndl=np.clip(normal@light,0,1);half=unit(light+unit((0,math.cos(ELEVATION),math.sin(ELEVATION))))
    spec=np.clip(normal@half,0,1)**np.where(paint,32,48)
    brightness=.40+ndl*visibility*1.00
    shaded=color*brightness[:,None]*np.array([1.02,.99,.93])
    shaded+=spec[:,None]*visibility[:,None]*np.where(skin,.07,.22)[:,None]
    shaded=np.where(glow[:,None],color*1.12,shaded)
    # Gentle film contrast, preserving detail in unlit metal instead of pure black faces.
    shaded=np.clip(shaded,0,1.35);shaded=shaded/(1+.12*shaded)
    pixels=np.zeros((h,w,4),dtype='uint8');pixels[valid,:3]=np.clip(shaded*255,0,255).astype('uint8');pixels[valid,3]=255
    out=Image.new('RGBA',(w,h));cast=Image.new('RGBA',(w,h));d=ImageDraw.Draw(cast)
    for _,world,_,_,_ in faces:
        ground=world.copy();ground[:,0]-=ground[:,2]*light[0]/light[2];ground[:,1]-=ground[:,2]*light[1]/light[2];ground[:,2]=0
        coords=project(ground,w,h,scale,origin,map_aligned)
        d.polygon([tuple(p[:2]) for p in coords],fill=(20,18,12,72))
    out.alpha_composite(cast.filter(ImageFilter.GaussianBlur(1.8*aa)))
    out.alpha_composite(Image.fromarray(pixels,'RGBA'))
    return out.resize((width,height),Image.Resampling.LANCZOS)
