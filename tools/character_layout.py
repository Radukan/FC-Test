"""Character pose layout and framing contract for stable Factorio.
The 18 armed rows are not eighteen ordinary full-circle facings. They encode the
north/east/south half of eight gun facings paired with independent stride axes;
the engine mirrors west-facing cases and reverses opposing movement cycles.
"""
import math
TAU=math.tau
# (gun facing, stride axis), in the stable mirrored layout. N=0, NE=1, E=2, ...
ARMED_ROWS=((0,0),(0,1),(0,2),
            (1,0),(1,1),(1,2),(1,3),
            (2,0),(2,1),(2,2),(2,3),
            (3,0),(3,1),(3,2),(3,3),
            (4,0),(4,1),(4,2))
WIDTH=768
HEIGHT=864
PIXELS_PER_UNIT=160
ORIGIN=440/864
SAFE_MARGIN=20

def pose_angles(pose,row):
    if pose=='running_with_gun':
        aim,move=ARMED_ROWS[row]
        return move*TAU/8,aim*TAU/8
    angle=row*TAU/8
    return angle,angle

def frame_spec(pose=None):
    if pose=='mining_with_tool':return {'width':896,'height':960,'origin':496/960,'ppu':PIXELS_PER_UNIT,'scale':.25}
    return {'width':WIDTH,'height':HEIGHT,'origin':ORIGIN,'ppu':PIXELS_PER_UNIT,'scale':.25}

def projected(point,pose=None):
    # Character ground axes are authored in screen/map space, not foreshortened twice.
    spec=frame_spec(pose)
    return (spec['width']/2+point[0]*spec['ppu'],
            spec['height']*spec['origin']+(point[1]-point[2]*math.cos(math.radians(48)))*spec['ppu'])

def assert_frame_fits(mesh,context):
    pose=getattr(mesh,"pose",None);spec=frame_spec(pose)
    points=[projected(p,pose) for vertices,_,_ in mesh.faces for p in vertices]
    # The cast shadow shares the canvas and must not be abruptly cropped either.
    for vertices,_,_ in mesh.faces:
        for x,y,z in vertices:points.append(projected((x+z*.65/1.35,y+z*.78/1.35,0),pose))
    xs=[p[0] for p in points];ys=[p[1] for p in points]
    bounds=(min(xs),min(ys),max(xs),max(ys))
    assert bounds[0]>=SAFE_MARGIN and bounds[1]>=SAFE_MARGIN and bounds[2]<=spec['width']-SAFE_MARGIN and bounds[3]<=spec['height']-SAFE_MARGIN,(context,bounds)
    return bounds
