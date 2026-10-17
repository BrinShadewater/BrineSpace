from pathlib import Path
import json,os,uuid,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
n=json.loads((P/'validate-evidence.json').read_text());w=json.loads((P/'validate-validation.json').read_text());v=json.loads((P/'packaging-validation.json').read_text())
assert n['failures']==0 and len(n['records'])==18 and not v['failures'] and w['exitCode']==0 and not w['timedOut']
status='installed_native_source_verified_owner_review_pending'
f=P/'helmet-manifest.json';m=json.loads(f.read_text());m['status']=status;f.write_text(json.dumps(m,indent=2)+'\n')
selection={'status':status,'runtimeInstalled':True,'fullSetComplete':False,'references':18,'statesPerMode':3,'source':'source-v2.png','sourceSha256':hashlib.sha256((P/'source-v2.png').read_bytes()).hexdigest(),'prompt':'tool-prompt.txt','fixedWholeSourceScale':.5476190476190477,'packageChecks':v['checks'],'nativeChecks':n['checks'],'nativeCaptures':18,'profileGuard':{'realProfileUnchanged':w['realProfileUnchanged'],'profileDelta':w['profileDelta']},'visualReview':'All18 revised whole-source poses, enlarged head comparison and all18 normal NPC native captures reviewed. East/South stronger down-gaze; West subtler. Complete lower helmet edge fit restored; original cut-minus4 review retained. Body outside recorded upper-head/neck ROI exact, neutral0/5 exact.','nativeScope':n['scope'],'remaining':['Continuous/full-motion owner review','Actual furniture contact/depth and task/gear/interruption/Continue contexts across full James library']}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
note='''

## James seated reading helmet gaze — October 1, 2026

Refreshed329bare/4232references and239helmet/3716references, zero retained; coverage
is provenance, not full-set acceptance. Fixed148px seated review covers192sources
and48exact standing/down/held/rise/read joins in both gears/four directions. All
eight original whole-source boards reviewed. Older diagnostic helmet donors kept
reading gaze too level beside bare down-pitch; exact joins did not prove gaze.

Selected james-seated-read-head-pitch-v2 overrides only18helmet read-seated
East/West/South refs. New built-in imagegen sheet/prompt/inputs hashed; copy remains
in project. Generated body and changed endpoints rejected for adoption; only
authored upper head/neck donors adopted within recordedROI. Source0/5 exact old
neutral; all original tablet/hands/belt tools/boots/body outsideROI exact. North,
bare and sit/down/rise untouched. Single.5476190476 whole-neutral East ruler
shared across generated heads, whole-pose foot registration; no isolated resizing
or flat helmet rotations. One frozen pooled grey-shell gain per facing shared
across interiors, face excluded. East/South clearer down gaze, West more subtle.

85package/112normal NPC-renderer checks0fail; all18prescribed reading slots captured
and reviewed. Engine0/no timeout; scratch APPDATA, strict owner unchangedtrue/delta[].
Initial head cut-minus4 removed lower helmet edge; expanded crop exposed it despite
technical pass. Prior artifacts/native interval archived before full cutoff repair;
new native interval passes and all18new captures reviewed. No actual furniture,
navigation, Continue, locker or continuous gameplay claim. Refreshed seated source
inventory still192refs/48exact joins; compare18replacement refs with174unchanged
selected references. Full James goal active, owner review pending.

Lesson: inherited pitched-donor provenance is not proof of tablet-directed gaze.
Review the equipped face separately from bare motion. A body-protection crop must
retain the complete pitched shell/chin/collar fit; a pixel guard alone can approve
a visibly cut helmet. Preserve previous evidence before correcting fit. Handoff:
character/james-seated-read-head-pitch-v2/HANDOFF.md.
'''
for f in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 data=f.read_bytes()
 if b'## James seated reading helmet gaze' in data:continue
 enc=note.encode();new=enc.lstrip(b'\n')+b'\n'+data if f.name=='CURRENT_STATUS.md' else data+enc
 temp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);os.replace(temp,f)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James seated reading gaze

## Objective and acceptance
Full James master/style/perspective/proportion/material/motion consistency and
cross-family polish. Active; this revision installed/source/native verified,
owner review pending.

## Accepted decisions and constraints
Matte shared helmet, downward tablet gaze, belt wrench, stable seated supports.
Exact original metadata/clocks and neutral endpoints; protect body outsideROI.

## Current state
Generated source-v2/tool-prompt/inputs frozen.18helmet East/West/South reading
refs override normal grid loader/ACTIVE_ASSETS; North/bare/sit/down/rise unchanged.
New authored upper head/neck donors, single whole-source.5476190476 ruler and
pooled facing grey-shell grade. Generated bodies/endpoints not adopted. Source
boards/native all18 reviewed. Initial clipped-edge evidence archived before fit
repair. validate.gd/.uid paired. Five guides updated; seated192source review and
inventory329bare/239helmet refreshed, still48exact cross-family seated joins.

## Verification
85package/112native checks0fail; prescribed source slots via normal NPC renderer,
not actual chair journey. Engine0/no timeout, scratch APPDATA/owner unchangedtrue.
Actual furniture depth/contact, Continue/gear changes and continuous gameplay
remain separately unproven. East/South down-gaze clearer, West subtler.

## Next action
Deterministic rebuild and selected192hash mapping; continue actual seated
furniture/depth/controller handoffs and full remaining-family motion review.
No provider/native job live. Full-set/owner/export acceptance remains open.
''')
print(json.dumps({'status':status,'nativeChecks':n['checks'],'profileDelta':w['profileDelta']}))
