"""Player-facing copy for Living World 0.5. No authoring/progression chatter in objects."""
from pathlib import Path
import json
from catalog import ROOT

def add_continuance_locale(put):
    groups={
      'mod-setting-name':{'sn-opening-audio':'Landing transmission and anthem','sn-inserter-vectors':'Inserter vector controls'},
      'mod-setting-description':{
        'sn-opening-audio':'Play the landing transmission followed by We Need a Living World on first arrival at Nauvis. Disable to keep the normal arrival soundtrack.',
        'sn-inserter-vectors':'Allow pickup and delivery positions to be configured within two tiles on either axis. Existing endpoints remain unchanged until adjusted. Applies to every inserter prototype.'},
      'controls':{'sn-configure-inserter':'Configure selected inserter vectors','sn-open-jukebox':'Open a nearby expedition jukebox'},
      'shortcut-name':{'sn-inserter-vectors':'Inserter vectors','sn-jukebox':'Expedition jukebox'},
      'sn-inserter':{
        'title':'Inserter vectors','range':'Select pickup and delivery tiles within two tiles on either axis. The center and identical endpoints are excluded.',
        'pickup':'Pickup','drop':'Delivery','reset':'Reset vectors','offset':'Relative tile: x __1__, y __2__',
        'select':'Select an inserter belonging to your force, then press Shift + I. Vector controls must be enabled in mod settings.'},
      'sn-jukebox':{
        'title':'Expedition jukebox','description':'Recorded scores and expedition transmissions. Playback is local by default. A surface broadcast requires an administrator in multiplayer.',
        'after-ash':'After the Ash','living-world':'We Need a Living World','transmission':'Landing transmission and anthem',
        'broadcast':'Broadcast across this surface','stop':'Stop jukebox','place':'Place or select an expedition jukebox nearby to access the archive.',
        'admin':'A multiplayer administrator is required to broadcast across the surface.'},
      'sn-lore':{'title':'Landing transmission: personal log','close':'Close transmission log'},
      'programmable-speaker-instrument':{'sn-expedition-archive':'Second Nature archive'},
      'programmable-speaker-note':{'sn-stop':'Silence','sn-after-the-ash':'After the Ash','sn-living-world':'We Need a Living World','sn-transmission':'Landing transmission'},
      'sn-gui':{'footer':'SECOND NATURE / A living world is worth the work.   /   v0.5.0'},
    }
    for group,entries in groups.items():
        for key,value in entries.items():put(group,key,value)
    score=json.loads((ROOT/'docs/art/living-world-score.json').read_text())
    put('sn-lore','transmission',score['intro'])
    put('sn-guide','topic-6','Expedition archive and precision logistics')
    put('sn-guide','text-6','PERSONAL LOG\nThe landing transmission plays before the expedition anthem on first arrival at Nauvis. The jukebox preserves the transmission, We Need a Living World and After the Ash for later playback. Select a jukebox or press Ctrl + Shift + J nearby. Local playback does not broadcast to the whole planet; multiplayer surface broadcasts require an administrator.\n\nINSERTER VECTORS\nOpen an inserter or select it and press Shift + I. Each grid covers offsets from -2 to +2 on both axes. Choose separate pickup and delivery tiles. The origin is blocked. Reset restores the current-direction default, bounded by the same range. Blueprint and robot placement preserve native custom vectors.\n\nLIVING-WORLD LOGISTICS\nThe vector servo inserter accelerates bulk transfer. The canopy stack inserter moves stacked cargo. Vital belts, tunnels and distribution manifolds share a 90-item-per-second base speed and retain normal belt stacking, filtering and priority controls. Underground connections span up to sixteen tiles.\n\nBIOLOGICAL DEFENSE\nRootweaver emplacements can use mycelial flechettes that slow exposed targets. Ordinary ballistic magazines remain compatible. Resonance diffusers disrupt movement with an electrical and pheromonal field. Pressure-lance rounds pierce armored targets and bind a small amount of actual airborne contamination at impact. They award no ecological fitness or science. Keep their firing lanes clear.\n\nTHE LIVING FRONTIER\nHabitat still grows and degrades over sustained time. The two-minute native decision hold, permanent Nauvis choice and five-world beacon victory remain unchanged.')
