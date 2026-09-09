"""The Restoration Warden: Second Nature's sealed field character.

Design intent
-------------
Second Nature is about reclaiming a poisoned world, so the character is not a
bare adventurer but a *sealed restoration warden*: hooded work parka, full-face
respirator with cheek filters, a lit visor band and a seeded back hopper. The
silhouette (hood + snout + pack) is what reads at 33 screen pixels, so that is
what the geometry spends its budget on.

Efficiency
----------
Sprite bytes are driven by high-frequency colour variation, not by resolution or
by transparent padding. This model is therefore authored for compressibility:

* a ten-entry flat palette per armour tier, reused across every part,
* broad uninterrupted panels (parka front, hopper, visor) instead of filigree,
* no exposed skin, hair or tattoo detail to dapple the shading,
* ``surface_finish='field'`` so the rasterizer keeps low-frequency grime and
  drops the fine speckle that defeats PNG's predictors,
* a ~2.4k face budget where the previous model used ~10.4k.

Geometry is authored in the proven skeleton the locomotion system already
solves for (ground 0, hip 1.10, shoulder 1.65, head 1.95), so gait, two-bone IK
and the tool/weapon aim frames are unchanged.
"""
import math

from industrial_art import Mesh, add, rot, mul
import gait
from gait import sub
from character_rig import limb, hand as build_hand
from body_motion import motion, mining_profile, join_transformed

# Ten flat tones per tier. Sealed rubber and canvas, oxidised brass, lit glass.
SUIT = (86, 92, 84)
RUBBER = (54, 58, 54)
STRAP = (134, 100, 58)
TRIM = (196, 192, 166)
DARK = (40, 43, 40)
LAMP = (150, 226, 176)

PARKA = ((142, 150, 116), (128, 142, 128), (118, 130, 146))
PLATE = ((166, 170, 152), (176, 180, 166), (196, 199, 190))
ACCENT = ((198, 128, 72), (74, 178, 174), (120, 208, 226))
GLASS = ((96, 196, 182), (92, 206, 198), (140, 226, 238))


def palette(tier):
    return {'suit': SUIT, 'rubber': RUBBER, 'strap': STRAP, 'trim': TRIM,
            'dark': DARK, 'lamp': LAMP, 'parka': PARKA[tier], 'plate': PLATE[tier],
            'accent': ACCENT[tier], 'glass': GLASS[tier]}


def loft(mesh, rings, color, sides=20, cap=True):
    """Elliptical rings lofted into a smooth shell."""
    loops = [[(x + rx * math.cos(i * math.tau / sides), y + ry * math.sin(i * math.tau / sides), z)
              for i in range(sides)] for x, y, z, rx, ry in rings]
    if cap:
        mesh.face(list(reversed(loops[0])), color)
        mesh.face(loops[-1], color)
    for a, b in zip(loops, loops[1:]):
        for i in range(sides):
            j = (i + 1) % sides
            mesh.face([a[i], a[j], b[j], b[i]], color)
    return loops


def panel(mesh, center, radius, color, stretch=(1, 1, 1), glow=False, rows=8, columns=18):
    """A rounded slab: masks, visors and pads without box facets."""
    rings = []
    for j in range(rows + 1):
        lat = -math.pi / 2 + j * math.pi / rows
        rings.append([add(center, (radius * stretch[0] * math.cos(lat) * math.cos(i * math.tau / columns),
                                   radius * stretch[1] * math.cos(lat) * math.sin(i * math.tau / columns),
                                   radius * stretch[2] * math.sin(lat))) for i in range(columns)])
    for a, b in zip(rings, rings[1:]):
        for i in range(columns):
            j = (i + 1) % columns
            mesh.face([a[i], a[j], b[j], b[i]], color, glow)


def boot_mesh(colors):
    """Sealed work boot: rounded heel and toe, ribbed sole, capped toe box."""
    boot = Mesh()
    outline = []
    for i in range(7):
        a = i * math.pi / 6
        outline.append((.082 * math.cos(a), .048 + .060 * math.sin(a)))
    for i in range(10):
        a = math.pi + i * math.pi / 9
        outline.append((.104 * math.cos(a), -.134 + .108 * math.sin(a)))

    def shell(levels, color):
        rings = [[(x * sx, -.045 + (y + .045) * sy, z) for x, y in outline] for z, sx, sy in levels]
        boot.face(list(reversed(rings[0])), color)
        boot.face(rings[-1], color)
        for a, b in zip(rings, rings[1:]):
            for i in range(len(a)):
                j = (i + 1) % len(a)
                boot.face([a[i], a[j], b[j], b[i]], color)

    shell([(-.095, .98, .98), (-.074, 1, 1), (-.052, .99, .99)], colors['dark'])
    shell([(-.051, .96, .97), (.020, .94, .94), (.078, .85, .80), (.112, .70, .54)], colors['rubber'])
    panel(boot, (0, -.132, .028), .092, colors['plate'], stretch=(1.02, .92, .56), rows=6, columns=14)
    boot.cyl(0, .010, .088, .068, .038, colors['rubber'], 14)
    return boot


def pack_mesh(colors, tier):
    """Back hopper of graded seed stock: the warden's read-at-a-glance profile."""
    pack = Mesh()
    depth = .112 + .016 * tier
    loft(pack, [(0, .196, 1.235, .108, .044), (0, .202, 1.295, .142, depth),
                (0, .202, 1.475, .148, depth), (0, .196, 1.552, .114, .070),
                (0, .188, 1.590, .058, .038)], colors['parka'], 14)
    # Lid, banding and the germination lamp.
    pack.box((0, .204, 1.578), (.246, depth * 1.7, .032), colors['plate'], .012)
    for z in (1.345, 1.442):
        pack.box((0, .205, z), (.268, depth * 1.76, .017), colors['strap'], .007)
    pack.ball((0, .210, 1.520), .025, colors['lamp'], stretch=(1, .55, 1), glow=True)
    pack.box((-.104, .216, 1.395), (.044, .038, .124), colors['accent'], .012)
    if tier:
        pack.box((.110, .218, 1.412), (.042, .038, .108), colors['plate'], .012)
    return pack


def head_mesh(colors, tier, phase):
    """Hood, full-face respirator, cheek filters and a lit visor band."""
    head = Mesh()
    hood = colors['plate'] if tier == 2 else colors['parka']
    # Hood: an ovoid drawn back off the face, not a helmet sphere.
    head.ball((0, .020, 1.938), .116, hood, stretch=(1.00, 1.10, 1.14))
    # Peaked brim shading the mask; this is what makes the head read as a hood.
    panel(head, (0, -.086, 1.998), .058, hood, stretch=(1.42, 1.00, .26), rows=5, columns=14)
    # Sealed collar closing the hood onto the shoulders.
    loft(head, [(0, .004, 1.762, .100, .088), (0, .008, 1.812, .116, .104),
                (0, .010, 1.850, .104, .094)], colors['rubber'], 16)
    # Respirator: a compact mask face with a short snout.
    panel(head, (0, -.072, 1.898), .078, colors['rubber'], stretch=(.90, .66, .84), rows=7, columns=16)
    panel(head, (0, -.118, 1.868), .042, colors['dark'], stretch=(.84, .62, .62), rows=5, columns=12)
    head.tube((0, -.146, 1.864), (0, -.132, 1.864), .026, colors['trim'], 8)
    # Visor band: one broad emissive strip is the character's signature.
    panel(head, (0, -.096, 1.946), .062, colors['glass'], stretch=(1.24, .42, .34), glow=True,
          rows=5, columns=16)
    panel(head, (0, -.090, 1.968), .064, colors['plate'], stretch=(1.24, .42, .12), rows=4, columns=12)
    for side in (-1, 1):
        head.tube((side * .074, -.058, 1.876), (side * .100, -.024, 1.876), .028, colors['accent'], 8)
        head.tube((side * .100, -.024, 1.876), (side * .107, -.010, 1.876), .018, colors['trim'], 6)
    if tier == 2:
        head.box((0, .026, 2.024), (.16, .14, .042), colors['plate'], .016)
        head.ball((.072, -.030, 2.000), .017, colors['lamp'], glow=True)
    return head


def warden(t=0, pose='idle', tier=0, move_angle=0, aim_angle=0):
    run = pose in ('running', 'running_with_gun')
    gun = 'gun' in pose
    mining = pose == 'mining_with_tool'
    facing = aim_angle if gun else move_angle
    relative = move_angle - facing
    rig = motion(t, pose, tier, relative)
    pelvis, torso, head_rig = rig['pelvis'], rig['torso'], rig['head']
    phase, bob = rig['phase'], rig['bob']
    c = palette(tier)

    m, shell, waist = Mesh(), Mesh(), Mesh()
    stride = (math.sin(relative), -math.cos(relative), 0)
    joints, foot_phases, hands, anchors, soles = {}, {}, {}, {}, {}

    for side in (-1, 1):
        sample = gait.foot_phase(t, side) if run else {'phase': 0, 'along': 0, 'lift': 0, 'pitch': 0, 'mode': 'stance'}
        foot_phases[side] = sample
        hip = pelvis.point((side * .158, 0, 1.10))
        stagger = side * .085 if mining else 0
        ankle = add((side * (.19 if mining else .17), stagger, .115 + sample['lift']), mul(stride, sample['along']))
        knee = gait.solve_two_bone(hip, ankle, gait.THIGH, gait.SHIN, pelvis.vector((0, -1, 0)))
        limb(m, hip, knee, .118, .098, c['suit'], 12)
        limb(m, knee, ankle, .086, .058, c['suit'], 10)
        m.ball(knee, .074, c['plate'], stretch=(.95, .80, .70))
        # Sealed cuff where the trouser meets the boot.
        cuff_a = add(knee, mul(sub(ankle, knee), .80))
        limb(m, cuff_a, ankle, .072, .062, c['rubber'], 10)
        boot = boot_mesh(c)
        cos_p, sin_p = math.cos(sample['pitch']), math.sin(sample['pitch'])
        rolled = Mesh()
        for vertices, color, glow in boot.faces:
            rolled.face([(x, y * cos_p - z * sin_p, y * sin_p + z * cos_p) for x, y, z in vertices], color, glow)
        lowest = min(p[2] for v, _, _ in rolled.faces for p in v)
        correction = max(0, .018 - ankle[2] - lowest)
        m.join(rolled, offset=add(ankle, (0, 0, correction)))
        soles[side] = ankle[2] + lowest + correction
        for name, point in (('hip', hip), ('knee', knee), ('ankle', ankle), ('toe', add(ankle, (0, -.20, .04)))):
            joints[name + '-' + str(side)] = point

    # Sealed undersuit from hip to collar, skinned between pelvis and thorax.
    body = Mesh()
    loft(body, [(0, .004, 1.00, .186, .112), (0, .006, 1.10, .208, .132),
                (0, 0, 1.24, .190, .124), (0, -.004, 1.40, .196, .130),
                (0, -.006, 1.56, .214, .142), (0, .004, 1.68, .196, .118)], c['suit'], 20)

    def skinned(point):
        weight = gait.smooth(max(0, min(1, (point[2] - 1.10) / .40)))
        return add(mul(pelvis.point(point), 1 - weight), mul(torso.point(point), weight))

    join_transformed(m, body, skinned)

    # Work parka: one broad flared shell, the largest flat area on the model.
    secondary = rig['secondary'] * .45
    hem = 1.105 + secondary
    loft(shell, [(0, .006, 1.672, .198, .126), (0, .004, 1.560, .216, .142),
                 (0, 0, 1.380, .226, .150), (0, -.004, 1.220, .232, .156),
                 (0, -.006, hem, .236, .158)], c['parka'], 20, cap=False)
    # Front placket and hem band read the coat as cloth at any zoom.
    shell.tube((0, -.146, 1.630), (0, -.160, hem + .02), .013, c['trim'], 8)
    loft(shell, [(0, -.006, hem + .026, .239, .161), (0, -.006, hem - .004, .236, .158)],
         c['strap'], 20, cap=False)
    # Shoulder yoke and collar.
    loft(shell, [(0, .004, 1.700, .150, .100), (0, .004, 1.742, .120, .086)], c['parka'], 18, cap=False)

    # Chest harness: sample canisters and a shoulder-mounted field slate.
    for side in (-1, 1):
        strap = [(side * .085, -.140, 1.678), (side * .125, -.172, 1.520), (side * .140, -.176, 1.330)]
        for a, b in zip(strap, strap[1:]):
            shell.tube(a, b, .020, c['strap'], 8)
        joints['chest-' + str(side)] = torso.point((side * .132, -.174, 1.425))
    shell.tube((-.140, -.176, 1.395), (.140, -.176, 1.395), .017, c['strap'], 8)
    for side in (-1, 1):
        shell.cyl(side * .148, -.150, 1.245, .046, .150, c['accent'], 12)
        shell.box((side * .148, -.158, 1.402), (.100, .050, .034), c['plate'], .012)
    shell.box((-.128, -.196, 1.560), (.120, .034, .088), c['plate'], .016)
    shell.box((-.128, -.214, 1.560), (.086, .010, .054), c['glass'], .006)

    waist.box((0, -.004, 1.086), (.40, .27, .062), c['strap'], .026)
    waist.box((0, -.150, 1.086), (.072, .028, .046), c['trim'], .010)
    for side in (-1, 1):
        waist.box((side * .214, .026, 1.062), (.086, .112, .128), c['parka'], .022)
        waist.box((side * .214, .026, 1.126), (.090, .116, .016), c['strap'], .006)
    join_transformed(m, waist, pelvis.point)
    join_transformed(shell, pack_mesh(c, tier), lambda p: p)

    if mining:
        theta = mining_profile(t)['angle']
        shaft = torso.vector((0, -math.sin(theta), math.cos(theta)))
        cutting = torso.vector((0, -math.cos(theta), -math.sin(theta)))
        center = torso.point((.075, -.35, 1.415))
        tool_bottom, tool_top = add(center, mul(shaft, -.36)), add(center, mul(shaft, 1.05))
        grips = {side: add(tool_bottom, mul(shaft, 1.41 * fraction)) for side, fraction in ((1, .48), (-1, .16))}
        anchors.update(tool_bottom=tool_bottom, tool_top=tool_top, tool_axis=shaft,
                       right_grip=grips[1], left_grip=grips[-1])
    elif gun:
        weapon_bob = bob + .006 * math.sin(phase * 2)
        grips = {1: (.085, -.385, 1.46 + weapon_bob), -1: (-.034, -.585, 1.455 + weapon_bob)}

    for side in (-1, 1):
        shoulder = torso.point((side * .25, 0, 1.65))
        if mining:
            forward = shaft
            wrist = add(grips[side], mul(shaft, -.065))
            hand_back, curl, bend = mul(cutting, -1), .95, (side * .60, .45, -.3)
        elif gun:
            wrist = grips[side]
            forward = (0, 0, -1) if side > 0 else (0, -1, 0)
            hand_back = (0, -1, 0) if side > 0 else (0, 0, 1)
            curl, bend = .88, (side * .45, .65, -.35)
        else:
            swing = -side * .29 * math.cos(phase - .14) if run else .008 * math.sin(phase)
            wrist = (side * .30 + .01 * math.sin(phase), swing,
                     1.10 + bob + (.035 * math.cos(phase * 2) if run else 0))
            forward, hand_back, curl, bend = (0, 0, -1), (0, 1, 0), .26, (side * .17, .8, -.35)
        elbow = gait.solve_two_bone(shoulder, wrist, .38, .35, bend)
        limb(m, shoulder, elbow, .082, .066, c['suit'], 12)
        limb(m, elbow, wrist, .066, .052, c['suit'], 12)
        m.ball(elbow, .058, c['suit'], stretch=(1, .90, .95))
        # Sealed glove cuff, then the articulated glove itself.
        cuff = add(wrist, mul(sub(elbow, wrist), .16))
        limb(m, cuff, wrist, .058, .052, c['rubber'], 10)
        hands[side] = build_hand(m, wrist, forward, hand_back, side, curl,
                                 (c['rubber'], c['plate'], c['dark']))
        shell.ball((side * .236, 0, 1.646), .076, c['parka'], stretch=(1, .88, .66))
        for name, point in (('shoulder', shoulder), ('elbow', elbow), ('wrist', wrist)):
            joints[name + '-' + str(side)] = point
        # Right pauldron from the first upgrade; both plates at bastion grade.
        if tier > 0 and side == 1 or tier == 2:
            shell.box((side * .268, .010, 1.672), (.132, .196, .078), c['plate'], .028)
            shell.box((side * .268, -.078, 1.680), (.084, .056, .016), c['trim'], .006)
        if tier == 2:
            shell.box((side * .276, .118, 1.616), (.140, .180, .132), c['plate'], .032)

    join_transformed(m, shell, torso.point)

    head = head_mesh(c, tier, phase)

    def head_point(point):
        return torso.point(head_rig.point(point))

    join_transformed(m, head, head_point)
    m.tube(torso.point((0, 0, 1.68)), head_point((0, .002, 1.79)), .074, c['rubber'], 12)
    joints.update(pelvis=pelvis.point((0, 0, 1.08)), thorax=torso.point((0, 0, 1.53)),
                  head=head_point((0, 0, 1.95)), neck=head_point((0, 0, 1.78)))

    if gun:
        z = weapon_bob
        m.box((.028, -.51, 1.447 + z), (.145, .53, .116), c['dark'], .025)
        m.box((.028, -.47, 1.516 + z), (.065, .34, .033), c['plate'], .009)
        m.tube((.028, -.67, 1.448 + z), (.028, -1.12, 1.448 + z), .025, c['plate'], 12)
        for j in range(3):
            m.tube((.028, -.80 + j * .070, 1.448 + z), (.028, -.772 + j * .070, 1.448 + z), .036, c['rubber'], 10)
        m.box((.028, -.39, 1.315 + z), (.085, .145, .19), c['accent'], .016)
        m.box((.028, -.24, 1.443 + z), (.10, .18, .12), c['strap'], .025)
        m.ball((.028, -.30, 1.520 + z), .022, c['lamp'], glow=True)
        anchors.update(gun_root=(.028, -.67, 1.448 + z), gun_muzzle=(.028, -1.12, 1.448 + z),
                       right_grip=grips[1], left_grip=grips[-1])
    if mining:
        m.tube(tool_bottom, tool_top, .026, c['strap'], 12)
        rear, neck, tip = (add(tool_top, mul(cutting, d)) for d in (-.22, .17, .50))
        m.tube(rear, neck, .064, c['plate'], 12)
        sideways = torso.vector((.072, 0, 0))
        up = mul(shaft, .051)
        ring = [add(neck, sideways), add(neck, up), add(neck, mul(sideways, -1)), add(neck, mul(up, -1))]
        for i in range(4):
            m.face([ring[i], ring[(i + 1) % 4], tip], c['trim'])
        anchors.update(tool_tip=tip, tool_neck=neck, strike_direction=cutting, tool_grip=grips[1])

    result = Mesh()
    result.join(m, facing)
    result.anchors = {name: rot(p, facing) for name, p in anchors.items()}
    result.joints = {name: rot(p, facing) for name, p in joints.items()}
    result.hands = {side: {name: rot(p, facing) for name, p in points.items()} for side, points in hands.items()}
    result.aim_angle, result.move_angle, result.pose = facing, move_angle, pose
    result.foot_phases, result.sole_heights, result.motion = foot_phases, soles, rig
    result.surface_finish = 'field'
    result.smooth_colors = {c['suit'], c['parka'], c['rubber'], c['plate'], c['glass']}
    result.palette = c
    result.style = {'suit': 'sealed', 'mask': 'respirator', 'visor': True, 'hood': True,
                    'pack': 'seed hopper', 'coverage': 'fully sealed', 'exposed_skin': False,
                    'tones': sorted({tuple(v) for k, v in c.items()})}
    return result
