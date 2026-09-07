"""Compiled raster kernels for offline art generation. Optional asset dependency."""
import math
import numpy as np
from numba import njit

@njit(cache=True)
def gbuffer(screen,world,local,normals,colors,glows,width,height):
    out=np.zeros((height,width,14),dtype=np.float32)
    out[:,:,0]=-1e9
    for i in range(len(screen)):
        a,b,c=screen[i,0],screen[i,1],screen[i,2]
        left=max(0,int(math.floor(min(a[0],b[0],c[0]))));right=min(width-1,int(math.ceil(max(a[0],b[0],c[0]))))
        top=max(0,int(math.floor(min(a[1],b[1],c[1]))));bottom=min(height-1,int(math.ceil(max(a[1],b[1],c[1]))))
        den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den)<1e-8:continue
        inverse=1/den;stepa=(b[1]-c[1])*inverse;stepb=(c[1]-a[1])*inverse
        for y in range(top,bottom+1):
            wa=((b[1]-c[1])*(left+.5-c[0])+(c[0]-b[0])*(y+.5-c[1]))*inverse
            wb=((c[1]-a[1])*(left+.5-c[0])+(a[0]-c[0])*(y+.5-c[1]))*inverse
            for x in range(left,right+1):
                wc=1-wa-wb
                if wa>=-1e-6 and wb>=-1e-6 and wc>=-1e-6:
                    depth=wa*a[2]+wb*b[2]+wc*c[2]
                    if depth>=out[y,x,0]-1e-6:
                        out[y,x,0]=depth
                        for k in range(3):
                            out[y,x,1+k]=wa*world[i,0,k]+wb*world[i,1,k]+wc*world[i,2,k]
                            out[y,x,4+k]=wa*local[i,0,k]+wb*local[i,1,k]+wc*local[i,2,k]
                            out[y,x,7+k]=normals[i,k]
                            out[y,x,10+k]=colors[i,k]
                        out[y,x,13]=glows[i]
                wa+=stepa;wb+=stepb
    return out

@njit(cache=True)
def shadow_depth(triangles,width,height):
    out=np.full((height,width),-1e9,dtype=np.float32)
    for i in range(len(triangles)):
        a,b,c=triangles[i,0],triangles[i,1],triangles[i,2]
        left=max(0,int(math.floor(min(a[0],b[0],c[0]))));right=min(width-1,int(math.ceil(max(a[0],b[0],c[0]))))
        top=max(0,int(math.floor(min(a[1],b[1],c[1]))));bottom=min(height-1,int(math.ceil(max(a[1],b[1],c[1]))))
        den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den)<1e-8:continue
        inverse=1/den;stepa=(b[1]-c[1])*inverse;stepb=(c[1]-a[1])*inverse
        for y in range(top,bottom+1):
            wa=((b[1]-c[1])*(left+.5-c[0])+(c[0]-b[0])*(y+.5-c[1]))*inverse
            wb=((c[1]-a[1])*(left+.5-c[0])+(a[0]-c[0])*(y+.5-c[1]))*inverse
            for x in range(left,right+1):
                wc=1-wa-wb
                if wa>=-1e-6 and wb>=-1e-6 and wc>=-1e-6:
                    depth=wa*a[2]+wb*b[2]+wc*c[2]
                    if depth>out[y,x]:out[y,x]=depth
                wa+=stepa;wb+=stepb
    return out
