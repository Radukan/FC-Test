"""Detailed adult expedition explorer with independently oriented stride and aim.
All surfaces are authored geometry. The torso, head, hands and weapon share one
rig so the muzzle cannot turn away from the arms. Tool motion shares the grips.
"""
import math
from industrial_art import Mesh,STEEL,DARK,EDGE,GOLD,COPPER,TEAL,WHITE,add,rot,mul

SKIN=(184,130,103)
HAIR=(61,31,20)
SUIT=(37,42,39)

def loft(mesh,rings,color,sides=20):
    loops=[]
    for x,y,z,rx,ry in rings:
        loops.append([(x+rx*math.cos(i*math.tau/sides),y+ry*math.sin(i*math.tau/sides),z) for i in range(sides)])
    mesh.face(list(reversed(loops[0])),color);mesh.face(loops[-1],color)
    for j in range(len(loops)-1):
        for i in range(sides):
            k=(i+1)%sides;mesh.face([loops[j][i],loops[j][k],loops[j+1][k],loops[j+1][i]],color)

def local_to_world(p,angle):return rot(p,angle)

def explorer(t=0,pose='idle',tier=0,move_angle=0,aim_angle=0):
    m=Mesh();upper=Mesh();run=pose in ('running','running_with_gun');gun='gun' in pose;mining=pose=='mining_with_tool'
    phase=t*math.tau
    step=.29*math.sin(phase) if run else .010*math.sin(phase)
    bob=.018*(1-math.cos(phase*2)) if run else .009*math.sin(phase)
    facing=aim_angle if gun else move_angle
    armor=(119,111,88) if tier==0 else ((104,111,99) if tier==1 else (145,141,119))
    # Legs keep their anatomical facing while the stride vector follows movement.
    stride_vector=(math.sin(move_angle),-math.cos(move_angle),0)
    for side in (-1,1):
        hip=rot((side*.158,0,1.09+bob),facing)
        knee=add(rot((side*.17,-.015,.61+bob),facing),mul(stride_vector,side*step*.53))
        ankle=add(rot((side*.17,.005,.12),facing),mul(stride_vector,side*step))
        ankle=add(ankle,(0,0,max(0,-side*step)*.25))
        m.tube(hip,knee,.123,SUIT,18);m.tube(knee,ankle,.083,SUIT,16)
        m.ball(knee,.113,armor,stretch=(.9,1.05,.85))
        # Greaves, boot caps, seams and thigh straps follow the same limb axis.
        m.tube(add(knee,(0,.027,-.1)),add(ankle,(0,.027,.12)),.067,armor,14)
        boot=Mesh();boot.box((0,-.055,.015),(.195,.33,.20),DARK,.06)
        boot.box((0,-.143,.05),(.18,.12,.055),armor,.02)
        boot.box((0,-.05,-.074),(.21,.35,.035),(20,24,22),.02)
        m.join(boot,facing,ankle)
        belt=add(mul(hip,.52),mul(knee,.48));m.ball(belt,.125,(68,56,42),stretch=(1,1,.3))
    # A fitted silhouette, articulated pelvis and curved protective shell.
    loft(upper,[(0,.006,1.00+bob,.215,.12),(0,.006,1.09+bob,.254,.153),
                (0,0,1.21+bob,.164,.104),(0,0,1.36+bob,.171,.115),
                (0,-.005,1.52+bob,.222,.155),(0,.005,1.66+bob,.24,.134)],SUIT)
    upper.ball((-.105,-.083,1.50+bob),.148,armor,stretch=(.9,.77,.93))
    upper.ball((.105,-.083,1.50+bob),.148,armor,stretch=(.9,.77,.93))
    upper.box((0,-.122,1.27+bob),(.22,.045,.25),DARK,.035)
    for i in range(4):upper.box((0,-.150,1.17+bob+i*.056),(.14,.016,.018),EDGE,.005)
    # Harness follows the curved chest and waist rather than a single square slab.
    for side in (-1,1):
        upper.tube((side*.13,-.10,1.65+bob),(side*.18,-.20,1.44+bob),.022,(117,78,38),8)
        upper.tube((side*.18,-.20,1.44+bob),(side*.12,-.13,1.15+bob),.018,(117,78,38),8)
        upper.box((side*.147,-.173,1.36+bob),(.052,.025,.063),EDGE,.009)
    for side in (-1,1):
        upper.tube((side*.238,.016,1.065+bob),(side*.157,-.077,1.26+bob),.012,COPPER,8)
    upper.box((0,0,1.11+bob),(.43,.30,.09),(92,69,43),.045)
    upper.box((0,-.163,1.11+bob),(.10,.035,.075),EDGE,.01)
    for side in (-1,1):upper.box((side*.225,.025,1.10+bob),(.12,.15,.205),DARK,.025)
    # Compact respirator pack, routed tubes and instrumentation.
    upper.box((0,.19,1.40+bob),(.31,.16,.47),armor,.05)
    for x in (-.10,.10):
        upper.cyl(x,.245,1.28+bob,.049,.28,EDGE,14)
        upper.tube((x,.26,1.58+bob),(x*.8,.11,1.72+bob),.018,DARK,8)
    for i in range(5):upper.box((0,.285,1.28+bob+i*.051),(.21,.014,.018),DARK,.002)
    upper.box((.07,.286,1.56+bob),(.07,.013,.022),TEAL,.002)
    # Hands and tool/weapon anchors belong to this torso rig.
    tool_bottom=tool_top=None
    if mining:
        swing=.5-.5*math.cos(phase)
        # Over-shoulder preparation, forward impact, then recovery.
        tool_bottom=(.06,-.39,1.17+bob+.43*(1-swing))
        tool_top=(.06,-.58- .50*swing,2.43+bob-1.22*swing)
        grip_right=tuple(a*.70+b*.30 for a,b in zip(tool_bottom,tool_top))
        grip_left=tuple(a*.45+b*.55 for a,b in zip(tool_bottom,tool_top))
    for side in (-1,1):
        shoulder=(side*.273,.0,1.65+bob)
        if mining:
            hand=grip_left if side<0 else grip_right
            elbow=(side*.34,-.22,1.42+bob+.16*(1-swing))
        elif gun:
            hand=(.072,-.40,1.425+bob) if side>0 else (-.028,-.66,1.43+bob)
            elbow=(side*.33,-.15,1.34+bob)
        else:
            # Normal walk arm swing opposes the corresponding leg.
            elbow=(side*.31,side*step*.48,1.31+bob)
            hand=(side*.29,side*step*.90,1.05+bob)
        upper.tube(shoulder,elbow,.080,SUIT,16);upper.tube(elbow,hand,.063,SUIT,16)
        upper.ball(shoulder,.116,armor,stretch=(1.06,.95,.80))
        upper.ball(elbow,.077,EDGE,stretch=(1,.8,.8))
        upper.ball(hand,.065,DARK,stretch=(.8,1,.85))
        for finger in range(3):upper.tube(add(hand,(-.035+finger*.023,-.03,-.035)),add(hand,(-.035+finger*.023,-.078,-.012)),.010,(89,82,68),6)
        if tier>0:
            upper.box((side*.30,.012,1.67+bob),(.16,.255,.135),armor,.035)
            upper.box((side*.30,-.09,1.69+bob),(.10,.09,.025),GOLD,.008)
    # Neck, face, shaped hairline, eyes, brow and small facial details.
    upper.tube((0,0,1.68+bob),(0,-.005,1.80+bob),.073,SKIN,16)
    upper.ball((0,-.006,1.951+bob),.151,SKIN,stretch=(.87,.91,1.18))
    upper.ball((0,-.012,1.865+bob),.12,SKIN,stretch=(.86,.82,.82))
    upper.ball((0,.05,1.991+bob),.158,HAIR,stretch=(.97,.82,1.0))
    # The face remains open; the brow-mounted optics leave the features visible.
    upper.ball((0,-.149,1.946+bob),.028,(196,141,111),stretch=(.55,1,.9))
    upper.box((0,-.135,1.895+bob),(.070,.013,.014),(120,57,49),.005)
    for x in (-.062,.062):
        upper.ball((x,-.127,1.977+bob),.025,(213,197,166),stretch=(1,.35,.58))
        upper.ball((x,-.140,1.978+bob),.012,(38,60,51),stretch=(1,.32,1))
        upper.tube((x-.028,-.119,2.007+bob),(x+.022,-.126,2.012+bob),.009,HAIR,6)
        upper.box((x,-.083,2.081+bob),(.092,.076,.046),DARK,.013)
        upper.box((x,-.126,2.082+bob),(.075,.018,.026),(64,132,137),.008)
    # Detailed tied hair, not a featureless block helmet.
    for i in range(7):
        angle=(i-3)*.19
        upper.tube((.11*math.sin(angle),.155,2.01+bob),(.04+.025*math.sin(phase+i),.255,1.68+bob-i*.006),.017,tuple(v+i*2 for v in HAIR),8)
    upper.ball((0,.164,1.99+bob),.052,GOLD,stretch=(1,.5,.6))
    for x in (-.137,.137):upper.ball((x,.015,1.95+bob),.036,armor)
    if tier==2:
        for side in (-1,1):
            upper.box((side*.31,.12,1.64+bob),(.18,.23,.21),armor,.04)
            upper.box((side*.31,.02,1.75+bob),(.13,.05,.025),GOLD,.006)
        upper.box((0,-.118,1.841+bob),(.20,.055,.067),DARK,.015)
    anchors={}
    if gun:
        recoil=.014*(.5-.5*math.cos(phase))
        upper.box((.028,-.51+recoil,1.447+bob),(.145,.53,.116),DARK,.025)
        upper.box((.028,-.47+recoil,1.516+bob),(.065,.34,.033),EDGE,.009)
        upper.tube((.028,-.67+recoil,1.448+bob),(.028,-1.12+recoil,1.448+bob),.025,STEEL,14)
        for j in range(4):upper.tube((.028,-.79+j*.055+recoil,1.448+bob),(.028,-.766+j*.055+recoil,1.448+bob),.036,EDGE,12)
        upper.box((.028,-.39+recoil,1.315+bob),(.085,.145,.19),COPPER,.016)
        upper.box((.028,-.24+recoil,1.443+bob),(.10,.18,.12),(104,89,64),.025)
        anchors['gun_root']=(.028,-.67+recoil,1.448+bob)
        anchors['gun_muzzle']=(.028,-1.12+recoil,1.448+bob)
        anchors['right_grip']=grip_right if mining else (.072,-.40,1.425+bob)
    if mining:
        upper.tube(tool_bottom,tool_top,.024,(96,78,53),12)
        left=add(tool_top,(-.38,-.045,0));right=add(tool_top,(.32,.045,-.02))
        upper.tube(left,right,.05,EDGE,12)
        upper.face([left,add(left,(-.16,-.035,-.04)),add(left,(.015,.03,.05))],STEEL)
        anchors['tool_tip']=add(left,(-.16,-.035,-.04))
        anchors['tool_grip']=grip_right
    m.join(upper,facing)
    m.anchors={name:rot(point,facing) for name,point in anchors.items()}
    m.aim_angle=facing;m.move_angle=move_angle
    return m
