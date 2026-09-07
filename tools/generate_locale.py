#!/usr/bin/env python3
"""Generate English prototype localization from the shared catalog; UI prose lives here."""
from collections import OrderedDict
import json
from catalog import MOD, load_catalog, load_constants
from campaign_locale import add_campaign_locale
from expedition_locale import add_expedition_locale
from continuance_locale import add_continuance_locale

def generate():
    k,c=load_catalog(),load_constants(); sections=OrderedDict()
    def put(section,key,value):
        value=str(value)
        assert '\u2014' not in value and '\u2013' not in value,(section,key)
        sections.setdefault(section,OrderedDict())[key]=value.replace('\n','\\n')
    for x in k['items']:
        put('item-name','sn-'+x['name'],x['title']);put('item-description','sn-'+x['name'],x['description'])
    for x in k.get('expedition',[]):
        for group in ('item','entity'):
            put(group+'-name','sn-'+x['name'],x['title']);put(group+'-description','sn-'+x['name'],x['description'])
    for x in k['fluids']:
        put('fluid-name','sn-'+x['name'],x['title']);put('fluid-description','sn-'+x['name'],x['description'])
    for x in k['machines']:
        for group in ('entity','item'):
            put(group+'-name','sn-'+x['name'],x['title']);put(group+'-description','sn-'+x['name'],x['description'])
    put('entity-name','sn-rootbreaker','Rootbreaker biter');put('entity-name','sn-canopy-breaker','Canopy breaker');put('entity-name','sn-blight-spitter','Blight spitter')
    put('entity-description','sn-native','A territorial native strain adapted to contaminated ground. Rapid ecological change provokes coordinated attacks.')
    for x in k['recipes']:
        put('recipe-name','sn-'+x['name'],x['title'])
        if x.get('effects'):
            parts=[]
            for key in c['axes']+['toxicity','pressure','pollution']:
                value=x['effects'].get(key)
                if value is None or isinstance(value,bool):continue
                label={'temperature':'Thermal fitness','pressure':'Native resistance','pollution':'Local pollution/spores'}.get(key,key.title())
                scale=c['pace']['pollution_capture'] if key=='pollution' and value<0 else (1 if key=='pollution' else c['pace']['fitness'])
                parts.append(f'{label}: {value*scale:+g}')
            put('recipe-description','sn-'+x['name'],f"Per completed {x['seconds']}-second cycle at crafting speed 1:\n"+' · '.join(parts)+'.\nBase rates shown: planetary multipliers, process optimization research and support ceilings also apply. Unpowered, ingredient-starved or output-blocked machines earn nothing.')
    for x in k['technologies']:
        put('technology-name','sn-'+x['name'],x['title']);put('technology-description','sn-'+x['name'],x['description'])
    for key,title in {
        'atmosphere':'Atmosphere','temperature':'Thermal balance','water':'Water cycle','soil':'Living soil','biodiversity':'Biodiversity',
        'toxicity':'Toxicity','pressure':'Native resistance','stability':'Ecological stability','stage':'Ecological stage'
    }.items():
        put('sn-axis',key,title);put('virtual-signal-name','sn-'+key,title)
    for key,text in {
        'atmosphere':'Suitability of atmospheric chemistry and pressure for the intended ecosystem. Not the engine pressure property.',
        'temperature':'Thermal suitability: higher is better on BOTH hot and cold worlds. Aquilo still needs heat pipes.',
        'water':'A stable water cycle needs atmosphere and thermal balance. Capped by atmosphere + 30 and thermal fitness + 35.',
        'soil':'Living soil needs water and low toxic load. Capped by water + 35 and 110 − 0.4 × toxicity.',
        'biodiversity':'Viable, diverse life - not merely raw biomass. Capped by atmosphere + 15, thermal balance + 20, water + 20, soil + 15, and 100 − 0.7 × toxicity.',
        'toxicity':'Persistent contamination from dirty processing and measured local exposure. Lower is better; capture toxins, treat the sludge and close the loop.',
        'pressure':'Resistance to ecological CHANGE. Growth raises it even without pollution; adaptation and supplied dampeners lower it. Raids require native nests and respect peaceful mode.'
    }.items():put('sn-axis-description',key,text)
    for i,stage in enumerate(c['stages']):put('sn-stage',stage['name'],f"{i:02d} / {stage['name'].replace('-',' ').title()}")
    ui={
        'title':'SECOND NATURE  /  Field station','toggle':'Open Second Nature · Shift + T','field-station':'Planet','living-network':'Living network','field-guide':'Field guide',
        'current-planet':'Current planet','stability':'   Stability __1__%','uncharted':'No field station contact. Visit this world to initialize its ecosystem. Unvisited planets do not decay.',
        'cap':'Current support ceiling: __1__%.','next-phase':'Next:','mature':'Self-sustaining. Keep every fitness axis ≥ 90 and toxicity ≤ 8; maintain the beacon supply loop.',
        'support-hint':'Fitness is not interchangeable. If a meter stops rising, improve its supporting climate or reduce toxicity. The field guide explains every ceiling.',
        'activity':'Produced in the last minute: __1__ / __2__ machines · Completed ecological cycles: __3__\nSampled local pollution/spores: __4__',
        'impact':'Reclaimed tiles: __1__ · New trees: __2__ · Captured pollution/spores: __3__',
        'raid-in':'NATIVE RESPONSE IN __1__ SECONDS. Defend the marked restoration installation or remove its supporting nest.',
        'native-rule':'Native response: __1__. Local grace: __2__ minutes. Waves need an existing nest 96-512 tiles away and give 45 seconds of warning. Clearing the perimeter is a valid defense.',
        'resistance-disabled':'Ecological-response waves are disabled by settings or peaceful mode. Vanilla enemy rules remain unchanged.',
        'no-natives':'No imported invasions here. This world retains its native hazards; Second Nature does not seed biters onto lifeless planets or replace demolishers.',
        'operation-rule':'Machines earn progress only on completed recipes. Check power, heat, inputs, byproduct output space and surface-stage requirements before expanding.',
        'network-heading':'Five worlds. One living system.',
        'network-description':'Research Second Nature, reach stage 5 on all five planets, and keep one of YOUR force’s beacons on each world completing cycles at least every 90 seconds. Sustain this for 10 uninterrupted minutes.\nEach axis must remain ≥ 90; toxicity must remain ≤ 8. Shared ecology, force-specific beacon logistics.',
        'world-state':'__1__ · Stability __2__% · __3__','beacon-online':'recent beacon cycle','beacon-offline':'no recent beacon cycle',
        'hold-time':'Network hold: __1__ min __2__ s / 10 min','research-goal':'Next step: research Second Nature at the end of the restoration technology tree.',
        'network-unvisited':'Establish contact with __1__.','network-restore':'Bring __1__ to self-sustaining status.',
        'network-supply':'Restore regular beacon shipments to __1__.','network-holding':'All systems meet the goal. Maintain production; the ten-minute hold is running.',
        'victory':'SECOND NATURE ACHIEVED. The factory can keep growing.','victory-disabled':'Network victory is disabled in mod settings. Ecological simulation and production continue.',
        'footer':'Progress comes from production. Recovery comes from balance.   /   v0.1.0',
    }
    for key,text in ui.items():put('sn-gui',key,text)
    planets={
        'nauvis':'NAUVIS / Rebuild a fragmented home. Begin with soil and atmospheric recovery, then establish watersheds and pioneer forests. Biters interpret restoration as an attack on their habitat.',
        'vulcanus':'VULCANUS / Weather the furnace. Heat and atmospheric instability make generic recovery slower. Basalt weathering supplies nutrients, while sheltered thermophiles become an export. Lava and demolishers remain.',
        'fulgora':'FULGORA / Life after the scrapyard. Toxic legacy waste, little water and thin soil define the challenge. Recover holmium catalysts from remediation; preserve the oil seas, lightning and islands.',
        'gleba':'GLEBA / Beyond the monoculture. A lush world is not necessarily a stable one. Rebalance invasive spores into symbiosis; preserve fertile crop tiles, spoilage and pentapod pressure.',
        'aquilo':'AQUILO / A garden beneath the ice. Climate recovery is slow without cryogenic gardens and reliable heat. Import living communities, recover water from ice and ammonia, and keep the thermal buffers circulating. No ice or foundation tiles are removed.'
    }
    for key,text in planets.items():put('sn-planet',key,text)
    guides=[
        ('Your first living factory',
         '1. Crush stone into silica in your inventory; smelt it into laboratory glass. In overhaul mode each red science pack also needs one glass.\n\n2. Research Pioneer biology. Build a pioneer bioreactor, connect electricity and water, and select mineral nutrients, then pioneer culture, then algae cultivation. A culture is returned by every algae cycle; no trees or starter seeds are mandatory.\n\n3. Research The living substrate. Compost algae into compost and biofilm. Logistic science consumes one compost. Make biochar and soil substrate in the composter.\n\n4. Research Field ecology. Supply a soil restoration station with substrate, culture and water. Its completed cycles improve the planet and produce ecological samples. Combine samples, glass and circuits into ecology science.\n\n5. Add atmospheric scrubbers, water filtration and watersheds. Empty EVERY output. Early spent filters and effluent can be buffered until Nothing left behind unlocks full reclamation.\n\n6. Add pioneer seed dispersers, heat exchangers and detoxifiers as needed. The dashboard shows current support ceilings and the next stage’s exact requirements. Do not solve a water shortage by building more seed dispensers.'),
        ('Close the loops',
         'FILTER LOOP\nBiochar → activated carbon → filter cartridges → scrubbers / filtration → spent cartridges → reclamation → carbon + glass + toxic effluent. Reclamation needs purified water; keep a little reserve to restart it.\n\nWASTE LOOP\nEffluent + neutralization charges → ordinary water + hazardous sludge → electric vitrification + glass → inert aggregate → concrete. Sludge is real inventory, not a magical negative-pollution button. Never let it back up at a detoxifier.\n\nTHERMAL LOOP\nFresh thermal buffers → climate exchangers / cryogenic gardens → depleted buffers → electrochemical recharge with biofilm and clean water → fresh buffers. Recycling buffers cannot manufacture fresh charge.\n\nSURPLUS SAMPLES\nEcological sample recovery returns nutrients and a little purified water; climate sample recovery returns glass and a little purified water; biosphere samples can be composted. These energy-consuming sinks keep mature operations running when research demand falls.\n\nPOWER\nA climate exchanger uses 4 MW, a beacon 5 MW, and all new assemblers require heat on Aquilo. Efficiency modules, solar, nuclear and later fusion are real infrastructure choices - not free green progress.'),
        ('Native resistance and dirty shortcuts',
         'Two pressures coexist. Ordinary pollution/spores still drive vanilla attacks where natives exist. Pollution is enabled on Vulcanus, Fulgora and Aquilo as well, but no new enemy populations are introduced. Ecological CHANGE also raises native resistance, especially new biodiversity. Fully maintained mature worlds quiet down as organisms adapt.\n\nSecond Nature waves happen only on Nauvis and Gleba. They need an existing enemy nest 96-512 tiles from a recently working restoration machine. You receive 45 seconds of warning. Clearing the perimeter is a valid solution. No nests means no scripted wave.\n\nBalanced waves contain at most 40 biters, with far fewer pentapods, a 20-minute local grace period and an eight-minute post-wave cooldown. Peaceful mode disables these waves. Settings can disable resistance independently of terraforming.\n\nPheromone dampeners consume biofilm, carbon and water to reduce resistance. Defend installations, maintain ammunition logistics, and expand in deliberate stages. An unpowered dampener does nothing.\n\nDirty pyrolysis produces carbon and soil cheaply. Atmospheric forcing rapidly improves atmosphere, but degrades thermal and water fitness and adds toxins. These are viable startup or emergency tools. They cannot meet the all-axis victory thresholds. Captured sludge must still be vitrified. Clean recipes trade fossil feedstocks for electricity, biological logistics and byproduct handling.'),
        ('Five planetary specialties',
         'NAUVIS / Your ecological workshop. Develop clean chemistry and a reliable water/filter loop before leaving. Restored land gradually greens around active machines, with sparse tree growth outside infrastructure.\n\nVULCANUS / Basalt weathering uses calcite, tungsten ore and water to improve thermal and soil fitness. Condition the world to stage 1 to cultivate thermophiles. Export them.\n\nFULGORA / Remediate scrap with mineral electrolyte. Recover heavy-metal concentrate, then combine it with local holmium into biocatalysts at stage 1. Oil oceans, ruins and cliffs are protected. Export catalysts.\n\nGLEBA / Spore towers consume filters and nutrients to cultivate symbionts. At stage 3, sheltered yumako and jellynut cultivation becomes efficient, but still needs seeds and perishable nutrient logistics. Export symbionts.\n\nALL THREE / Assemble biodiversity matrices in a recovering (stage 3) ecosystem. These feed sanctuaries and support climate science. Planet identity conditions prevent off-world specialty production.\n\nAQUILO / Import biodiversity matrices to build cryogenic gardens. Buffer heat and turn ice/ammonia into water-cycle recovery. Existing heat mechanics never switch off. Gardens are sheltered sprite overlays: ice and foundation support remain unchanged.'),
        ('Automation, multiplayer and the endgame',
         'Place an ecology circuit monitor and wire it to your factory. It outputs atmosphere, thermal balance, water, soil, biodiversity, toxicity, resistance and stability as integers 0-100. Stage is 0-5. Two additional signals report total planetary and local chunk pollution. Its first section is reserved for telemetry; filters there are overwritten.\n\nExamples: enable detoxifiers when toxicity > 5; enable seed supply when biodiversity < 96; enable thermal buffer production when thermal balance < 97; enable dampeners when resistance > 20. Use a decider latch if you want separate start/stop thresholds.\n\nStage 5 needs every fitness axis ≥ 90, toxicity ≤ 8, total pollution ≤ 500 and a completed hotspot survey with no chunk above 10. Aim for 95-100, not exactly 90; gentle environmental drift and local exposure mean a threshold-edge build will lose stability.\n\nUnlock Gaia coordination, feed a beacon on each living world, and research Second Nature with the resulting restoration science. Then hold all five stage-5 ecosystems for ten uninterrupted minutes with a recent completed beacon cycle on each world. Beacons need a cycle at least every 90 seconds. A broken link resets the timer.\n\nIn multiplayer, ecology is shared per planet. Research and beacon shipments belong to each force; one force cannot win using another’s beacons.\n\nOverhaul progression is a startup setting. Turn it off to preserve vanilla recipes while keeping restoration content. Before removing this mod from a save, disable Network victory, save again, and back up the save; this restores the stock Space Age end condition. Removing a content overhaul can still remove its machines and items.')
    ]
    for i,(title,text) in enumerate(guides,1):put('sn-guide',f'topic-{i}',title);put('sn-guide',f'text-{i}',text)
    for key,text in {
        'welcome':'[Second Nature] Your next megaproject is a living planet. Press Shift + T or the leaf shortcut for the dashboard and field guide. Start with silica → glass → Pioneer biology.',
        'milestone':'[Second Nature] __1__ reached __2__. New ecosystems and production conditions are available.',
        'raid-warning':'[Second Nature] Native resistance on __1__: a restoration installation will be attacked in __2__ seconds. __3__',
        'raid':'[Second Nature] __1__: __2__ native organisms mobilized against restoration.',
        'network-interrupted':'[Second Nature] The network hold was interrupted. __1__',
        'victory':'[Second Nature] Five worlds breathe together. The factory no longer survives at the expense of its home - it sustains it. SECOND NATURE ACHIEVED.',
        'admin-only':'[Second Nature] Only an administrator can rebuild the machine index.',
        'reindexed':'[Second Nature] Machine index reconciled. Planetary progress was preserved.'
    }.items():put('sn-message',key,text)
    for key,text in {'dashboard':'Open the Second Nature field station.','status':'Print a read-only planetary status report.','reindex':'Administrator: rescan restoration machines after script-built entities; preserves progress.'}.items():put('sn-command',key,text)
    setting_info={
        'overhaul-progression':('Overhaul vanilla progression','Default on. Add glass, compost and ecological materials to science, and integrate restoration technologies before rockets. Disable for an additive restoration campaign. Changing this requires a restart.'),
        'restoration-speed':('Restoration speed','Multiplier for ecological gains, toxic debt and drift. Does not change physical production, recipe durations, pollution capture or the ten-minute victory hold. Default 1.'),
        'native-resistance':('Native resistance','Off disables scripted ecological-response waves. Balanced respects local grace, warnings and cooldowns. Relentless uses a lower threshold and shorter cooldown. Vanilla pollution attacks are unchanged; peaceful mode is always respected.'),
        'grace-minutes':('Local resistance grace period (minutes)','Time after the first completed restoration/dirty-impact cycle on EACH planet before scripted native waves can begin. Default 20.'),
        'living-terrain':('Visible terrain recovery','Safely recolor eligible natural ground and show Aquilo garden overlays. Never modifies water, lava, ice, oil oceans, farmland, cliffs, resources, player paving, ghosts or occupied tiles. Disabling stops future changes; it does not undo existing vegetation.'),
        'tree-growth':('Sparse new forest growth','Plant trees only on eligible, unoccupied, restored ground with generous clearance from infrastructure and other trees. Requires Visible terrain recovery. Disabling stops future growth, not existing trees.'),
        'network-victory':('Network victory replaces escape victory','Use the five-world, ten-minute living network as the end condition. Disable to restore the prior stock Space Age finish setting. Disable and save BEFORE uninstalling the mod.'),
        'show-welcome':('Show the first-join field briefing','Print a short guide and dashboard shortcut when first joining with Second Nature.')
    }
    for key,(title,text) in setting_info.items():put('mod-setting-name','sn-'+key,title);put('mod-setting-description','sn-'+key,text)
    for key,text in {'off':'Off','balanced':'Balanced','relentless':'Relentless'}.items():put('string-mod-setting','sn-native-resistance-'+key,text)
    put('item-group-name','sn-restoration','Second Nature')
    put('shortcut-name','sn-dashboard','Second Nature field station');put('controls','sn-toggle-dashboard','Toggle Second Nature field station')
    for key,text in {'sn-restoration-domain':'Restoration domain (1 = supported planet)','sn-planet-identity':'Restoration planet (1 Nauvis / 2 Vulcanus / 3 Fulgora / 4 Gleba / 5 Aquilo)','sn-ecological-stage':'Ecological stage (0-5)'}.items():put('surface-property-name',key,text)
    put('mod-name','second-nature','Second Nature  -  Planetary Restoration')
    put('mod-description','second-nature','A Space Age overhaul about restoring atmosphere, climate, watersheds, soil and biodiversity on five worlds. Clean loops, dirty shortcuts, native resistance and a sustained planetary-network victory.')
    add_campaign_locale(put)
    add_expedition_locale(put)
    add_continuance_locale(put)
    put('sn-layout','footprint','Footprint: __1__ x __2__ tiles.')
    put('mod-setting-name','sn-menu-music','Second Nature menu music')
    put('mod-setting-description','sn-menu-music','Play After the Ash, an original atmospheric score for the main menu. Uses the game music-volume setting. Disable to restore the standard menu track.')
    version=json.loads((MOD/'info.json').read_text())['version']
    put('sn-gui','footer',f'SECOND NATURE / Verdant Works   /   v{version}')
    put('sn-message','welcome',f'[Second Nature] Verdant Works {version} / Press Shift + T for the field station, Ctrl + Shift + P for local smog, Shift + I for inserter vectors, and Ctrl + Shift + J for the jukebox. Begin with stone → silica → glass and Pioneer biology.')
    text='; Generated by tools/generate_locale.py. Edit the catalog or the generator, not this file.\n'
    for section,entries in sections.items():
        text+='\n['+section+']\n'+''.join(key+'='+value+'\n' for key,value in entries.items())
    (MOD/'locale/en/second-nature.cfg').write_text(text,encoding='utf-8')
    print(f'Generated {sum(map(len,sections.values()))} English locale entries.')
if __name__=='__main__':generate()
