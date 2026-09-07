"""Measurable whole-body motion and grip contracts, not a client-playtest claim."""
import math

from body_motion import mining_profile, motion
from explorer_model import explorer
from gait import dot, sub, length


def test_pelvis_and_shoulders_counter_rotate_and_shift_weight():
    hip_yaw=[];shoulder_yaw=[];hip_roll=[];shoulder_roll=[];head=[]
    for frame in range(16):
        m=explorer(frame/16,'running',0)
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
            m=explorer(frame/20,'mining_with_tool',0,facing,facing)
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
    impact=explorer(.5,'mining_with_tool')
    ready=explorer(.28,'mining_with_tool')
    assert impact.motion['torso'].pitch-ready.motion['torso'].pitch>.24
    assert ready.joints['pelvis'][2]-impact.joints['pelvis'][2]>.07
    assert 0<=impact.anchors['tool_tip'][2]<.15
    assert impact.anchors['tool_tip'][2]<impact.anchors['tool_neck'][2]
    for i in range(20):
        m=explorer(i/20,'mining_with_tool')
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
        first=explorer(0,pose)
        last=explorer(1,pose)
        for name in first.joints:
            assert length(sub(first.joints[name],last.joints[name]))<1e-9,(pose,name)


def test_relaxed_arms_swing_opposite_the_advancing_leg():
    first=explorer(0,'running')
    other=explorer(.5,'running')
    assert first.joints['ankle--1'][1]<first.joints['ankle-1'][1]
    assert first.joints['wrist-1'][1]<first.joints['wrist--1'][1]
    assert other.joints['ankle-1'][1]<other.joints['ankle--1'][1]
    assert other.joints['wrist--1'][1]<other.joints['wrist-1'][1]
