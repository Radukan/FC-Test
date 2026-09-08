"""Twelve new power silhouettes, with explicit native fluid seams."""
import math
from industrial_art import Mesh,STEEL,DARK,EDGE,GOLD,COPPER,TEAL,WHITE,RED,TAU,fan,hose,tank,cabinet


def build(name,t,size,width=None,height=None):
    from energy_models import solar,foundation
    m=Mesh();foundation(m,width or size,height or size)
    if name=='river-turbine':
        for x in (-.58,.58):m.tube((x,-.10,.40),(x,-.10,1.40),.09,STEEL,14)
        m.tube((-.7,-.1,1.25),(.7,-.1,1.25),.15,EDGE,20)
        for x in (-.42,.42):
            for i in range(20):
                a=i*TAU/20+t*TAU;b=(i+1)*TAU/20+t*TAU
                m.tube((x,-.1+math.cos(a),1.25+math.sin(a)),(x,-.1+math.cos(b),1.25+math.sin(b)),.052,COPPER,8)
                if i%2==0:m.tube((x,-.1,1.25),(x,-.1+math.cos(a),1.25+math.sin(a)),.025,EDGE,8)
        for i in range(10):
            a=i*TAU/10+t*TAU
            m.box((0,-.1+math.cos(a),1.25+math.sin(a)),(.95,.20,.12),(96,126,133),.04)
        m.box((.95,.28,.60),(.55,1.3,.65),STEEL,.12)
    elif name=='steam-piston':
        for x in (-.52,.52):
            m.tube((x,-.7,.8),(x,.55,.8),.30,STEEL,24)
            m.tube((x,.55,.8),(x,1.0+.15*math.sin(t*TAU),.8),.055,COPPER,12)
            m.box((x,1.07,.65),(.40,.26,.32),EDGE,.06)
        m.tube((-.82,-.20,1.26),(.82,-.20,1.26),.07,COPPER,12)
        fan(m,0,.1,1.14,.29,t)
    elif name=='producer-gas-engine':
        tank(m,-.45,.08,.40,1.65,(129,109,75))
        m.cyl(-.45,.08,2.0,.13,.42,DARK,16)
        m.box((.65,0,.67),(.60,1.7,.63),STEEL,.13)
        for i in range(5):m.box((.65,-.62+i*.3,1.0),(.69,.09,.06),EDGE,.02)
        hose(m,[(-.45,-.12,1.50),(.64,-.12,1.50),(.64,-.12,1.0)],.09,COPPER)
    elif name=='solar-tower':
        m.cyl(0,0,.25,.55,.40,STEEL,24);m.cyl(0,0,.65,.19,3.30,EDGE,20)
        m.ball((0,0,3.95),.36,(197,163,85),stretch=(1,1,1.3),glow=True)
        for x,y in ((-2.2,-2.2),(0,-2.3),(2.2,-2.2),(-2.2,0),(2.2,0),(-2.2,2.2),(0,2.3),(2.2,2.2)):
            m.tube((x,y,.25),(x,y,.69),.05,EDGE,10);solar(m,x,y,.75,1.65,1.36,.35)
        for x,y in ((-1,-1),(1,-1),(-1,1),(1,1)):m.tube((x,y,.26),(0,0,3.76),.028,COPPER,8)
    elif name=='biogas-turbine':
        for x in (-1.1,1.1):tank(m,x,.25,.59,1.6,(74,125,88))
        m.box((0,-.8,.71),(1.5,1.8,.85),STEEL,.16)
        fan(m,0,-.7,1.17,.57,t)
        hose(m,[(-1.1,.2,2.15),(-1.1,-.8,2.15),(1.1,-.8,2.15),(1.1,.2,2.15)],.12,COPPER)
        cabinet(m,1.6,-1.45,.75,1.0)
    elif name=='heat-recovery-turbine':
        m.tube((0,-1.4,1.2),(0,1.4,1.2),.84,STEEL,36)
        for y in (-1.4,-.7,0,.7,1.4):m.tube((0,y-.04,1.2),(0,y+.04,1.2),.9,EDGE,28)
        m.box((1.28,0,.74),(.63,3.4,.71),DARK,.12)
        for i in range(8):m.box((1.28,-1.36+i*.39,1.12),(.73,.10,.07),COPPER,.03)
        m.cyl(-1.3,.6,.3,.30,1.27,STEEL,20)
    elif name=='photonic-canopy':
        for x in (-3.25,0,3.25):
            for y in (-2.9,0,2.9):
                for side in (-1,1):m.tube((x+side*.9,y,.25),(x+side*.9,y,1.70),.04,EDGE,10)
                solar(m,x,y,1.83,2.85,2.50,.22)
        for y in (-3.5,3.5):m.tube((-3.9,y,.31),(3.9,y,.31),.075,COPPER,12)
        cabinet(m,3.75,3.5,.81,1.2)
    elif name=='planetary-thermal-tap':
        m.cyl(0,0,.30,1.20,.50,DARK,40)
        m.cyl(0,0,.80,.58,3.7,STEEL,28)
        for x,y in ((-1.35,-1.35),(1.35,-1.35),(1.35,1.35),(-1.35,1.35)):
            m.tube((x,y,.35),(x*.32,y*.32,4.55),.10,EDGE,14)
            for z in (1.2,2.1,3.0):m.tube((x*(1-z/6),y*(1-z/6),z),(0,0,z+.5),.048,COPPER,10)
        m.ring((0,0,4.4),.8,.07,COPPER)
        for x in (-3.0,3.0):
            for y in (-1.4,1.4):
                m.box((x,y,.73),(1.38,2.05,.90),STEEL,.18);fan(m,x,y,1.20,.57,t)
            hose(m,[(x,-2.7,.6),(x,-2.7,1.4),(0,-2.7,1.4),(0,0,1.4)],.18,COPPER)
    elif name=='combined-cycle':
        for x in (-2,0,2):
            m.tube((x,-1.9,1.0),(x,1.1,1.0),.60,STEEL,28)
            for y in (-1.8,-.9,0,.9):m.tube((x,y-.04,1.0),(x,y+.04,1.0),.66,EDGE,24)
        m.box((0,2.17,1.15),(5.9,1.25,1.7),DARK,.20)
        for x in (-2.2,0,2.2):m.cyl(x,2.17,2.0,.32,1.6,STEEL,24)
        for i in range(12):m.box((-2.64+i*.48,1.46,1.22),(.18,.12,1.28),COPPER,.03)
    elif name=='biofuel-cell':
        for x in (-1.9,-.65,.65,1.9):
            m.box((x,0,1.02),(.70,3.9,1.45),(68,103,85),.13)
            for y in (-1.4,-.7,0,.7,1.4):m.box((x,y,1.77),(.80,.12,.06),EDGE,.02)
            m.box((x,-2.0,1.25),(.40,.04,.065),TEAL,.01)
        for y in (-2.35,2.35):m.tube((-2.3,y,.68),(2.3,y,.68),.12,COPPER,16)
    elif name=='salt-reactor':
        m.cyl(0,0,.28,1.3,.45,STEEL,40)
        m.ball((0,0,1.0),1.27,(113,126,103),stretch=(1,1,.78))
        m.ring((0,0,1.35),1.21,.09,EDGE)
        for i in range(6):
            a=i*TAU/6;x,y=.78*math.cos(a),.78*math.sin(a)
            m.cyl(x,y,1.52,.12,.67,STEEL,16);m.ball((x,y,2.20),.07,TEAL,glow=True)
        for side in (-1,1):
            for offset in (-1,0,1):
                m.tube((side*2.4,offset,.18),(side*1.1,offset,.45),.13,COPPER,12)
                m.tube((offset,side*2.4,.18),(offset,side*1.1,.45),.13,COPPER,12)
    elif name=='plasma-generator':
        # Native fusion converter: retain its narrow 3 x 5 hookup layout.
        m.box((0,0,.55),(2.40,4.4,.58),DARK,.15)
        for y in (-1.30,-.45,.45,1.30):
            m.ring((0,y,1.25),.67,.09,COPPER)
            m.ball((0,y,1.20),.46,(100,83,156),stretch=(1,.7,1),glow=True)
            for x in (-.83,.83):m.tube((x,y,.5),(x,y,1.68),.12,EDGE,12)
        for y in (-1.0,0):
            for side in (-1,1):hose(m,[(side*.8,y,1),(side*1.5,y,0)],.09,COPPER)
        for x in (-1,1):
            hose(m,[(x,1.6,.65),(x,2.5,0)],.10,COPPER)
            hose(m,[(x,-1.6,.65),(x,-2.5,0)],.10,TEAL)
        hose(m,[(0,-1.8,.65),(0,-2.5,0)],.09,COPPER)
    else:raise KeyError(name)
    return m


def fluid_nozzles(m,size):
    m.port_anchors=[]
    for side in (-1,1):
        tip=(0,side*size/2,0)
        m.tube((0,side*(size/2-.38),.49),(0,side*(size/2-.08),.26),.115,EDGE,16)
        m.tube((0,side*(size/2-.08),.26),tip,.11,COPPER,16)
        m.port_anchors.append(tip)
    return m
