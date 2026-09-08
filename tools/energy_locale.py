"""Nightglass energy/rail UI copy. Prototype descriptions live in shared.energy."""

def add_energy_locale(put):
    entries={
        'internal-charge':'Metered solar traction reserve',
        'installed-panels':'Factory-installed roof photovoltaics',
        'installed-battery':'Factory-installed rail battery',
        'solar-rail':'Solar rail / onboard energy',
        'charge':'Battery: __1__ / __2__ MJ',
        'mode':'__1__ / current speed ceiling __2__ km/h',
        'day':'Daylight traction','twilight':'Twilight derating','night':'Night battery operation',
        'invalid-grid':'Unsupported or missing onboard components',
        'rail-help':'Only the installed roof panels charge this locked battery grid. There are no fuel slots and no factory-grid connection. Stop in daylight to recharge. Night operation has reduced power and speed; an empty battery provides no traction. The lowest solar speed cap applies to a consist containing solar locomotives.'
    }
    for key,value in entries.items():put('sn-energy',key,value)
