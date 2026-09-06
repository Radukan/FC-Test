import pytest, math
from catalog import load_catalog,load_constants
K,C=load_catalog(),load_constants()

@pytest.mark.parametrize('planet',C['planets'])
def test_initial_state_is_bounded_and_does_not_decay_before_first_work(lua,planet):
    m=lua.eval('require("shared.model")');s=m.new(planet)
    before=[s['values'][axis] for axis in C['axes']]
    m.advance(s,60*60*100,1)
    assert [s['values'][axis] for axis in C['axes']]==before
    assert all(0<=x<=100 for x in before)
    assert 0<=s['stage']<5


def test_effects_require_positive_completed_cycles(lua):
    m=lua.eval('require("shared.model")');s=m.new('nauvis');before=s['values']['atmosphere']
    for count in (0,-1):m.apply(s,lua.table_from({'atmosphere':20}),count,1)
    assert s['values']['atmosphere']==before
    assert s['cycles']==0


def test_support_ceiling_and_no_destructive_positive_application(lua):
    lua.execute('''
      local M=require('shared.model'); local s=M.new('aquilo')
      M.apply(s,{biodiversity=100,water=100,soil=100},1,1)
      assert(s.values.biodiversity <= M.cap(s,'biodiversity'))
      assert(s.values.water <= M.cap(s,'water'))
      s.values.water=90;s.values.atmosphere=0
      M.apply(s,{water=1},1,1)
      assert(s.values.water==90,'positive restoration must not instantly destroy above-cap stock')
    ''')


def test_toxicity_is_a_hard_biodiversity_constraint(lua):
    lua.execute('''
      local M=require('shared.model'); local s=M.new('nauvis')
      for k in pairs(s.values) do s.values[k]=100 end
      s.values.biodiversity=0;s.toxicity=100
      M.apply(s,{biodiversity=1000},1,1)
      assert(s.values.biodiversity==30)
      M.apply(s,{toxicity=-100,biodiversity=1000},1,1)
      assert(s.values.biodiversity==100 and s.toxicity==0)
    ''')


def test_dirty_forcing_cannot_win_by_maxing_one_meter(lua):
    lua.execute('''
      local M=require('shared.model');local K=require('shared.catalog')
      local s=M.new('nauvis');M.apply(s,K.by_recipe['sn-atmospheric-forcing'].effects,100000,1)
      assert(s.values.atmosphere==100 and s.toxicity==100)
      assert(s.stage==0 and not M.ready(s))
    ''')


def test_all_stage_thresholds_required(lua):
    lua.execute('''
      local M=require('shared.model');local s=M.new('nauvis')
      for k in pairs(s.values) do s.values[k]=100 end
      s.toxicity=0;M.refresh(s);assert(M.ready(s))
      s.values.water=89.99;M.refresh(s);assert(not M.ready(s))
      s.values.water=90;s.toxicity=8.001;M.refresh(s);assert(not M.ready(s))
      s.toxicity=8;M.refresh(s);assert(M.ready(s))
    ''')


def test_counter_deltas_survive_idle_rescan_switch_and_reset(lua):
    lua.execute('''
      local M=require('shared.model');local r={produced=120,recipe='clean'}
      assert(M.completed(r,120,'clean')==0)
      assert(M.completed(r,122,'clean')==2)
      assert(M.completed(r,125,'dirty')==0)
      assert(M.completed(r,126,'dirty')==1)
      assert(M.completed(r,0,'dirty')==0)
      assert(M.completed(r,2,'dirty')==2)
    ''')


def test_growth_not_clean_air_alone_provokes_resistance(lua):
    lua.execute('''
      local M=require('shared.model');local s=M.new('nauvis')
      M.apply(s,{biodiversity=3},1,1);assert(s.pressure>0)
      local p=s.pressure;s.first_operation=1;M.advance(s,60,1);assert(s.pressure<p)
      M.apply(s,{pressure=-1000},1,1);assert(s.pressure==0)
    ''')


def test_pollution_exposure_creates_bounded_toxic_debt(lua):
    lua.execute('''
      local M=require('shared.model');local s=M.new('nauvis');s.first_operation=1;s.ambient=100000000
      M.advance(s,60*60,1);assert(s.toxicity>30 and s.toxicity<=100)
      for k,v in pairs(s.values) do assert(v>=0 and v<=100) end
    ''')


@pytest.mark.parametrize('planet',C['planets'])
def test_full_kit_can_restore_each_planet_in_finite_time(lua,planet):
    # A throughput balance test, NOT a simulated technology/logistics playthrough.
    lua.globals().test_planet=planet
    minutes=lua.execute('''
      local C=require('shared.constants');local K=require('shared.catalog');local M=require('shared.model')
      local s=M.new(test_planet);s.first_operation=1
      local names={'sn-air-scrubbing','sn-thermal-balancing','sn-watershed-restoration','sn-soil-restoration','sn-pioneer-reseeding','sn-mineral-detoxification','sn-habitat-restoration'}
      local kit={4,4,3,3,3,2,1}
      for _, machine in ipairs(K.machines) do
        if machine.planet==test_planet then names[#names+1]='sn-'..machine.fixed;kit[#kit+1]=2 end
      end
      for minute=1,180 do
        for i,name in ipairs(names) do
          local r=K.by_recipe[name]
          if not r.stage or s.stage>=r.stage then M.apply(s,r.effects,60/r.seconds*kit[i],1) end
        end
        M.advance(s,60,1)
        if M.ready(s) then return minute end
      end
      error('full kit failed to restore '..test_planet)
    ''')
    assert 5<minutes<180


def test_save_serialization_preserves_future_model_result(lua):
    lua.execute('''
      local M=require('shared.model');local s=M.new('fulgora');s.first_operation=1
      M.apply(s,{atmosphere=20,water=10,soil=15,toxicity=-30},2,1)
      local function clone(t) local out={}; for k,v in pairs(t) do out[k]=type(v)=='table' and clone(v) or v end;return out end
      local saved=clone(s)
      for i=1,100 do M.advance(s,1,1);M.advance(saved,1,1) end
      for k,v in pairs(s.values) do assert(saved.values[k]==v) end
      assert(s.toxicity==saved.toxicity and s.stage==saved.stage and s.pressure==saved.pressure)
    ''')
