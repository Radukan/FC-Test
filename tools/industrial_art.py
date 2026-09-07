"""Original orthographic mesh renderer for the Ironbound expedition art.
No imported models, textures, game sprites or GPU dependencies. Models are authored
as riveted solids; Pillow rasterizes sorted, lit polygons with antialiased shadows.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

TAU = math.tau
STEEL=(92,94,79); DARK=(34,37,31); EDGE=(151,147,124); GOLD=(189,139,57)
COPPER=(153,96,55); WHITE=(181,179,152); GREEN=(89,138,72); TEAL=(55,142,139)
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
        b=min(max(b,min(w,d)*.24),min(w,d)*.82)
        ring=[]
        for cx,cy,start in ((w-b,d-b,0),(-w+b,d-b,90),(-w+b,-d+b,180),(w-b,-d+b,270)):
            for i in range(5):
                a=math.radians(start+i*90/4);ring.append((cx+b*math.cos(a),cy+b*math.sin(a)))
        zbevel=min(b,h*.35)
        rings=[[(x+a*.96,y+v*.96,z-h) for a,v in ring],
               [(x+a,y+v,z-h+zbevel) for a,v in ring],
               [(x+a,y+v,z+h-zbevel) for a,v in ring],
               [(x+a*.96,y+v*.96,z+h) for a,v in ring]]
        self.face(rings[-1],c);self.face(list(reversed(rings[0])),color(c,.7))
        for low,high in zip(rings,rings[1:]):
            for i in range(len(ring)):self.face([low[i],low[(i+1)%len(ring)],high[(i+1)%len(ring)],high[i]],c)
    def tube(self,a,b,r,c=EDGE,sides=12):
        if r<.035:sides=min(sides,8)
        axis=norm(sub(b,a));u=norm(cross(axis,(0,0,1) if abs(axis[2])<.9 else (0,1,0)));v=cross(axis,u)
        def ring(p):return [add(p,add(mul(u,r*math.cos(i*TAU/sides)),mul(v,r*math.sin(i*TAU/sides)))) for i in range(sides)]
        p,q=ring(a),ring(b)
        self.face(p,c);self.face(q,c)
        for i in range(sides):j=(i+1)%sides;self.face([p[i],p[j],q[j],q[i]],c)
    def cyl(self,x,y,z,r,h,c=STEEL,sides=16):self.tube((x,y,z),(x,y,z+h),r,c,sides)
    def ball(self,p,r,c=TEAL,stretch=(1,1,1),glow=False):
        rows,cols=(4,8) if r<.05 else ((6,12) if r<.11 else (9,18))
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


def hose(m,points,r=.035,c=DARK):
    for a,b in zip(points,points[1:]):m.tube(a,b,r,c,10)
def gauge(m,x,y,z,r=.12,t=0):
    m.tube((x,y,z),(x,y+.045,z),r,EDGE,20)
    m.tube((x,y+.046,z),(x,y+.054,z),r*.81,WHITE,20)
    angle=-.5+t*.8
    m.tube((x,y+.065,z),(x+math.sin(angle)*r*.67,y+.065,z+math.cos(angle)*r*.67),.008,DARK,6)
    for i in range(5):
        a=-1+i*.5;m.tube((x+math.sin(a)*r*.63,y+.06,z+math.cos(a)*r*.63),(x+math.sin(a)*r*.73,y+.06,z+math.cos(a)*r*.73),.005,DARK,4)
def handwheel(m,x,y,z,r=.15,angle=0):
    m.tube((x,y,z),(x,y+.05,z),r,DARK,18)
    for i in range(4):
        a=angle+i*math.pi/2
        m.tube((x,y+.07,z),(x+math.sin(a)*r,y+.07,z+math.cos(a)*r),.022,COPPER,8)
    m.ball((x,y+.09,z),.037,EDGE)
def cabinet(m,x,y,z,scale=1,t=0):
    m.box((x,y,z),(.42*scale,.29*scale,.63*scale),STEEL,.035)
    m.box((x,y+.15*scale,z),(.35*scale,.025,.54*scale),DARK,.02)
    gauge(m,x,y+.18*scale,z+.13*scale,.10*scale,t)
    for i in range(4):m.box((x,y+.185*scale,z-.03*scale-i*.055*scale),(.26*scale,.018,.016),EDGE,.002)
    m.box((x+.11*scale,y+.20*scale,z-.18*scale),(.045,.025,.05),GOLD,.005)
def detailing(m,name,t):
    if name=='ecology-monitor':return
    size=4.6 if name in ('cryogenic-garden','planetary-beacon') else 2.7
    p=size*.43
    # Utility skid: conduits, flanges, pressure instrumentation and replaceable filters.
    hose(m,[(-p,-p,.50),(-p,-p*.4,.50),(-p,p*.55,.5),(-p*.70,p*.78,.66)],.033)
    hose(m,[(p,-p,.53),(p,p*.7,.53),(p*.75,p,.53)],.04,EDGE)
    cabinet(m,-p*.65,p*.88,.79,.8,.4+.18*math.sin(t*TAU))
    if name in ('air-scrubber','thermal-exchanger'):
        for x in (-.9,.9):
            m.box((x,.78,.87),(.12,.52,.7),EDGE,.018)
            for i in range(4):m.box((x,.81,.62+i*.12),(.17,.58,.025),STEEL,.005)
    elif name in ('materials-kiln','pyrolyzer','forcing-tower'):
        for z in (.62,.84,1.06):
            m.box((0,.868,z),(1.65,.025,.018),DARK,.003)
        m.box((0,.90,.84),(.63,.10,.44),EDGE,.04)
        m.box((0,.961,.84),(.43,.035,.27),(109,56,25),.02)
        handwheel(m,.45,.93,1.00,.14,t*.08)
        hose(m,[(-.86,-.3,.6),(-.92,-.3,1.65),(-.4,-.3,1.65)],.06,COPPER)
    elif name in ('algae-vat','spore-tower','detoxifier','reclamation-plant','electrolyzer'):
        hose(m,[(-.65,.8,.55),(-.65,.85,1.5),(.60,.85,1.5),(.60,.85,.6)],.045,EDGE)
        gauge(m,.42,1.0,1.16,.10,t*.2)
        handwheel(m,.78,.94,.65,.13,t*.1)
    elif name in ('composter','soil-enricher','basalt-conditioner','fulgoran-reclaimer'):
        for i in range(5):m.box((-.7+i*.32,1.0,.64),(.12,.38,.12),EDGE,.012)
        m.cyl(.8,-.75,.46,.24,.42,STEEL)
        m.ring((.8,-.75,.8),.25,.025,COPPER)
    elif name in ('hydroponics-bay','sanctuary','cryogenic-garden'):
        for x in (-p,p):
            hose(m,[(x,-p,.7),(x,-p,1.6),(x,p,1.6)],.025,COPPER)
        for i in range(7):m.box((-.75+i*.25,-p,.75),(.12,.23,.06),WHITE,.01)
    return m


def platform(m,size=2.7):
    for x in (-size*.39,size*.39):
        for y in (-size*.39,size*.39):m.box((x,y,.12),(.42,.42,.24),DARK)
    m.box((0,0,.24),(size,size,.3),STEEL,.1)
    m.box((0,0,.42),(size-.12,size-.12,.1),DARK)
    for x in (-size*.46,size*.46):m.box((x,0,.36),(.09,size*.85,.14),EDGE,.01)
    for i in range(6):
        x=-size*.38+i*size*.14
        m.face([(x,-size/2-.005,.19),(x+.16,-size/2-.005,.19),(x+.27,-size/2-.005,.36),(x+.11,-size/2-.005,.36)],GOLD)
    m.rivets(0,size*.48,.41,size*.8,8)
    for side in (-1,1):
        for i in range(9):m.box((side*size*.44,-size*.38+i*size*.095,.487),(.15,.032,.018),EDGE,.003)
        for corner in (-1,1):
            x=side*size*.38;y=corner*size*.38
            m.cyl(x,y,.43,.066,.052,EDGE,6)
            m.cyl(x,y,.485,.026,.012,DARK,8)


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


_PORTS=None
def fluid_ports(m,name):
    global _PORTS
    if _PORTS is None:
        from lupa.lua52 import LuaRuntime
        from catalog import MOD,plain
        runtime=LuaRuntime(unpack_returned_tuples=True);runtime.globals().package.path=str(MOD/'?.lua')+';'+runtime.globals().package.path
        _PORTS=plain(runtime.eval('require("shared.fluid_ports")'))
    m.port_anchors=[]
    for port in _PORTS.get(name,[]):
        dx,dy={0:(0,-1),4:(1,0),8:(0,1),12:(-1,0)}[port['direction']]
        x,y=port['position'];tip=(x+dx*.5,y+dy*.5,0)
        inner=(x-dx*.42,y-dy*.42,.50)
        knee=(x+dx*.31,y+dy*.31,.50)
        end=(tip[0]-dx*.12,tip[1]-dy*.12,.015)
        m.tube(inner,knee,.115,STEEL,16)
        m.tube(knee,end,.115,STEEL,16)
        m.tube(end,tip,.18,EDGE,20)
        m.tube(add(tip,(-dx*.005,-dy*.005,0)),add(tip,(dx*.005,dy*.005,0)),.105,DARK,16)
        mark=TEAL if port['flow']=='input' else GOLD
        m.tube(add(end,(-dx*.12,-dy*.12,.01)),add(end,(-dx*.08,-dy*.08,.01)),.124,mark,16)
        m.port_anchors.append({'box':port['box'],'position':tip,'direction':port['direction']})


def machine_legacy(name,t=0):
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
        m.cyl(0,0,.5,.94,h,STEEL if name=="materials-kiln" else DARK,28)
        m.ball((0,0,.5+h),.94,STEEL if name=="materials-kiln" else DARK,stretch=(1,1,.22))
        m.box((0,-.9,.85),(1.0,.08,.56),EDGE)
        m.box((0,-.955,.85),(.8,.045,.36),color(RED,1+.2*math.sin(t*TAU)))
        for i in range(5):m.box((-.33+i*.17,-.99,.85),(.035,.02,.35),DARK,0)
        m.cyl(.62,.5,h+.5,.25,.7 if name!='forcing-tower' else 1.0,DARK)
        m.ring((.62,.5,h+1.1),.3,.06,EDGE)
        for i in range(4):m.box((-.8+i*.24,.8,.65+h/2),(.1,.2,h*.8),COPPER)
        fan(m,-.45,-.05,h+.52,.38,t)
    elif name=='air-scrubber':
        for x in (-.66,.66):
            m.cyl(x,.2,.43,.51,1.17,STEEL,24)
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
    detailing(m,name,t)
    fluid_ports(m,name)
    return m


def machine(name,t=0):
    from solarpunk_models import machine as build
    return build(name,t)


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
    for x in (-2.2,2.2):
        m.box((x,.1,2.095),(.45,3.8,.055),DARK,.018)
        for y in (-1.2,-.4,.4,1.2):
            m.box((x,y,2.14),(.35,.59,.055),STEEL,.025)
            m.rivets(x,y-.21,2.175,.23,3)
        hose(m,[(x,1.5,2.1),(x,1.9,2.1),(x*.7,2.0,2.1)],.06,COPPER)
    for x in (-3.6,3.6):
        handwheel(m,x,1.91,1.51,.18)
        for y in (-1.1,-.7,-.3,.1):m.box((x,y,2.01),(1.02,.095,.10),EDGE,.015)
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
        # Rootweaver: three curved seed chambers, not a conventional twin gun barrel.
        q.cyl(0,0,.72,.40,.62,STEEL,24)
        for x,z in ((-.34,1.13),(.34,1.13),(0,1.46)):
            q.ball((x,-.41+recoil,z),.245,GREEN,stretch=(.86,1.65,.82))
            q.tube((x,-.53+recoil,z),(x,-1.02+recoil,z),.075,DARK,14)
            q.tube((x,-.95+recoil,z),(x,-1.08+recoil,z),.13,COPPER,16)
            hose(q,[(x,.26,.91),(x,.23,z),(x,-.12,z+.14)],.032,TEAL)
            q.ball((x,-1.095+recoil,z),.054,color(TEAL,1+.18*math.sin(t*TAU)),glow=True)
        q.ring((0,0,.89),.43,.035,COPPER)
    elif kind=='arc-turret':
        # Resonance diffuser: concentric organic horns around a charged core.
        q.cyl(0,0,1.27,.18,.38,EDGE)
        for i in range(5):
            a=i*TAU/5+t*.10
            q.ball((.44*math.cos(a),.44*math.sin(a),1.54),.22,STEEL,stretch=(1,.75,1.35))
            hose(q,[(0,0,1.22),(.40*math.cos(a),.40*math.sin(a),1.45),(.38*math.cos(a),.38*math.sin(a),1.85)],.044,COPPER)
        for z,r in ((1.44,.33),(1.74,.28),(2.0,.18)):q.ring((0,0,z),r,.039,EDGE)
        q.ball((0,0,1.90),.21,color(TEAL,1+.2*math.sin(t*TAU)),glow=True)
    else:
        # Pressure lance: a toroidal nozzle, buffer reservoirs and converging field rings.
        for x in (-.58,.58):
            q.ball((x,.05,1.10),.37,STEEL,stretch=(.80,1.8,.9))
            hose(q,[(x,.6,1.15),(x,-.50,1.15),(x*.4,-.85,1.32)],.075,COPPER)
        q.tube((0,.16,1.30),(0,-1.85+recoil,1.30),.19,DARK,24)
        for y,r in ((-.38,.46),(-.78,.40),(-1.18,.33),(-1.63,.24)):
            for i in range(20):
                a=i*TAU/20;b=(i+1)*TAU/20
                q.tube((r*math.cos(a),y+recoil,1.3+r*math.sin(a)),(r*math.cos(b),y+recoil,1.3+r*math.sin(b)),.045,EDGE,8)
            q.tube((0,y+recoil,1.3),(0,y-.04+recoil,1.3),r*.52,color(TEAL,1+.16*math.sin(t*TAU)),16)
        q.ball((0,-1.98+recoil,1.3),.14,TEAL,glow=True)
    q.box((0,.43,1.05),(.58,.18,.40),DARK,.03)
    for i in range(5):q.box((-.22+i*.11,.54,1.05),(.052,.024,.31),EDGE,.004)
    for x in (-.38,.38):
        hose(q,[(x,.3,.9),(x,.45,1.3),(x*.7,.15,1.45)],.025,COPPER)
    q.rivets(0,.40,1.38,.56,5)
    m.join(q,angle);return m


def wall(mask=0,advanced=False):
    m=Mesh();c=EDGE if advanced else STEEL
    m.box((0,0,.15),(.95,.88,.28),DARK)
    m.box((0,0,.65),(.64,.55,.94),c)
    for bit,(x,y) in enumerate(((0,-.5),(.5,0),(0,.5),(-.5,0))):
        if mask&(1<<bit):m.box((x*.65,y*.65,.63),(.65 if x else .43,.65 if y else .43,.88),c)
    m.box((0,0,1.15),(.72,.62,.13),GOLD if not advanced else TEAL)
    for x in (-.20,.2):
        m.box((x,.295,.73),(.08,.025,.36),DARK,0)
        for z in (.49,.96):m.ball((x,.32,z),.03,EDGE)
    for z in (.4,.7,1.0):m.box((0,.284,z),(.51,.018,.023),EDGE,.002)
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


def logistics(name,t=0):
    m=Mesh()
    if name in ('vector-inserter','canopy-inserter'):
        m.cyl(0,0,.07,.43,.19,DARK,24);m.cyl(0,0,.26,.35,.27,STEEL,24)
        m.ring((0,0,.52),.33,.045,TEAL if name=='canopy-inserter' else COPPER)
        m.ball((0,0,.56),.24,EDGE,stretch=(1,1,.48))
        m.box((0,-.17,.64),(.22,.28,.22),STEEL,.1)
        for i in range(8):
            a=i*TAU/8;m.cyl(.33*math.cos(a),.33*math.sin(a),.43,.026,.04,GOLD,8)
    elif name=='vital-splitter':
        m.box((0,0,.19),(1.95,.93,.33),DARK,.3)
        for x in (-.50,.50):
            m.cyl(x,0,.36,.36,.42,STEEL,24)
            fan(m,x,0,.79,.30,t)
        m.tube((-.58,0,.74),(.58,0,.74),.07,COPPER)
        m.box((0,.25,.88),(.36,.25,.19),EDGE,.12)
        m.box((0,.39,.90),(.18,.02,.05),TEAL,.01)
    elif name=='jukebox':
        m.cyl(0,0,.05,.57,.18,DARK,24)
        m.ball((0,0,.7),.58,STEEL,stretch=(.85,.65,1.1))
        for x in (-.23,.23):
            m.tube((x,.29,.58),(x,.36,.58),.19,DARK,20)
            m.tube((x,.36,.58),(x,.39,.58),.13,EDGE,20)
            m.ball((x,.40,.58),.07,TEAL,stretch=(1,.4,1))
        m.box((0,.24,1.02),(.40,.17,.20),DARK,.08)
        for i in range(5):m.box((-.14+i*.07,.34,.96),(.035,.014,.05+.07*(.5+.5*math.sin(t*TAU+i))),TEAL,.01)
        m.tube((-.32,-.04,1.08),(-.32,-.04,1.66),.024,EDGE,8)
    else:
        m.box((0,0,.10),(1.6,1.1,.18),DARK,.2)
        for i in range(7):m.box((0,-.45+i*.15,.22),(1.4,.065,.05),TEAL,.015)
        for x in (-.73,.73):m.box((x,0,.22),(.10,1.13,.12),EDGE,.04)
    return m


def explorer(t=0,pose='idle',tier=0,move_angle=0,aim_offset=0,aim_angle=None):
    from explorer_model import explorer as build
    return build(t,pose,tier,move_angle,move_angle+aim_offset if aim_angle is None else aim_angle)


def render(mesh,width=320,height=None,ppu=64,angle=0,aa=1,origin=.70,map_aligned=False):
    from pbr_raster import render as raster
    return raster(mesh,width,height,ppu,angle,aa,origin,map_aligned)
