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


def scalp_shell(mesh,phase):
    """A continuous hair shell lofted over the skull.

    The previous crown was a single flattened ball that started behind the brow,
    so the character read as balding: a wide band of bare forehead showed between
    the brow ridge and where the hair actually began. This walks an explicit
    surface from the hairline, over the crown, to the nape, hugging the skull
    loft closely enough to look like hair rather than a helmet.
    """
    cx,cy,cz=0.0,.005,1.960
    rx,ry,rz=.132,.132,.175
    rings=8;segments=24
    # The shell stops just above the brow in front and runs lower at the back,
    # which is what separates a wolf cut from a bowl cut.
    phi_front,phi_back=1.44,2.08

    def point(phi,a,lift):
        sx,cs=math.sin(phi),math.cos(phi)
        return (cx+(rx+lift)*sx*math.sin(a),
                cy+(ry+lift)*sx*math.cos(a),
                cz+(rz+lift)*cs)

    # Start the walk slightly off the pole so ring 0 is a small circle rather
    # than a degenerate point, then close that circle with a fan. Converging
    # every segment on one vertex leaves a visible crater at the crown.
    phi_start=.16
    grid=[]
    for i in range(rings+1):
        u=i/rings
        row=[]
        for j in range(segments):
            a=j*math.tau/segments
            # Rim depth varies with azimuth: shallow at the face, deep at the nape.
            limit=phi_front+(phi_back-phi_front)*(math.cos(a)+1)*.5
            # Hug the skull. A thick offset reads as a helmet, not as hair.
            # The back of the head is the widest part of the skull, so the
            # shell needs extra clearance there or bare scalp shows through
            # at the nape where the rim curves back inboard.
            back=(math.cos(a)+1)*.5
            lift=.011+.002*math.sin(u*math.pi)+.014*back*u
            row.append(point(phi_start+u*(limit-phi_start),a,lift))
        grid.append(row)

    apex=point(0,0,.013)
    for j in range(segments):
        k=(j+1)%segments
        mesh.face([apex,grid[0][j],grid[0][k]],(30,24,38))
    for i in range(rings):
        for j in range(segments):
            k=(j+1)%segments
            shade=26+int(6*math.sin(i*.7+j*.3))
            mesh.face([grid[i][j],grid[i][k],grid[i+1][k],grid[i+1][j]],
                      (shade,shade-6,shade+8))


def wolfcut(mesh,phase):
    scalp_shell(mesh,phase)
    # Side-swept fringe. Tips are held at or above the brow line and pushed
    # outboard past the eyes: a denser curtain buries the face at game zoom and
    # reads worse than the balding it was meant to fix.
    for side in (-1,1):
        count=6 if side<0 else 4
        for i in range(count):
            spread=i/max(1,count-1)
            lock(mesh,
                 (side*(.020+spread*.055),-.086+spread*.030,2.074),
                 (side*(.098+spread*.030),-.104+spread*.026,2.010),
                 (side*(.118+spread*.036),-.070+spread*.040,1.968+spread*.006),
                 .026,(24+i*2,18+i,32+i*2))
    # Cheek-length side panels frame the face without covering it.
    for side in (-1,1):
        for i in range(5):
            lock(mesh,(side*.108,.005+i*.020,2.062),
                 (side*(.152+i*.003),-.008+i*.030,1.965),
                 (side*(.146+i*.009),.028+i*.035,1.862-i*.022+.006*math.sin(phase+i)),.035,
                 (27+i*2,20+i,36+i*2))
    # Longer shagged nape and crown layers distinguish a wolf cut from a bob.
    for i in range(9):
        x=(i-4)*.028
        lock(mesh,(x,.104,2.060), (x*1.22,.171,1.940),
             (x*1.32+.006*math.sin(phase+i),.205,1.752+(i%3)*.018),.032,(25+i%3*3,20,34+i%3*4))
    for side in (-1,1):
        for i in range(3):
            lock(mesh,(side*.06,.03,2.120),(side*.145,.068+i*.035,2.032),
                 (side*(.17+i*.014),.10+i*.035,1.955-i*.017),.038,HAIR)
