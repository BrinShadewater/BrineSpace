from pathlib import Path
import json,io,contextlib
p=Path(__file__).resolve().parent
r=p.parents[1]
source_path=r/'character/james-west-carry-walk-keys-v1/inventory_full_set_v18.py'
source=source_path.read_text(encoding='utf-8')
source=source.replace("out=r/'character/james-full-set-review-2026-10-02';out.mkdir(exist_ok=True)","out=r/'character/james-full-set-review-2026-10-02/current-selection-v31';out.mkdir(exist_ok=True)")
namespace={'__file__':str(source_path)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(source,str(source_path),'exec'),namespace)
now=json.loads((namespace['out']/'source-inventory.json').read_bytes())
prior=json.loads((r/'character/james-full-set-review-2026-10-02/current-selection-v27/source-inventory.json').read_bytes())
changed=[]
for gear,bank in prior['states'].items():
    assert set(bank)==set(now['states'][gear])
    for key,row in bank.items():
        current=now['states'][gear][key]
        for field in ['frameCount','frameDurationsMs','loop','pivot','standingHeight','frameWidth','frameHeight']:
            assert row[field]==current[field],(gear,key,field)
        a=[(r/f).resolve() for f in row['frameFiles']]
        b=[(r/f).resolve() for f in current['frameFiles']]
        if a!=b:changed.append(dict(gear=gear,state=key))
expected={(gear,action+'-'+direction) for gear in ['bare','helmet'] for action in ['inspect','interact'] for direction in ['south','north','west']}
assert {(c['gear'],c['state']) for c in changed}==expected,changed
for key in ['missingFrameSources','invalidDeclaredCounts','invalidClockLengths']:assert now['summary'][key]==0
proof=dict(changedSourceStates=changed,allOtherEffectiveSourcePathsExact=True,allStateCountsClocksCanvasPivotsRulersExact=True,scope='Primary literal catalog/grid sources only; does not execute cargo special-player cues or imply complete animation quality.')
(p/'effective-selection-comparison.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(dict(changedSourceStates=len(changed),allOtherEffectiveSourcePathsExact=True)))
