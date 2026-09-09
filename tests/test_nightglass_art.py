import hashlib,json
from PIL import Image
from catalog import ROOT,MOD,load_catalog
from atlas_io import Atlas,paths
from warden_model import warden
from character_layout import PIXELS_PER_UNIT


def test_warden_reads_as_sealed_field_gear_with_a_lit_visor_and_seed_pack():
    """The signature silhouette is hood + respirator + back hopper, and the
    visor is emissive so the character stays legible on unlit night terrain."""
    import warden_model
    m=warden(.25,'running',0)
    c=m.palette
    assert m.style['pack']=='seed hopper' and m.style['suit']=='sealed'
    assert sum(1 for _,col,_ in m.faces if col==c['parka'])>100
    assert sum(1 for _,col,_ in m.faces if col==c['suit'])>100
    assert any(glow for _,_,glow in m.faces)
    assert sum(1 for _,col,glow in m.faces if glow and col==c['glass'])>20
    # Each armour tier must be visually distinct, not a recolour of one tone.
    assert len({warden_model.palette(t)['parka'] for t in range(3)})==3
    assert len({warden_model.palette(t)['plate'] for t in range(3)})==3


def test_hd_atlases_double_texel_density_without_changing_world_scale_or_exceeding_texture_limits():
    manifest=json.loads((ROOT/'docs/art/sprite-manifest.json').read_text())
    report=json.loads((ROOT/'docs/art/character-render.json').read_text())
    assert len(report)==15
    for name,entry in report.items():
        spec=manifest[name];view=entry['view']
        assert view['ppu']==PIXELS_PER_UNIT and spec['scale']==.25
        assert view['ppu']*spec['scale']==PIXELS_PER_UNIT*.25
        assert view['width'] in (768,896) and view['height'] in (864,960)
        for filename,digest in entry['files'].items():
            assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest
        for path in paths(spec):
            with Image.open(path) as image:assert max(image.size)<=8192
        atlas=Atlas(spec)
        assert atlas.frame(spec['direction_count']-1,spec['frame_count']-1).getbbox()
        atlas.close()
    assert any('stripes' in manifest[name] for name in report)


def test_striped_atlases_declare_pages_the_engine_accepts():
    """The engine rejects a stripe that declares more lines than the animation has
    directions with "Invalid stripeLine height", and every page must describe exactly
    the pixels its file contains. Both are checked here so a re-render cannot ship a
    character the game refuses to load."""
    manifest=json.loads((ROOT/'docs/art/sprite-manifest.json').read_text())
    striped=[(name,spec) for name,spec in manifest.items() if 'stripes' in spec]
    assert striped
    for name,spec in striped:
        directions=spec['direction_count']
        rows_per_direction=spec['frame_count']//spec['line_length']
        lines=0
        for stripe in spec['stripes']:
            height_in_frames=stripe['height_in_frames']
            assert 0<height_in_frames<=directions,(name,height_in_frames,directions)
            assert height_in_frames%rows_per_direction==0,(name,height_in_frames)
            assert stripe['width_in_frames']==spec['line_length'],(name,stripe['width_in_frames'])
            path=MOD/stripe['filename'].split('__second-nature__/')[1]
            with Image.open(path) as image:
                assert image.size==(spec['width']*stripe['width_in_frames'],
                                    spec['height']*height_in_frames),(name,path.name,image.size)
            lines+=height_in_frames
        assert lines==directions*rows_per_direction,(name,lines)


def test_power_and_train_atlases_are_original_complete_and_have_all_directions():
    report=json.loads((ROOT/'docs/art/energy-manifest.json').read_text())
    for filename,digest in report['files'].items():assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest
    energy=load_catalog()['energy']
    for p in energy['plants']:
        for direction in ('north','east','south','west'):
            assert p['name']+'-'+direction in report['specs']
    signatures=[]
    for t in energy['trains']:
        spec=report['specs'][t['name']]
        assert spec['direction_count']==64 and spec['apply_projection'] is False
        spec=dict(spec,frame_count=1)
        atlas=Atlas(spec);signatures.append(hashlib.sha256(atlas.frame(16).tobytes()).hexdigest())
        assert atlas.frame(63).getbbox();atlas.close()
    assert len(set(signatures))==3
    for spec in report['specs'].values():
        with Image.open(MOD/spec['filename'].split('__second-nature__/')[1]) as image:
            assert max(image.size)<=8192 and image.mode=='RGBA'
