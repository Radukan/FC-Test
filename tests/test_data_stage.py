from pathlib import Path
import os,re
import pytest
from PIL import Image
from catalog import ROOT,MOD,load_catalog,load_constants,plain
from factorio_data import DataStage
K,C=load_catalog(),load_constants()

@pytest.fixture(scope='module',params=[('2.0.77',True),('2.0.77',False)])
def stage(request):
    version,overhaul=request.param
    default=ROOT/'.cache'/('factorio-data-2.0.77' if version.startswith('2.0') else 'factorio-data')
    path=Path(os.environ.get('FACTORIO_DATA_20' if version.startswith('2.0') else 'FACTORIO_DATA_21',default))
    if not path.exists():pytest.skip(f'Fetch Wube factorio-data {version} to run source-data integration tests; see docs/DEVELOPING.md.')
    result=DataStage(path,overhaul)
    assert result.version==version,'Tests are pinned to the documented game versions.'
    result.overhaul=overhaul
    return result


def test_all_lua_files_compile_as_52(lua):
    for path in sorted(MOD.rglob('*.lua')):lua.compile(path.read_text(),name='@'+str(path))


def test_research_graph_has_no_cycles_and_all_prerequisites_exist(stage):
    techs=stage.raw.technology;visiting=set();done=set()
    def visit(name,trail):
        assert techs[name] is not None,f'Missing technology {name}'
        assert name not in visiting,'Research cycle: '+' -> '.join(trail+[name])
        if name in done:return
        visiting.add(name)
        for _,pre in (techs[name]['prerequisites'] or {}).items():visit(pre,trail+[name])
        visiting.remove(name);done.add(name)
    for name in techs.keys():visit(name,[])


def test_every_disabled_recipe_is_unlocked_and_every_unlock_exists(stage):
    unlocks={}
    for name,t in stage.raw.technology.items():
        for _,effect in (t['effects'] or {}).items():
            if effect['type']=='unlock-recipe':
                assert stage.raw.recipe[effect['recipe']] is not None
                unlocks.setdefault(effect['recipe'],[]).append(name)
    for r in K['recipes']:
        name='sn-'+r['name']
        assert r.get('enabled') or name in unlocks, f'Unreachable recipe {name}'
        if not r.get('enabled'):assert len(unlocks[name])==1, f'Duplicate unlock {name}'


def test_engine_recipe_category_version_adapter(stage):
    for r in K['recipes']:
        proto=stage.raw.recipe['sn-'+r['name']]
        if stage.version.startswith('2.1'):
            assert proto['category'] is None
            assert r['category'] in list(proto['categories'].values())
        else:assert proto['categories'] is None and proto['category']==r['category']


def test_all_recipes_have_matching_machine_and_sufficient_fluid_ports(stage):
    for r in K['recipes']:
        # Base categories have established vanilla machines; validate custom categories completely.
        if not r['category'].startswith('sn-'):continue
        capable=[]
        for _,p in stage.raw['assembling-machine'].items():
            cats=set((p['crafting_categories'] or {}).values())
            if r['category'] in cats:capable.append(p)
        assert capable,r['name']
        required_in=sum(e[2]=='fluid' for e in r['ingredients'] if len(e)>2)
        required_out=sum(e[2]=='fluid' for e in r['results'] if len(e)>2)
        for p in capable:
            boxes=list((p['fluid_boxes'] or {}).values())
            assert sum(b['production_type'] in ('input','input-output') for b in boxes)>=required_in,r['name']
            assert sum(b['production_type'] in ('output','input-output') for b in boxes)>=required_out,r['name']


def test_operations_are_fixed_powered_surface_gated_and_nonproductive(stage):
    ops=[r for r in K['recipes'] if r.get('operation')]
    for r in ops:
        hosts=[m for m in K['machines'] if m.get('fixed')==r['name']]
        assert len(hosts)==1
        p=stage.raw['assembling-machine']['sn-'+hosts[0]['name']]
        recipe=stage.raw.recipe['sn-'+r['name']]
        assert p.fixed_recipe=='sn-'+r['name']
        assert p.energy_source.type=='electric' and p.energy_usage
        assert p.heating_energy
        assert recipe.allow_productivity is False and recipe.allow_quality is False and recipe.auto_recycle is False
        conditions={v['property']:v for _,v in recipe.surface_conditions.items()}
        assert conditions['sn-restoration-domain']['min']==1
        if r.get('planet'):assert conditions['sn-planet-identity']['min']==C['profiles'][r['planet']]['id']
        if r.get('stage'):assert conditions['sn-ecological-stage']['min']==r['stage']


def test_quality_recycling_cannot_create_fresh_charge_or_revert_waste(stage):
    for name in ('thermal-buffer','depleted-thermal-buffer','spent-filter','hazardous-sludge','gaia-cell','ecological-data','biodiversity-matrix'):
        assert stage.raw.recipe['sn-'+name+'-recycling'] is None,name
    for name in ('air-scrubber','composter','planetary-beacon'):
        assert stage.raw.recipe['sn-'+name+'-recycling'] is not None,name


def test_labs_and_startup_switch(stage):
    for name in ('lab','biolab'):
        assert all('sn-'+p+'-science-pack' in stage.raw.lab[name].inputs.values() for p in ('ecology','climate','restoration'))
    for name,ingredient in [('automation-science-pack','sn-glass'),('logistic-science-pack','sn-compost'),('chemical-science-pack','sn-filter-cartridge')]:
        values=[v.name for v in stage.raw.recipe[name].ingredients.values()]
        assert (ingredient in values)==stage.overhaul
    prereqs=list(stage.raw.technology['rocket-silo'].prerequisites.values())
    assert ('sn-closed-loops' in prereqs)==stage.overhaul


def test_starting_glass_cannot_hijack_automatic_stone_brick_smelting(stage):
    glass=stage.raw.recipe['sn-glass'];brick=stage.raw.recipe['stone-brick']
    assert glass.enabled and stage.raw.recipe['sn-silica'].enabled
    assert glass.ingredients[1].name=='sn-silica'
    assert brick.ingredients[1].name=='stone'
    assert 'crafting' in stage.raw.character['character'].crafting_categories.values()


def test_custom_chains_bootstrap_without_wood_seed_or_spoilage(stage):
    # Structural availability audit: vanilla inputs/techs are assumed available; custom intermediates are NOT.
    # This catches custom science/unlock self-dependencies, not physical transport or engine crafting bugs.
    raw=stage.raw
    available={name for kind in stage.lua.globals().defines.prototypes.item.keys() for name in (raw[kind] or {}).keys() if not name.startswith('sn-')}
    available.update(name for name in raw.fluid.keys() if not name.startswith('sn-'))
    available-= {'wood','spoilage','yumako-seed','jellynut-seed'}
    researched={name for name in raw.technology.keys() if not name.startswith('sn-')}
    enabled={r['name'] for r in K['recipes'] if r.get('enabled')}
    produced=set()
    for _ in range(100):
        changed=False
        for t in K['technologies']:
            name='sn-'+t['name']
            if name in researched:continue
            if all(pre in researched for pre in t['prerequisites']) and all(ingredient[0] in available for ingredient in t['science']):
                researched.add(name);enabled.update(t['unlocks']);changed=True
        for r in K['recipes']:
            if r['name'] in produced or r['name'] not in enabled:continue
            if not all(i[0] in available for i in r['ingredients']):continue
            if r['category'].startswith('sn-'):
                hosts=[m for m in K['machines'] if r['category'][3:] in m['categories']]
                if not any('sn-'+m['name'] in available for m in hosts):continue
            produced.add(r['name']);available.update(i[0] for i in r['results']);changed=True
        if not changed:break
    for name in ('sn-soil-enricher','sn-ecology-science-pack','sn-climate-science-pack','sn-restoration-science-pack','sn-gaia-cell'):
        assert name in available,f'Custom dependency deadlock: {name}; techs not reached: {[t["name"] for t in K["technologies"] if "sn-"+t["name"] not in researched]}'
    assert 'sn-living-worlds' in researched
    # Hydroponic crops need real planet seeds; the pioneer timber bootstrap must not.
    assert 'pioneer-timber' in produced


def test_custom_art_files_exist_have_correct_dimensions_and_transparency(stage):
    for kind,protos in stage.raw.items():
        for name,p in protos.items():
            if not name.startswith('sn-'):continue
            icon=p['icon']
            if icon and icon.startswith('__second-nature__/'):
                path=MOD/icon.removeprefix('__second-nature__/')
                assert path.is_file(),str(path)
                with Image.open(path) as image:
                    assert image.size==(p.icon_size,p.icon_size)
                    assert image.mode=='RGBA'
    assert Image.open(MOD/'graphics/garden.png').size==(256,192)


def test_research_and_world_conditions_use_existing_prototypes(stage):
    for planet in C['planets']:
        p=stage.raw.planet[planet]
        assert p.surface_properties['sn-planet-identity']==C['profiles'][planet]['id']
        assert p.surface_properties['sn-restoration-domain']==1
        assert p.pollutant_type==('spores' if planet=='gleba' else 'pollution')
    for name,t in stage.raw.technology.items():
        if not name.startswith('sn-'):continue
        for _,ingredient in t.unit.ingredients.items():
            family=stage.raw.item if stage.version.startswith("2.1") else stage.raw.tool
            assert family[ingredient[1]],(name,ingredient[1])
    for _,profile in C['profiles'].items():
        if profile.get('tree'):assert stage.raw.tree[profile['tree']],profile['tree']


def test_desolate_map_controls_and_presets_preserve_resources_and_gleba(stage):
    settings=stage.raw.planet.nauvis.map_gen_settings
    assert settings.autoplace_settings.entity.treat_missing_as_default is False
    assert settings.autoplace_settings.entity.settings.fish is None
    assert settings.autoplace_settings.entity.settings['iron-ore'] is not None
    assert settings.autoplace_settings.entity.settings['crude-oil'] is not None
    for name in ['biter-spawner','spitter-spawner','small-worm-turret','medium-worm-turret','big-worm-turret','behemoth-worm-turret']:
        assert settings.autoplace_settings.entity.settings[name] is not None
    assert all(stage.raw.tree[name] is None for name in settings.autoplace_settings.entity.settings.keys())
    assert all('rock' in name or 'decal' in name for name in settings.autoplace_settings.decorative.settings.keys())
    presets=stage.raw['map-gen-presets'].default
    assert presets.default.basic_settings is None and presets.default.advanced_settings is None
    assert presets['sn-last-landing'].advanced_settings.pollution.enabled is True
    assert presets['sn-quiet-reclamation'].basic_settings.peaceful_mode is True
    assert presets['sn-brood-frontier'].basic_settings.autoplace_controls['enemy-base'].size==1.5
    assert stage.raw.planet.gleba.pollutant_type=='spores'


def test_nauvis_pollution_recruitment_is_removed_but_spores_are_untouched(stage):
    for name in C['native_names']:
        unit=stage.raw.unit[name]
        if unit:assert unit.absorptions_to_join_attack.pollution>=1e29
        nest=stage.raw['unit-spawner'][name]
        if nest:
            assert nest.absorptions_per_second.pollution.absolute==0
            assert nest.absorptions_per_second.pollution.proportional==0
    assert stage.raw['airborne-pollutant'].pollution.affects_evolution is False
    assert stage.raw['unit-spawner']['gleba-spawner'].absorptions_per_second.spores is not None


def test_friendly_native_has_original_multidirectional_art_and_zero_attack_damage(stage):
    unit=stage.raw.unit['sn-bloomback']
    assert unit.run_animation.direction_count==8 and unit.run_animation.frame_count==4
    assert unit.attack_parameters.damage_modifier==0
    assert unit.alternative_attacking_frame_sequence is None
    assert Image.open(MOD/'graphics/entity/bloomback.png').size==(384,768)
    assert stage.raw['simple-entity-with-owner']['sn-bloom-nest'] is not None
    assert stage.raw.container['sn-lander'].inventory_size>=len(C['landing_cargo'])


def test_main_menu_background_is_a_real_packaged_image(stage):
    constants=stage.raw['utility-constants'].default
    assert len(constants.main_menu_simulations)==0
    assert constants.main_menu_background_image_location=='__second-nature__/graphics/menu/last-landing.jpg'
    image=Image.open(MOD/'graphics/menu/last-landing.jpg')
    assert image.width>=1280 and image.height>=720


def test_campaign_startup_switches_are_reversible():
    path=ROOT/'.cache/factorio-data-2.0.77'
    if not path.exists():pytest.skip('Pinned stable data checkout required')
    result=DataStage(path,True,{'sn-desolate-start':False,'sn-biter-metabolism':False,'sn-menu-background':False})
    settings=result.raw.planet.nauvis.map_gen_settings.autoplace_settings.entity
    assert settings.settings.fish is not None and settings.treat_missing_as_default is not False
    assert result.raw.unit['small-biter'].absorptions_to_join_attack.pollution>0
    assert result.raw['airborne-pollutant'].pollution.affects_evolution is True
    assert result.raw['utility-constants'].default.main_menu_background_image_location=='__core__/graphics/background-image.jpg'
