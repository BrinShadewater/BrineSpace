from pathlib import Path
from PIL import Image
import hashlib,json,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-west-whole-master-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((D/'keyposes-review.json').read_text());assert all(sha(R/p)==h for p,h in q['protectedInputs'].items())
master=Image.open(R/'character/bill-west-master-head-audit-v1/master-sole-registered.png').convert('RGBA');crop=master.crop((32,0,288,256));assert sum(master.getchannel('A').tobytes())==sum(crop.getchannel('A').tobytes())
receipts=[]
for slot,revision,call,raw,status in [(0,1,'generation-call.json','raw-000.png','preferred'),(12,1,'pose-012/generation-call-v1.json','pose-012/raw-rejected-v1.png','rejected'),(24,1,'pose-024/generation-call-v1.json','pose-024/raw-v1.png','preferred'),(36,1,'pose-036/generation-call-v1.json','pose-036/raw-rejected-v1.png','rejected'),(12,2,'pose-012/generation-call-v2.json','pose-012/raw-preferred.png','preferred'),(36,2,'pose-036/generation-call-v2.json','pose-036/raw-preferred.png','preferred')]:
 args=json.loads((D/call).read_text());receipts.append({'slot':slot,'revision':revision,'status':status,'argumentsFile':call,'argumentsSHA256':sha(D/call),'rawFile':raw,'rawSHA256':sha(D/raw),'referenceHashes':{p:sha(Path(p)) for p in args['referenced_image_paths']}})
(D/'generation-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n');ast.parse(Path(__file__).read_text())
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')];r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
q.update(pythonSyntax=6,pngLFS=len(pngs),browserProofSHA256=sha(D/'browser-keyposes.png'),generationReceiptsSHA256=sha(D/'generation-receipts.json'));(D/'keyposes-review.json').write_text(json.dumps(q,indent=2)+'\n')
note=f'''\n\n## Bill West whole master keyposes — October 4, 2026

character/bill-west-whole-master-pilot-v1: whole-source built-in edits for bare
walking landmarks000/012/024/036. Existing48phase head/material study inspected;
still provisional/unselected. Six exact generation calls/receipts/raw outputs
retained:fourpreferred,two rejected. Initial012/036 copied the wide000stance from
the supporting whole pose and failed closed-foot geometry; retained/rejected in
full. Retry uses target plus original high-resolution West master only, explicit
overlapping feet. No rejected partial art or anatomical correction admitted.

Preferred raws1254square uniformly export256 LANCZOS with wholeY only0/-1/0/+1.
Original complete-source bottoms exact; height deltas+1/+2/+1/-1,widths+4/0/+1/-2,
silhouetteIoU .942/.957/.967/.953. Reference352×320 sole-registered master crops
only transparent margin to256; complete original alpha retained, then common4x
reference export. Original high-resolution master supplements the reduced whole
reference. No local colour grade, head stamps, body stretching or per-part fit.
All six raws,four preferred packed poses,complete two-row comparison and
master/first-stride comparison visually inspected; browser gallery verified.
Angular warmer face/matte quilt detail improved; small hair/patch/harness variance
remains provisional. Exact bottoms/density are not rigid boot contact or motion
proof. Eight protected original/reference inputs unchanged,6Python syntax,
{len(pngs)}PNG LFS. No Godot/native/profile run or runtime source change.

Important bounded lesson: a completed stride used as a whole material reference
can override a closed-foot target despite explicit preserve-pose wording. Reject
the wrong whole pose; use original high-resolution identity support and explicit
target foot arrangement. This is a demonstrated retry for these two poses, not a
universal recipe or proof for all48phases. Exact tool arguments govern provenance;
prepared prompt text is a separate authoring contract.

Four landmark poses are an uninstalled study, not a complete loop or partial
walking installation. Existing selected banks,installedEast and prior48study
remain intact. Next:complete the44intermediate whole phases against these
landmarks/original master,then verify full loop/source geometry and native
distance-driven playback before admission. Do not repeatedly reopen old rejected
trials or broaden unrelated polish. Full Bill objective still open; owner wants
wrap soon. No commit/export/paid external generation requested or performed.
http://127.0.0.1:8791/character/bill-west-whole-master-pilot-v1/.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text('''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Bill West whole master poses

## Objective and acceptance
Finish master consistency with bounded West work. Four whole walking landmarks
closer in source review; not full-loop acceptance or normal installation.

## Accepted decisions and constraints
Preserve exact pose arrangement, original timing/density, selected East and
equipment, older48study and rejected trials. Whole figure edits only, uniform
export/whole translation. Reversible art work authorized; no commit/export.

## Current state
character/bill-west-whole-master-pilot-v1: four preferred whole landmark poses,
six built-in generation calls/receipts/raws,two rejected wide-stride generations,
prepared references/contracts, geometry metrics, two comparison boards and
verified browser gallery. Six Python tools. All eight maintained records updated.

## Verification
All raws/four packed candidates and complete source boards visually reviewed.
Original bottoms exact,height+1/+2/+1/-1,width+4/0/+1/-2,wholeY0/-1/0/+1,
IoU .942-.967. Closed-foot retries preserve narrow arrangement. Eight protected
inputs exact,6Python syntax/20PNG LFS. No native/profile test, no partial manifest
or runtime selection. Minor hair/patch/harness variance remains provisional.

## Next action
Complete44intermediate whole West phases against original master and the four
landmarks; preserve pose before propagating material approach. Full48loop review
and native distance-driven motion required before admission. Supporting completed
stride contaminated closed-foot poses: reject rather than fit, retry with original
master and exact overlapping boots. Do not admit old rejected046v5 or overwrite
installedEast. Full Bill objective active; avoid expanding unrelated polish.
''',encoding='utf-8')
print(json.dumps({'preferredWholePoses':4,'rejectedGenerations':2,'generationReceipts':6,'maintainedRecords':8,'pythonSyntax':6,'pngLFS':len(pngs),'normalAdmission':False}))
