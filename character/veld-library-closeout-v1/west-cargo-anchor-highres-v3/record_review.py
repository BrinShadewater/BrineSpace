from pathlib import Path
import json,hashlib,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[2];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();validation=json.loads((R/'output/veld-west-cargo-anchor-highres-v3/validation.json').read_text());assert validation['passed'] and not validation['realProfileChanges']
text="""# Project handoff

Updated: October 4, 2026 · Brine Space · Original-master West standing cargo key

## Objective and acceptance
Resolve Veld cargo family stance/material drift against original masters before wider animation admission. This revision is a staged paired authoring still, not finished cargo motion or owner acceptance.

## Accepted decisions and constraints
Original high-resolution West directional master is sole identity/material target. Small target editv2 failed again; high-resolution target replaces that method, not an uncontrolled video retry. Preserve full original/generated sources, fixed whole-key density/registration and original rigid helmet. No anatomical stencils, per-frame scaling or exposure changes.

## Current state
One built-in imagegen high-resolution master arm/case edit: source.png, exactprompt/INPUTS and unaltered right-half reference crop. Two built-in jobs this interval: low-resolution targetedv2 rejected (head30px vs27), high-resolutionv3 now staged. No MiniMax job. Paired bare/helmet stills and single finite carry-west1000ms review manifests, common256/pivot128224/H148. build_key.py uses one uniform neutral-height calibration (147px source span before Lanczos edge coverage exports148px), fixed integer whole-key floor/near-heel placement and standard alpha/component cleanup. No RGB grading or per-part replacement. Corrected output head27/top76/floor223 matches original; headaxis130vs133 (3pxforward), front bootextent109..147vs107..147 (2pxtoe-outline difference). Keep these limits visible; no exact original-body or footgeometry claim. Body outside original-shell area exact.

## Verification
5build checks,7byte-exact rebuildoutputs,28nativeplayer checks0failures and2three-scale presentations (47/93/148px), both viewed. Native includes exact pixels/pivot/density/dry state, entry/terminal/idle return and fresh-player snapshot continuation; no walking/root/controller/contact or diskContinue proof.636targetinputs/2931owner nonlogfiles unchanged. All ending-West inventory722uniquePNGs/38manifests unchanged; earlier358/15 audit covered narrower standing/action/cargo keys. Fixture script/UID and runner saved. Evidence output/veld-west-cargo-anchor-highres-v3.

## Next action
Review the small forward-head/bootoutline variance as part of full joins. Author coherent unload with samecase/stance, derive pickup by exact reversal, then repair/review carry and planted turns without resetting their timing. Obtain exact deposited-case endpoint before first/last generation; do not animate against a mismatched old case. Full library, controller interruptions and fresh-processContinue remain open. No live job or approval gate; no normal loader changes.
"""
(P/'HANDOFF.md').write_text(text,encoding='utf8');(P/'VERDICT.md').write_text('# Staged authoring-key verdict\n\nHigh-resolution source is substantially closer to original identity/materials and preserves original-sized27px head and148px standing density. Bare/helmet native still presentations reviewed; staged for coherent cargo motion authoring, not admitted as a gait. Remaining3px forward headposition and2px frontboot outline difference must stay in join review. Previous low-resolution keys are rejected.\n',encoding='utf8')
title='## Veld original-master West cargo key staged — October 4, 2026';note=title+'\n\nHigh-resolution master arm/case edit staged at character/veld-library-closeout-v1/west-cargo-anchor-highres-v3/. Small-reference targetededitv2 rejected (30pxhead vs27); high-resolution editv3 matches27pxhead/148pxstanding/top76/floor223, mutedblue patch/charcoal quilt and detailed hardware. One uniform whole-key calibration/near-heel registration; no RGB or anatomical-region repair. Head3pxforward and fronttoeoutline2pxdifferent remain visible limits. Original rigidWest shell reused; outside-shellbody exact.5build/7byte-exact rebuild/28native checks0; both native47/93/148px presentations viewed.636inputs/2931ownerfiles unchanged; selected ending-West722PNGs/38manifests unchanged. Staged paired still manifests only; no new cargo motion, MiniMax job, normal admission or controller/diskContinue acceptance. Next: exact same-case deposited endpoint, coherentunload/reversedpickup, carry/turnjoins and wider lifecycle gates. Full Veld library unfinished.\n\n'
p=R/'docs/CURRENT_STATUS.md'
for attempt in range(20):
 before=p.stat();tmp=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp')
 with p.open('r',encoding='utf8') as f:
  if title in ''.join(f.readline() for _ in range(120)):break
 with tmp.open('wb') as out,p.open('rb') as src:
  out.write(note.encode())
  while chunk:=src.read(1024*1024):out.write(chunk)
 after=p.stat()
 if (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns):
  try:tmp.replace(p);break
  except PermissionError:pass
 tmp.unlink();time.sleep(.5)
else:raise RuntimeError('Concurrent CURRENT_STATUS edits/lock prevented update')
parent=P.parent/'HANDOFF.md';section='\n\n## Original-master West standing cargo key staged — October 4, 2026\n\nHigh-resolution master edit in west-cargo-anchor-highres-v3 is substantially closer:27pxhead/148pxheight/top76/floor223, mutedpatch/charcoal/hardware.3pxforwardhead/2pxfronttoeoutline variance explicitly retained. Low-reference targetedv2 rejected. Source/exactprompts/inputs retained; no MiniMax job or normal admission. Originalrigidshell/bodyoutsideexact,5build/7rebuild/28nativeplayerchecks0,2three-scale presentations viewed;636inputs/2931ownerfiles unchanged. Ending-West722PNGs/38manifests unchanged. Next exactdepositedsamecase endpoint before unload/reversedpickup; then carry/turn/controllerinterruption/Continue. Staged still only; full library unfinished.\n'
if '## Original-master West standing cargo key staged' not in parent.read_text(encoding='utf8'):
 with parent.open('a',encoding='utf8') as f:f.write(section)
files=[f for f in P.iterdir() if f.is_file() and f.name!='FINAL_REVIEW.json']+[R/'tests/test_veld_west_cargo_key_v3.gd',R/'tests/test_veld_west_cargo_key_v3.gd.uid',R/'tools/run_veld_west_cargo_key_v3.py',R/'output/veld-west-cargo-anchor-highres-v3/validation.json']
(P/'FINAL_REVIEW.json').write_text(json.dumps({'scope':'Paired still key and scoped native/rebuild/selection evidence; not gait or normal admission','failures':0,'bindings':{f.relative_to(R).as_posix():sha(f) for f in files}},indent=2)+'\n');print('Recorded staged key milestone and',len(files),'bound artifacts.')
