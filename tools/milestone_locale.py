"""Milestone and in-game field-guide copy, generated from the shared Lua lists."""
from catalog import load_module


def add_milestone_locale(put):
    milestones = load_module('shared.achievements')
    for entry in milestones['all']:
        put('achievement-name', 'sn-' + entry['name'], entry['title'])
        put('achievement-description', 'sn-' + entry['name'], entry['description'])

    tips = load_module('shared.tips')
    put('tips-and-tricks-item-category-name', tips['category'], 'Second Nature')
    for entry in tips['items']:
        put('tips-and-tricks-item-name', 'sn-' + entry['name'], entry['title'])
        put('tips-and-tricks-item-description', 'sn-' + entry['name'], entry['text'])

    for key, text in {
        'milestones': 'Milestones',
        'milestone-intro': 'Restoration milestones recorded for your force. They are tracked in the modded achievement list and never affect vanilla or Steam progress. Planetary milestones are awarded to every force with recorded restoration work on that world, so no one wins credit for a planet they never touched.',
        'milestone-count': '__1__ of __2__ milestones earned',
        'milestone-when': 'Earned __1__ minutes ago.',
        'milestone-note': 'The achievement window also lists condition milestones the game evaluates by itself: wind power, beacon construction, coordination-cell and matrix output, restoration research, a fully clean grid, and a finish with no dirty shortcuts.'
    }.items():
        put('sn-gui', key, text)
    put('sn-message', 'milestone-earned', '[Second Nature] Milestone reached: __1__')
