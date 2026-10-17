"""All current selected families, registered masters and source clocks for review."""
from pathlib import Path
import json, hashlib, re
P = Path(__file__).resolve().parent
R = P.parents[1]
I = R/'character/bill-selected-source-audit-2026-10-01-locomotion-v16/source-inventory.json'
a = json.loads(I.read_text())
b = (R/'scripts/grid_canvas.gd').read_text().split('func _load_major_bill_animations() -> void:',1)[1].split('\nfunc ',1)[0]
assert hashlib.sha256(b.encode()).hexdigest() == a['loaderBlockSha256']
data, records, cache = {}, [], {}
def group(k):
    for name, prefixes in [
        ('Locomotion', ('idle-','walk-','run-')),
        ('Work and tools', ('interact-','kneel-','repair-','stand-','torch-','weld-','inspect-')),
        ('Cargo', ('carry-','pickup-','unload-','salvage-')),
        ('Rest and seated', ('sit-','read-seated-','lie-down-','get-up-','sleep-','bunk-')),
        ('Meals', ('eat-','drink-')),
        ('Death and recovery', ('death-','recover-air-')),
        ('Water', ('swim-','tread-'))]:
        if k.startswith(prefixes): return name
    return 'Equipment'
for gear, states in a['selectedStateSources'].items():
    for key, s in states.items():
        if s['manifest'] not in cache:
            cache[s['manifest']] = json.loads((R/s['manifest']).read_text())
        m = cache[s['manifest']]
        assert hashlib.sha256((R/s['manifest']).read_bytes()).hexdigest() == a['manifestSha256'][s['manifest']]
        st = next(t for t in m['states'] if t['id'] == key)
        files = s['sourceFiles']
        assert all((R/f[6:]).is_file() for f in files), key
        dur = st.get('frameDurationsMs', [1000/st.get('fps',m.get('fps',12))]*len(files))
        assert len(files) == len(dur) and min(dur)>0
        d = key.split('-')[-1]
        assert d in ['east','west','north','south']
        dirs = re.findall(r'(?:east|west|north|south)',key)
        origin = dirs[-2] if '-turn-' in key else d
        masters = {}
        for role,di in [('source',origin),('destination',d)]:
            f = f'character/bill-seated-{"helmet-" if gear=="helmet" else ""}{di}-coherent-v1/frames/sit-down-{di}/000.png'
            assert (R/f).is_file()
            masters[role] = '../../'+f
        data.setdefault(key, {'group':group(key),'profiles':{}})['profiles'][gear] = {
            'files':['../../'+f[6:] for f in files], 'durations':dur,
            'pivot':s['pivot'], 'height':s['standingHeight'], 'loop':st.get('loop',True),
            'masters':masters, 'manifest':s['manifest']}
        records.append({'gear':gear,'key':key,'manifest':s['manifest'],
                        'frames':len(files),'durationMs':sum(dur),'group':group(key)})
template = (P/'template.html').read_text(encoding='utf-8')
(P/'index.html').write_text(template.replace('/*SOURCE_DATA*/',json.dumps(data)),encoding='utf-8')
(P/'source-review.json').write_text(json.dumps({
    'inventory':I.relative_to(R).as_posix(),
    'inventorySha256':hashlib.sha256(I.read_bytes()).hexdigest(),
    'loaderBlockSha256':a['loaderBlockSha256'], 'manifestSha256':a['manifestSha256'],
    'scope':'All selected keys available for source review. Building does not prove all-frame visual acceptance or runtime behavior.',
    'rows':records},indent=2)+'\n')
print(json.dumps({'bare':sum(r['gear']=='bare' for r in records),
                  'helmet':sum(r['gear']=='helmet' for r in records),
                  'families':sorted(set(r['group'] for r in records))}))
