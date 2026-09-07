"""Hierarchical, cyclic human motion for the adult clothed explorer.

Pure authoring math, not runtime physics. Pelvis and thorax counter-rotate;
the head stabilizes above them. Tools retain their own grip/aim frame, and
secondary garment motion is bounded and reduced by rigid armor.
"""
import math
from dataclasses import dataclass
from gait import add, sub, mul, smooth

TAU = math.tau


@dataclass(frozen=True)
class Transform:
    pivot: tuple = (0, 0, 0)
    offset: tuple = (0, 0, 0)
    pitch: float = 0
    roll: float = 0
    yaw: float = 0

    def vector(self, p):
        x, y, z = p
        c, s = math.cos(self.pitch), math.sin(self.pitch)
        y, z = y * c - z * s, y * s + z * c
        c, s = math.cos(self.roll), math.sin(self.roll)
        x, z = x * c + z * s, -x * s + z * c
        c, s = math.cos(self.yaw), math.sin(self.yaw)
        return x * c - y * s, x * s + y * c, z

    def point(self, p):
        return add(add(self.pivot, self.offset), self.vector(sub(p, self.pivot)))


def join_transformed(destination, source, transform):
    for vertices, color, glow in source.faces:
        destination.face([transform(p) for p in vertices], color, glow)


def keyframed(t, keys):
    """Cyclic, eased anticipation, fast downstroke, brief impact and recovery."""
    t %= 1
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if a <= t <= b:
            return va + (vb - va) * smooth((t - a) / (b - a))
    return keys[-1][1]


def mining_profile(t):
    return {
        'angle': math.radians(keyframed(t, [(0, 20), (.28, -32), (.50, 137), (.56, 139), (.66, 123), (1, 20)])),
        'lean': keyframed(t, [(0, .035), (.27, -.065), (.50, .20), (.57, .205), (.71, .09), (1, .035)]),
        'drop': keyframed(t, [(0, -.008), (.28, .012), (.50, -.073), (.57, -.065), (.72, -.020), (1, -.008)]),
        'twist': keyframed(t, [(0, -.015), (.28, -.11), (.50, .095), (.60, .070), (1, -.015)]),
        'drive': keyframed(t, [(0, 0), (.28, .025), (.50, -.035), (.60, -.025), (1, 0)]),
    }


def motion(t, pose, tier, relative_stride=0):
    phase = t * TAU
    running = pose in ('running', 'running_with_gun')
    mining = pose == 'mining_with_tool'
    if running:
        sway = math.sin(phase)
        bob = -.022 - .025 * math.cos(phase * 2)
        pelvis = Transform((0, 0, 1.08), (.024 * sway, 0, bob), roll=.040 * sway, yaw=.085 * sway)
        torso = Transform((0, 0, 1.10), (.012 * sway, 0, bob),
                          pitch=.095 * math.cos(relative_stride),
                          roll=.095 * math.sin(relative_stride) - .045 * sway, yaw=-.080 * sway)
        head = Transform((0, 0, 1.77), (0, 0, -.008 * math.cos(phase * 2 - .35)),
                         pitch=-torso.pitch * .65 + .018 * math.sin(phase * 2 - .3),
                         roll=-torso.roll * .65, yaw=-torso.yaw * .60)
        secondary = -.032 * math.cos(phase * 2 - .65) + .006 * math.sin(phase - .2)
    elif mining:
        p = mining_profile(t)
        bob = p['drop']
        pelvis = Transform((0, 0, 1.08), (.018 * math.sin(phase), p['drive'] * .30, bob),
                           pitch=p['lean'] * .24, roll=-.02 * math.sin(phase), yaw=p['twist'] * .55)
        torso = Transform((0, 0, 1.10), (0, p['drive'], bob), pitch=p['lean'], yaw=p['twist'])
        head = Transform((0, 0, 1.77), pitch=.055 - p['lean'] * .25, yaw=-p['twist'] * .35)
        # A bounded recoil after the impact, not unrestrained rigid-plate wobble.
        impact_age = (t % 1) - .50
        secondary = (.029 * math.exp(-impact_age * 15) * math.sin(impact_age * 52)
                     if impact_age > 0 else .007 * math.sin(phase))
    else:
        bob = .004 * math.sin(phase)
        pelvis = Transform((0, 0, 1.08), offset=(.005 * math.sin(phase), 0, bob))
        torso = Transform((0, 0, 1.10), offset=(0, 0, bob), roll=.006 * math.sin(phase))
        head = Transform((0, 0, 1.77), pitch=.007 * math.sin(phase + .4))
        secondary = .003 * math.sin(phase - .3)
    secondary *= (1, .35, .10)[tier]
    return {'pelvis': pelvis, 'torso': torso, 'head': head, 'bob': bob,
            'secondary': secondary, 'phase': phase, 'running': running, 'mining': mining}
