"""Articulated limb meshes and visible gloved hands for the expedition rig."""
import math
from gait import add,sub,mul,dot,unit,length

def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def limb(mesh,a,b,ra,rb,color,sides=16):
    axis=unit(sub(b,a));u=unit(cross(axis,(0,1,0) if abs(axis[1])<.9 else (1,0,0)));v=cross(axis,u)
    rings=[]
    for t,bulge in ((0,.90),(.18,1.05),(.65,1.0),(1,.88)):
        r=(ra*(1-t)+rb*t)*bulge;center=add(a,mul(sub(b,a),t))
        rings.append([add(center,add(mul(u,r*math.cos(i*math.tau/sides)),mul(v,r*math.sin(i*math.tau/sides)))) for i in range(sides)])
    mesh.face(list(reversed(rings[0])),color);mesh.face(rings[-1],color)
    for a,b in zip(rings,rings[1:]):
        for i in range(sides):j=(i+1)%sides;mesh.face((a[i],a[j],b[j],b[i]),color)

def hand(mesh,wrist,forward=(0,0,-1),back=(0,1,0),side=1,curl=.25,colors=None):
    forward=unit(forward);back=unit(sub(back,mul(forward,dot(back,forward))));across=unit(cross(forward,back))
    leather,knuckle,seam=colors or ((38,32,45),(109,111,125),(21,18,27))
    def p(x,y,z):return add(wrist,add(mul(across,x),add(mul(forward,y),mul(back,z))))
    # Palm and cuff have real width/thickness; the digits are not hidden in a black sphere.
    corners=[p(x,y,z) for z in (-.027,.027) for y in (0,.125) for x in (-.064,.064)]
    for face in ((0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)):
        mesh.face([corners[i] for i in face],leather)
    mesh.tube(p(0,-.012,0),p(0,.025,0),.073,seam,14)
    mesh.tube(p(0,-.015,0),p(0,-.002,0),.078,knuckle,14)
    mesh.face([p(-.05,.025,.029),p(.05,.025,.029),p(.046,.09,.036),p(-.046,.09,.036)],knuckle)
    joints={'wrist':wrist,'palm':p(0,.065,0)}
    for finger,(x,size) in enumerate(((-.047,.092),(-.016,.116),(.016,.112),(.047,.087))):
        root=p(x,.112,.002);current=root;joints[f'finger-{finger}-0']=root
        for bone,fraction in enumerate((.43,.33,.24)):
            angle=curl*(bone+1)*.62
            direction=add(mul(forward,math.cos(angle)),mul(back,-math.sin(angle)))
            end=add(current,mul(direction,size*fraction))
            limb(mesh,current,end,.018 if bone<2 else .015,.016 if bone<2 else .012,leather,10)
            mesh.ball(current,.020,knuckle,stretch=(1,1,.8))
            current=end;joints[f'finger-{finger}-{bone+1}']=end
    root=p(side*.061,.043,0);mid=add(root,add(mul(across,side*.042),mul(forward,.037)))
    tip=add(mid,add(mul(forward,.052),mul(back,-.015-curl*.015)))
    limb(mesh,root,mid,.028,.024,leather,12);limb(mesh,mid,tip,.023,.017,leather,12)
    mesh.ball(mid,.026,knuckle)
    joints['thumb-0'],joints['thumb-1'],joints['thumb-2']=root,mid,tip
    return joints
