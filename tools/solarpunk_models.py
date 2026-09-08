"""Distinct process architectures for the Verdant Works art set.
Factory materials and maintenance access remain industrial; contained vegetation,
solar shades and copper service loops give biological plants a restrained solarpunk layer.
"""
import math
from industrial_art import Mesh,STEEL,DARK,EDGE,GOLD,COPPER,WHITE,GREEN,TEAL,BLUE,VIOLET,RED,TAU,add,rot,mul,color
from industrial_art import hose,gauge,handwheel,cabinet,fan,fluid_ports
from catalog import load_catalog
SIZES={x['name']:x['footprint'] for x in load_catalog()['machines']}
SAGE=(106,132,91);GLASS=(43,101,108);SOLAR=(32,57,65);SOIL=(67,60,41)

def deck(m,w,d=None):
    d=d or w
    m.box((0,0,.20),(w-.20,d-.20,.28),STEEL,min(w,d)*.13)
    m.box((0,0,.355),(w-.34,d-.34,.06),DARK,min(w,d)*.13)
    for x in (-w*.37,w*.37):
        for y in (-d*.37,d*.37):
            m.cyl(x,y,.015,.18,.18,DARK,12);m.cyl(x,y,.36,.065,.035,EDGE,8)
    for x in (-w*.44,w*.44):
        for i in range(max(5,int(d*3))):
            y=-d*.39+i*d*.78/(max(5,int(d*3))-1)
            m.box((x,y,.40),(.15,.045,.035),EDGE,.009)
    # Short segmented hazard bands and visible fasteners, not a single square outline.
    for y in (-d*.45,d*.45):
        for i in range(5):
            x=-w*.25+i*w*.125
            m.box((x,y,.375),(w*.075,.075,.05),GOLD if i%2==0 else DARK,.015)

def vertical_vessel(m,x,y,r,h,fill=STEEL,base=.38):
    m.cyl(x,y,base,r+.07,.16,DARK,24)
    m.cyl(x,y,base+.16,r,h,fill,28)
    m.ball((x,y,base+.16+h),r,STEEL,stretch=(1,1,.34))
    for z in (base+.20,base+h*.55,base+h+.13):m.ring((x,y,z),r+.025,.045,EDGE)
    for a in (.4,2.5,4.5):
        p=(x+(r+.01)*math.cos(a),y+(r+.01)*math.sin(a),base+.3)
        m.tube(p,add(p,(0,0,h*.73)),.035,COPPER,10)
    gauge(m,x,y+r+.065,base+h*.62,.115,.2)

def horizontal_drum(m,x,y,z,r,length,fill=STEEL):
    m.tube((x-length/2,y,z),(x+length/2,y,z),r,fill,28)
    for xx in (x-length*.48,x-length*.22,x+length*.22,x+length*.48):
        m.tube((xx-.035,y,z),(xx+.035,y,z),r+.035,EDGE,24)
    for xx in (x-length*.33,x+length*.33):m.box((xx,y,.52),(.20,r*1.7,.32),DARK,.09)

def arched_pipe(m,a,b,height,r=.035,c=EDGE):
    points=[]
    for i in range(15):
        t=i/14
        points.append((a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t,a[2]*(1-t)+b[2]*t+math.sin(t*math.pi)*height))
    hose(m,points,r,c)

def solar_awning(m,x,y,z,w=1.3,d=.62):
    m.box((x,y,z),(w,d,.07),EDGE,.05)
    m.box((x,y,z+.046),(w-.10,d-.09,.02),SOLAR,.025)
    for i in range(7):m.box((x-w*.41+i*w*.82/6,y,z+.061),(.013,d*.82,.008),(86,119,123),.002)
    for xx in (x-w*.40,x+w*.40):m.tube((xx,y,.40),(xx,y,z),.025,STEEL,8)

def bed(m,x,y,z,w,d,plant_size=.75,flowers=False):
    m.box((x,y,z),(w,d,.24),SAGE,.17)
    m.box((x,y,z+.135),(w-.15,d-.13,.025),SOIL,.13)
    columns=max(2,int(w/.42));rows=max(1,int(d/.48))
    for i in range(columns):
        for j in range(rows):
            px=x-w*.36+i*w*.72/max(1,columns-1);py=y-d*.24+j*d*.48/max(1,rows-1)
            m.plant(px,py,z+.16,plant_size)
            if flowers and i%2==0:m.ball((px,py,z+.16+plant_size*.58),.055,(190,164,95))

def railing(m,a,b):
    m.tube(add(a,(0,0,.48)),add(b,(0,0,.48)),.029,EDGE,8)
    for t in (0,.5,1):
        p=add(a,mul((b[0]-a[0],b[1]-a[1],b[2]-a[2]),t));m.tube(p,add(p,(0,0,.5)),.025,STEEL,8)

def finishing(m,name,t):
    size=SIZES[name]
    if size>1:
        q=size*.38
        cabinet(m,q,-q,.74,.85,.42+.12*math.sin(t*TAU))
        hose(m,[(-q,-q,.45),(-q,q*.3,.45),(-q*.64,q*.58,.72)],.039,DARK)
        if size>=5:
            railing(m,(-q,-q,.43),(-q*.25,-q,.43))
            solar_awning(m,-q*.30,q*.90,1.15,1.10,.45) if name in ('algae-vat','hydroponics-bay','spore-tower','sanctuary','cryogenic-garden') else None
    fluid_ports(m,name)
    return m

def machine(name,t=0):
    m=Mesh();size=SIZES[name];deck(m,size)
    if name=='algae-vat':
        # A staggered fermentation train and a shared circulation spine.
        for x,y,r,h,fill in ((-1.16,-.45,.68,1.70,GLASS),(.25,.55,.58,1.42,GREEN),(1.21,-.40,.44,1.05,TEAL)):
            vertical_vessel(m,x,y,r,h,fill)
            for side in range(4):
                a=side*math.pi/2
                for i in range(2):m.ball((x+(r+.045)*math.cos(a),y+(r+.045)*math.sin(a),.72+((t+i*.45)%1)*h*.68),.03,WHITE,glow=True)
        hose(m,[(-1.16,-.45,2.24),(-1.16,1.16,2.24),(.25,1.16,1.7),(1.21,1.16,1.52),(1.21,-.40,1.52)],.070,COPPER)
        m.cyl(-.25,-1.15,.4,.32,.34,STEEL);fan(m,-.25,-1.15,.76,.30,t)
        handwheel(m,.77,1.17,.89,.17,t*.15)
    elif name=='composter':
        # Open elliptical drum with turning paddles and an offset drive motor.
        horizontal_drum(m,0,.10,1.04,.72,1.68,STEEL)
        m.box((0,-.18,1.67),(1.40,.93,.13),EDGE,.19)
        m.box((0,-.18,1.75),(1.18,.72,.035),SOIL,.17)
        for i in range(4):m.box((-.51+i*.34,-.18+.18*math.sin(t*TAU),1.79),(.09,.57,.08),COPPER,.015)
        m.cyl(.88,.10,.50,.25,.73,DARK);m.ring((.88,.10,1.2),.27,.045,GOLD)
        m.box((-.85,-.70,.68),(.43,.83,.38),SAGE,.12)
    elif name=='hydroponics-bay':
        # Stepped terraces under a light skeletal greenhouse, not a factory box.
        for y,z in ((-1.18,.52),(0,.73),(1.18,.94)):bed(m,0,y,z,3.65,.86,.90,True)
        for x in (-1.96,1.96):
            arched_pipe(m,(x,-1.72,.51),(x,1.72,.51),1.91,.055,WHITE)
        m.tube((-1.96,0,2.43),(1.96,0,2.43),.065,COPPER,12)
        for y in (-1.1,0,1.1):m.tube((-1.8,y,1.87),(1.8,y,1.87),.023,TEAL,8)
        m.ball((0,0,2.48),.12,color(TEAL,1+.20*math.sin(t*TAU)),glow=True)
        vertical_vessel(m,1.55,-1.7,.26,.65,GLASS)
    elif name=='electrolyzer':
        # Membrane cell plates, two gas separators and copper buswork.
        for i in range(7):
            x=-1.20+i*.36;m.box((x,.26,1.12),(.15,1.8,1.33),EDGE,.05)
            m.box((x,-.67,1.12),(.11,.045,1.08),GLASS,.012)
        for z in (.60,1.80):m.tube((-1.42,-.70,z),(1.23,-.70,z),.10,COPPER,16)
        vertical_vessel(m,-1.55,1.24,.38,1.14,BLUE);vertical_vessel(m,1.52,1.22,.31,.92,WHITE)
        hose(m,[(-1.55,1.22,1.8),(-.75,1.25,1.80),(-.75,.25,1.8)],.06,EDGE)
        fan(m,0,-1.35,.46,.43,t)
    elif name=='reclamation-plant':
        # Clarifier, cyclone and staged filter bank have visibly different functions.
        m.cyl(-.91,-.05,.39,.93,.68,STEEL,32);m.cyl(-.91,-.05,1.08,.82,.025,BLUE)
        m.ring((-.91,-.05,1.12),.95,.055,EDGE)
        rotor=Mesh();rotor.box((.0,.0,1.15),(1.72,.07,.045),WHITE,.01);m.join(rotor,t*TAU,(-.91,-.05,0))
        vertical_vessel(m,1.00,.7,.55,1.87,EDGE)
        for x in (-.8,0,.8):vertical_vessel(m,x,-1.55,.24,.67,COPPER)
        hose(m,[(-.91,.83,1.02),(-.91,1.65,1.02),(1,1.65,1.02),(1,.70,1.3)],.10,EDGE)
        handwheel(m,1.48,1.0,.86,.16)
    elif name=='materials-kiln':
        # A large horizontal electric furnace with a circular service face.
        horizontal_drum(m,0,.20,1.28,.91,3.45,STEEL)
        for x in (-1.70,1.70):
            m.tube((x,.20,1.28),(x+.03,.20,1.28),.82,EDGE,32)
        for i in range(8):m.box((-.98+i*.28,-.72,1.3),(.11,.10,1.14),COPPER,.025)
        for i in range(6):m.box((-.85+i*.33,-1.32,.62),(.15,.71,.20),EDGE,.06)
        m.box((0,-.74,1.09),(1.16,.09,.58),DARK,.16)
        m.box((0,-.803,1.09),(.91,.02,.35),color(RED,1+.25*math.sin(t*TAU)),.12)
        fan(m,1.4,1.2,.46,.35,t)
    elif name=='pyrolyzer':
        # Compact soot-dark retort, condenser coil and exhaust stack.
        vertical_vessel(m,-.25,.10,.64,1.03,DARK)
        m.cyl(.75,.57,.42,.23,1.65,DARK)
        m.cyl(.75,.57,2.05,.30,.11,EDGE)
        for z in (.60,.81,1.02,1.23):m.ring((.78,-.63,z),.25,.04,COPPER)
        hose(m,[(-.22,.12,1.55),(-.22,-.60,1.55),(.78,-.63,1.27)],.062,COPPER)
        m.box((-.22,-.57,.85),(.62,.075,.38),color(RED,1+.20*math.sin(t*TAU)),.13)
        handwheel(m,-.77,.48,.82,.15)
    elif name=='air-scrubber':
        # One central intake fan, three cyclone cartridges and a low service saddle.
        m.cyl(0,-.23,.40,.73,.72,STEEL,28);fan(m,0,-.23,1.13,.64,t)
        for x,y,h in ((-.76,.65,1.38),(0,.90,1.70),(.77,.65,1.15)):
            vertical_vessel(m,x,y,.23,h,EDGE)
        hose(m,[(-.76,.65,1.6),(-.76,-.1,1.6),(0,-.1,1.35),(.77,-.1,1.35),(.77,.65,1.35)],.06,COPPER)
        gauge(m,.85,-.25,.75,.11,t*.2)
    elif name=='soil-enricher':
        # Open soil bed with an auger, a culture tank and a low spreading manifold.
        m.box((-.26,.06,.70),(1.62,1.96,.44),SAGE,.24)
        m.box((-.26,.06,.94),(1.39,1.72,.035),SOIL,.18)
        for i in range(6):
            y=-.62+i*.25;m.box((-.24+.17*math.sin(t*TAU+i*.25),y,1.01),(.98,.075,.08),EDGE,.015)
        vertical_vessel(m,.84,.38,.29,.98,GLASS)
        m.tube((-.95,-.85,.75),(.96,-.85,.75),.075,COPPER)
        for x in (-.65,0,.65):m.tube((x,-.85,.75),(x,-1.05,.47),.040,EDGE)
    elif name=='seed-disperser':
        # A radial flower of seed bins with a rotating metering head.
        m.cyl(0,0,.39,.44,.50,STEEL)
        for i in range(5):
            a=i*TAU/5;vertical_vessel(m,.78*math.cos(a),.78*math.sin(a),.22,.58,SAGE)
        m.cyl(0,0,.91,.15,.74,EDGE)
        rotor=Mesh()
        for i in range(5):
            a=i*TAU/5
            rotor.ball((.46*math.cos(a),.46*math.sin(a),1.65),.20,GOLD,stretch=(1,.6,.4))
            rotor.tube((0,0,1.55),(.62*math.cos(a),.62*math.sin(a),1.63),.032,EDGE,8)
        m.join(rotor,t*TAU);m.ball((0,0,1.74),.12,TEAL,glow=True)
    elif name=='watershed':
        # Offset reservoirs linked by a channel and an island of pumps.
        for x,y,r in ((-.87,-.15,1.04),(1.00,.73,.72)):
            m.cyl(x,y,.40,r,.63,EDGE,32);m.cyl(x,y,1.045,r-.105,.018,BLUE,32)
            m.ring((x,y,1.085),r,.05,WHITE)
        m.box((.18,.28,.76),(1.1,.42,.32),EDGE,.18);m.box((.18,.28,.94),(.94,.30,.025),BLUE,.14)
        arm=Mesh();arm.box((0,0,1.11),(1.8,.065,.04),WHITE,.01);m.join(arm,t*TAU,(-.87,-.15,0))
        for x in (.55,1.25):fan(m,x,-1.12,.54,.29,t)
        bed(m,-1.38,1.44,.6,1.18,.46,.50)
    elif name=='thermal-exchanger':
        # Vertical fin banks and a crosswise copper recuperator.
        for side in (-1,1):
            for i in range(8):m.box((side*1.07,-1.17+i*.32,1.22),(.58,.12,1.52),EDGE,.025)
        horizontal_drum(m,0,.16,1.28,.42,1.44,COPPER)
        for x in (-1.0,1.0):
            hose(m,[(x,-1.52,.54),(x,-1.52,2.08),(x,1.52,2.08),(x,1.52,.62)],.09,COPPER)
        for y in (-1.04,.18,1.40):fan(m,0,y,.49,.38,t)
        gauge(m,.57,-.30,1.2,.13,t*.15)
    elif name=='detoxifier':
        # Different reaction stages, shielded sludge vessels and a containment hood.
        for x,y,r,h in ((-1.20,.20,.46,1.70),(0,.80,.56,2.04),(1.23,.18,.38,1.30)):
            vertical_vessel(m,x,y,r,h,VIOLET)
        for x in (-.65,.10,.85):m.box((x,-1.30,.72),(.52,.72,.61),STEEL,.19)
        arched_pipe(m,(-1.65,.52,.70),(1.65,.52,.70),2.17,.085,EDGE)
        hose(m,[(-1.2,-.24,.73),(-1.2,-1.2,.73),(.95,-1.2,.73)],.065,COPPER)
        m.ball((0,.8,2.74),.105,color(TEAL,1+.22*math.sin(t*TAU)),glow=True)
    elif name=='pheromone-dampener':
        m.cyl(0,0,.4,.61,.39,SAGE);m.cyl(0,0,.81,.18,.90,EDGE)
        for i,(z,r) in enumerate(((1.0,.68),(1.43,.56),(1.81,.40))):
            m.ball((0,0,z),r,STEEL,stretch=(1,1,.19))
            m.ring((0,0,z+.08),r*.9,.030,color(TEAL,1+.22*math.sin(t*TAU+i)))
        for x in (-.82,.82):m.cyl(x,-.27,.4,.22,.76,GLASS)
        bed(m,0,-.95,.51,1.36,.32,.33)
    elif name=='forcing-tower':
        # The dirty counterpart is a tall asymmetrical smokestack, not another kiln.
        m.cyl(-.26,.12,.39,.68,1.46,DARK,28)
        m.cyl(-.26,.12,1.86,.40,1.12,DARK,24)
        for z in (1.7,2.2,2.9):m.ring((-.26,.12,z),.44 if z>2 else .7,.04,COPPER)
        m.cyl(.80,.69,.42,.25,1.29,STEEL)
        hose(m,[(.8,.69,1.5),(.8,-.6,1.5),(-.2,-.6,1.1)],.085,EDGE)
        m.box((-.24,-.60,1.03),(.53,.04,.50),color(RED,1+.22*math.sin(t*TAU)),.10)
        for z in (.65,1.0,1.35,1.7,2.05,2.4):m.box((-.81,.38,z),(.12,.20,.045),EDGE,.006)
    elif name=='basalt-conditioner':
        m.box((0,.29,.90),(3.02,2.6,.91),DARK,.37)
        m.box((0,.35,1.39),(2.57,2.12,.07),STEEL,.25)
        for i in range(8):m.box((-.98+i*.28,.20,1.5+.08*math.sin(t*TAU+i*.45)),(.13,1.50,.21),EDGE,.025)
        for x in (-1.56,1.56):
            m.tube((x-.06,.34,1.0),(x+.06,.34,1.0),.65,COPPER,28)
            m.tube((x-.075,.34,1.0),(x+.075,.34,1.0),.48,DARK,28)
        for i in range(7):m.ball((-.85+(i%4)*.53,1.0+(i//4)*.26,1.72),.20,STEEL,stretch=(1,.8,.65))
        m.box((0,-1.25,.70),(1.40,.78,.38),GOLD,.22)
    elif name=='fulgoran-reclaimer':
        m.cyl(-.53,.06,.42,1.20,.49,DARK,32);m.ring((-.53,.06,.92),1.22,.07,COPPER)
        rotor=Mesh()
        for i in range(6):
            a=i*TAU/6;rotor.box((.84*math.cos(a),.84*math.sin(a),1.03),(.42,.36,.23),EDGE,.07)
        m.join(rotor,t*TAU,(-.53,.06,0))
        for y in (-.99,.11,1.17):m.box((1.32,y,.79),(.73,.81,.71),STEEL,.19)
        m.cyl(-.53,.06,.95,.18,1.30,EDGE)
        boom=Mesh();boom.tube((0,0,2.30),(1.36,0,2.30),.07,GOLD);boom.cyl(1.36,0,1.90,.27,.32,TEAL)
        m.join(boom,t*TAU,(-.53,.06,0))
    elif name=='spore-tower':
        m.cyl(0,0,.4,.69,2.40,GLASS,28)
        for i in range(6):
            angle=i*TAU/6;z=.62+i*.32
            m.ball((.91*math.cos(angle),.91*math.sin(angle),z),.37,SAGE,stretch=(1,1,.72))
            arched_pipe(m,(0,0,z),(.91*math.cos(angle),.91*math.sin(angle),z),.24,.035,COPPER)
        for z in (.63,1.15,1.67,2.19,2.78):m.ring((0,0,z),.72,.052,EDGE)
        m.ball((0,0,2.93),.31,color(GOLD,1+.16*math.sin(t*TAU)),stretch=(1,1,.42),glow=True)
        bed(m,-1.12,-1.24,.54,1.36,.64,.60)
    elif name=='cryogenic-garden':
        # Heated habitat pods on insulated runners, with accessible manifolds.
        for x,y in ((-1.82,-.53),(0,1.04),(1.82,-.53)):
            m.box((x,y,.58),(1.6,2.7,.38),WHITE,.41)
            bed(m,x,y,.91,1.30,2.15,.68)
            for yy in (-1.13,1.13):arched_pipe(m,(x-.74,y+yy,.81),(x+.74,y+yy,.81),1.03,.052,WHITE)
            m.tube((x,y-1.16,1.94),(x,y+1.16,1.94),.05,TEAL)
        for x in (-2.65,2.65):
            hose(m,[(x,-2.55,.50),(x,2.45,.50),(x*.7,2.45,.8)],.115,COPPER)
            for y in (-1.8,-.6,.6,1.8):m.ring((x,y,.55),.20,.035,EDGE)
        for x in (-.70,.70):fan(m,x,-2.16,.65,.38,t)
        m.ball((0,1.04,2.08),.11,color(TEAL,1+.2*math.sin(t*TAU)),glow=True)
    elif name=='sanctuary':
        # A vaulted living court with a central tree and terraced habitat beds.
        m.cyl(0,0,.4,2.42,.22,SAGE,40)
        m.cyl(0,0,.63,1.07,.16,SOIL,28)
        m.tube((0,0,.76),(0,0,2.38),.10,COPPER,14)
        for i in range(7):
            a=i*TAU/7;branch=(.68*math.cos(a),.68*math.sin(a),1.93+(i%2)*.36)
            m.tube((0,0,1.5),branch,.037,COPPER,10)
            m.ball(branch,.43,GREEN,stretch=(1.1,.8,.68))
        for i in range(6):
            a=i*TAU/6
            bed(m,1.85*math.cos(a),1.85*math.sin(a),.79,.95,.67,.60,True)
            m.tube((2.56*math.cos(a),2.56*math.sin(a),.47),(0,0,3.68),.064,WHITE,12)
        m.ring((0,0,2.95),.88,.035,COPPER)
        m.ball((0,0,3.68),.17,color(TEAL,1+.2*math.sin(t*TAU)),glow=True)
        m.box((0,-2.61,.58),(1.40,.48,.20),EDGE,.15)
    elif name=='planetary-beacon':
        # Tall interplanetary gyro with a broad service ring and slim antenna petals.
        m.cyl(0,0,.40,1.08,.72,STEEL,36)
        m.cyl(0,0,1.12,.38,1.07,EDGE,28)
        m.ball((0,0,2.66),.79,color(TEAL,1+.12*math.sin(t*TAU)),glow=True)
        for z,r in ((2.05,1.21),(2.66,1.49),(3.27,1.17)):m.ring((0,0,z),r,.060,COPPER)
        arm=Mesh();arm.box((0,0,2.68),(3.00,.10,.075),WHITE,.018);m.join(arm,t*TAU)
        for i in range(4):
            a=i*TAU/4+.4;x,y=2.25*math.cos(a),2.25*math.sin(a)
            m.tube((x,y,.46),(x*.8,y*.8,3.02),.079,EDGE,14)
            m.ball((x*.8,y*.8,3.12),.22,WHITE,stretch=(.65,.65,2.1))
            solar_awning(m,x*.76,y*.76,1.11,.86,.42)
    elif name=='ecology-monitor':
        m.box((0,0,.64),(.83,.73,.53),STEEL,.16)
        m.box((0,.387,.73),(.66,.045,.33),DARK,.09)
        for i in range(5):m.box((-.23+i*.115,.416,.62+.09*(1+math.sin(t*TAU+i))/2),(.045,.018,.08+.09*(1+math.sin(t*TAU+i))),TEAL,.008)
        m.cyl(.27,-.15,.87,.026,.42,EDGE,8)
    else:raise KeyError(name)
    return finishing(m,name,t)
