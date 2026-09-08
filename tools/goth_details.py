"""Original goth clothing, wolf-cut locks and botanical/circuit ink for the adult rig."""
import math
from industrial_art import Mesh, add, mul
from gait import sub, unit, dot
from character_rig import cross

PALE=(220,207,216)
INK=(29,26,39)
HAIR=(23,18,30)
SILVER=(151,158,167)
CLOTH=(24,22,31)


def tattoo(mesh,a,b,ra=.073,rb=.057,side=1):
    axis=unit(sub(b,a));face=unit(sub((side*.28,-1,0),mul(axis,dot((side*.28,-1,0),axis))))
    tangent=unit(cross(axis,face))
    def point(t,angle):
        radius=(ra*(1-t)+rb*t)*(1.032 if t<.7 else .96)
        return add(add(a,mul(sub(b,a),t)),add(mul(face,radius*math.cos(angle)),mul(tangent,radius*math.sin(angle))))
    path=[point(.13+i*.085,.14*math.sin(i*.9)) for i in range(9)]
    for p,q in zip(path,path[1:]):mesh.tube(p,q,.0045,INK,6)
    for i in range(1,7):
        t=.13+i*.085
        mesh.tube(point(t,.14*math.sin(i*.9)),point(t+.035,(-1 if i%2 else 1)*.62),.0038,INK,6)
    for i in range(4):
        t=.32+i*.025
        mesh.tube(point(t,.55),point(t,1.15),.0035,INK,6)


def skirt(mesh,pelvis,joints,phase,tier):
    """Pleated mini skirt over opaque undershorts, draped around moving thighs."""
    n=32;rings=[]
    for z,rx,ry,weight in ((1.12,.25,.16,0),(.99,.274,.18,.18),(.82,.30,.225,1)):
        ring=[]
        for i in range(n):
            angle=i*math.tau/n
            p=pelvis.point((rx*math.cos(angle),ry*math.sin(angle),z))
            if weight:
                # Leg-aware hem: do not leave a rigid, clipping horizontal cone.
                for side in (-1,1):
                    hip,knee=joints['hip-'+str(side)],joints['knee-'+str(side)]
                    t=max(0,min(.75,(hip[2]-p[2])/max(.08,hip[2]-knee[2])))
                    center=add(hip,mul(sub(knee,hip),t))
                    influence=max(0,1-abs(p[0]-center[0])/.30)
                    if math.sin(angle)<0:p=(p[0],min(p[1],center[1]-.145*influence*weight),p[2])
                    else:p=(p[0],max(p[1],center[1]+.13*influence*weight),p[2])
                pleat=(.010 if i%2 else -.005)*weight
                p=(p[0]+pleat*math.cos(angle),p[1]+pleat*math.sin(angle),p[2]+.008*weight*math.sin(phase+i*.8))
            ring.append(p)
        rings.append(ring)
    for a,b in zip(rings,rings[1:]):
        for i in range(n):
            j=(i+1)%n
            color=(31,24,37) if i%2 else (23,22,30)
            mesh.face([a[i],a[j],b[j],b[i]],color)
    for i in range(n):mesh.tube(rings[-1][i],rings[-1][(i+1)%n],.007,(79,37,57),6)
    for side in (-1,1):
        points=[pelvis.point((side*(.21-.022*i),-.166,1.08-.018*math.sin(i*math.pi/7))) for i in range(8)]
        for a,b in zip(points,points[1:]):mesh.tube(a,b,.006,SILVER,6)
    return rings


def lock(mesh,start,mid,tip,width,color):
    axis=unit(sub(tip,start));across=unit(cross(axis,(0,1,0) if abs(axis[1])<.9 else (1,0,0)))
    a,b=add(start,mul(across,width)),add(start,mul(across,-width))
    c,d=add(mid,mul(across,width*.75)),add(mid,mul(across,-width*.75))
    ridge=add(mid,(0,-.010,.006))
    mesh.face([a,b,d,c],color);mesh.face([c,d,tip],color)
    mesh.face([a,c,ridge],tuple(min(255,v+7) for v in color));mesh.face([c,tip,ridge],color)


def wolfcut(mesh,phase):
    mesh.ball((0,.018,2.077),.135,HAIR,stretch=(1.06,.95,.68))
    # Uneven, feathered fringe. Eyes remain visible below the fringe.
    for i in range(7):
        x=(i-3)*.035
        lock(mesh,(x,-.055,2.12),(x+.012,-.129,2.07),(x+(.014 if i%2 else -.012),-.151,2.033+(i%3)*.009),.025,HAIR)
    for side in (-1,1):
        for i in range(5):
            lock(mesh,(side*.108,.005+i*.020,2.075),
                 (side*(.158+i*.003),-.008+i*.030,1.97),
                 (side*(.151+i*.009),.028+i*.035,1.865-i*.022+.006*math.sin(phase+i)),.035,
                 (27+i*2,20+i,36+i*2))
    # Longer shagged nape and crown layers distinguish a wolf cut from a bob.
    for i in range(9):
        x=(i-4)*.028
        lock(mesh,(x,.104,2.075), (x*1.22,.171,1.945),
             (x*1.32+.006*math.sin(phase+i),.205,1.755+(i%3)*.018),.032,(25+i%3*3,20,34+i%3*4))
    for side in (-1,1):
        for i in range(3):
            lock(mesh,(side*.06,.03,2.135),(side*.145,.068+i*.035,2.04),
                 (side*(.17+i*.014),.10+i*.035,1.96-i*.017),.038,HAIR)
