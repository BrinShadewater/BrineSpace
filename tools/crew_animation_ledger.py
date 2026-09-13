"""Inventory every selected crew clip without inferring visual acceptance."""
from pathlib import Path
import csv,json,hashlib,collections

ROOT=Path(__file__).resolve().parents[1]
PACKS={'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}
OUT=ROOT/'docs/crew-animation-ledger'

def category(key):
    if key.startswith('interact-'):return 'instrument'
    if key.startswith('repair-'):return 'repair'
    if key.startswith(('eat-','drink-','read-seated-')):return 'daily-life'
    if key.startswith('death-'):return 'death'
    if key.startswith(('swim-','tread-','recover-air-','salvage-')):return 'water'
    return 'other-motion-and-transitions'

def main():
    OUT.mkdir(exist_ok=True)
    path=OUT/'clips.csv'
    prior={}
    if path.exists():
        with path.open(newline='',encoding='utf-8') as f:
            prior={(r['actor'],r['variant'],r['state']):r for r in csv.DictReader(f)}
    rows=[]
    for actor,folder in PACKS.items():
        root=ROOT/'character'/folder
        for variant,manifests in json.loads((root/'catalog.json').read_text()).items():
            if variant not in ['body','equipment']:continue
            for relative in manifests:
                manifest=root/relative;data=json.loads(manifest.read_text())
                for state in data['states']:
                    digest=hashlib.sha256()
                    for frame in state['frameFiles']:digest.update((manifest.parent/frame).read_bytes())
                    digest.update(json.dumps({'pivot':data['pivot'],'durations':state['frameDurationsMs']},sort_keys=True).encode())
                    key=(actor,variant,state['id']);old=prior.get(key,{})
                    status=old.get('visual_status','needs-evidence-reconciliation')
                    if old.get('selected_sha256') and old['selected_sha256']!=digest.hexdigest():status='changed-since-recorded-review'
                    rows.append(dict(actor=actor,variant=variant,state=state['id'],category=category(state['id']),frames=len(state['frameFiles']),manifest=manifest.relative_to(ROOT).as_posix(),selected_sha256=digest.hexdigest(),visual_status=status,evidence=old.get('evidence',''),next_action=old.get('next_action','Reconcile prior evidence; review or replace as needed')))
    rows.sort(key=lambda r:(r['actor'],r['variant'],r['state']))
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    counts={variant:dict(collections.Counter(r['category'] for r in rows if r['variant']==variant)) for variant in ['body','equipment']}
    summary={'totalClips':len(rows),'categories':counts,'visualStatusCounts':dict(collections.Counter(r['visual_status'] for r in rows)),'meaning':'An unresolved ledger row is missing reconciled acceptance evidence, not proof that its art must be regenerated.'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))

if __name__=='__main__':main()
