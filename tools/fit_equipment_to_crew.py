"""Apply reviewed, per-prop scale corrections to authored room defaults.

One-time migration using output/crew-scale-catalog-before's frozen native catalog
and defaults-before-scale.json. Never capture a new baseline over the final layout.
Preserves floor foot anchors and wall contact; no source image resampling.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/crew-scale-catalog-before'
TARGETS = {
    'crew_hab': {'full_wall_crew-hab-berth-wall': .72, 'hab_chair': .62, 'hab_desk': .70, 'hab_berth_west': .68, 'hab_berth_east': .68},
    'crew_lounge': {'full_wall_crew-lounge-built-in': .72, 'lounge_galley': .70, 'book_console': .80, 'lounge_sofa': .75},
    'med_bay': {'full_wall_medical-treatment-wall': .65, 'med_bed_0': .70, 'med_bed_1': .70, 'med_console': .65, 'med_supply': .80},
    'med_office': {'office_exam': .72, 'office_consultation': .80},
    'med_center': {'medical_treatment': .82, 'medical_imaging': .85},
    'cryo_chamber': {'cryo_console': .62, 'cryo_pod_0': .80, 'cryo_pod_1': 1.0},
    'observation_room': {'wooden-desk': .70, 'chair-rear': .82},
    'current_turbine': {'life_console': .60},
    'heat_recovery': {'life_console': .60},
    'biomass_digester': {'life_console': .85},
    'mycelium_nursery': {'bench': .70, 'filter': .80},
    'clone_lab': {'clone_console': .70, 'clone_nutrients': .80},
    'bio_lab': {'bio_centrifuge': .80, 'bio_cold_storage': .80},
    'anomaly_lab': {'anomaly_diagnostics': .72},
    'xeno_lab': {'xeno_workbench': .75, 'xeno_scanner': .80, 'xeno_samples': .85},
    'research_lab': {'research_specimens': .80, 'research_scanner': .85},
    'solar_array': {'thermal_monitor': .65},
    'shield_generator': {'hull_monitor': .65},
    'listening_post': {'acoustic_listener': .80},
    'maintenance_bay': {'maintenance_diagnostics': .70},
    'reactor': {'reactor_console': .80},
    'isolation_vault': {'full_wall_emergency-isolation-wall': .70},
}

def main():
    path = ROOT / 'rooms/full-wall-v1/default-layouts.json'
    baseline = OUT / 'defaults-before-scale.json'
    if not baseline.exists():
        raise SystemExit('Missing frozen pre-scale defaults; refusing to scale current defaults again.')
    original = json.loads(baseline.read_text(encoding='utf-8'))
    current = json.loads(path.read_text(encoding='utf-8'))
    catalog = json.loads((OUT / 'runtime.json').read_text(encoding='utf-8'))
    asset_ids = {x['view']: x['asset'] for x in json.loads((ROOT / 'rooms/full-wall-v1/editor-catalog.json').read_text())}
    editor_ids = asset_ids.copy()
    # Full-wall wrappers apply their own authoring identity; a few Studio entries
    # still use a legacy room-* alias. Bind to the consumer that paints the prop.
    for room in catalog:
        source = ROOT / room['view'].removeprefix('res://')
        if source.exists():
            match = re.search(r'full_wall_prop\.gd"\)\.new\("([^"]+)"\)', source.read_text())
            if match:
                asset_ids[room['view']] = match[1]
    # Undo this tool's earlier alias-only writes without touching other keys.
    previous = OUT / 'scale-changes.json'
    if previous.exists():
        for change in json.loads(previous.read_text()):
            if change['layout'].rsplit('/',1)[0] == asset_ids[next(r['view'] for r in catalog if r['id']==change['room'])]:
                continue
            dest = current['layouts'][change['layout']]
            base = original['layouts'].get(change['layout'], {})
            for name in [change['prop'], 'size/'+change['prop']]:
                if name in base: dest[name] = base[name]
                else: dest.pop(name, None)
    changes = []
    for room in catalog:
        targets = TARGETS.get(room['id'], {})
        for view in room['views']:
            key = asset_ids[room['view']] + '/' + str(view['quarter'])
            old = original['layouts'].get(key, {})
            new = current['layouts'].setdefault(key, {})
            for prop in view['props']:
                identity = prop['id']
                factor = targets.get(identity)
                if factor is None:
                    continue
                x, y, w, h = prop['rect']
                if room['id']=='cryo_chamber' and identity.startswith('cryo_pod_'):
                    factor = 62.0/w # One human-sized shell in every orientation.
                vx, vy, vw, vh = prop['visual_bounds']
                scale = old.get('size/' + identity, [1, 1])[0] * factor
                # Floor props retain the bottom-center foot anchor.
                at = [x + w * (1-factor)/2, y + h * (1-factor)]
                if room['id']=='cryo_chamber' and identity.startswith('cryo_pod_'):
                    index=int(identity[-1])
                    if view['quarter']==0: at=[20.0+index*80.0,-132.0]
                    elif view['quarter']==2: at=[-170.0+index*80.0,40.0]
                    elif view['quarter']==3: at=[-158.0+index*86.0,-132.0]
                if prop['full_wall']:
                    if w >= h:
                        # Preserve the outward source edge and center the bank.
                        at[1] = vy - (vy-y)*factor if y < 0 else y+h-h*factor
                    else:
                        at = [x if x < 0 else x+w-w*factor, y+h*(1-factor)/2]
                new['size/' + identity] = [round(scale, 6)] * 2
                new[identity] = [round(n, 6) for n in at]
                if editor_ids[room['view']] != asset_ids[room['view']]:
                    alias = editor_ids[room['view']] + '/' + str(view['quarter'])
                    editor = current['layouts'].setdefault(alias, {})
                    editor[identity] = new[identity].copy()
                    editor['size/'+identity] = new['size/'+identity].copy()
                changes.append({'room': room['id'], 'layout': key, 'prop': identity,
                                'factor': factor, 'before_rect': prop['rect'],
                                'before_visual': prop['visual_bounds'],
                                'scale': scale, 'position': new[identity]})
    path.write_text(json.dumps(current, indent=2) + '\n', encoding='utf-8')
    (OUT / 'scale-changes.json').write_text(json.dumps(changes, indent=2) + '\n', encoding='utf-8')
    print(f'{len(changes)} placements adjusted across {len(set(x["room"] for x in changes))} rooms')

if __name__ == '__main__':
    main()
