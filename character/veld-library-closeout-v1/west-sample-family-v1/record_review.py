from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[2]
v=json.loads((R/'output/veld-west-sample-family-v1/validation.json').read_bytes());assert v['passed'] and not v['realProfileChanges']
checks=json.loads((P/'PREVIEW_REVIEW.json').read_bytes());assert checks['failures']==0
selected=json.loads((P/'SELECTED_INPUTS.json').read_bytes())
for name,digest in selected['bindings'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
(P/'VERDICT.json').write_text(json.dumps({'status':'Staged appearance improvement; not ready for normal admission','wholeRawFramesReviewed':142,'nativeHelmetChronologyReviewed':142,'nativeChecks':2808,'nativePresentations':458,'apngPixelHoldChecks':900,'ownerProfileUnchanged':True,'selectedSourceFilesUnchanged':len(selected['bindings']),'positive':['Original small head, brown bun, warm skin and charcoal quilted suit remain much closer to master','Returns to original standing stance','Same rigid helmet shell tracks moving head; body outside fitting exact','All lower/rise poses retained with explicit uniform timing adjustment'],'remaining':['Foot shifts/contact during lowering and rising','Vial grows during stowing around raw105..112','Ordinary controller and complete adjoining cargo joins remain unverified'],'scope':'Source and native player review only; no normal selection or controller changes'},indent=2)+'\n')
title='## Veld original West sample family staged — October 3, 2026'
note=title+'''

Original-master standing-to-kneel/sample/rise source preserved at
character/veld-library-closeout-v1/west-sample-family-v1/. One direct Hailuo02
job448673608622559 succeeded,6s/768square/24fps, estimated USD0.28 (billing
unverified). Exact input/prompt/task, all142 raw frames and uneroded fixed3:1
alpha extraction retained. All142 raw poses and142 native helmet chronology
poses inspected. Native standing height returns148px; head width27..29 versus
master27. Face/brown bun/warm skin/charcoal suit substantially closer to master.

Complete142-slot source per gear plus kneel29..53, repair54..90, stand91..115.
Lower/rise each25 slots uniformly40ms/1000ms instead of1042ms; every pose retained,
explicit approximately4percent acceleration to match existing1s timers. Whole
source original5917ms holds unchanged. Repair is finite and holds terminal pose
through4s; no false repeating vial draw. Same original33x39 West helmet shell
tracks head geometry without resizing body; outside fitting142/142 pixel exact.

Final2808 native checks/0failures,458 presentations at47/93/148px; nonloop endpoint
hold, repair4s hold, state return and fresh-player snapshot continuation pass.
900 APNG grouped pixel/hold checks pass. Real profile2931 files and921 targeted
inputs unchanged. Selected18 old source files unchanged. Earlier source-holds
native interval preserved at output/veld-west-sample-family-v1-source-holds/;
final bound interval output/veld-west-sample-family-v1/.

Still staged: lowering/rising foot shifts and ground contact need review; vial
visibly grows during stowing around105..112. No patching, per-pose refloor/recenter,
colour rescue, pose omission or normal admission. Source material/endpoint success
does not certify planted contact or stable props. Next refine these demonstrated
motion defects before controller/cargo-family admission; remaining directions,
furniture/water/death and full new-process Continue remain open. Full Veld set
incomplete. Handoff: this candidate's HANDOFF.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 3, 2026 · Project: Brine Space · Task: West sample family

## Objective and acceptance
Match West lowering, sample inspection and rising to original master and staged idle/walk/scanner. Whole Veld set remains incomplete.

## Accepted decisions and constraints
Whole poses, common256canvas/pivot128224/standingHeight148. Keep warm skin/brown bun with silver temple streak/charcoal quilted suit/blue patch. No anatomy/colour/per-pose rescale/recenter/refloor rescue. Repair means sample inspection. Existing generation authorization applies.

## Current state
One Hailuo02 task448673608622559, estimated USD0.28, billing unverified. All142 raw/source slots preserved; complete bare/helmet source plus87 phase slots per gear. Phases29..53/54..90/91..115. Lower/rise25slots each retimed uniformly40ms to1s; raw fullsource timing unchanged. Repair finite, pins last pose through4s. Original rigid33x39 West shell follows head; body outside fitting exact. Appearance and final standing joins improve substantially. No normal/controller changes.

## Verification
All142 raw frames, old18 source poses, paired joining poses and142 native helmet chronology frames inspected. Final2808 native checks/0failures and458 presentations;900 APNG pixel/hold checks. State entry/nonloop terminal/repair4s hold/return/fresh-player restore verified.2931 real profile files and921 targeted inputs unchanged. Original timing native interval preserved separately; final output/veld-west-sample-family-v1. Paired fixture UID and scratch-profile runner saved.

## Next action
Resolve visible foot shifts/contact and vial enlargement during stowing105..112 using coherent source revision; do not hide these poses or patch body/prop locally. Then prove ordinary controller and adjoining cargo/action joins before family admission. Other directional material, furniture, water/death and fresh-process Continue remain open. Not ready for normal installation.
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

parent=P.parent/'HANDOFF.md';text=parent.read_text(encoding='utf-8');section='\n## Original West sample family staged\nWhole lowering/examination/rising source142 plus87 phase slots per gear.2808 native checks passed. Appearance/standing joins improve; foot contact and vial enlargement during stowing remain. No normal changes. See west-sample-family-v1/HANDOFF.md.\n'
if '## Original West sample family staged' not in text:parent.write_text(text+section,encoding='utf-8')
print('Recorded sample source review; selected18 sources unchanged.')
