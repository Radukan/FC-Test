import hashlib,json
from PIL import Image,ImageChops,ImageStat
from catalog import ROOT,MOD,load_catalog


def test_all_catalog_item_building_icons_have_individual_art_and_canonical_size():
    report=json.loads((ROOT/'docs/art/icon-manifest.json').read_text())
    k=load_catalog()
    expected={x['name'] for group in ('items','fluids','machines','expedition') for x in k[group]}
    assert expected<=set(report)
    hashes={}
    for name,spec in report.items():
        path=ROOT/spec['file'];digest=hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest==spec['sha256']
        assert digest not in hashes,(name,hashes.get(digest))
        hashes[digest]=name
        with Image.open(path) as image:
            assert image.size==(64,64) and image.mode=='RGBA'
            assert image.getchannel('A').getbbox()


def test_previously_confusing_pairs_differ_at_real_inventory_zoom():
    pairs=[('silica','glass'),('biochar','activated-carbon'),('filter-cartridge','spent-filter'),
           ('compost','soil-substrate'),('thermal-buffer','depleted-thermal-buffer'),
           ('field-pole','field-crate'),('biogas','bioleachate'),('vector-inserter','canopy-inserter'),
           ('field-armor','expedition-armor'),('expedition-armor','bastion-armor')]
    for a,b in pairs:
        def icon(name):
            with Image.open(MOD/f'graphics/icons/{name}.png') as im:
                im=im.resize((32,32),Image.Resampling.LANCZOS)
                bg=Image.new('RGBA',im.size,(48,48,45,255));bg.alpha_composite(im)
                return bg.convert('RGB')
        difference=ImageStat.Stat(ImageChops.difference(icon(a),icon(b))).mean
        assert sum(difference)/3>7,(a,b,difference)
