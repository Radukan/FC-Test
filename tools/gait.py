"""Deterministic two-bone kinematics and a grounded locomotion cycle.
Units are authored-model units. Rendering and native gameplay movement are separate.
"""
import math

STANCE=.62
STEP_SPAN=.70
FOOT_LIFT=.265
THIGH=.55
SHIN=.51
RUN_FRAMES=16
MINING_FRAMES=20
MINING_SPEED=.26
# One stance sweeps STEP_SPAN while the root advances at constant speed.
CYCLE_DISTANCE_TILES=STEP_SPAN/STANCE*(80*.5/32)
DISTANCE_PER_FRAME=CYCLE_DISTANCE_TILES/RUN_FRAMES

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,t):return tuple(x*t for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def length(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/max(1e-12,length(a)))
def smooth(t):return t*t*(3-2*t)

def solve_two_bone(root,target,upper,lower,bend):
    delta=sub(target,root);distance=length(delta)
    assert distance<upper+lower-1e-6,('unreachable limb target',distance,upper+lower)
    assert distance>abs(upper-lower)+1e-6,('overfolded limb target',distance)
    axis=unit(delta)
    direction=sub(bend,mul(axis,dot(bend,axis)))
    if length(direction)<1e-8:direction=sub((1,0,0),mul(axis,axis[0]))
    direction=unit(direction)
    along=(upper*upper-lower*lower+distance*distance)/(2*distance)
    height=math.sqrt(max(0,upper*upper-along*along))
    return add(add(root,mul(axis,along)),mul(direction,height))

def foot_phase(cycle,side):
    phase=(cycle+(0 if side<0 else .5))%1
    if phase<STANCE:
        t=phase/STANCE
        along=STEP_SPAN*(.5-t)
        lift=0
        pitch=(-.12*(1-t/.14)) if t<.14 else (.20*((t-.82)/.18) if t>.82 else 0)
        mode='stance'
    else:
        t=(phase-STANCE)/(1-STANCE)
        along=STEP_SPAN*(-.5+smooth(t))
        lift=FOOT_LIFT*math.sin(math.pi*t)**1.25
        pitch=.22*math.sin(math.pi*t)
        mode='swing'
    return {'phase':phase,'along':along,'lift':lift,'pitch':pitch,'mode':mode}

def knee_flexion(hip,knee,ankle):
    a=unit(sub(hip,knee));b=unit(sub(ankle,knee))
    return 180-math.degrees(math.acos(max(-1,min(1,dot(a,b)))))
