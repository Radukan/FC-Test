"""Field Crew UI text, generated into the normal English locale."""

def add_field_drone_locale(put):
    entries={
        'title':'Field construction crew',
        'introduction':'[Second Nature] Your inventory-fed field crew is enabled. Ctrl + Shift + B pauses/resumes it and opens this monitor. No armor or power supply is needed. Use the normal blueprint, deconstruction and upgrade planners.',
        'tuning-1':'Field drones: reach 22 tiles, flight 2.52 tiles/second, work cycle 1.25 seconds.',
        'tuning-2':'Field drones: reach 26 tiles, flight 3 tiles/second, work cycle 1 second.',
        'stats':'Active: __1__/__2__   Packed: __3__\nBuilt: __4__   Removed: __5__   Upgraded: __6__',
        'help':'AUTO-ENABLED with the researched kit in your inventory. Ctrl + Shift + B: pause/resume and open this monitor. Carry a controller, drones and materials. Use blueprints, copy/paste, deconstruction and upgrade planners. Research tunes reach and speed.',
        'pause':'Pause + recall', 'enable':'Enable crew', 'hide':'Hide',
        'hide-help':'Hide this monitor. An enabled crew keeps working.',
        'off':'Field drones are paused. All reserved supplies have been returned.',
        'working':'Drones are building, deconstructing, upgrading or returning with cargo.',
        'waiting':'Waiting for nearby ghosts, deconstruction orders or upgrade orders with suitable carried materials.',
        'character':'Field drones require a connected, controllable character. Remote view, editor and cutscenes pause work.',
        'permission':'Your permission group does not allow construction.',
        'research':'Research Field construction robotics first: 20 automation science packs after Automation.',
        'controller':'Carry a field drone controller in your character inventory.',
        'platform':'Wind-up field drones do not operate on space platforms.',
        'no-drones':'Carry wind-up construction drones in your character inventory.',
        'loose-items':'Clear or explicitly mark loose items beneath the ghost for deconstruction first.',
        'materials':'A target needs matching-quality materials or is a specialized packed item. Underground upgrades reserve a pair when connected.'
    }
    for key,value in entries.items():put('sn-drones',key,value)
    put('shortcut-name','sn-field-drones','Field drones: pause/resume (Ctrl + Shift + B)')
    put('controls','sn-toggle-field-drones','Field drones: pause/resume (Ctrl + Shift + B)')
    put('mod-setting-name','sn-field-drone-limit','Personal field-drone crew limit')
    put('mod-setting-description','sn-field-drone-limit','Maximum concurrent wind-up construction drones for this player. Default 64, maximum 128. Drones and building materials must be carried in your inventory; no roboport or logistics network is used. The server-wide safety limit is 512 active field drones. Lowering the limit recalls surplus workers without losing reserved supplies.')
