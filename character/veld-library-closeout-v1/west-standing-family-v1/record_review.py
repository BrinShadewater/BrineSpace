from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[2]
report=json.loads((R/'output/veld-west-standing-family-v1/validation.json').read_bytes())
assert report['passed'] and not report['realProfileChanges']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads((R/'character/veld-library-closeout-v1/installed/selected-library.json').read_bytes());refs=set();manifests=set()
for gear in ['bare','helmet']:
 for key in ['idle-west','walk-west','interact-west','repair-west']:
  entry=inv['resolved'][gear][key];manifests.add(entry['manifest'])
  refs.update(entry['frameFiles'])
for name in manifests:assert sha(R/name)==inv['bindings'][name],name
for name in refs:assert sha(R/name)==inv['sourceBindings'][name],name
(P/'SELECTION_REVIEW.json').write_text(json.dumps({'unchangedWestSources':len(refs),'unchangedWestManifests':len(manifests),'failures':0,'normalSelectionChanged':False},indent=2)+'\n')
title='## Veld original West standing family staged — October 3, 2026'
note=title+f'''

Original-master West idle/walk/scanner reviewed together, staged at
character/veld-library-closeout-v1/west-standing-family-v1/. One direct MiniMax
Hailuo02 job448662724624752 succeeded (6s/768square/24fps; estimated USD0.28,
billing unverified). Exact input, prompt, task record and full142-frame source
retained. Requested final standing stop was not achieved: source keeps walking.
No retry; no stop/start transition acceptance claimed.

Fixed whole-canvas3:1 downsample and alpha separation only; no colour/anatomy,
nonuniform scaling, per-pose recenter/refloor or erosion repairs. All142 raw slots
inspected in chronology. Source height144..149 versus master148; head27..29
versus master27. Brown bun/small face/charcoal quilted suit are substantially closer
than rejected sheets, with minor cloth/detail variation still needing motion review.
Paired family reuses complete142-slot original idle and scanner plus raw26..49,
a consecutive24-slot/1000ms full alternating walk cycle. Entire source preserved.
Existing original West helmet shell registered once; body outside its region
pixel exact. Common256canvas/pivot128224/standingHeight148. Walk timing uses
original rounded source holds, including phase26 offset.

592 build checks,1232 APNG grouped pixel/hold checks and3738 native checks passed;
616 native presentations at47/93/148px. All48 new walk poses and bare/helmet joins
visually reviewed. Player state-entry/loop/return and fresh-player snapshot restore
pass. First interval preserved: two incorrect idle-to-idle reset expectations
fixed in fixture; existing idle playback correctly continues. Later passing
interval before quoted resource-path cleanup also preserved. Final native
interval: output/veld-west-standing-family-v1/.752 targeted inputs and2931 real
owner profile files unchanged. Selected West{len(refs)} source files and{len(manifests)} manifests
still match installed inventory. No normal selection or controller changes.

This is staged appearance/motion review, not gameplay/contact/disk Continue
acceptance. Remaining West kneel/repair/cargo joins use older stance; installing
only these3 states would reintroduce the11px family jump. West scanner source does
not change curiosity's East/1.02s dispatch. Next: bring adjoining West actions into
same original stance, then verify physical stride/contact and actual controller
timing before coherent admission. Full Veld completion remains open.
Handoff: character/veld-library-closeout-v1/west-standing-family-v1/HANDOFF.md.

'''
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 3, 2026 · Project: Brine Space · Task: Veld West standing family

## Objective and acceptance
Finish existing selected Veld library against original masters, with consistent materials, proportions, registration and native transitions. This interval stages West idle/walk/scanner together.

## Accepted decisions and constraints
Original West authority preserves small face, dark brown bun with intentional silver temple streak, warm skin and charcoal quilted suit. Whole poses; fixed canvas/ruler; no local anatomy/colour or per-pose registration rescue. Keep approved planted turns. Existing reversible generation authorization applies.

## Current state
Paired bare/helmet manifests and previews here: idle142, walk24, scanner142 per gear. One MiniMax job448662724624752, estimated USD0.28 (billing unverified); complete142-slot source, prompt and input retained under walk-source-v1. Source did not achieve requested final stop. Walk uses raw26..49 in sequence with exact1000ms holds. Existing original shell uses fixed placement; body outside shell exact. No normal selection/controller changes. Minor cloth/detail variation remains for motion review.

## Verification
592 build checks,1232 APNG pixel/hold checks,3738 final native checks/0failures with616 presentations at47/93/148px. All142 raw source frames and24 walk poses per gear plus joining poses visually reviewed. State-entry/loop/return/fresh-player restore verified; not physical foot contact or normal controller/disk Continue. Real profile2931 files and752 targeted inputs unchanged. Selected West{len(refs)} sources/{len(manifests)} manifests match installed inventory. First two mistaken idle-to-idle reset assertions and pre-path-map passing interval preserved separately. Final evidence output/veld-west-standing-family-v1. Test, paired UID and scratch-profile runner saved in tests/ and tools/.

## Next action
Bring West kneel/repair and adjoining cargo/action poses onto original stance before admitting a partial11px shift. Verify native physical stride/contact and actual controller duration/dispatch. Complete remaining directional material/furniture/water/death checks and full fresh-process Continue. Whole library is not finished.
''',encoding='utf-8')
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(20):
  with path.open('r',encoding='utf-8') as f:head=''.join(next(f,'') for _ in range(120))
  if title in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-'+uuid.uuid4().hex+'.tmp')
  with tmp.open('wb') as dest,path.open('rb') as source:dest.write(note.encode('utf-8'));shutil.copyfileobj(source,dest,1024*1024)
  after=path.stat()
  if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):tmp.unlink();time.sleep(.5);continue
  try:tmp.replace(path)
  except PermissionError:tmp.unlink();time.sleep(.5);continue
  print(path.name,'updated');break
 else:raise RuntimeError('Concurrent update prevented prepend: '+str(path))
parent=P.parent/'HANDOFF.md';text=parent.read_text(encoding='utf-8')
section='\n## Original West standing family staged\nIdle142/walk24/scanner142 per gear share original stance.3738 native checks passed/616 presentations; full142 source retained, final stop not achieved. No normal selection/controller changes. See west-standing-family-v1/HANDOFF.md. Adjoining West actions and physical contact/controller/disk Continue checks precede admission.\n'
if '## Original West standing family staged' not in text:parent.write_text(text+section,encoding='utf-8')
print('Selected West sources unchanged:',len(refs),'manifests:',len(manifests))
