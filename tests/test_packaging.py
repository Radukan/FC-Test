import configparser,hashlib,json,re,sys,zipfile
from pathlib import Path
import pytest
from catalog import ROOT,MOD,load_catalog
from package import build

@pytest.mark.parametrize('target',['2.0'])
def test_installable_packages_are_branch_correct_complete_and_deterministic(tmp_path,target):
    a=build(target,tmp_path/'a');b=build(target,tmp_path/'b')
    assert a.read_bytes()==b.read_bytes()
    with zipfile.ZipFile(a) as z:
        root='second-nature_'+json.loads((MOD/'info.json').read_text())['version']+'/'
        names=z.namelist()
        assert all(n.startswith(root) for n in names)
        assert all(not any(part in n.split('/') for part in ('.git','.cache','tests','tools','artifacts')) for n in names)
        info=json.loads(z.read(root+'info.json'))
        assert info['factorio_version']==target
        assert all(('2.0.77' if target=='2.0' else '2.1.17') in d for d in info['dependencies'])
        assert {root+x for x in ('control.lua','data.lua','settings.lua','README.md','LICENSE','thumbnail.png')}<=set(names)
        assert root+'graphics/garden.png' in names
        assert root+'sound/music/after-the-ash.ogg' in names
        assert len([n for n in names if '/graphics/technology/' in n])==len(load_catalog()['technologies'])
    assert a.with_suffix('.zip.sha256').read_text().split()[0]==hashlib.sha256(a.read_bytes()).hexdigest()


def test_locale_has_no_duplicates_and_covers_all_catalog_entries():
    cfg=configparser.RawConfigParser(strict=True);cfg.optionxform=str
    cfg.read(MOD/'locale/en/second-nature.cfg',encoding='utf-8')
    k=load_catalog()
    for group in ('item','fluid','technology'):
        key={'item':'items','fluid':'fluids','technology':'technologies'}[group]
        for entry in k[key]:assert cfg.has_option(group+'-name','sn-'+entry['name'])
    for m in k['machines']:assert cfg.has_option('entity-description','sn-'+m['name'])
    for r in k['recipes']:
        assert cfg.has_option('recipe-name','sn-'+r['name'])
        if r.get('effects'):assert cfg.has_option('recipe-description','sn-'+r['name'])
    for path in MOD.rglob('*.lua'):
        for section,key in re.findall(r'[\{,]\s*"(sn-[\w-]+)\.([\w-]+)"\s*[,}]',path.read_text()):
            assert cfg.has_option(section,key),(path,section,key)


def test_generated_locale_matches_source_catalog():
    import generate_locale
    path=MOD/'locale/en/second-nature.cfg';before=path.read_bytes()
    generate_locale.generate()
    assert path.read_bytes()==before,'Generated localization was stale'


def test_mod_metadata_and_changelog_are_consistent():
    info=json.loads((MOD/'info.json').read_text());change=(MOD/'changelog.txt').read_text()
    assert info['version']=='0.4.0' and 'Version: '+info['version'] in change
    assert info['factorio_version']=='2.0'
    assert any(s.startswith('space-age >=') for s in info['dependencies'])
    assert re.search(r'Version: 0\.4\.0\nDate: 2026-09-07',change)


def test_game_runtime_has_no_network_filesystem_or_legacy_global_dependencies():
    for path in list((MOD/'scripts').glob('*.lua'))+[MOD/'control.lua']:
        text=path.read_text()
        assert not re.search(r'\b(os\.|io\.|loadfile\(|dofile\(|global\.)',text),path
        assert 'game.entity_prototypes' not in text
        assert '.unit_group' not in text


def test_experimental_builds_are_no_longer_published():
    with pytest.raises(ValueError, match='stable'):
        build('2.1')
