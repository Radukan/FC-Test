"""Adult, fully clothed explorer with hierarchical human locomotion and tool work.

The pelvis, thorax and head have distinct transforms. Arms solve between moving
shoulders and actual grips; gun aim stays independent of body counter-rotation.
"""
import math
from industrial_art import Mesh, STEEL, DARK, EDGE, GOLD, COPPER, TEAL, WHITE, add, rot, mul
import gait
from character_rig import limb, hand as build_hand
from body_motion import motion, mining_profile, join_transformed
import goth_details as goth

SKIN = goth.PALE
HAIR = goth.HAIR
SUIT = goth.CLOTH


def loft(mesh, rings, color, sides=24):
    loops = [[(x + rx * math.cos(i * math.tau / sides), y + ry * math.sin(i * math.tau / sides), z)
              for i in range(sides)] for x, y, z, rx, ry in rings]
    mesh.face(list(reversed(loops[0])), color)
    mesh.face(loops[-1], color)
    for a, b in zip(loops, loops[1:]):
        for i in range(sides):
            j = (i + 1) % sides
            mesh.face([a[i], a[j], b[j], b[i]], color)


def rounded_panel(mesh, center, radius, color, stretch=(1, 1, 1)):
    # Higher curvature resolution on fitted fabric/armor than a low-sided primitive.
    rows, columns = 12, 28
    rings = []
    for j in range(rows + 1):
        latitude = -math.pi / 2 + j * math.pi / rows
        rings.append([add(center, (radius * stretch[0] * math.cos(latitude) * math.cos(i * math.tau / columns),
                                  radius * stretch[1] * math.cos(latitude) * math.sin(i * math.tau / columns),
                                  radius * stretch[2] * math.sin(latitude))) for i in range(columns)])
    for a, b in zip(rings, rings[1:]):
        for i in range(columns):
            j = (i + 1) % columns
            mesh.face([a[i], a[j], b[j], b[i]], color)


def chest_panel(mesh, side, color, displacement=0):
    """Fitted teardrop volume: fullness low down, taper blended into the thorax."""
    x=side*.108
    rings=[(x,-.10,1.355,.025,.015),(x,-.114,1.390,.081,.051),
           (x,-.116,1.438,.119,.085),(x,-.105,1.490,.118,.081),
           (x,-.083,1.550,.088,.055),(x,-.055,1.610,.045,.022),
           (x,-.040,1.640,.012,.005)]
    loft(mesh,[(a,b,z+displacement,rx,ry) for a,b,z,rx,ry in rings],color,28)
    return rings


def boot_mesh(armor):
    """Rounded heel/toe outline and curved toe cap, not three beveled boxes."""
    boot=Mesh();outline=[]
    for i in range(9):
        a=i*math.pi/8;outline.append((.087*math.cos(a),.050+.063*math.sin(a)))
    for i in range(13):
        a=math.pi+i*math.pi/12;outline.append((.109*math.cos(a),-.139+.112*math.sin(a)))
    def shell(levels,color):
        rings=[[(x*sx,-.045+(y+.045)*sy,z) for x,y in outline] for z,sx,sy in levels]
        boot.face(list(reversed(rings[0])),color);boot.face(rings[-1],color)
        for a,b in zip(rings,rings[1:]):
            for i in range(len(a)):
                j=(i+1)%len(a);boot.face([a[i],a[j],b[j],b[i]],color)
    shell([(-.095,.98,.98),(-.078,1,1),(-.056,.99,.99)],(20,24,22))
    shell([(-.055,.96,.97),(.012,.94,.94),(.069,.86,.81),(.103,.71,.55)],DARK)
    rounded_panel(boot,(0,-.137,.024),.096,armor,stretch=(1.02,.94,.59))
    boot.cyl(0,.007,.085,.071,.040,DARK,20)
    return boot


def explorer(t=0, pose='idle', tier=0, move_angle=0, aim_angle=0):
    run, gun, mining = pose in ('running', 'running_with_gun'), 'gun' in pose, pose == 'mining_with_tool'
    facing = aim_angle if gun else move_angle
    relative = move_angle - facing
    rig = motion(t, pose, tier, relative)
    pelvis, torso, head_rig = rig['pelvis'], rig['torso'], rig['head']
    phase, bob = rig['phase'], rig['bob']
    m, shell, waist, skin = Mesh(), Mesh(), Mesh(), Mesh()
    armor = (42, 43, 53) if tier == 0 else ((62, 59, 76) if tier == 1 else (88, 85, 103))
    stride = (math.sin(relative), -math.cos(relative), 0)
    joints, foot_phases, hands, anchors, soles = {}, {}, {}, {}, {}

    for side in (-1, 1):
        sample = gait.foot_phase(t, side) if run else {'phase': 0, 'along': 0, 'lift': 0, 'pitch': 0, 'mode': 'stance'}
        foot_phases[side] = sample
        hip = pelvis.point((side * .158, 0, 1.10))
        # A staggered, braced stance transfers weight through a mining strike.
        stagger = side * .085 if mining else 0
        ankle = add((side * (.19 if mining else .17), stagger, .115 + sample['lift']), mul(stride, sample['along']))
        knee = gait.solve_two_bone(hip, ankle, gait.THIGH, gait.SHIN, pelvis.vector((0, -1, 0)))
        limb(m, hip, knee, .127, .105, SKIN, 20)
        shorts_end=add(hip,mul(gait.sub(knee,hip),.50))
        limb(m,hip,shorts_end,.135,.125,SUIT,20)
        if side==1:goth.tattoo(m,hip,knee,.132,.108,side)
        limb(m, knee, ankle, .090, .061, SUIT, 16)
        m.ball(knee, .111, armor, stretch=(.95, 1, .76))
        top = add(add(knee, mul(gait.sub(ankle, knee), .15)), (0, -.046, 0))
        bottom = add(add(knee, mul(gait.sub(ankle, knee), .84)), (0, -.046, 0))
        limb(m, top, bottom, .075, .050, armor, 14)
        boot = boot_mesh(armor)
        c, s = math.cos(sample['pitch']), math.sin(sample['pitch'])
        rolled = Mesh()
        for vertices, color, glow in boot.faces:
            rolled.face([(x, y * c - z * s, y * s + z * c) for x, y, z in vertices], color, glow)
        lowest = min(p[2] for v, _, _ in rolled.faces for p in v)
        sole_correction = max(0, .018 - ankle[2] - lowest)
        m.join(rolled, offset=add(ankle, (0, 0, sole_correction)))
        soles[side] = ankle[2] + lowest + sole_correction
        belt = add(hip, mul(gait.sub(knee, hip), .44))
        m.ball(belt, .126, (68, 56, 42), stretch=(1, 1, .24))
        for name, point in [('hip', hip), ('knee', knee), ('ankle', ankle), ('toe', add(ankle, (0, -.20, .04)))]:
            joints[name + '-' + str(side)] = point

    # Smoothly skinned waist-to-thorax fabric, with separately moving rigid gear.
    loft(skin, [(0, .006, 1.00, .215, .12), (0, .006, 1.09, .254, .153),
                (0, 0, 1.21, .164, .104), (0, 0, 1.36, .171, .115),
                (0, -.005, 1.52, .227, .155), (0, .005, 1.66, .24, .134)], SUIT)
    def skinned(point):
        weight = gait.smooth(max(0, min(1, (point[2] - 1.10) / .40)))
        return add(mul(pelvis.point(point), 1 - weight), mul(torso.point(point), weight))
    join_transformed(m, skin, skinned)
    secondary = rig['secondary'] * .45
    for side in (-1, 1):
        center = (side * .108, -.116, 1.438 + secondary)
        chest_panel(shell,side,armor,secondary)
        joints['chest-' + str(side)] = torso.point(center)
        # The fitted protective garment remains fully covered. Harness straps
        # follow its curved surface; heavier chest plates strongly damp motion.
        points = [(side * .13, -.148, 1.63), (side * .156, -.199, 1.52 + secondary),
                  (side * .166, -.211, 1.44 + secondary), (side * .12, -.152, 1.18)]
        for a, b in zip(points, points[1:]):
            shell.tube(a, b, .019, (117, 78, 38), 8)
        shell.box((side * .145, -.198, 1.34), (.052, .027, .063), EDGE, .009)
    shell.box((0, -.122, 1.27), (.22, .045, .25), DARK, .035)
    for i in range(4):
        shell.box((0, -.150, 1.17 + i * .056), (.14, .016, .018), EDGE, .005)
    waist.box((0, 0, 1.11), (.43, .30, .09), (92, 69, 43), .045)
    waist.box((0, -.163, 1.11), (.10, .035, .075), EDGE, .01)
    for side in (-1, 1):
        waist.box((side * .225, .025, 1.10), (.12, .15, .205), DARK, .025)
        waist.tube((side * .238, .016, 1.065), (side * .157, -.077, 1.21), .012, COPPER, 8)
    skirt_rings=goth.skirt(m,pelvis,joints,phase,tier)
    join_transformed(m, waist, pelvis.point)
    shell.box((0, .19, 1.40), (.31, .16, .47), armor, .05)
    for x in (-.10, .10):
        shell.cyl(x, .245, 1.28, .049, .28, EDGE, 14)
        shell.tube((x, .26, 1.58), (x * .8, .11, 1.72), .018, DARK, 8)
    for i in range(5):
        shell.box((0, .285, 1.28 + i * .051), (.21, .014, .018), DARK, .002)
    shell.box((.07, .286, 1.56), (.07, .013, .022), TEAL, .002)

    if mining:
        theta = mining_profile(t)['angle']
        shaft = torso.vector((0, -math.sin(theta), math.cos(theta)))
        cutting = torso.vector((0, -math.cos(theta), -math.sin(theta)))
        back = mul(cutting, -1)
        center = torso.point((.075, -.35, 1.415))
        tool_bottom, tool_top = add(center, mul(shaft, -.36)), add(center, mul(shaft, 1.05))
        grips = {side:add(tool_bottom,mul(shaft,1.41*fraction)) for side,fraction in ((1,.48),(-1,.16))}
        anchors.update(tool_bottom=tool_bottom, tool_top=tool_top, tool_axis=shaft,
                       right_grip=grips[1], left_grip=grips[-1])
    elif gun:
        # The weapon stays on the requested aim axis while the shoulders sway.
        weapon_bob = bob + .006 * math.sin(phase * 2)
        grips = {1: (.085, -.385, 1.46 + weapon_bob), -1: (-.034, -.585, 1.455 + weapon_bob)}

    for side in (-1, 1):
        shoulder = torso.point((side * .273, 0, 1.65))
        if mining:
            forward = shaft
            wrist = add(grips[side], mul(shaft, -.065))
            hand_back, curl, bend = back, .95, (side * .60, .45, -.3)
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
        limb(m, shoulder, elbow, .086, .074, SKIN, 20)
        limb(m, elbow, wrist, .071, .055, SKIN, 20)
        goth.tattoo(m,elbow,wrist,.074,.057,side)
        goth.tattoo(m,shoulder,elbow,.091,.077,side)
        m.ball(shoulder, .112, armor, stretch=(1.06, .95, .80))
        m.ball(elbow, .077, EDGE, stretch=(1, .8, .8))
        hands[side] = build_hand(m, wrist, forward, hand_back, side, curl)
        for name, point in [('shoulder', shoulder), ('elbow', elbow), ('wrist', wrist)]:
            joints[name + '-' + str(side)] = point
        if tier > 0:
            shell.box((side * .30, .012, 1.67), (.16, .255, .135), armor, .035)
            shell.box((side * .30, -.09, 1.69), (.10, .09, .025), GOLD, .008)
        if tier == 2:
            shell.box((side * .31, .12, 1.64), (.18, .23, .21), armor, .04)
            shell.box((side * .31, .02, 1.75), (.13, .05, .025), GOLD, .006)
    join_transformed(m, shell, torso.point)

    head = head_mesh(phase, tier)
    def head_point(point):
        return torso.point(head_rig.point(point))
    join_transformed(m, head, head_point)
    m.tube(torso.point((0, 0, 1.68)), head_point((0, -.005, 1.80)), .073, SKIN, 16)
    joints.update(pelvis=pelvis.point((0, 0, 1.08)), thorax=torso.point((0, 0, 1.53)),
                  head=head_point((0, 0, 1.95)), neck=head_point((0, 0, 1.78)))

    if gun:
        z = weapon_bob
        m.box((.028, -.51, 1.447 + z), (.145, .53, .116), DARK, .025)
        m.box((.028, -.47, 1.516 + z), (.065, .34, .033), EDGE, .009)
        m.tube((.028, -.67, 1.448 + z), (.028, -1.12, 1.448 + z), .025, STEEL, 14)
        for j in range(4):
            m.tube((.028, -.79 + j * .055, 1.448 + z), (.028, -.766 + j * .055, 1.448 + z), .036, EDGE, 12)
        m.box((.028, -.39, 1.315 + z), (.085, .145, .19), COPPER, .016)
        m.box((.028, -.24, 1.443 + z), (.10, .18, .12), (104, 89, 64), .025)
        anchors.update(gun_root=(.028, -.67, 1.448 + z), gun_muzzle=(.028, -1.12, 1.448 + z),
                       right_grip=grips[1], left_grip=grips[-1])
    if mining:
        m.tube(tool_bottom, tool_top, .026, (96, 78, 53), 14)
        # Forged, tapered point follows the downward cutting tangent.
        rear, neck, tip = (add(tool_top, mul(cutting, distance)) for distance in (-.22, .17, .50))
        m.tube(rear, neck, .064, EDGE, 14)
        sideways = torso.vector((.072, 0, 0))
        up = mul(shaft, .051)
        ring = [add(neck, sideways), add(neck, up), add(neck, mul(sideways, -1)), add(neck, mul(up, -1))]
        for i in range(4):
            m.face([ring[i], ring[(i + 1) % 4], tip], STEEL)
        anchors.update(tool_tip=tip, tool_neck=neck, strike_direction=cutting, tool_grip=grips[1])
    result = Mesh()
    result.join(m, facing)
    result.anchors = {name: rot(p, facing) for name, p in anchors.items()}
    result.joints = {name: rot(p, facing) for name, p in joints.items()}
    result.hands = {side: {name: rot(p, facing) for name, p in points.items()} for side, points in hands.items()}
    result.aim_angle, result.move_angle, result.pose = facing, move_angle, pose
    result.foot_phases, result.sole_heights, result.motion = foot_phases, soles, rig
    result.surface_finish = 'goth'
    result.style={'skin':SKIN,'hair':'wolfcut','tattoos':True,'skirt':True,'coverage':'opaque undershorts','skirt_rings':skirt_rings}
    return result

def head_mesh(phase,tier):
    head=Mesh()
    head.ball((0,-.006,1.951),.151,SKIN,stretch=(.87,.91,1.18))
    head.ball((0,-.012,1.865),.12,SKIN,stretch=(.86,.82,.82))
    head.ball((0,-.149,1.946),.028,(229,215,224),stretch=(.55,1,.9))
    head.box((0,-.135,1.895),(.070,.014,.016),(49,24,46),.005)
    for x in (-.062,.062):
        head.tube((x-.027,-.148,1.989),(x+.027,-.148,1.989),.007,(24,20,30),8)
        head.ball((x,-.151,1.977),.021,(221,220,218),stretch=(1,.25,.48))
        head.ball((x,-.158,1.978),.011,(89,111,125),stretch=(1,.25,1))
        head.tube((x-.028,-.122,2.007),(x+.022,-.129,2.012),.009,HAIR,6)
        head.tube((x,-.136,1.96),(x+.015,-.135,1.94),.0035,(25,21,32),6)
    goth.wolfcut(head,phase)
    for side in (-1,1):
        head.ball((side*.14,.01,1.948),.025,SKIN)
        for i in range(10):
            a=i*math.tau/10;b=(i+1)*math.tau/10
            head.tube((side*.155,.02+.018*math.cos(a),1.91+.025*math.sin(a)),
                      (side*.155,.02+.018*math.cos(b),1.91+.025*math.sin(b)),.0045,goth.SILVER,6)
    head.box((0,0,1.715),(.155,.19,.030),(23,20,28),.008)
    head.ball((0,-.112,1.674),.015,goth.SILVER,stretch=(.8,.4,1))
    if tier==2:head.box((0,-.118,1.841),(.20,.055,.060),(39,38,48),.015)
    return head
