"""Measurable whole-body motion and grip contracts, not a client-playtest claim."""
import math

from body_motion import mining_profile, motion
from warden_model import warden
from gait import dot, sub, length


def test_pelvis_and_shoulders_counter_rotate_and_shift_weight():
    hip_yaw=[];shoulder_yaw=[];hip_roll=[];shoulder_roll=[];head=[]
    for frame in range(16):
        m=warden(frame/16,'running',0)
        hip=sub(m.joints['hip-1'],m.joints['hip--1'])
        shoulder=sub(m.joints['shoulder-1'],m.joints['shoulder--1'])
        hip_yaw.append(math.atan2(hip[1],hip[0]));shoulder_yaw.append(math.atan2(shoulder[1],shoulder[0]))
        hip_roll.append(hip[2]);shoulder_roll.append(shoulder[2]);head.append(m.joints['head'][2])
    assert max(hip_yaw)-min(hip_yaw)>.14
    assert max(shoulder_yaw)-min(shoulder_yaw)>.13
    assert sum(a*b for a,b in zip(hip_yaw,shoulder_yaw))<-.03
    assert max(hip_roll)-min(hip_roll)>.02 and max(shoulder_roll)-min(shoulder_roll)>.035
    assert max(head)-min(head)>.035


def test_head_has_independent_stabilization_and_secondary_motion_is_armor_damped():
    values=[]
    for tier in range(3):
        samples=[motion(i/32,'running',tier) for i in range(32)]
        values.append(max(abs(s['secondary']) for s in samples))
        assert any(abs(s['head'].pitch)>0 for s in samples)
        assert len({round(s['head'].offset[2],5) for s in samples})>8
    assert .02<values[0]<.04
    assert values[1]<values[0]*.4 and values[2]<values[0]*.15


def test_right_palm_is_higher_along_the_shaft_and_both_hands_stay_attached():
    for facing in (0,math.pi/2,math.pi,3*math.pi/2):
        for frame in range(20):
            m=warden(frame/20,'mining_with_tool',0,facing,facing)
            axis=m.anchors['tool_axis']
            assert abs(length(axis)-1)<1e-10
            right,left=m.hands[1]['palm'],m.hands[-1]['palm']
            assert dot(sub(right,left),axis)>.25
            assert length(sub(right,m.anchors['right_grip']))<1e-9
            assert length(sub(left,m.anchors['left_grip']))<1e-9
            for side in (-1,1):
                assert abs(length(sub(m.joints['shoulder-'+str(side)],m.joints['elbow-'+str(side)]))-.38)<1e-8
                assert abs(length(sub(m.joints['elbow-'+str(side)],m.joints['wrist-'+str(side)]))-.35)<1e-8


def test_power_stroke_accelerates_into_impact_with_body_drive_and_ground_clearance():
    def velocity(t):return (mining_profile(t+.0001)['angle']-mining_profile(t)['angle'])/.0001
    windup=max(abs(velocity(i/1000)) for i in range(0,270))
    downstroke=max(velocity(i/1000) for i in range(280,500))
    assert downstroke>windup*3
    impact=warden(.5,'mining_with_tool')
    ready=warden(.28,'mining_with_tool')
    assert impact.motion['torso'].pitch-ready.motion['torso'].pitch>.24
    assert ready.joints['pelvis'][2]-impact.joints['pelvis'][2]>.07
    assert 0<=impact.anchors['tool_tip'][2]<.15
    assert impact.anchors['tool_tip'][2]<impact.anchors['tool_neck'][2]
    for i in range(20):
        m=warden(i/20,'mining_with_tool')
        assert min(m.sole_heights.values())>=0


def test_swing_foot_velocity_no_longer_stops_instantly_at_lift_off():
    from gait import foot_phase,STANCE,STEP_SPAN
    eps=.00001
    expected=-STEP_SPAN/STANCE
    a,b=foot_phase(STANCE,-1),foot_phase(STANCE+eps,-1)
    assert abs((b['along']-a['along'])/eps-expected)<.01
    a,b=foot_phase(1-eps,-1),foot_phase(1,-1)
    assert abs((b['along']-a['along'])/eps-expected)<.01


def test_pose_math_is_loop_continuous():
    for pose in ('idle','running','running_with_gun','mining_with_tool'):
        first=warden(0,pose)
        last=warden(1,pose)
        for name in first.joints:
            assert length(sub(first.joints[name],last.joints[name]))<1e-9,(pose,name)


def test_relaxed_arms_swing_opposite_the_advancing_leg():
    first=warden(0,'running')
    other=warden(.5,'running')
    assert first.joints['ankle--1'][1]<first.joints['ankle-1'][1]
    assert first.joints['wrist-1'][1]<first.joints['wrist--1'][1]
    assert other.joints['ankle-1'][1]<other.joints['ankle--1'][1]
    assert other.joints['wrist--1'][1]<other.joints['wrist-1'][1]


def test_warden_is_fully_sealed_with_no_exposed_skin():
    """The restoration warden works in a poisoned atmosphere. Nothing may render
    bare skin or hair, and the suit must stay a closed volume in every pose."""
    from warden_model import warden
    for pose in ('idle','running','running_with_gun','mining_with_tool'):
        m=warden(.25,pose,0,math.pi/2,math.pi/2)
        assert m.style['exposed_skin'] is False
        assert m.style['coverage']=='fully sealed'
        assert m.style['mask']=='respirator' and m.style['visor'] and m.style['hood']


def test_warden_palette_stays_small_and_flat_for_compressible_sprites():
    """Sprite bytes track colour variety, not resolution. Every tier must draw
    from one small flat palette, and the finish must skip high-frequency wear."""
    from warden_model import warden
    for tier in range(3):
        m=warden(0,'idle',tier)
        assert m.surface_finish=='field'
        # Every rendered tone is either a palette entry or the mesh builder's
        # own 0.7x underside shade of one; no free-floating extra hues.
        from industrial_art import color as shade
        base={tuple(v) for v in m.palette.values()}
        shades={shade(c,.7) for c in base}
        tones={tuple(c) for _,c,_ in m.faces}
        assert len(base)<=10,(tier,len(base))
        assert tones<=base|shades,(tier,sorted(tones-base-shades))


def test_right_palm_grips_at_48_percent_of_the_shaft_and_the_left_stays_lower():
    for phase in (0,.25,.5,.75):
        m=warden(phase,'mining_with_tool')
        a=m.anchors;shaft=sub(a['tool_top'],a['tool_bottom']);size=length(shaft)
        for side,expected in ((1,.48),(-1,.16)):
            fraction=dot(sub(m.hands[side]['palm'],a['tool_bottom']),a['tool_axis'])/size
            assert abs(fraction-expected)<1e-8


def test_boots_have_a_rounded_outline_and_curved_toe_cap():
    from warden_model import boot_mesh, palette
    m=boot_mesh(palette(0))
    assert len(m.faces)>150
    assert len({round(p[0],5) for v,_,_ in m.faces for p in v})>15
    assert min(p[2] for v,_,_ in m.faces for p in v)>-.10


def test_warden_geometry_budget_stays_below_the_replaced_model():
    """The old explorer carried ~10.4k faces, most of it face/hair detail that
    was invisible in game but expensive to encode. Hold the new budget down."""
    from warden_model import warden
    for pose in ('idle','running','running_with_gun','mining_with_tool'):
        assert len(warden(.25,pose,2,0,0).faces)<7000,pose


def test_warden_stands_at_a_vanilla_character_height():
    """Lock the projected body height into the stock range so the warden never
    dwarfs the machines it builds."""
    import math
    from character_layout import PIXELS_PER_UNIT
    from warden_model import warden

    model = warden(0, 'idle', 0, move_angle=0)
    sin_e, cos_e = math.sin(math.radians(48)), math.cos(math.radians(48))
    screen = [sin_e * y - cos_e * z for face, _, _ in model.faces for _, y, z in face]
    tiles = (max(screen) - min(screen)) * PIXELS_PER_UNIT * 0.25 / 32
    assert 1.50 <= tiles <= 1.65, tiles

    width = [x for face, _, _ in model.faces for x, _, _ in face]
    span = (max(width) - min(width)) * PIXELS_PER_UNIT * 0.25 / 32
    assert 0.7 <= span <= 1.1, span
