"""Record only observed visual coverage and verified normal source admission."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1]
base=root/'character/marsh-v2/supplemental/cargo-matched-v1'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
world=base/'world-review'
assessment={'actuallyInspected':[{'file':f'route-{i:02}-pairs.png','sha256':sha(world/f'route-{i:02}-pairs.png')} for i in range(8)],'scope':'All eight source/native route boards,62pairs, inspected. Sampled still images, not continuously watched cadence.','observations':'Normal selection is visible through pickup, loaded swimming, turns, drain, carry and unload. Ivory/olive/charcoal suit and sandy hair remain recognizable. Body/root, case, head/grade, kick, contact and family joins remain provisional.','fullGoalComplete':False}
(world/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
p=world/'verification.json';r=read(p);r['visualReviewed']=True;r['visualScope']=assessment['scope'];p.write_text(json.dumps(r,indent=2)+'\n')
p=base/'player-review/verification.json';r=read(p)
for board in r['boards']:board['actuallyInspected']=True
r['visualScope']='Four cardinal dry carry triplets (12 of144native captures), old/selected/own-idle at source/station scale inspected. Remaining132captures generated, not visually accepted.'
r['visualObservations']='New side bodies are less bulky and closer to idle; source and station height preserved. Cases differ from old sources, head and matte suit detail remain softer/different than own idle. No complete head/material/contact/cadence acceptance.'
p.write_text(json.dumps(r,indent=2)+'\n')
current=read(root/'character/marsh-selected-normal-audit-2026-10-03-post-cargo/inventory.json')['states']
old=read(root/'character/marsh-full-family-audit-2026-10-03/inventory.json')['states']
assert set(old)==set(current)
changed=[]
for key,s in current.items():
    prior=old[key]
    signature=([f['sha256'] for f in s['frames']],s['state']['frameDurationsMs'],s['state']['loop'],s['pivot'],s['standingHeight'])
    old_signature=([f['sha256'] for f in prior['frames']],prior['durationsMs'],prior['loop'],prior['pivot'],prior['standingHeight'])
    if signature!=old_signature:changed.append(key)
assert len(changed)==9 and all(k.startswith(('equip-helmet-','remove-helmet-')) or k=='cargo-drain-south' for k in changed),changed
comparison={'comparison':'Source hashes, ordered holds,loop,pivot,height; path-only admission differences ignored.','changedStates':changed,'changedCount':len(changed),'added':0,'removed':0,'fullGoalComplete':False}
(root/'character/marsh-selected-normal-audit-2026-10-03-post-cargo/comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
note='''
## Marsh cargo bank normal admission — October 3, 2026

Normal catalogue now selects the reviewed48cargo states through eight manifests
in character/marsh-v2/supplemental/cargo-matched-v1.200whole PNG copies,272ordered
slots; source metadata, timing, strides, pivots and height preserved. Exactly48states
changed,180others preserved;228normal body states/1190slots/86body manifests.
No actor/gameplay/resource/save/room changes, no new generation. Admission is
reversible source progress during polish, not owner/full-set visual acceptance.
All eight source manifests and200unique PNGs matched preceding World09 hashes.

Actual normal-catalogue player proof:1653checks,0failures,48states/272exactslots,
272same-clock player restores,144first/middle/last comparison captures. Four cardinal
dry carry triplets (12captures) actually inspected: side bodies closer to idle than
old bulky sources; heads and matte material detail still differ.132other captures
generated, not newly visually accepted. Normal actual expedition proof uses NO
manifest injections:15221checks,0failures,3710samples,62exact source/native pairs,
62actor/player restores and pause holds, all12phases, one dry/alive completion,
credit only after safe unloading. Eight route boards/62pairs actually inspected.
No continuous cadence, contact, all actor-facing routes, disk fullSave/TitleContinue
or full-family acceptance inferred. q2/Southdrain06 fixture is prescribed airlock/
site setup, not paid-building proof; normal free-build/failure-disable flags false.
Both jobs exit0, no errors/warnings/SCRIPT ERROR;5509bounded inputs and2931owner
non-log files unchanged across combined scratchAPPDATA interval.

Authoritative inventory character/marsh-selected-normal-audit-2026-10-03-post-cargo/
inventory.json. Compared by source hashes/holds/loop/pivot/height with frozen private
full-family audit,9states differ:8new gesture aliases and later Southdrain06,
0added/removed. The48private cargo
states are now normal-selected; path copying is not an art change. Body/root/case,
head/proportion/grade, swim kick, floor contact and transitions remain provisional.
Retain source-specific density and occupied heights; H148metadata is not a universal
occupied-height ruler. Never infer current normal admission from private overlay
tests; load actual catalogue and require current source/native pixel parity.
Full Marsh objective active. Next reconcile remaining visual-family coverage and
review native seams/cadence/contact before cross-family head/material polish.
'''
canonical=root/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [root/'character/ANIMATION_PIPELINE.md',root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('rb') as f:f.seek(max(0,p.stat().st_size-100000));tail=f.read().decode('utf-8',errors='ignore')
    if '## Marsh cargo bank normal admission' not in tail:
        with p.open('a',encoding='utf-8') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('12new boards inspected; normal228/1190inventory reconciled:8gesture+1Southdrain06 differences; pipeline/bible/status/skill recorded')
