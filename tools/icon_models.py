"""Purpose-built inventory silhouettes. Native-sized icons, original geometry."""
import math
from industrial_art import Mesh,DARK,EDGE,GOLD,COPPER,STEEL,WHITE,TEAL,RED,GREEN,BLUE,TAU

CREAM=(215,213,191);SILVER=(170,180,185);INK=(31,37,38)


def flask(m,x,y,z,c,round_body=True,scale=1):
    if round_body:m.ball((x,y,z+.28*scale),.27*scale,c,stretch=(1,1,1.15))
    else:m.box((x,y,z+.26*scale),(.43*scale,.38*scale,.52*scale),c,.08)
    m.cyl(x,y,z+.42*scale,.085*scale,.30*scale,SILVER,16)
    m.cyl(x,y,z+.71*scale,.13*scale,.07*scale,COPPER,16)
    m.tube((x-.12*scale,y-.19*scale,z+.22*scale),(x-.12*scale,y-.19*scale,z+.43*scale),.014*scale,CREAM,8)


def crystal(m,center,r,height,c,sides=6):
    x,y,z=center;ring=[(x+r*math.cos(i*TAU/sides),y+r*math.sin(i*TAU/sides),z+height*.35) for i in range(sides)]
    tip=(x+r*.18,y-r*.1,z+height)
    base=(x,y,z)
    for i in range(sides):j=(i+1)%sides;m.face([ring[i],ring[j],tip],c);m.face([ring[j],ring[i],base],tuple(int(v*.7) for v in c))


def leaf(m,x,y,z,size=.5,c=GREEN):
    m.face([(x-size*.1,y-size*.45,z),(x-size*.5,y+.1*size,z+.12*size),(x,y+size*.65,z+.24*size),(x+size*.48,y+.08*size,z+.10*size)],c)
    m.tube((x,y-size*.45,z+.008),(x,y+size*.58,z+.24*size),.012,CREAM,6)


def item(name):
    m=Mesh()
    if name=='silica':
        for x,y,r,h in [(-.23,0,.22,.53),(.19,.06,.21,.41),(0,-.25,.20,.35)]:crystal(m,(x,y,0),r,h,(204,219,222))
    elif name=='glass':
        for i in range(3):
            plate=Mesh();plate.box((0,0,0),(.66,.47,.035),(95+i*20,172+i*10,184+i*10),.025)
            m.join(plate,-.14+i*.12,(i*.035,i*.06,.12+i*.08))
        m.tube((-.31,-.13,.30),(.25,-.13,.30),.017,CREAM,6)
    elif name=='mineral-nutrients':
        m.ball((0,0,.27),.32,(175,175,135),stretch=(1,.83,1));m.cyl(0,0,.52,.19,.08,COPPER,18)
        for x,y in [(-.10,0),(.08,.05),(0,-.09)]:crystal(m,(x,y,.59),.07,.1,(220,226,199))
        m.box((0,-.272,.28),(.26,.025,.17),(106,134,67),.025)
    elif name=='microbial-culture':
        m.cyl(0,0,.05,.37,.12,EDGE,28);m.cyl(0,0,.18,.31,.03,(109,169,111),28)
        for x,y in [(-.14,.05),(.10,.10),(.06,-.14)]:m.ball((x,y,.23),.09,(168,205,104),stretch=(1.1,.7,.3))
        m.ring((0,0,.22),.35,.024,SILVER)
    elif name=='algal-biomass':
        for x,y,z,s in [(-.18,0,.09,.64),(.17,.05,.14,.58),(0,-.12,.22,.70)]:leaf(m,x,y,z,s,(91,154,71))
    elif name=='compost':
        for i in range(7):
            a=i*TAU/7;m.ball((.23*math.cos(a),.19*math.sin(a),.14),.17,(124,88+i*3,55),stretch=(1,1,.72))
        m.tube((0,0,.22),(0,0,.58),.025,(126,164,74),8);leaf(m,.06,0,.46,.40,(142,188,80))
    elif name=='biochar':
        for x,y,r,h in [(-.21,.05,.22,.43),(.18,.10,.21,.33),(0,-.18,.20,.29)]:crystal(m,(x,y,0),r,h,(57,64,62),5)
    elif name=='activated-carbon':
        for x,y,z in [(-.18,0,.10),(.13,.04,.13),(-.02,-.14,.33)]:
            m.tube((x,y-.28,z),(x,y+.24,z),.10,(46,62,62),16)
            m.tube((x,y-.30,z),(x,y-.275,z),.075,SILVER,16)
    elif name=='filter-cartridge':
        m.cyl(0,0,.08,.22,.56,(61,136,143),22)
        for z in (.08,.2,.32,.44,.56,.65):m.cyl(0,0,z,.25,.035,EDGE,22)
    elif name=='spent-filter':
        m.tube((-.2,-.22,.20),(.2,.21,.46),.21,(83,76,61),22)
        m.box((.08,-.18,.38),(.37,.06,.29),(147,78,53),.03)
        m.face([(-.08,-.22,.32),(.22,-.22,.34),(.04,-.22,.53)],(230,180,62))
        m.tube((.06,-.23,.36),(.06,-.23,.44),.017,INK,6)
    elif name=='soil-substrate':
        m.box((0,0,.19),(.69,.50,.34),(119,92,59),.055)
        for z in (.12,.22,.31):m.box((0,-.254,z),(.61,.015,.025),(187,158,96),.004)
        m.box((0,0,.38),(.48,.32,.035),(82,131,67),.025)
    elif name=='seed-mix':
        for i,c in enumerate(((194,167,105),(157,187,97),(204,191,137))):
            m.ball((-.22+i*.22,0,.30),.18,c,stretch=(.77,.60,1.40));m.cyl(-.22+i*.22,0,.52,.10,.065,EDGE,12)
        leaf(m,0,-.14,.26,.35,(79,133,68))
    elif name=='ceramic-membrane':
        m.cyl(0,0,.08,.37,.11,CREAM,32)
        for x in (-.2,0,.2):
            for y in (-.16,.04,.22):
                if x*x+y*y<.10:m.cyl(x,y,.192,.045,.012,(63,90,103),8)
        m.ring((0,0,.20),.35,.026,(137,169,177))
    elif name in ('thermal-buffer','depleted-thermal-buffer'):
        full=name=='thermal-buffer';c=(199,122,55) if full else (97,125,144)
        m.box((0,0,.30),(.48,.40,.58),c,.10)
        for i in range(5):m.box((0,0,.08+i*.12),(.60,.44,.035),EDGE,.01)
        m.cyl(0,0,.62,.15,.08,DARK,16)
        if full:m.face([(-.06,-.23,.18),(.09,-.23,.36),(0,-.23,.36),(.07,-.23,.52),(-.13,-.23,.30),(-.025,-.23,.30)],(245,199,101))
        else:m.box((.15,.08,.76),(.33,.32,.07),SILVER,.02)
    elif name=='neutralization-charge':
        m.box((0,0,.28),(.48,.46,.49),CREAM,.075)
        for x in (-.18,.18):m.box((x,0,.29),(.055,.5,.55),(190,137,59),.008)
        m.face([(-.12,-.24,.27),(0,-.24,.44),(.12,-.24,.27),(0,-.24,.12)],(129,166,100))
    elif name=='hazardous-sludge':
        m.cyl(0,0,.08,.28,.54,(119,104,116),24)
        for z in (.1,.56):m.cyl(0,0,z,.31,.05,(192,147,65),24)
        m.ball((.21,-.14,.065),.24,(107,58,121),stretch=(1,.8,.2))
        m.face([(-.12,-.29,.29),(0,-.29,.47),(.12,-.29,.29)],(224,191,82))
    elif name=='vitrified-waste':
        m.box((0,0,.17),(.62,.42,.30),(98,100,80),.055)
        for x,y in [(-.14,-.05),(.17,.03)]:crystal(m,(x,y,.27),.12,.25,(166,140,88),5)
    elif name=='biofilm':
        m.tube((-.25,.10,.24),(.25,.10,.24),.17,(112,177,166),24)
        m.tube((-.27,.10,.24),(-.24,.10,.24),.10,CREAM,20)
        m.face([(-.25,.05,.18),(.25,.05,.18),(.25,-.40,.055),(-.25,-.40,.055)],(128,195,181))
        for x in (-.14,.04,.19):m.tube((x,-.05,.15),(x,-.33,.085),.009,CREAM,6)
    elif name=='ecological-data':
        m.box((0,0,.15),(.55,.68,.20),SILVER,.045);m.box((0,0,.27),(.42,.54,.03),CREAM,.02);leaf(m,0,0,.30,.52,(97,160,89));m.box((0,.29,.31),(.21,.10,.07),COPPER,.02)
    elif name=='climate-data':
        m.box((0,0,.28),(.60,.46,.48),SILVER,.06);m.box((0,-.239,.30),(.43,.025,.31),INK,.035)
        for i,c in enumerate(((78,147,176),(110,185,184),(213,143,70))):m.box((-.13+i*.13,-.26,.29),(.075,.016,.12+i*.065),c,.009)
        m.tube((.17,.05,.50),(.17,.05,.78),.036,COPPER,8)
    elif name=='biosphere-data':
        m.box((0,0,.12),(.78,.46,.20),EDGE,.07)
        for i,c in enumerate(((136,184,94),(101,164,185),(187,117,155))):flask(m,-.24+i*.24,0,.19,c,True,.47)
    elif name=='thermophile-culture':flask(m,0,0,.05,(183,105,68),True,1.1);m.ring((0,0,.29),.31,.035,COPPER)
    elif name=='symbiotic-culture':
        flask(m,-.20,.06,0,(126,169,102),True,.80);flask(m,.20,-.06,.05,(159,107,176),False,.78)
    elif name=='heavy-metal-cake':
        m.cyl(0,0,.04,.34,.24,(113,90,122),12)
        for i in range(6):a=i*TAU/6;m.tube((0,0,.29),(.28*math.cos(a),.28*math.sin(a),.29),.011,(197,151,101),6)
    elif name=='holmium-catalyst':
        m.box((0,0,.10),(.68,.52,.13),DARK,.07);crystal(m,(0,0,.16),.23,.54,(213,141,103),6)
        for side in (-1,1):m.tube((side*.27,-.16,.16),(side*.16,.06,.59),.026,SILVER,8)
    elif name=='biodiversity-matrix':
        m.cyl(0,0,.07,.37,.18,(115,167,100),6)
        for i in range(6):a=i*TAU/6;leaf(m,.22*math.cos(a),.22*math.sin(a),.29,.26,(159,201,108))
        m.ball((0,0,.30),.09,(202,199,122))
    elif name=='gaia-cell':
        m.ball((0,0,.36),.26,(134,187,111))
        for i in range(3):
            a=i*TAU/3;m.tube((.34*math.cos(a),.34*math.sin(a),.04),(.10*math.cos(a),.10*math.sin(a),.66),.055,COPPER,12)
        m.ring((0,0,.36),.31,.035,SILVER)
    elif name.endswith('science-pack'):
        if name=='ecology-science-pack':flask(m,0,0,0,(106,186,94),True,1.05);leaf(m,0,-.22,.27,.30,CREAM)
        elif name=='climate-science-pack':
            flask(m,-.13,0,0,(82,168,195),False,.9);flask(m,.21,.09,.05,(225,165,82),True,.65)
        else:
            m.box((0,0,.12),(.76,.50,.20),(129,110,160),.05)
            for i,c in enumerate(((115,174,97),(165,130,187),(104,176,198))):flask(m,-.24+i*.24,0,.17,c,True,.55)
    elif name=='alloy-stock':
        for i in range(3):
            beam=Mesh();beam.box((0,0,0),(.64,.14,.12),SILVER,.016);beam.box((0,-.076,0),(.52,.015,.055),(78,88,85),.007)
            m.join(beam,-.17,(.03*i,.16*i,.08+i*.075))
    elif name=='biopellet':
        for x,y in ((-.19,.05),(.18,.04),(0,-.20)):m.cyl(x,y,.08,.14,.32,(138,169,91),12)
    elif name=='bio-ash':
        m.cyl(0,0,.04,.36,.12,(128,143,150),20)
        for i in range(7):a=i*TAU/7;m.ball((.19*math.cos(a),.17*math.sin(a),.19),.12,(202,202,181),stretch=(1,1,.6))
    else:raise KeyError(name)
    return m


def fluid(name):
    m=Mesh()
    if name=='clean-water':
        flask(m,0,0,0,(102,185,213),True,1);m.tube((.22,-.15,.45),(.22,-.15,.63),.018,CREAM,6);m.tube((.13,-.15,.54),(.31,-.15,.54),.018,CREAM,6)
    elif name=='oxygen':
        for x,z,r in ((-.19,.22,.19),(.16,.44,.23),(-.08,.70,.11)):m.ball((x,0,z),r,(151,197,215));m.ring((x,0,z+r*.45),r*.8,.012,CREAM)
    elif name=='hydrogen':
        m.cyl(0,0,.05,.19,.64,(168,94,115),24);m.cyl(0,0,.70,.07,.10,SILVER,12)
        m.tube((-.17,0,.80),(.17,0,.80),.025,EDGE,8)
    elif name=='electrolyte':
        flask(m,0,0,0,(202,169,82),False,.95)
        for x in (-.11,.11):m.tube((x,0,.42),(x,0,.85),.027,COPPER,10)
    elif name=='bioleachate':flask(m,0,0,0,(112,166,84),True,1);leaf(m,.22,-.1,.45,.34,CREAM)
    elif name=='toxic-effluent':
        flask(m,-.08,0,.02,(142,93,162),False,.9);m.ball((.21,-.19,.12),.19,(106,54,137),stretch=(1,1,.30))
        m.face([(-.18,-.21,.30),(.03,-.21,.30),(-.075,-.21,.50)],(221,183,78))
    elif name=='producer-gas':
        for x,y,z,r in [(-.22,0,.25,.18),(0,0,.44,.25),(.23,.05,.31,.18)]:m.ball((x,y,z),r,(185,130,76))
        m.tube((-.31,.02,.06),(.30,.02,.06),.052,COPPER,10)
    elif name=='biogas':
        m.ball((-.18,.03,.30),.17,(99,163,115));m.ball((.16,.08,.45),.22,(138,184,130));leaf(m,0,-.15,.20,.52,(166,198,105))
    elif name=='synthetic-gas':
        points=[(-.27,0,.18),(0,0,.49),(.28,0,.25)]
        for a,b in zip(points,points[1:]):m.tube(a,b,.039,SILVER,10)
        for p in points:m.ball(p,.14,(92,153,193))
    else:raise KeyError(name)
    return m


def gear(name):
    m=Mesh()
    if name in ('field-armor','expedition-armor','bastion-armor'):
        tier=('field-armor','expedition-armor','bastion-armor').index(name)
        c=((111,128,104),(123,151,163),(146,131,164))[tier]
        m.box((0,0,.32),(.53,.27,.64),c,.13)
        for side in (-1,1):
            m.box((side*(.31+.03*tier),0,.36 if tier==0 else .52),(.18+.045*tier,.30,.43 if tier==0 else .24+.04*tier),c,.07)
            m.box((side*.18,-.16,.35),(.09,.035,.38),DARK,.02)
        m.box((0,-.17,.40),(.20,.04,.22),CREAM if tier==0 else (TEAL if tier==1 else (187,173,218)),.05)
        if tier==2:
            m.face([(-.22,-.17,.57),(.22,-.17,.57),(.18,-.19,.22),(0,-.20,.08),(-.18,-.19,.22)],(145,158,181))
            m.box((0,-.205,.39),(.13,.025,.13),(170,137,209),.035)
    elif name in ('carbine','induction-rifle','lance-rifle'):
        tier=('carbine','induction-rifle','lance-rifle').index(name)
        m.box((0,.15,.22),(.20,.68,.18),STEEL,.04)
        m.box((0,.56,.22),(.29,.40,.25),COPPER if tier==0 else (BLUE if tier==1 else (144,123,169)),.06)
        m.tube((0,-.10,.24),(0,-.75-tier*.13,.24),.035+tier*.009,DARK,16)
        if tier==1:
            for y in (-.46,-.31,-.16):m.cyl(0,y,.29,.09,.055,(104,176,195),14)
        elif tier==2:
            for side in (-1,1):m.box((side*.075,-.53,.24),(.035,.61,.075),CREAM,.012)
        m.box((0,.06,.08),(.12,.19,.20),DARK,.02)
    elif name in ('ballistic-magazine','mycelial-magazine'):
        bio=name.startswith('mycelial')
        m.box((0,0,.25),(.42,.24,.49),(90,139,86) if bio else DARK,.055)
        for x in (-.12,0,.12):m.cyl(x,0,.48,.043,.20,(154,190,111) if bio else (212,166,79),12)
        if bio:leaf(m,0,-.15,.28,.30,(193,217,125))
    elif name=='induction-cell':
        for x in (-.15,.15):m.cyl(x,0,.06,.13,.48,(83,150,181),20);m.cyl(x,0,.55,.09,.07,CREAM,14)
        m.tube((-.16,0,.28),(.16,0,.28),.045,COPPER,10)
    elif name=='lance-cell':
        crystal(m,(0,0,.15),.13,.69,CREAM,4)
        for side in (-1,1):m.box((side*.16,0,.27),(.12,.18,.42),(166,117,83),.03)
    elif name=='ecoshield-equipment':
        m.cyl(0,0,.05,.37,.15,SILVER,6);m.ball((0,0,.27),.24,(90,157,179),stretch=(1,1,.55))
        for i in range(3):a=i*TAU/3;m.box((.29*math.cos(a),.29*math.sin(a),.30),(.13,.13,.09),CREAM,.03)
    elif name in ('vector-inserter','canopy-inserter'):
        stack=name.startswith('canopy');c=(84,151,126) if stack else (196,142,70)
        m.cyl(0,.18,.06,.22,.18,DARK,20)
        m.tube((0,.18,.23),(.05,0,.66),.066,c,12)
        m.ball((.05,0,.66),.09,EDGE)
        m.tube((.05,0,.66),(.06,-.33,.81),.055,c,12)
        for side in (-1,1):m.tube((.06,-.33,.81),(.06+side*.14,-.43,.69),.035,EDGE,10)
        if stack:
            for z in (.33,.40,.47):m.box((.06,-.43,z),(.30,.24,.04),CREAM,.01)
    elif name in ('vital-belt','vital-underground-belt','vital-splitter'):
        lanes=2 if name=='vital-splitter' else 1
        for i in range(lanes):
            x=(i-(lanes-1)/2)*.41;m.box((x,0,.12),(.38,.82,.19),DARK,.05)
            for j in range(5):m.box((x,-.31+j*.15,.23),(.32,.063,.05),(91,159,151),.013)
        if name=='vital-underground-belt':m.box((0,.25,.38),(.49,.35,.39),STEEL,.13);m.box((0,.06,.34),(.32,.025,.20),INK,.04)
        if name=='vital-splitter':m.tube((-.2,.22,.37),(.2,-.22,.37),.09,COPPER,14)
    elif name=='field-dressing':
        m.box((0,0,.24),(.62,.45,.42),CREAM,.1)
        m.box((0,-.233,.24),(.32,.02,.08),RED,.012);m.box((0,-.233,.24),(.08,.02,.27),RED,.012)
    else:raise KeyError(name)
    return m
