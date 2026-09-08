import json
import math
import pytest
from catalog import ROOT,MOD,load_catalog,plain
from factorio_data import DataStage


@pytest.fixture(scope='module')
def energy_data():
    path=ROOT/'.cache/factorio-data-2.0.77'
    if not path.exists():pytest.skip('Pinned stable data required')
    return DataStage(path)


@pytest.fixture
def energy_lua(game_lua):
    game_lua.execute((ROOT/'tests/energy_fixture.lua').read_text())
    game_lua.execute("R=require('scripts.solar_rail');P=require('scripts.power');E=require('shared.energy');S=require('scripts.state')")
    return game_lua


def test_six_power_options_cover_passive_active_clean_and_polluting(energy_data):
    e=load_catalog()['energy'];assert len(e['plants'])>=5
    assert sum(p['kind']=='burner-generator' for p in e['plants'])==3
    assert sum(p.get('pollution',0)>0 for p in e['plants'])==2
    for p in e['plants']:
        entity=energy_data.raw[p['kind']]['sn-'+p['name']]
        assert entity and entity.tile_width==p['size']
        assert energy_data.raw.item[entity.name].place_result==entity.name
        if p['kind']=='burner-generator':
            assert entity.burner.emissions_per_minute.pollution==p['pollution']
            assert entity.energy_source.emissions_per_minute is None
    biomass=energy_data.raw['burner-generator']['sn-biopellet-engine']
    assert plain(biomass.burner.fuel_categories)==['sn-grown-fuel']
    assert energy_data.raw.item['sn-biopellet'].burnt_result=='sn-bio-ash'
    assert energy_data.raw.item['sn-bio-ash'].fuel_value is None


def test_solar_locomotives_have_no_fuel_slots_and_only_locked_solar_battery_grids(energy_data):
    data=energy_data.raw;trains=load_catalog()['energy']['trains']
    assert len(trains)==3
    previous=0
    for t in trains:
        p=data.locomotive['sn-'+t['name']]
        assert previous<p.max_speed<data.locomotive.locomotive.max_speed
        previous=p.max_speed
        assert p.energy_source.fuel_inventory_size==0
        assert plain(p.energy_source.fuel_categories)==['sn-solar-traction']
        assert p.energy_source.smoke is None and p.energy_source.initial_fuel is None
        grid=data['equipment-grid'][p.equipment_grid]
        assert grid.locked is True and plain(grid.equipment_categories)==['sn-solar-rail']
        panel=data['solar-panel-equipment']['sn-solar-rail-panel-'+str(t['tier'])]
        battery=data['battery-equipment']['sn-solar-rail-battery-'+str(t['tier'])]
        assert panel.power==str(t['solar_watts'])+'W'
        assert battery.energy_source.buffer_capacity==str(t['battery_joules'])+'J'
        assert t['night_speed']<t['day_speed'] and t['night_power']<1
    assert data.item['sn-solar-drive-charge'].hidden is True
    assert data.recipe['sn-solar-drive-charge'] is None
    assert data.locomotive.locomotive.energy_source.fuel_inventory_size==3


def test_new_locomotives_start_empty_and_configuration_does_not_refill_them(energy_lua):
    energy_lua.execute('''
      local e=mock.rail('sn-sunseed-locomotive');local r=R.register(e)
      assert(#e.grid.equipment==2 and mock.battery(e).energy==0 and r.credit==0)
      mock.battery(e).energy=12345
      R.init();R.init();R.register(e)
      assert(#e.grid.equipment==2 and mock.battery(e).energy==12345)
    ''')


def test_motor_only_receives_withdrawn_joules_and_idle_credit_is_returned(energy_lua):
    energy_lua.execute('''
      local e=mock.rail('sn-sunseed-locomotive');local rec=R.register(e);local b=mock.battery(e)
      b.energy=100000;game.tick=6;R.tick()
      assert(rec.credit==18000 and b.energy==82000 and e.burner.remaining_burning_fuel==18000)
      e.burner.remaining_burning_fuel=11000
      game.tick=12;R.tick()
      assert(b.energy+e.burner.remaining_burning_fuel+e.burner.heat==93000)
      assert(rec.consumed==7000)
      R.flush(e)
      assert(b.energy==93000 and rec.credit==0 and e.burner.currently_burning==nil)
    ''')


def test_foreign_energy_and_unsupported_equipment_never_get_credited(energy_lua):
    energy_lua.execute('''
      local e=mock.rail('sn-sunseed-locomotive');R.register(e);local b=mock.battery(e)
      b.energy=50000;game.tick=6;R.tick()
      local before=b.energy
      e.burner.currently_burning={name='coal'};e.burner.remaining_burning_fuel=10000000
      R.flush(e);assert(b.energy==before and e.burner.currently_burning==nil)
      e.grid.equipment[#e.grid.equipment+1]={name='fission-reactor-equipment',energy=10000000}
      game.tick=12;R.tick()
      assert(e.burner.currently_burning==nil and R.status(e).mode=='invalid-grid')
    ''')


def test_darkness_caps_speed_and_reduces_battery_power_without_accelerating_trains(energy_lua):
    energy_lua.execute('''
      local e=mock.rail('sn-daybreak-locomotive');local rec=R.register(e);mock.battery(e).energy=1000000
      e.surface.darkness=1;e.train.speed=.9;game.tick=6;R.tick()
      assert(e.train.speed==.6 and rec.credit==450000*.1*.55)
      e.train.speed=.2;game.tick=7;R.tick();assert(e.train.speed==.2)
      R.flush(e);mock.battery(e).energy=0;game.tick=12;R.tick()
      assert(e.burner.currently_burning==nil and rec.credit==0)
    ''')


def test_solar_consists_obey_lowest_cap_after_coupling(energy_lua):
    energy_lua.execute('''
      local a=mock.rail('sn-sunseed-locomotive');local b=mock.rail('sn-daybreak-locomotive')
      R.register(a);R.register(b);b.train=a.train;a.train.speed=.9;a.surface.darkness=1
      game.tick=6;R.tick();assert(a.train.speed==.22)
    ''')


def test_wind_and_geothermal_outputs_are_bounded_and_never_power_airless_platforms(energy_lua):
    energy_lua.execute('''
      local s=game.surfaces[1];local wind=mock.entity('sn-wind-turbine',s,{x=0,y=0},nil,true)
      local geo=mock.entity('sn-geothermal-bore',s,{x=100,y=0},nil,true)
      P.register(wind);P.register(geo)
      assert(geo.power_production==1200000/60)
      local lo,hi=1e30,0
      for tick=0,10000,120 do local w=P.output(wind,tick);assert(w>=0 and w<=120000);lo=math.min(lo,w);hi=math.max(hi,w) end
      assert(hi-lo>40000)
      s.wind_speed=0;assert(P.output(wind,0)==0)
      s.platform={};assert(P.output(geo,0)==0)
      s.platform=nil;s.properties.pressure=0;assert(P.output(wind,0)==0)
    ''')
