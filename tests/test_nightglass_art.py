import hashlib,json
from PIL import Image
from catalog import ROOT,MOD,load_catalog
from atlas_io import Atlas,paths
from explorer_model import explorer
import goth_details


def test_goth_style_uses_pale_skin_ink_wolfcut_and_a_covered_pleated_skirt():
    m=explorer(.25,'running',0)
    assert m.style['skin']==goth_details.PALE
    assert m.style['hair']=='wolfcut' and m.style['tattoos'] and m.style['skirt']
    assert m.style['coverage']=='opaque undershorts'
    assert sum(c==goth_details.INK for _,c,_ in m.faces)>100
    assert sum(c==goth_details.PALE for _,c,_ in m.faces)>100
    assert len(m.style['skirt_rings'][-1])==32
    assert min(p[2] for p in m.style['skirt_rings'][-1])>.70


def test_hd_atlases_double_texel_density_without_changing_world_scale_or_exceeding_texture_limits():
    manifest=json.loads((ROOT/'docs/art/sprite-manifest.json').read_text())
    report=json.loads((ROOT/'docs/art/character-render.json').read_text())
    assert len(report)==15
    for name,entry in report.items():
        spec=manifest[name];view=entry['view']
        assert view['ppu']==160 and spec['scale']==.25 and view['ppu']*spec['scale']==40
        assert view['width'] in (768,896) and view['height'] in (864,960)
        for filename,digest in entry['files'].items():
            assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest
        for path in paths(spec):
            with Image.open(path) as image:assert max(image.size)<=8192
        atlas=Atlas(spec)
        assert atlas.frame(spec['direction_count']-1,spec['frame_count']-1).getbbox()
        atlas.close()
    assert any('stripes' in manifest[name] for name in report)


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
