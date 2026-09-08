from catalog import ROOT
from factorio_data import DataStage


def test_iron_sticks_and_wood_free_poles_need_no_green_science():
    for overhaul in (False,True):
        p=DataStage(ROOT/'.cache/factorio-data-2.0.77',overhaul)
        assert p.raw.recipe['iron-stick'].enabled is True
        assert p.raw.recipe['iron-stick'].hide_from_player_crafting is False
        assert p.raw.recipe['small-electric-pole'].enabled is True
        assert any(i.name=='iron-stick' for i in p.raw.recipe['small-electric-pole'].ingredients.values())


def test_existing_forces_regain_startup_iron_sticks_on_configuration(game_lua):
    game_lua.execute('''
      local force=mock.player_force;force.recipes={['iron-stick']={enabled=false}}
      mock.configure();assert(force.recipes['iron-stick'].enabled)
    ''')
