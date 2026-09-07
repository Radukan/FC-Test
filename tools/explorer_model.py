"""Detailed adult expedition explorer with independently oriented stride and aim.
All surfaces are authored geometry. The torso, head, hands and weapon share one
rig so the muzzle cannot turn away from the arms. Tool motion shares the grips.
"""
import math
from industrial_art import Mesh,STEEL,DARK,EDGE,GOLD,COPPER,TEAL,WHITE,add,rot,mul
import gait
from character_rig import limb,hand as build_hand

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
    step=.24*math.sin(phase) if run else .008*math.sin(phase)
    bob=-.035*math.cos(phase*2) if run else .007*math.sin(phase)
    facing=aim_angle if gun else move_angle
    armor=(119,111,88) if tier==0 else ((104,111,99) if tier==1 else (145,141,119))
    stride_vector=(math.sin(move_angle),-math.cos(move_angle),0)
    bend=rot((0,-1,0),facing)
    joints={};phases={}
    # Stance feet remain planted in height. The swing leg clears the ground and
    # shortens through knee flexion, with constant femur/tibia lengths.
    for side in (-1,1):
        sample=gait.foot_phase(t,side) if run else {'phase':0,'along':0,'lift':0,'pitch':0,'mode':'stance'}
        phases[side]=sample
        hip=rot((side*.158+.016*math.sin(phase) if run else side*.158,0,1.10+bob),facing)
        ankle=add(rot((side*.17,0,.115),facing),mul(stride_vector,sample['along']))
        ankle=add(ankle,(0,0,sample['lift']))
        knee=gait.solve_two_bone(hip,ankle,gait.THIGH,gait.SHIN,bend)
        limb(m,hip,knee,.127,.105,SUIT,18);limb(m,knee,ankle,.090,.061,SUIT,16)
        m.ball(knee,.111,armor,stretch=(.95,1.0,.76))
        shin_front=rot((0,-.046,0),facing)
        top=add(gait.add(knee,gait.mul(gait.sub(ankle,knee),.15)),shin_front)
        bottom=add(gait.add(knee,gait.mul(gait.sub(ankle,knee),.84)),shin_front)
        limb(m,top,bottom,.075,.050,armor,14)
        boot=Mesh();boot.box((0,-.055,.015),(.21,.35,.20),DARK,.06)
        boot.box((0,-.143,.05),(.195,.13,.061),armor,.03)
        boot.box((0,-.05,-.074),(.22,.37,.035),(20,24,22),.025)
        # Toe roll on lift-off and controlled heel strike during contact.
        pitch=sample['pitch'];c,ss=math.cos(pitch),math.sin(pitch)
        rolled=Mesh()
        for vertices,color,glow in boot.faces:
            rolled.face([(x,y*c-z*ss,y*ss+z*c) for x,y,z in vertices],color,glow)
        m.join(rolled,facing,ankle)
        belt=gait.add(hip,gait.mul(gait.sub(knee,hip),.44));m.ball(belt,.126,(68,56,42),stretch=(1,1,.24))
        joints['hip-'+str(side)]=hip;joints['knee-'+str(side)]=knee;joints['ankle-'+str(side)]=ankle
        joints['toe-'+str(side)]=add(rot((0,-.20,.04),facing),ankle)
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
        theta=math.radians(-18+158*swing)
        tool_bottom=(.065,-.40,1.48+bob)
        shaft=(0,-math.sin(theta),math.cos(theta))
        tool_top=add(tool_bottom,mul(shaft,1.15))
        cutting_direction=(0,-math.cos(theta),-math.sin(theta))
        grip_right=tuple(a*.96+b*.04 for a,b in zip(tool_bottom,tool_top))
        grip_left=tuple(a*.83+b*.17 for a,b in zip(tool_bottom,tool_top))
    hand_joints={}
    for side in (-1,1):
        shoulder=(side*.273,0,1.65+bob)
        if mining:
            wrist=grip_left if side<0 else grip_right
            forward=shaft;back=(0,1,0);curl=.95
        elif gun:
            wrist=(.085,-.385,1.46+bob) if side>0 else (-.034,-.585,1.455+bob)
            forward=(0,0,-1) if side>0 else (0,-1,0)
            back=(0,-1,0) if side>0 else (0,0,1);curl=.88
        else:
            wrist=(side*.31,side*step*.90,1.07+bob+.04*math.cos(phase+side))
            forward=(0,0,-1);back=(0,1,0);curl=.22
        elbow=gait.solve_two_bone(shoulder,wrist,.38,.35,(side,.38,-.2))
        limb(upper,shoulder,elbow,.086,.074,SUIT,16);limb(upper,elbow,wrist,.071,.055,SUIT,16)
        upper.ball(shoulder,.116,armor,stretch=(1.06,.95,.80));upper.ball(elbow,.077,EDGE,stretch=(1,.8,.8))
        h=build_hand(upper,wrist,forward,back,side,curl)
        hand_joints[side]=h
        joints['shoulder-'+str(side)]=rot(shoulder,facing)
        joints['elbow-'+str(side)]=rot(elbow,facing)
        joints['wrist-'+str(side)]=rot(wrist,facing)
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
        rear=add(tool_top,mul(cutting_direction,-.22))
        neck=add(tool_top,mul(cutting_direction,.17))
        tip=add(tool_top,mul(cutting_direction,.50))
        upper.tube(rear,neck,.057,EDGE,12)
        # A tapered forged point, not a flat crossbar presented to the ground.
        side=(.067,0,0);up=(0,-cutting_direction[2]*.045,cutting_direction[1]*.045)
        ring=[add(neck,side),add(neck,up),add(neck,mul(side,-1)),add(neck,mul(up,-1))]
        for i in range(4):upper.face([ring[i],ring[(i+1)%4],tip],STEEL)
        anchors['tool_tip']=tip
        anchors['tool_neck']=neck
        anchors['strike_direction']=cutting_direction
        anchors['tool_grip']=grip_right
    m.join(upper,facing)
    m.anchors={name:rot(point,facing) for name,point in anchors.items()}
    m.aim_angle=facing;m.move_angle=move_angle
    m.joints=joints;m.foot_phases=phases;m.pose=pose
    m.hands={side:{key:rot(point,facing) for key,point in values.items()} for side,values in hand_joints.items()}
    return m
