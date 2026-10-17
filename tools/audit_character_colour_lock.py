"""Verify every frozen colour export, approved correction, and seven palette files.

An exact drift gate, not an assertion that every legacy pose is visually accepted.
"""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/palette-standard-v1'
REV=ROOT/'character/veld-consistency-v1'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    mapped=read(BASE/'mapping.json')['files'];changes=read(REV/'mapping.json');errors=[];counts={}
    injury_path=ROOT/'character/marsh-injury-runtime-v1/installation.json'
    if injury_path.exists():
        for rel,record in read(injury_path)['frames'].items():
            if rel in mapped:errors.append('Injury export unexpectedly replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    quality_path=ROOT/'character/marsh-quality-pass-v2/installation.json'
    if quality_path.exists():
        for rel,record in read(quality_path)['frames'].items():
            if rel in mapped:errors.append('Quality export unexpectedly replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    chat_path=ROOT/'character/marsh-crew-chat-v1/installation.json'
    if chat_path.exists():
        for rel,record in read(chat_path)['frames'].items():
            if rel in mapped:errors.append('Conversation export replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    chat_v2_path=ROOT/'character/marsh-crew-chat-v2/installation.json'
    if chat_v2_path.exists():
        for rel,record in read(chat_v2_path)['frames'].items():
            if rel in mapped:errors.append('Conversation revision replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    quality_v3_path=ROOT/'character/marsh-quality-pass-v3/installation.json'
    if quality_v3_path.exists():
        for rel,record in read(quality_v3_path)['frames'].items():
            if rel in mapped:errors.append('Quality revision replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    diagnostic_path=ROOT/'character/marsh-diagnostics-v4/installation.json'
    if diagnostic_path.exists():
        for rel,record in read(diagnostic_path)['frames'].items():
            if rel in mapped:errors.append('Diagnostic revision replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    diagnostic_v5_path=ROOT/'character/marsh-diagnostics-v5/installation.json'
    if diagnostic_v5_path.exists():
        for rel,record in read(diagnostic_v5_path)['frames'].items():
            if rel in mapped:errors.append('Diagnostic complete pose replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    diagnostic_v6_path=ROOT/'character/marsh-diagnostics-v6/installation.json'
    if diagnostic_v6_path.exists():
        for rel,record in read(diagnostic_v6_path)['frames'].items():
            if rel in mapped:errors.append('Diagnostic outline revision replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    diagnostic_v7_path=ROOT/'character/marsh-diagnostics-v7/installation.json'
    if diagnostic_v7_path.exists():
        for rel,record in read(diagnostic_v7_path)['frames'].items():
            if rel in mapped:errors.append('Diagnostic style revision replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    fullset_path=ROOT/'character/marsh-quality-pass-v4/installation.json'
    if fullset_path.exists():
        for rel,record in read(fullset_path)['frames'].items():
            if rel in mapped:errors.append('Full set grade replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    repair_path=ROOT/'character/marsh-master-repair-v1/installation.json'
    if repair_path.exists():
        for rel,record in read(repair_path)['frames'].items():
            if rel in mapped:errors.append('Master repair replaces a frozen path: '+rel)
            else:mapped[rel]={'actor':'marsh','sha256':record['sha256']}
    marsh_run=read(ROOT/'character/marsh-run-match-v1/colour-lock.json')
    for rel,record in marsh_run.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Run baseline mismatch: '+rel)
        changes[rel]=record
    marsh_carry=read(ROOT/'character/marsh-carry-chain-v1/colour-lock.json')
    for rel,record in marsh_carry.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Carry baseline mismatch: '+rel)
        changes[rel]=record
    cargo_endpoint=read(ROOT/'character/marsh-carry-chain-v1/cargo-drain-endpoint-colour-lock.json')
    for rel,record in cargo_endpoint.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Cargo drain baseline mismatch: '+rel)
        changes[rel]=record
    cargo_middle=read(ROOT/'character/marsh-cargo-drain-match-v1/colour-lock.json')
    for rel,record in cargo_middle.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Cargo rise baseline mismatch: '+rel)
        changes[rel]=record
    salvage=read(ROOT/'character/marsh-salvage-match-v1/colour-lock.json')
    for rel,record in salvage.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Salvage baseline mismatch: '+rel)
        changes[rel]=record
    swim_pickup=read(ROOT/'character/marsh-swim-pickup-match-v1/colour-lock.json')
    for rel,record in swim_pickup.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Swim pickup baseline mismatch: '+rel)
        changes[rel]=record
    maintenance=read(ROOT/'character/marsh-maintenance-match-v1/colour-lock.json')
    for rel,record in maintenance.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Maintenance baseline mismatch: '+rel)
        changes[rel]=record
    welding=read(ROOT/'character/marsh-welding-match-v1/colour-lock.json')
    for rel,record in welding.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Welding baseline mismatch: '+rel)
        changes[rel]=record
    seated=read(ROOT/'character/marsh-seated-match-v1/colour-lock.json')
    for rel,record in seated.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Seated baseline mismatch: '+rel)
        changes[rel]=record
    rest=read(ROOT/'character/marsh-rest-match-v1/colour-lock.json')
    for rel,record in rest.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Rest baseline mismatch: '+rel)
        changes[rel]=record
    furniture=read(ROOT/'character/marsh-furniture-match-v1/colour-lock.json')
    for rel,record in furniture.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Furniture baseline mismatch: '+rel)
        changes[rel]=record
    water=read(ROOT/'character/marsh-water-match-v1/colour-lock.json')
    for rel,record in water.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Water baseline mismatch: '+rel)
        changes[rel]=record
    water_turns=read(ROOT/'character/marsh-water-turn-match-v1/colour-lock.json')
    for rel,record in water_turns.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Water turn baseline mismatch: '+rel)
        changes[rel]=record
    loaded_water=read(ROOT/'character/marsh-loaded-water-match-v1/colour-lock.json')
    for rel,record in loaded_water.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Loaded water baseline mismatch: '+rel)
        changes[rel]=record
    shutdown=read(ROOT/'character/marsh-shutdown-injury-match-v1/colour-lock.json')
    for rel,record in shutdown.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Shutdown baseline mismatch: '+rel)
        changes[rel]=record
    recovery=read(ROOT/'character/marsh-water-recovery-match-v1/colour-lock.json')
    for rel,record in recovery.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Water recovery baseline mismatch: '+rel)
        changes[rel]=record
    galley=read(ROOT/'character/marsh-galley-match-v1/colour-lock.json')
    for rel,record in galley.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Galley baseline mismatch: '+rel)
        changes[rel]=record
    tone=read(ROOT/'character/marsh-controller-tone-v1/colour-lock.json')
    for rel,record in tone.items():
        previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
        if record['before']!=previous:errors.append('Controller tone baseline mismatch: '+rel)
        changes[rel]=record
    polish_path=ROOT/'character/marsh-full-polish-v1/colour-lock.json'
    if polish_path.exists():
        for rel,record in read(polish_path).items():
            previous=changes.get(rel,{}).get('after',mapped[rel]['sha256'])
            if record['before']!=previous:errors.append('Full polish baseline mismatch: '+rel)
            changes[rel]=record
    lock=read(REV/'palette-lock.json')
    for actor,h in lock.items():
        if sha(BASE/'palettes'/f'{actor}.json')!=h:errors.append('Palette changed: '+actor)
    for rel,e in mapped.items():
        expected=changes.get(rel,{}).get('after',e['sha256'])
        if sha(ROOT/rel)!=expected:errors.append('Unexpected frame change: '+rel)
        counts[e['actor']]=counts.get(e['actor'],0)+1
    # New selected art cannot silently bypass the lock through a new filename.
    selected_states=0;selected_files=set()
    for actor,folder in [('bill','major-bill-v3'),('veld','dr-veld-v2'),('branforth','chief-engineer-branforth-v2'),('marsh','marsh-v2')]:
        base=ROOT/'character'/folder;cat=read(base/'catalog.json')
        for variant in ['body','equipment']:
            for f in cat[variant]:
                p=base/f
                for s in read(p)['states']:
                    selected_states+=1
                    selected_files.update((p.parent/f).resolve().relative_to(ROOT).as_posix() for f in s['frameFiles'])
    for actor in ['margot','josh','river']:
        base=ROOT/'character'/('margot-polish-v1' if actor=='margot' else 'robot-polish-v1')
        pack=read(base/'manifest.json' if actor=='margot' else base/actor/'manifest.json')
        for s in pack['states']:
            selected_states+=1;selected_files.update((base/f).resolve().relative_to(ROOT).as_posix() for f in s['frameFiles'])
    errors.extend('Unreviewed selected frame: '+f for f in selected_files-set(mapped))
    report={'lockedPalettes':len(lock),'checkedPngPaths':len(mapped),'selectedStateVariants':selected_states,'selectedPngPaths':len(selected_files),'counts':counts,'corrections':len(changes),'errors':errors}
    (REV/'colour-lock-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
