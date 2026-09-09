import configparser,hashlib,json,math,re,struct,subprocess
from pathlib import Path
import pytest
from PIL import Image
from catalog import ROOT,MOD,load_catalog


def test_no_long_dash_punctuation_in_repository_text():
    files=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
    for name in set(files):
        p=ROOT/name
        if p.suffix.lower() not in {'.md','.txt','.lua','.py','.cfg','.json','.yml','.yaml','.csv'} or not p.is_file():continue
        text=p.read_text()
        assert '\u2014' not in text and '\u2013' not in text,name


def test_equipment_descriptions_are_about_objects_not_development_requests():
    catalog=load_catalog()
    forbidden=re.compile(r'from the (?:very )?(?:start|beginning)|early[- ]game|mid[- ]game|late[- ]game|native consumable|no exotic|not conjured|no passive invulnerability|your prompt|woodless frontier|now (?:you|from)',re.I)
    for group in ('items','fluids','machines','expedition'):
        for entry in catalog[group]:
            assert not forbidden.search(entry['description']),(entry['name'],entry['description'])
            assert len(entry['description'])>25


def test_menu_score_is_a_complete_stereo_vorbis_track():
    path=MOD/'sound/music/after-the-ash.ogg';data=path.read_bytes()
    assert data[:4]==b'OggS' and len(data)>100000
    start=27+data[26]
    assert data[start:start+7]==b'\x01vorbis'
    channels=data[start+11];rate=struct.unpack_from('<I',data,start+12)[0]
    assert channels==2 and rate==32000
    position=0;last_granule=0
    while position<len(data):
        assert data[position:position+4]==b'OggS'
        count=data[position+26];header=27+count
        body=sum(data[position+27:position+header])
        granule=struct.unpack_from('<Q',data,position+6)[0]
        if granule<2**63:last_granule=max(last_granule,granule)
        position+=header+body
    assert abs(last_granule/rate-96)<.1
    report=json.loads((ROOT/'docs/art/menu-score.json').read_text())
    assert report['sha256']==hashlib.sha256(data).hexdigest()
    assert .03<report['decoded_rms']<.15 and report['decoded_peak']<.9


def test_native_armed_rows_are_paired_not_a_full_circle_turnaround():
    from character_layout import ARMED_ROWS,pose_angles
    assert len(ARMED_ROWS)==18
    assert [a for a,_ in ARMED_ROWS]==[0]*3+[1]*4+[2]*4+[3]*4+[4]*3
    for row,(aim,stride) in enumerate(ARMED_ROWS):
        movement,looking=pose_angles('running_with_gun',row)
        assert looking==aim*math.tau/8 and movement==stride*math.tau/8


def test_weapon_muzzle_and_torso_share_the_requested_aim():
    from character_layout import ARMED_ROWS,pose_angles,projected
    from warden_model import warden
    for row in range(18):
        movement,aim=pose_angles('running_with_gun',row)
        mesh=warden(.25,'running_with_gun',0,movement,aim)
        a=projected(mesh.anchors['gun_root']);b=projected(mesh.anchors['gun_muzzle'])
        dx,dy=b[0]-a[0],b[1]-a[1];size=math.hypot(dx,dy)
        assert abs(dx/size-math.sin(aim))<1e-6
        assert abs(dy/size+math.cos(aim))<1e-6
        assert mesh.aim_angle==aim


def test_pickaxe_and_shadow_fit_every_mining_frame_and_direction():
    from character_layout import pose_angles,assert_frame_fits
    from gait import MINING_FRAMES
    from warden_model import warden
    for tier in range(3):
        for direction in range(8):
            movement,aim=pose_angles('mining_with_tool',direction)
            for frame in range(MINING_FRAMES):
                mesh=warden(frame/MINING_FRAMES,'mining_with_tool',tier,movement,aim)
                assert_frame_fits(mesh,(tier,direction,frame))
                assert 'tool_tip' in mesh.anchors and 'tool_grip' in mesh.anchors


def test_character_frames_share_a_consistent_foot_anchor():
    from character_layout import frame_spec, PIXELS_PER_UNIT
    art=json.loads((ROOT/'docs/art/sprite-manifest.json').read_text())
    for tier in range(3):
        for pose in ('idle','idle_with_gun','running','running_with_gun','mining_with_tool'):
            spec=art[f'warden-{tier}-{pose}']
            view=frame_spec(pose)
            report=json.loads((ROOT/'docs/art/character-render.json').read_text())[f'warden-{tier}-{pose}']
            assert report['view']==view and view['ppu']==PIXELS_PER_UNIT and spec['scale']==.25
            crop=report['crop']
            assert (spec['width'],spec['height'])==(crop[2]-crop[0],crop[3]-crop[1])
            assert spec['apply_projection'] is False
            pivots=(view['width']/2-crop[0],view['height']*view['origin']-crop[1])
            for axis,size in enumerate((spec['width'],spec['height'])):
                world=(pivots[axis]-size/2)*spec['scale']+spec['shift'][axis]*32
                assert abs(world)<1e-4


def test_character_asset_alpha_does_not_touch_top_or_sides():
    art=json.loads((ROOT/'docs/art/sprite-manifest.json').read_text())
    for tier in range(3):
        s=art[f'warden-{tier}-mining_with_tool']
        from atlas_io import Atlas
        image=Atlas(s)
        for direction in range(s['direction_count']):
            for frame in range(s['frame_count']):
                tile=image.frame(direction,frame)
                alpha=tile.getchannel('A').point(lambda n:255 if n>16 else 0);box=alpha.getbbox()
                assert box and min(box[0],box[1],s['width']-box[2],s['height']-box[3])>=2,(tier,direction,frame,box)


def test_shipped_sprites_are_colour_optimized_and_stay_true_rgba():
    """Every shipped PNG must be RGBA and reasonably encoded.

    The engine's atlas builder and several ledgers expect four channels, and
    oxipng will silently rewrite any <=256-colour sheet as an indexed image.
    A full re-optimisation of 630 files is far too slow for the suite, so this
    samples the largest atlases, which are where a regression would matter.
    """
    from catalog import MOD
    from PIL import Image

    files = sorted((MOD / 'graphics').rglob('*.png'))
    assert len(files) > 500
    for path in files:
        with Image.open(path) as image:
            assert image.mode == 'RGBA', (path.name, image.mode)

    ledger = json.loads((ROOT / 'docs/art/optimization.json').read_text())
    assert ledger['total_bytes'] == sum(p.stat().st_size for p in files)

    # Re-optimising a 47 MPx atlas costs minutes, so spot-check a mid-sized
    # sheet instead; `tools/optimize_sprites.py --check` covers all of them.
    from optimize_sprites import budget, optimize_bytes
    ranked = sorted(files, key=lambda p: -p.stat().st_size)
    path = ranked[len(ranked) // 2]
    data = path.read_bytes()
    assert len(optimize_bytes(data, budget(path.relative_to(MOD)))) >= len(data), path.name
