"""Original orthographic mesh renderer for the Ironbound expedition art.
No imported models, textures, game sprites or GPU dependencies. Models are authored
as riveted solids; Pillow rasterizes sorted, lit polygons with antialiased shadows.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

TAU = math.tau
STEEL=(65,79,85); DARK=(27,35,39); EDGE=(121,140,146); GOLD=(212,146,54)
COPPER=(163,94,53); WHITE=(185,192,184); GREEN=(99,177,102); TEAL=(47,170,173)
BLUE=(49,117,164); RED=(173,73,49); VIOLET=(149,100,166)

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,s): return tuple(x*s for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a): return mul(a,1/max(1e-9,math.sqrt(dot(a,a))))
def rot(p,a): return (p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a),p[2])
def color(c,f): return tuple(max(0,min(255,round(x*f))) for x in c[:3])

class Mesh:
    def __init__(self): self.faces=[]
    def face(self,verts,c,glow=False): self.faces.append((list(verts),c,glow))
    def join(self,other,angle=0,offset=(0,0,0)):
        self.faces.extend(([add(rot(p,angle),offset) for p in v],c,g) for v,c,g in other.faces)
    def box(self,center,size,c=STEEL,bevel=.05):
        x,y,z=center;w,d,h=(v/2 for v in size);b=min(bevel,w*.4,d*.4)
        ring=[(-w+b,-d),(w-b,-d),(w,-d+b),(w,d-b),(w-b,d),(-w+b,d),(-w,d-b),(-w,-d+b)]
        low=[(x+a,y+v,z-h) for a,v in ring];high=[(x+a,y+v,z+h) for a,v in ring]
        self.face(high,c);self.face(list(reversed(low)),color(c,.65))
        for i in range(8):self.face([low[i],low[(i+1)%8],high[(i+1)%8],high[i]],c)
        inset=[(x+a*.96,y+v*.96,z+h+.025) for a,v in ring]
        self.face(inset,color(c,1.08))
    def tube(self,a,b,r,c=EDGE,sides=12):
        axis=norm(sub(b,a));u=norm(cross(axis,(0,0,1) if abs(axis[2])<.9 else (0,1,0)));v=cross(axis,u)
        def ring(p):return [add(p,add(mul(u,r*math.cos(i*TAU/sides)),mul(v,r*math.sin(i*TAU/sides)))) for i in range(sides)]
        p,q=ring(a),ring(b)
        self.face(p,c);self.face(q,c)
        for i in range(sides):j=(i+1)%sides;self.face([p[i],p[j],q[j],q[i]],c)
    def cyl(self,x,y,z,r,h,c=STEEL,sides=16):self.tube((x,y,z),(x,y,z+h),r,c,sides)
    def ball(self,p,r,c=TEAL,stretch=(1,1,1),glow=False):
        rows,cols=6,12
        grid=[]
        for j in range(rows+1):
            lat=-math.pi/2+j*math.pi/rows
            grid.append([add(p,(r*stretch[0]*math.cos(lat)*math.cos(i*TAU/cols),r*stretch[1]*math.cos(lat)*math.sin(i*TAU/cols),r*stretch[2]*math.sin(lat))) for i in range(cols)])
        for j in range(rows):
            for i in range(cols):self.face([grid[j][i],grid[j][(i+1)%cols],grid[j+1][(i+1)%cols],grid[j+1][i]],c,glow)
    def ring(self,p,r,t,c=EDGE,angle=0):
        for i in range(20):
            a=i*TAU/20+angle;b=(i+1)*TAU/20+angle
            self.tube(add(p,(r*math.cos(a),r*math.sin(a),0)),add(p,(r*math.cos(b),r*math.sin(b),0)),t,c,6)
    def rivets(self,x,y,z,w,n=5):
        for i in range(n):self.cyl(x-w/2+i*w/(n-1),y,z,.034,.025,EDGE,6)
    def vent(self,x,y,z,w,d):
        self.box((x,y,z),(w,d,.07),DARK)
        for i in range(7):self.box((x-w*.4+i*w*.8/6,y,z+.045),(.026,d*.88,.035),EDGE,0)
    def leaf(self,p,a,size=1):
        v=[(-.02,0,0),(-.16,.18,.06),(0,.45,.13),(.16,.18,.06)]
        self.face([add(p,rot(mul(q,size),a)) for q in v],GREEN)
    def plant(self,x,y,z,scale=1):
        self.tube((x,y,z),(x,y,z+.6*scale),.023*scale,COPPER,6)
        for i in range(4):self.leaf((x,y,z+.1*scale+i*.12*scale),i*2.3,scale)


def platform(m,size=2.7):
    for x in (-size*.39,size*.39):
        for y in (-size*.39,size*.39):m.box((x,y,.12),(.42,.42,.24),DARK)
    m.box((0,0,.24),(size,size,.3),STEEL,.1)
    m.box((0,0,.42),(size-.12,size-.12,.1),DARK)
    for x in (-size*.46,size*.46):m.box((x,0,.36),(.09,size*.85,.14),EDGE,.01)
    for i in range(6):
        x=-size*.38+i*size*.14
        m.face([(x,-size/2-.005,.19),(x+.16,-size/2-.005,.19),(x+.27,-size/2-.005,.36),(x+.11,-size/2-.005,.36)],GOLD)
    m.rivets(0,size*.48,.41,size*.8,6)


def tank(m,x,y,r=.4,h=1.3,c=TEAL):
    m.cyl(x,y,.4,r+.06,.14,EDGE)
    m.cyl(x,y,.54,r,h,c)
    for z in (.57,.54+h*.46,.54+h):m.cyl(x,y,z,r+.035,.07,STEEL)
    m.ball((x,y,.54+h),r,STEEL,stretch=(1,1,.4))
    for a in (-math.pi/2,0):
        p=(x+math.cos(a)*(r+.022),y+math.sin(a)*(r+.022),.8)
        m.tube(p,add(p,(0,0,h*.48)),.025,WHITE,6)


def fan(m,x,y,z,r,t):
    m.cyl(x,y,z,r,.11,EDGE)
    m.cyl(x,y,z+.11,r*.87,.02,DARK)
    for i in range(5):
        a=i*TAU/5+t*TAU
        v=[(.10,0,.15),(r*.76,-r*.15,.16),(r*.67,r*.30,.19),(.1,.1,.15)]
        m.face([add((x,y,z),rot(q,a)) for q in v],STEEL)
    m.cyl(x,y,z+.15,r*.18,.06,COPPER)


def machine(name,t=0):
    m=Mesh();big=name in ('cryogenic-garden','planetary-beacon');platform(m,4.6 if big else (1 if name=='ecology-monitor' else 2.7))
    if name=='algae-vat':
        tank(m,-.65,.15,.46,1.35,GREEN);tank(m,.62,.2,.42,1.15,TEAL)
        for x in (-.65,.62):
            m.tube((x,.1,1.95),(x,-.8,1.95),.08,COPPER)
            for side in range(4):
                a=side*math.pi/2
                for i in range(2):m.ball((x+math.cos(a)*.475,.18+math.sin(a)*.475,.84+(t+i*.45)%1*.7),.036,WHITE,glow=True)
        m.box((0,-.9,.8),(.55,.4,.65),STEEL)
    elif name=='composter':
        m.box((0,0,.9),(1.9,1.85,.8),EDGE)
        m.box((0,0,1.32),(1.65,1.6,.04),DARK)
        for i in range(9):m.ball((-.65+i%3*.6,-.55+i//3*.5,1.38),.22,COPPER,stretch=(1,1,.5))
        m.tube((-.95,0,1.5),(.95,0,1.5),.11,STEEL)
        for i in range(4):m.box((-.7+i*.45,.32*math.sin(t*TAU),1.48+.2*math.cos(t*TAU)),(.12,.75,.12),GOLD)
        m.box((.92,-.5,1),(.32,.8,.5),DARK)
    elif name in ('hydroponics-bay','sanctuary','cryogenic-garden'):
        beds=3 if big else 2
        for j in range(beds):
            y=-1.15+j*1.0 if big else -.65+j*1.25
            m.box((0,y,.63),(3.6 if big else 2.1,.85,.38),WHITE if big else EDGE)
            m.box((0,y,.83),(3.35 if big else 1.9,.66,.05),(53,65,44))
            for i in range(6 if big else 4):m.plant((-1.45 if big else -.78)+i*.52,y,.87,.8)
        for x in ((-1.95,1.95) if big else (-1.13,1.13)):
            m.box((x,.0,1.15),(.13,3.65 if big else 2.15,1.4),STEEL)
        if name=='hydroponics-bay':
            for y in (-1.05,1.05):m.tube((-1.1,y,1.6),(1.1,y,1.6),.05,TEAL)
            m.box((.0,0,1.85),(2.1,.35,.12),EDGE)
            m.cyl(0,0,1.91,.14,.06,color(TEAL,1+.18*math.sin(t*TAU)))
        elif name=='sanctuary':
            for a in range(8):
                ang=a*TAU/8;m.tube((1.12*math.cos(ang),1.12*math.sin(ang),.5),(0,0,2.4),.045,EDGE)
            m.ball((0,0,2.3),.22,color(TEAL,1+.18*math.sin(t*TAU)),glow=True)
        else:
            for y in (-1.9,1.9):
                m.tube((-1.9,y,1.9),(1.9,y,1.9),.13,WHITE)
            for i in range(7):m.box((-1.4+i*.46,1.55,2.1),(.11,.6,.55),EDGE)
            fan(m,1.15,-1.4,1.9,.42,t)
    elif name=='electrolyzer':
        for x in (-.7,.7):
            for y in (-.7,.7):tank(m,x,y,.28,1.15,BLUE)
        m.box((0,0,1.7),(2,.16,.18),COPPER)
        for x in (-.7,.7):m.tube((x,-.7,1.8),(x,.7,1.8),.04,TEAL)
        fan(m,0,-.8,.5,.24,t)
    elif name=='reclamation-plant':
        for x,y,h in ((-.7,.45,1.25),(.15,.45,1.75),(.75,-.5,.85)):
            tank(m,x,y,.31,h,EDGE)
            for z in range(4):m.ring((x,y,.75+z*.22),.34,.034,COPPER)
        m.box((-.55,-.65,.65),(.85,.7,.42),BLUE);fan(m,-.55,-.65,.89,.28,t)
    elif name in ('materials-kiln','pyrolyzer','forcing-tower'):
        h=1.6 if name=='forcing-tower' else 1.0
        m.box((0,0,.5+h/2),(1.8,1.7,h),STEEL if name=='materials-kiln' else DARK,.13)
        m.box((0,-.9,.85),(1.0,.08,.56),EDGE)
        m.box((0,-.955,.85),(.8,.045,.36),color(RED,1+.2*math.sin(t*TAU)))
        for i in range(5):m.box((-.33+i*.17,-.99,.85),(.035,.02,.35),DARK,0)
        m.cyl(.62,.5,h+.5,.25,.7 if name!='forcing-tower' else 1.0,DARK)
        m.ring((.62,.5,h+1.1),.3,.06,EDGE)
        for i in range(4):m.box((-.8+i*.24,.8,.65+h/2),(.1,.2,h*.8),COPPER)
        fan(m,-.45,-.05,h+.52,.38,t)
    elif name=='air-scrubber':
        for x in (-.66,.66):
            m.box((x,.2,1),(.95,1.7,1.15),STEEL)
            fan(m,x,.2,1.61,.42,t)
            for j in range(5):m.box((x,-.67,.7+j*.15),(.74,.05,.052),EDGE,0)
        m.box((0,1.05,.8),(1.8,.3,.45),COPPER)
    elif name=='soil-enricher':
        tank(m,.72,.5,.37,.8,GREEN)
        m.box((-.36,-.2,.72),(1.18,1.7,.5),EDGE)
        m.box((-.36,-.2,.99),(1.0,1.45,.04),COPPER)
        for i in range(5):
            z=1.08+.08*math.sin(t*TAU+i)
            m.box((-.35,-.7+i*.27,z),(.86,.12,.12),DARK)
        m.tube((.72,.5,1.4),(.72,-.8,1.4),.1,TEAL)
        m.box((-.6,1.0,.78),(.65,.3,.5),STEEL)
    elif name=='seed-disperser':
        for x,y in ((-.8,-.65),(.8,-.65),(-.8,.65),(.8,.65)):tank(m,x,y,.26,.6,GOLD)
        m.cyl(0,0,.5,.22,1.6,STEEL)
        q=Mesh();q.box((0,0,2.1),(2.2,.22,.16),EDGE);q.box((0,0,2.1),(.22,2.2,.16),EDGE)
        m.join(q,t*TAU)
        m.ball((0,0,2.16),.17,GREEN,glow=True)
    elif name=='watershed':
        m.cyl(0,0,.45,1.04,.8,EDGE)
        m.cyl(0,0,1.26,.91,.025,BLUE)
        m.ring((0,0,1.28),1.04,.08,STEEL)
        q=Mesh();q.box((0,0,1.34),(1.9,.10,.06),WHITE);m.join(q,t*TAU)
        m.box((1.05,.3,.8),(.35,.8,.5),STEEL)
        m.tube((-.95,0,.7),(-1.2,0,.7),.16,BLUE)
    elif name=='thermal-exchanger':
        for j in range(6):m.box((-.8+j*.32,.35,1.4),(.11,1.65,1.8),EDGE)
        for z in (.62,2.26):m.tube((-.95,-.5,z),(.95,-.5,z),.10,COPPER)
        for x in (-.62,.62):fan(m,x,-.65,.56,.43,t)
    elif name=='detoxifier':
        for x,y,h in ((-.65,.35,1.4),(.65,.35,1.4),(0,-.7,.8)):tank(m,x,y,.31,h,VIOLET)
        for x in (-.65,.65):m.box((x,-.04,1.6),(.2,.06,.15),GOLD)
        m.cyl(0,.6,.7,.11,1.6,STEEL)
        m.ball((0,.6,2.3),.09,color(TEAL,1+.3*math.sin(t*TAU)),glow=True)
    elif name=='pheromone-dampener':
        m.cyl(0,0,.4,.54,.4,STEEL);m.cyl(0,0,.8,.14,1.6,EDGE)
        for z,r in ((1.1,.6),(1.6,.75),(2.15,.44)):
            m.cyl(0,0,z,r,.08,STEEL)
            m.ring((0,0,z+.1),r*.85,.03,color(TEAL,1+.2*math.sin(t*TAU)))
    elif name=='basalt-conditioner':
        m.box((0,.15,.82),(1.95,1.9,.75),DARK)
        for i in range(7):
            m.box((-.7+i*.23,-.1,1.24+.08*math.sin(t*TAU+i)),(.12,1.1,.2),EDGE)
        for x in (-.95,.95):m.box((x,.45,1.55),(.24,1.15,.6),GOLD)
        for i in range(6):m.ball((-.6+(i%3)*.55,.65+(i//3)*.2,1.6),.19,STEEL)
        m.tube((.0,-.8,.8),(.0,-1.2,.8),.22,COPPER)
    elif name=='fulgoran-reclaimer':
        for x in (-.72,.72):
            m.box((x,-.2,.85),(.88,1.8,.8),COPPER)
            m.box((x,-.2,1.26),(.73,1.55,.03),DARK)
            for i in range(6):m.box((x+(.12 if i%2 else -.16),-.75+(i//2)*.45,1.34),(.27,.24,.13),EDGE)
        m.cyl(0,.65,.45,.15,1.65,STEEL)
        q=Mesh();q.box((.45,0,2.1),(1.1,.22,.12),GOLD);q.cyl(.87,0,1.82,.22,.21,TEAL);m.join(q,t*TAU)
    elif name=='spore-tower':
        for x,y in ((-.65,-.6),(.65,-.6),(0,.6)):tank(m,x,y,.29,1.45,GREEN)
        m.cyl(0,0,.5,.16,1.9,STEEL)
        m.ball((0,0,2.45),.38,GOLD,stretch=(1,1,.5))
        for i in range(6):m.ball((.4*math.cos(i+t*TAU),.4*math.sin(i+t*TAU),2.4+.12*math.sin(t*TAU+i)),.052,GREEN,glow=True)
    elif name=='planetary-beacon':
        for x in (-1.6,1.6):
            for y in (-1.6,1.6):m.box((x,y,1.1),(.48,.48,1.8),EDGE)
        m.cyl(0,0,.45,.75,.75,STEEL)
        m.ball((0,0,2.0),.7,color(TEAL,1+.15*math.sin(t*TAU)),glow=True)
        m.ring((0,0,2.0),1.25,.09,COPPER,t*TAU)
        q=Mesh();q.tube((-1.2,0,2),(1.2,0,2),.08,WHITE);m.join(q,t*TAU)
        for y in (-1.7,1.7):m.box((0,y,2.5),(.18,.18,1.3),STEEL)
    elif name=='ecology-monitor':
        m.box((0,0,.65),(.84,.72,.58),STEEL)
        m.box((0,-.385,.72),(.64,.035,.36),DARK,0)
        for i in range(5):m.box((-.23+i*.115,-.413,.6+(.12+.10*math.sin(t*TAU+i))/2),(.045,.01,.12+.10*math.sin(t*TAU+i)),TEAL,0)
        m.cyl(.27,.12,.92,.034,.34,EDGE,6)
    return m


def lander(t=0):
    m=Mesh()
    for x in (-3.4,3.4):
        for y in (-1.75,1.65):
            m.box((x,y,.12),(1,.8,.24),DARK)
            m.tube((x,y,.28),(x*.82,y*.84,1.18),.16,EDGE)
    m.box((0,0,1.35),(5.5,5.5,1.45),STEEL,.5)
    m.box((0,-1.65,2.13),(3.3,1.8,.62),EDGE,.3)
    m.box((0,-2.1,2.46),(2.7,.9,.08),(24,61,77),.2)
    m.box((0,-2.55,1.63),(3.6,.4,.72),DARK,.15)
    m.box((0,-.1,2.2),(2.65,1.7,.35),GOLD,.16)
    m.box((0,-.1,2.385),(1.7,1.0,.025),STEEL,.06)
    for x in (-1.12,1.12):m.rivets(x,-.72,2.41,.22,3)
    for y in (-.6,.4):
        m.tube((-1.95,y,2.2),(-1.95,y+.4,2.2),.06,COPPER)
        m.tube((1.95,y,2.2),(1.95,y+.4,2.2),.06,COPPER)
    for x in (-1.6,1.6):
        m.box((x,1.35,2.15),(1.1,1.55,.28),DARK)
        m.vent(x,1.35,2.31,.9,1.25)
    for x in (-3.6,3.6):
        m.box((x,.2,1.15),(2.2,4.7,.45),DARK,.25)
        m.box((x,.15,1.55),(1.35,3.25,.85),STEEL,.3)
        m.cyl(x,1.55,.88,.52,.9,EDGE)
        m.cyl(x,1.55,1.8,.43,.03,DARK)
        fan(m,x,1.25,2.13,.38,t)
        m.box((x,-1.8,1.47),(.95,.15,.21),GOLD)
        m.box((x,-1.9,1.47),(.36,.02,.10),color(TEAL,1+.2*math.sin(t*TAU)))
    m.box((0,2.88,1.08),(2.2,.16,.95),DARK)
    for j in range(4):m.box((0,2.99,.75+j*.16),(2.04,.14,.055),EDGE,0)
    for x in (-2.5,2.5):m.rivets(x,2.75,1.96,.3,3)
    m.tube((1.7,.5,2.2),(1.7,.5,3.4),.04,EDGE,8)
    m.ball((1.7,.5,3.44),.075,TEAL,glow=True)
    return m


def turret(kind,t=0,angle=0,base=True):
    m=Mesh();big=kind=='lance-turret';s=3.7 if big else 1.9
    if base:
        platform(m,s)
        m.cyl(0,0,.4,s*.37,.26,DARK)
        m.ring((0,0,.69),s*.33,.06,COPPER)
    q=Mesh();recoil=.12*math.sin(t*TAU)
    q.box((0,0,1.04),(1.35 if big else .9,1.5 if big else .8,.6),STEEL,.12)
    if kind=='sentry-turret':
        for x in (-.21,.21):
            q.tube((x,.0,1.17),(x,-1.25+recoil,1.17),.10,DARK)
            for y in (-.9,-.7,-.5):q.tube((x,y,1.17),(x,y+.07,1.17),.14,EDGE)
        q.box((.57,.1,1.0),(.35,.54,.42),GOLD)
    elif kind=='arc-turret':
        q.cyl(0,0,1.35,.14,.9,EDGE)
        for z,r in ((1.45,.37),(1.7,.3),(1.95,.22)):
            q.ring((0,0,z),r,.065,COPPER)
        q.ball((0,0,2.25),.25,color(TEAL,1+.25*math.sin(t*TAU)),glow=True)
        q.tube((-.42,-.1,1.22),(-.42,-.7,1.7),.07,EDGE)
        q.tube((.42,-.1,1.22),(.42,-.7,1.7),.07,EDGE)
    else:
        for x in (-.32,.32):
            q.box((x,-1.15+recoil,1.3),(.25,2.6,.32),DARK)
            q.box((x,-1.15+recoil,1.48),(.13,2.4,.08),TEAL)
            for i in range(7):q.box((x,-2.2+i*.35+recoil,1.27),(.42,.12,.53),EDGE)
        q.box((0,.76,1.12),(1.1,.6,.65),GOLD)
    m.join(q,angle);return m


def wall(mask=0,advanced=False):
    m=Mesh();c=EDGE if advanced else STEEL
    m.box((0,0,.15),(.95,.88,.28),DARK)
    m.box((0,0,.65),(.64,.55,.94),c)
    for bit,(x,y) in enumerate(((0,-.5),(.5,0),(0,.5),(-.5,0))):
        if mask&(1<<bit):m.box((x*.65,y*.65,.63),(.65 if x else .43,.65 if y else .43,.88),c)
    m.box((0,0,1.15),(.72,.62,.13),GOLD if not advanced else TEAL)
    for x in (-.20,.2):m.box((x,.295,.73),(.08,.025,.36),DARK,0)
    return m


def equipment(kind):
    m=Mesh()
    if kind=='field-pole':
        m.box((0,0,.12),(.6,.6,.2),DARK)
        for x in (-.16,.16):m.tube((x,0,.15),(x*.3,0,2.7),.06,STEEL,8)
        for z in (.5,1,1.5,2):m.tube((-.14,0,z),(.14,0,z+.45),.032,EDGE,6)
        m.box((0,0,2.65),(1.3,.16,.12),EDGE)
        for x in (-.53,0,.53):m.cyl(x,0,2.72,.09,.18,WHITE,8)
    elif kind=='field-crate':
        m.box((0,0,.42),(.9,.9,.8),STEEL)
        m.box((0,0,.86),(.98,.98,.1),EDGE)
        for x in (-.4,.4):m.box((x,0,.46),(.08,1,.78),GOLD)
        m.box((0,-.52,.55),(.23,.05,.2),DARK)
    else:
        m.box((0,0,.2),(.9,.65,.32),STEEL)
        m.cyl(0,0,.38,.24,.07,TEAL)
    return m


def explorer(t=0,pose='idle',tier=0,move_angle=0,aim_offset=0):
    m=Mesh();run=pose in ('running','running_with_gun');gun='gun' in pose
    stride=.32*math.sin(t*TAU) if run else .018*math.sin(t*TAU)
    bob=.025*abs(math.sin(t*TAU)) if run else .012*math.sin(t*TAU)
    suit=(37,45,52);armor=STEEL if tier<2 else (97,111,119)
    for side in (-1,1):
        hip=(side*.145,0,1.0+bob);knee=(side*.17,side*stride*.50,.58+bob)
        foot=(side*.17,side*stride,.10+max(0,-side*stride)*.25)
        m.tube(hip,knee,.12,suit);m.tube(knee,foot,.087,suit)
        m.ball(knee,.115,armor,stretch=(.9,1,1.05))
        m.box(add(foot,(0,-.065,0)),(.20,.34,.20),DARK,.06)
        m.tube(add(knee,(0,.035,-.08)),add(foot,(0,.035,.11)),.075,armor)
    # Fitted, fully covered adult expedition suit; shaped torso with layered armor.
    m.ball((0,0,1.06+bob),.25,suit,stretch=(1,.62,.65))
    m.ball((0,0,1.25+bob),.22,suit,stretch=(.74,.65,.95))
    m.ball((0,-.005,1.48+bob),.27,suit,stretch=(.97,.66,.88))
    m.box((0,-.14,1.48+bob),(.37,.12,.35),armor,.06)
    m.box((0,-.211,1.50+bob),(.07,.014,.27),GOLD,.015)
    m.box((0,0,1.13+bob),(.39,.32,.12),COPPER,.04)
    m.box((.18,-.12,1.10+bob),(.13,.13,.21),DARK)
    m.box((0,.22,1.39+bob),(.32,.18,.47),STEEL)
    for x in (-.11,.11):m.cyl(x,.23,1.48+bob,.065,.2,TEAL,8)
    for side in (-1,1):
        shoulder=(side*.29,0,1.59+bob)
        if pose=='mining_with_tool':
            reach=.45+.25*math.sin(t*TAU);elbow=(side*.32,-.22,1.35+bob+reach*.3);hand=(side*.13,-.42,1.1+bob+reach)
        elif gun:
            elbow=(side*.33,-.12,1.30+bob);hand=(side*.14,-.42,1.38+bob)
        else:
            elbow=(side*.32,-side*stride*.7,1.22+bob);hand=(side*.31,-side*stride,1.02+bob)
        m.ball(shoulder,.14,armor,stretch=(1.05,1,1))
        m.tube(shoulder,elbow,.081,suit);m.tube(elbow,hand,.073,suit);m.ball(hand,.083,DARK)
        if tier>0:m.box((side*.32,0,1.59+bob),(.2,.29,.17),EDGE)
    m.tube((0,0,1.66+bob),(0,0,1.77+bob),.095,suit)
    skin=(187,135,109)
    m.ball((0,-.015,1.91+bob),.19,skin,stretch=(.85,.9,1.13))
    # Copper-dark hair, ponytail, helmet crown and an open face / visor frame.
    m.ball((0,.075,1.95+bob),.19,(73,44,33),stretch=(.92,.68,1.10))
    m.tube((0,.20,1.93+bob),(.045,.30,1.64+bob),.07,(73,44,33),8)
    m.box((0,-.12,2.047+bob),(.30,.12,.065),armor)
    m.box((0,-.177,1.956+bob),(.26,.025,.055),TEAL,.01)
    for x in (-.17,.17):m.ball((x,0,1.925+bob),.06,EDGE)
    if tier==2:
        m.box((0,-.145,1.83+bob),(.27,.075,.1),DARK)
        for x in (-.30,.30):m.box((x,.14,1.58+bob),(.22,.28,.27),GOLD)
    if gun:
        g=Mesh();g.box((0,-.51,1.4+bob),(.18,.72,.15),DARK)
        g.box((0,-.48,1.50+bob),(.08,.44,.06),EDGE)
        g.tube((0,-.62,1.4+bob),(0,-.99,1.4+bob),.035,STEEL,8)
        g.box((0,-.37,1.25+bob),(.11,.16,.22),COPPER)
        m.join(g,aim_offset)
    if pose=='mining_with_tool':
        h=1.2+.45*(.5+.5*math.sin(t*TAU))
        m.tube((0,-.46,h),(0,-.68,h+.55),.034,EDGE,8)
        m.box((0,-.68,h+.53),(.59,.12,.12),STEEL)
    result=Mesh();result.join(m,move_angle);return result


def render(mesh,width=320,height=None,ppu=64,angle=0,aa=2,origin=.70):
    import numpy as np
    height=height or width;w,h=width*aa,height*aa
    out=Image.new('RGBA',(w,h));shadow=Image.new('RGBA',(w,h))
    sd=ImageDraw.Draw(shadow)
    elev=math.radians(48);view=(0,math.cos(elev),math.sin(elev));light=norm((-.6,-.8,1.1))
    halfway=norm(add(view,light))
    def project(p):return (w/2+p[0]*ppu*aa,h*origin+(p[1]*math.sin(elev)-p[2]*math.cos(elev))*ppu*aa,dot(p,view))
    faces=[([rot(p,angle) for p in v],c,g) for v,c,g in mesh.faces]
    for v,c,g in faces:
        points=[project((p[0]+p[2]*.42,p[1]+p[2]*.58,.015))[:2] for p in v]
        sd.polygon(points,fill=(10,15,19,70))
    pixels=np.zeros((h,w,4),dtype=np.uint8);zbuf=np.full((h,w),-1e20,dtype=np.float32)
    for vertices,c,glow in faces:
        n=norm(cross(sub(vertices[1],vertices[0]),sub(vertices[2],vertices[0])))
        if dot(n,view)<0:n=mul(n,-1)
        specular=max(0,dot(n,halfway))**24*.23
        shade=1 if glow else .43+.61*max(0,dot(n,light))+.09*max(0,n[2])+specular
        base=np.array(color(c,shade),dtype=float)
        projected=[project(p) for p in vertices]
        for i in range(1,len(vertices)-1):
            pa,pb,pc=projected[0],projected[i],projected[i+1]
            xmin=max(0,int(math.floor(min(pa[0],pb[0],pc[0]))));xmax=min(w-1,int(math.ceil(max(pa[0],pb[0],pc[0]))))
            ymin=max(0,int(math.floor(min(pa[1],pb[1],pc[1]))));ymax=min(h-1,int(math.ceil(max(pa[1],pb[1],pc[1]))))
            if xmin>xmax or ymin>ymax:continue
            den=(pb[1]-pc[1])*(pa[0]-pc[0])+(pc[0]-pb[0])*(pa[1]-pc[1])
            if abs(den)<1e-7:continue
            yy,xx=np.ogrid[ymin:ymax+1,xmin:xmax+1];xx=xx+.5;yy=yy+.5
            a=((pb[1]-pc[1])*(xx-pc[0])+(pc[0]-pb[0])*(yy-pc[1]))/den
            b=((pc[1]-pa[1])*(xx-pc[0])+(pa[0]-pc[0])*(yy-pc[1]))/den
            cc=1-a-b;depth=a*pa[2]+b*pb[2]+cc*pc[2]
            old=zbuf[ymin:ymax+1,xmin:xmax+1]
            mask=(a>=-1e-5)&(b>=-1e-5)&(cc>=-1e-5)&(depth>=old-1e-6)
            if not mask.any():continue
            old[mask]=depth[mask]
            # Surface-anchored fine grain gives metal some wear without frame flicker.
            va,vb,vc=vertices[0],vertices[i],vertices[i+1]
            u=a*dot(va,(61,29,43))+b*dot(vb,(61,29,43))+cc*dot(vc,(61,29,43))
            grain=1+(np.sin(u*5.1)*np.sin(u*2.73))*(0 if glow else .036)
            rgb=np.clip(grain[...,None]*base,0,255).astype(np.uint8)
            region=pixels[ymin:ymax+1,xmin:xmax+1];region[mask,:3]=rgb[mask];region[mask,3]=255
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(2.1*aa)))
    out.alpha_composite(Image.fromarray(pixels,'RGBA'))
    return out.resize((width,height),Image.Resampling.LANCZOS)
