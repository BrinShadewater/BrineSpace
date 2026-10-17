from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
refs=json.loads((p/'rise-reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/c['source']).read_bytes()).hexdigest()==c['sha256'] for c in refs['sources'])
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(temp,path)
for name,verdict in [('rise-v1-review-evidence.json','Rejected: first pose barely rises; second almost standing; undersized shared helmet.'),('rise-v2-review-evidence.json','Rejected: spacing still uneven; second bare crown at standing height; second helmet too small.'),('rise-v4-review-evidence.json','All three common-canvas bare poses visually inspected. Preferred authored midpoint: crown99->88->76; ground225->224->224. Native world/timing/case seam acceptance pending.'),('rise-v4-helmet-review-evidence.json','All three common-canvas helmet poses visually inspected. Preferred paired draft: crown95->85->68; ground225->224->224. Final step larger; helmet fit materially closer. Native world/motion acceptance pending.')]:
    data=json.loads((p/name).read_bytes());data.update(visualReviewPending=False,reviewed=verdict,selected=False,nativeWorldMotionAccepted=False)
    atomic(p/name,(json.dumps(data,indent=2)+'\n').encode())
for name in ['package_rise_v4-validation.json','package_rise_v4_helmet-validation.json']:
    g=json.loads((p/name).read_bytes());assert g['exitCode']==0 and g['realProfileUnchanged'] and not g['timedOut']
art=['rise-generated-v4-bare.png','rise-generated-v4-helmet.png','rise-v4/bare/000.png','rise-v4/helmet/000.png']
e={'selected':False,'fullGoalComplete':False,'method':'Built-in image_gen direct original crouch edit, then equipment-only paired edit. Native Godot uniform251/1254full-canvas resize and transparent padding, no translation/grade/height normalization.','preferredDraft':'v4 paired midpoint','originalEndpointHashesUnchanged':True,'artHashes':{f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in art},'reviewedPresentations':{'v1':8,'v2':8,'v4':6},'rejected':['v1 uneven rise/undersized helmet','v2 uneven rise/second near standing','v3 bare raw near-standing proportions; not packaged'],'v4NativePackages':2,'ownerProfileUnchanged':True,'nativeMotionAccepted':False,'remaining':['Bind paired rise between exact original unload4/5 in staged and normal action paths; preserve exact cue4.','Update embedded-case suppression for rise frames; replay actual native source/world chronology.','Resolve case hardware/boot overlap and checkpoint floor-art revision binding.','V9 collar/head turn; normal disk/title/new-process Continue; other directions/full master and cross-family review.']}
(p/'rise-acceptance.json').write_text(json.dumps(e,indent=2)+'\n')
section='''## James West rise midpoint authored and registered — October 2, 2026

V1/V2 paired drafts packaged and all16 common-canvas presentations reviewed;
rejected uneven pose spacing and undersized second helmet. V3 bare raw remains
near-standing relative to case ruler; not packaged. Sources/prompts preserved.
V4 direct original crouch edit preserves sparse composition; paired equipment
edit supplies shared helmet. Two native Godot packages pass/owner unchanged.
Full1254canvas uniformly resized251 then padded to256/p128224/H148, no per-pose
height normalization, floor translation, grade or alpha retouch. Six original/
draft/original presentations reviewed; all four original endpoint hashes match.

V4 bare crown99->88->76 and ground225->224->224; helmet95->85->68 with same
ground. Bare spacing materially improved; helmet final rise remains larger.
Preferred authored paired midpoint, NOT normal-selected or native motion accepted.
Boot/case overlaps and full timing still require actual source/world replay.
Original standing endpoint hides boot differently; no claim this fixes that seam.

Lesson: multi-pose sheets can change pose scale/helmet fit despite shared packaging.
Direct sparse original-canvas edit gave useful midpoint without per-pose stretching.
Choose scale from original case/feet rulers, not output canvas dimensions alone.
First V4 package assumed1280 but actual1254 and failed cleanly; preserved first
script/log/guard, corrected dimension and full-canvas packaging. First helmet
preparation shell quoting failed/missing script; replaced with saved Python helper,
then successful native package. No owner profile or original source changes.

Next bind exact endpoints/paired midpoint with preserved release4 ownership,
embedded-case suppression and native chronological replay, then case hardware/
boot seam and floor-art checkpoint binding, V9 collar/head turn, normal Continue,
other directions/full master and cross-family polish. Full goal incomplete.
Evidence:character/james-floor-case-west-v1/rise-acceptance.json and paired
bare-rise-v4-review.png/helmet-rise-v4-review.png. No commit/export.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West rise/prop seam

## Objective and acceptance
Full James set matching directional masters/style/camera/height/proportions/matte
grade, then cross-family polish. Incomplete; candidate unselected.

## Accepted decisions and constraints
Original endpoints/cue4/owner profile/normal loader/geometry preserved. Built-in
authored midpoint; uniform full-canvas packaging, p128224/H148; no pose stretching.

## Current state
V1/V2 spacing/helmet drafts rejected; V3 bare raw not packaged. V4 preferred paired
midpoint/raw/exact prompts/native frames/three-pose review boards retained. Two
native packages pass, six presentations reviewed, four endpoint hashes unchanged.
Bare crown99/88/76, helmet95/85/68; ground225/224/224. Five guides updated.
V6 case staged; earlier lifecycle/checkpoint evidence still scoped to prior sources.

## Verification
V4 two native packages engine0/owner unchanged. Shared251/1254scale/no translation;
source registration review only, no new native world/motion/normal Continue test.
First failed dimension package retained; quoting failure corrected with saved helper.

## Next action
Bind rise clip to exact unload4/5 and preserve cue4 in both action paths; embedded
case suppression must cover midpoint. Replay native chronology before acceptance.
Resolve case hardware/boot seam and floor-art checkpoint binding; V9 collar/head
turn; normal disk/title/new-process Continue; all directions/master/cross-family.
No commit/export. Goal active/incomplete.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Preferred paired V4 draft recorded; five guides and handoff updated; goal incomplete.')
