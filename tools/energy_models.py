"""Original Nightglass generating plants and three recognizable solar locomotives."""
import math
from industrial_art import Mesh,STEEL,DARK,EDGE,GOLD,COPPER,TEAL,WHITE,RED,TAU,fan,hose,tank,cabinet

PANEL=(35,68,103)
PAINT=(117,135,119)


def solar(m,x,y,z,w,d,slope=.16):
    points=[(x-w/2,y-d/2,z+slope),(x+w/2,y-d/2,z+slope),(x+w/2,y+d/2,z),(x-w/2,y+d/2,z)]
    m.face(points,PANEL)
    for a,b in zip(points,points[1:]+points[:1]):m.tube(a,b,.025,EDGE,8)
    for i in range(1,8):
        xx=x-w/2+w*i/8;m.tube((xx,y-d/2,z+slope+.006),(xx,y+d/2,z+.006),.007,(121,158,174),6)
    for i in range(1,4):
        yy=y-d/2+d*i/4;zz=z+slope*(1-i/4)+.008
        m.tube((x-w/2,yy,zz),(x+w/2,yy,zz),.006,(90,128,145),6)


def foundation(m,size):
    m.box((0,0,.12),(size-.14,size-.14,.22),DARK,.12)
    for x in (-size*.39,size*.39):
        for y in (-size*.39,size*.39):m.box((x,y,.16),(.31,.31,.30),STEEL,.09)
    for side in (-1,1):m.box((side*(size/2-.12),0,.28),(.08,size-.4,.10),EDGE,.02)


def plant(name,t=0):
    m=Mesh();sizes={'micro-solar':2,'burner-set':2,'wind-turbine':3,'biopellet-engine':3,'geothermal-bore':5,'cogenerator':4}
    size=sizes[name];foundation(m,size)
    if name=='micro-solar':
        for x in (-.65,.65):m.tube((x,.5,.24),(x,.5,.82),.045,EDGE,10)
        solar(m,0,0,.58,1.64,1.53,.27)
        m.box((.53,.75,.31),(.34,.25,.20),STEEL,.05)
    elif name=='burner-set':
        tank(m,-.31,0,.36,.74,PAINT)
        m.cyl(-.31,0,1.25,.15,.70,DARK,16);m.ring((-.31,0,1.92),.20,.025,COPPER)
        m.box((.46,-.08,.66),(.52,1.0,.74),STEEL,.08)
        rotor=Mesh();rotor.box((0,0,0),(.09,.56,.075),GOLD,.025);m.join(rotor,t*TAU,(.46,-.08,1.07))
        m.box((-.35,-.43,.70),(.43,.06,.39),DARK,.06)
        m.box((-.35,-.472,.69),(.22,.02,.12),RED,.02)
        hose(m,[(-.15,.36,.64),(.27,.36,.64),(.47,.24,.64)],.04,COPPER)
    elif name=='wind-turbine':
        m.cyl(0,0,.24,.34,.36,STEEL,28)
        m.cyl(0,0,.60,.13,2.93,EDGE,20)
        m.cyl(0,0,1.32,.22,1.70,DARK,20)
        for blade in range(3):
            for j in range(12):
                a=t*TAU+blade*TAU/3+j*.12;b=a+.15;z=1.30+j*.143
                m.face([(.83*math.cos(a),.83*math.sin(a),z),(.45*math.cos(a+.28),.45*math.sin(a+.28),z),
                        (.45*math.cos(b+.28),.45*math.sin(b+.28),z+.16),(.83*math.cos(b),.83*math.sin(b),z+.16)],PAINT)
        for z in (1.27,3.08):m.ring((0,0,z),.84,.035,EDGE)
        for x,y in ((-1,-1),(1,-1),(1,1),(-1,1)):m.tube((x,y,.25),(0,0,3.42),.018,COPPER,8)
        cabinet(m,.67,.74,.66,.85)
    elif name=='biopellet-engine':
        for x in (-.6,.6):
            tank(m,x,-.2,.33,.92,PAINT)
            m.cyl(x,-.2,1.48,.13,.3,EDGE,16)
        m.box((0,.57,.62),(1.80,.65,.55),DARK,.13)
        for i in range(7):m.box((-.72+i*.24,.57,.91),(.11,.73,.07),COPPER,.02)
        fan(m,0,.57,.94,.26,t)
        hose(m,[(-.63,-.14,1.28),(-.63,.64,1.32),(.63,.64,1.32),(.63,-.14,1.28)],.048,COPPER)
        m.box((0,-1.08,.53),(.65,.43,.40),STEEL,.08)
        for i in range(4):m.box((-.19+i*.12,-1.30,.53),(.035,.02,.25),EDGE,.01)
        m.ball((.2,-1.32,.65),.033,TEAL,glow=True)
    elif name=='geothermal-bore':
        m.cyl(-.85,0,.26,.77,.42,DARK,36)
        m.cyl(-.85,0,.68,.52,1.35,STEEL,32)
        m.ring((-.85,0,1.90),.69,.067,COPPER)
        for i in range(6):
            a=i*TAU/6;m.tube((-.85+.65*math.cos(a),.65*math.sin(a),.45),(-.85+.45*math.cos(a),.45*math.sin(a),2.02),.08,EDGE,12)
        m.box((1,.1,.62),(1.25,2.8,.74),STEEL,.12)
        for y in (-.65,.65):fan(m,1,y,1.06,.42,t)
        for y in (-1.12,1.12):
            hose(m,[(-.9,y,.41),(-.9,y,1.13),(.75,y,1.13)],.14,COPPER)
            m.cyl(-.9,y,.32,.21,.16,EDGE,20)
        m.box((-.4,-1.78,.51),(2.8,.47,.35),DARK,.09)
        for i in range(10):m.box((-1.5+i*.25,-1.78,.7),(.13,.52,.04),EDGE,.01)
        cabinet(m,1.66,1.56,.72,1.1)
    elif name=='cogenerator':
        m.box((0,0,.87),(2.26,2.9,1.18),STEEL,.16)
        for side in (-1,1):
            m.cyl(side*.78,.7,1.46,.22,1.42,DARK,24)
            m.ring((side*.78,.7,2.88),.28,.045,COPPER)
            for y in (-.85,-.28,.29):m.box((side*1.22,y,.95),(.28,.39,.65),EDGE,.06)
        for y in (-.65,.20):fan(m,0,y,1.49,.4,t)
        m.box((0,-1.57,.80),(1.02,.24,.83),DARK,.12)
        for i in range(6):m.box((-.39+i*.15,-1.71,.85),(.065,.025,.41),GOLD,.012)
        hose(m,[(-1.56,-1.25,.38),(-1.56,-1.25,1.05),(-1.56,1.34,1.05),(0,1.34,1.05)],.12,COPPER)
    return m


def locomotive(tier=1):
    m=Mesh();paint=(103,122,101) if tier==1 else ((112,130,146) if tier==2 else (149,141,161))
    m.box((0,0,.33),(1.38,5.2,.39),DARK,.14)
    for y in (-1.72,1.72):
        m.box((0,y,.22),(1.48,1.13,.32),STEEL,.1)
        for x in (-.67,.67):
            for yy in (y-.32,y+.32):
                m.tube((x-.09,yy,.23),(x+.09,yy,.23),.22,DARK,20)
                m.tube((x-.10,yy,.23),(x+.10,yy,.23),.075,EDGE,14)
        m.box((0,y,.46),(.64,.88,.08),COPPER,.06)
    for y in (-2.73,2.73):
        m.box((0,y,.30),(.50,.32,.19),EDGE,.06)
        for x in (-.52,.52):m.box((x,y*.96,.45),(.27,.16,.21),DARK,.04)
    # Three different silhouettes: exposed shunter, covered freight and smooth express.
    if tier==1:
        m.box((0,-1.37,1.02),(1.27,1.40,1.12),paint,.20)
        m.box((0,-2.10,1.20),(.90,.07,.48),(61,112,127),.05)
        m.box((0,.75,.78),(1.12,2.58,.48),paint,.17)
        solar(m,0,.55,1.10,1.24,2.66,.07)
        m.box((0,-1.33,1.61),(1.44,1.61,.10),DARK,.10)
        for side in (-1,1):hose(m,[(side*.49,-.57,.85),(side*.68,-.22,.86),(side*.68,1.8,.86)],.038,COPPER)
    elif tier==2:
        m.box((0,0,.99),(1.30,4.50,1.10),paint,.23)
        m.box((0,-2.27,1.15),(.91,.075,.47),(67,118,133),.08)
        solar(m,0,-.37,1.56,1.40,3.70,.05)
        for side in (-1,1):
            solar(m,side*.63,1.14,1.37,.30,1.45,.12)
            for y in (-.9,-.3,.3):m.box((side*.677,y,.86),(.02,.31,.24),DARK,.03)
    else:
        rings=[]
        for y,rx,z,h in [(-2.55,.24,.77,.50),(-2.12,.56,1.02,.98),(-1.25,.70,1.09,1.19),(1.6,.68,1.02,1.08),(2.43,.42,.88,.72)]:
            ring=[(rx*math.cos(i*TAU/20),y,z+h*.5*math.sin(i*TAU/20)) for i in range(20)];rings.append(ring)
        m.face(list(reversed(rings[0])),paint);m.face(rings[-1],paint)
        for a,b in zip(rings,rings[1:]):
            for i in range(20):j=(i+1)%20;m.face([a[i],a[j],b[j],b[i]],paint)
        m.face([(-.47,-1.90,1.46),(.47,-1.90,1.46),(.33,-2.28,1.21),(-.33,-2.28,1.21)],(66,114,138))
        solar(m,0,.1,1.67,1.24,2.97,.005)
        for side in (-1,1):
            m.tube((side*.69,-1.44,1.07),(side*.69,1.98,1.07),.025,COPPER,8)
            m.box((side*.70,1.82,.64),(.025,.76,.13),DARK,.02)
    for side in (-1,1):
        for y in (-2.14,2.14):m.ball((side*.46,y,1.03 if y<0 else .77),.078,(206,194,144) if y<0 else RED,glow=True)
        m.tube((side*.71,-1.9,.65),(side*.71,1.9,.65),.022,EDGE,8)
    m.surface_finish='hull'
    return m
