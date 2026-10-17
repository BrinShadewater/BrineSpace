from pathlib import Path
import json,hashlib,os,uuid,time
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'pickup-carry-contact-v48'
inputs=json.loads((out/'inputs.json').read_bytes())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert all(sha(r/x['file'])==x['sha256'] for x in inputs['sourceRecords'])
equal={}
for mode in ['bare','helmet']:
    rows={x['label']:x for x in inputs['sourceRecords'] if x['mode']==mode}
    equal[mode]=rows['pickup5']['sha256']==rows['normal-walk0']['sha256']
    assert equal[mode]
    assert np.array_equal(np.asarray(Image.open(r/rows['pickup5']['file'])),np.asarray(Image.open(r/rows['normal-walk0']['file'])))
review=dict(reviewedBoards=1,reviewedSources=14,pickupTerminalExactNormalWalkEntry=equal,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Normal pickup5 is byte/pixel-exact to normal carry-west0 for both gears.','Staged V44 prep0 widens stance after pickup5 and changes body/case presentation; its start is inappropriate after the actual normal pickup terminal.','Staged V16 walk entry has different fabric/detail and case size from normal pickup/normal walk; geometry/material reconciliation required.','Do not insert V44 after normal pickup solely because its timing tests pass. Preserve the coherent current terminal while repairing whole staged carrying family against masters.'],scope='Native-size fixed-pivot West source comparison, not continuous cadence or original-master acceptance.')
(out/'review.json').write_text(json.dumps(review,indent=2)+'\n')
section='''### James actual pickup-to-carry source join checked — October 2, 2026

V48 fixed-pivot native-size board visually reviewed:14West sources, seven per gear,
normal pickup4/5, staged V44prep0/1/2, staged V16walk0 and normal walk0. Both gears'
normal pickup5 and normal walk0 are byte/pixel-exact. Existing normal endpoint is
coherent. V44prep0 would reopen the stance after pickup5 and change case/body
presentation; staged V16walk0 also differs in fabric detail and case scale. Do not
insert this preparation after actual normal pickup merely because timing passed.

Lesson: compare candidate entry to the actual predecessor state, not a convenient
standing reference. Retain exact normal pickup-to-walk endpoint while reconciling
the staged whole carrying family against original masters. Exact endpoint equality
does not establish interior cadence, every direction, interruptions or full motion.
Next review current carry interiors and the authoritative master together, repair
staged material/proportions/contact, then integrate appropriate transitions.
Normal sources/controller unchanged by V48; full goal remains incomplete.
Evidence:character/james-west-carry-walk-keys-v1/pickup-carry-contact-v48/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James normal dry workshop pickup installed'.encode());new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
(out/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched set; incomplete.\n\n'+section+'\nChanged: comparison/review, local closeout helpers and five guides. All14source hashes stable; both gear endpoints exact. No runtime/art mutation by V48.\n',encoding='utf-8')
parent=p/'HANDOFF.md'
if section.encode().split(b'\n',1)[0] not in parent.read_bytes():
    with parent.open('ab') as f:f.write(b'\n'+section.encode())
print(json.dumps(dict(reviewedSources=14,exactNormalEndpoints=2,guidesUpdated=5,normalChanged=False)))
