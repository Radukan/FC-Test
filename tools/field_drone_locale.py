"""Field Crew UI text, generated into the normal English locale."""

def add_field_drone_locale(put):
    entries={
        'title':'Field construction crew',
        'stats':'Active: __1__/__2__   Packed: __3__   Built: __4__',
        'help':'Ctrl + Shift + B: enable or pause. Carry a field controller, drones and construction materials. Radius: 18 tiles. Set the crew limit in per-player mod settings.',
        'pause':'Pause + recall', 'enable':'Enable crew', 'hide':'Hide',
        'hide-help':'Hide this monitor. An enabled crew keeps working.',
        'off':'Field drones are paused. All reserved supplies have been returned.',
        'working':'Drones are constructing or returning to their operator.',
        'waiting':'Waiting for nearby entity or tile ghosts with matching carried materials.',
        'character':'Field drones require a connected, controllable character. Remote view, editor and cutscenes pause work.',
        'permission':'Your permission group does not allow construction.',
        'research':'Research Field construction robotics first: 20 automation science packs after Automation.',
        'controller':'Carry a field drone controller in your character inventory.',
        'platform':'Wind-up field drones do not operate on space platforms.',
        'no-drones':'Carry wind-up construction drones in your character inventory.',
        'loose-items':'Clear loose items beneath the ghost first. Field drones do not collect or transport dropped cargo.',
        'materials':'A nearby ghost needs matching-quality materials, or a specialized packed item that field drones cannot place.'
    }
    for key,value in entries.items():put('sn-drones',key,value)
    put('shortcut-name','sn-field-drones','Toggle field construction drones')
    put('controls','sn-toggle-field-drones','Toggle field construction drones')
    put('mod-setting-name','sn-field-drone-limit','Personal field-drone crew limit')
    put('mod-setting-description','sn-field-drone-limit','Maximum concurrent wind-up construction drones for this player. Default 64, maximum 128. Drones and building materials must be carried in your inventory; no roboport or logistics network is used. The server-wide safety limit is 512 active field drones. Lowering the limit recalls surplus workers without losing reserved supplies.')
