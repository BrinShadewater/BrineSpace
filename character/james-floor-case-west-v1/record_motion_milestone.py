from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'motion_v6-evidence.json').read_bytes())
guard=json.loads((p/'motion_v6-validation.json').read_bytes())
review=json.loads((p/'motion-review.json').read_bytes())
inputs=json.loads((p/'motion_v6-inputs.json').read_bytes())
assert data['checks']==648 and data['failures']==0
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert len([c for c in data['results'] if 'label' in c])==90
assert len([c for c in data['results'] if c.get('motion')])==2
assert review['losslessApngDecodedChecks']==180
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
refs=json.loads((p/'rise-reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/c['source']).read_bytes()).hexdigest()==c['sha256'] for c in refs['sources'])
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review.update(visualReviewPending=False,reviewed='All90 chronological source/prop and actual fixed-camera room presentations inspected in six boards. Native APNGs verified lossless RGB/durations; no claim of continuous browser playback watched. Source4 crouch to5 standing is abrupt in original selected unload; separate V6 case still changes hardware and boot overlap at idle. Full handoff visual acceptance FAILED/PENDING authored rising interiors and material/occlusion polish.',continuousPlaybackWatched=False,continuousHandoffAccepted=False,ordinaryContinueAcceptance=False)
atomic(p/'motion-review.json',(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'fullGoalComplete':False,'checks':648,'failures':0,'actualPrescribedReturns':2,'nativeChronologicalSourceWorldPairsReviewed':90,'losslessApngRgbDurationChecks':180,'targetedInputsUnchanged':14,'ownerProfileUnchanged':True,'visualHandoffAccepted':False,'confirmedFindings':['Original selected unload4 crouch to5 standing is too abrupt; need authored intermediate full-body rise.','Separate V6 case has a remaining hardware/boot-overlap switch despite closer matte grade.'],'authoringStarted':{'source':'rise-generated-v1.png','sha256':hashlib.sha256((p/'rise-generated-v1.png').read_bytes()).hexdigest(),'prompt':'rise-prompt-v1.txt','method':'Built-in image_gen, exact paired original4/5 endpoint board.','status':'Raw two interior poses per gear reviewed at source sheet scale only. Native shared registration, proportion/helmet/case and motion evaluation pending; not packaged or admitted.'},'remaining':['Native package/register raw rise candidate against all four original endpoints; judge spacing, body/helmet proportions and matte grade.','Author/revise then bind intermediate rising poses while preserving original whole endpoint/cue identity.','Resolve original embedded versus separate case/boot occlusion and sprite revision/checkpoint binding.','V9 collar/head turn, normal paired Save/Continue, other cardinals/full master/cross-family set.']}
(p/'motion-acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James West chronological handoff exposes original rise jump — October 2, 2026

Two actual carry power-loss returns/both gears captured45native20ms samples each,
fixed camera at unload anchor;90source/room pairs inspected in six chronological
boards.648native checks0fail, case fixed through first27.604unit departure. Four
lossless APNGs/native-only and registered source/native;180decoded RGB/duration
checks0fail.20ms samples plus600msviewer terminal hold; repeat resets preview,
not authored actor loop. Engine0/owner unchanged/14targeted hashes unchanged.

Visual handoff NOT accepted: original selected unload4 crouch to5 full standing
jumps too abruptly before separate-case switch; V6 prop still changes hardware/
boot overlap at idle. Technical pass does not certify motion. All sampled frames
inspected; APNG playback not claimed continuously watched in browser. Fixed
camera/source registration distinguishes actor rise from case contact or camera
movement. Native-only previews preserve room colours without GIF palette flash.

Started built-in raw rise-generated-v1.png/exact prompt:two interior poses per
gear, using exact paired original4/5 endpoint board/hashes. Source-scale sheet
inspection only; native packaging/registration/proportion/helmet/pose-spacing and
motion acceptance pending. No original artwork mutated, no intermediate admitted.
Lesson: a sparse terminal/idle review can miss an earlier original-pose jump;
capture the whole chronological neighborhood before assuming the prop caused it.
Next native rise comparison, revise/bind authored interiors, resolve case/boot
seam and floor-sprite/checkpoint revision, V9 collar/head turn, normal Continue,
other cardinals/full James/master/cross-family review. Goal active/incomplete.
Evidence:character/james-floor-case-west-v1/motion-acceptance.json,
motion-review.json,motion_v6-evidence.json,rise-reference-evidence.json.
No normal selection, commit/export or full motion acceptance.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West rise/prop seam

## Objective and acceptance
Full James set matching directional masters/style/perspective/size/proportions/
matte grade, then cross-family polish. Incomplete; candidate unselected.

## Accepted decisions and constraints
Preserve original endpoints/cue/normal loader/geometry/owner profile. Built-in
authored interiors; uniform native packaging/shared p128224/H148/floor222.
Technical gates and sparse source review do not certify continuous motion.

## Current state
V6 case preferred staged visual audition; earlier lifecycle/disk gates preserved.
New motion_v6.gd90native source/world samples, six boards/four lossless APNGs.
Original unload4-to5 rise jumps too abruptly; case/boot hardware still switches.
New raw rise-generated-v1.png/exact prompt and paired original endpoint reference
board/hashes; source-scale draft only, not packaged or admitted. Five guides updated.

## Verification
648native checks0fail/two returns/both gears/90chronological pairs reviewed;
180APNG RGB/duration checks0fail. Engine0/owner unchanged/14targeted hashes.
0.9second excerpt includes viewer-only600msfinal hold; no full V9 clip or browser
continuous-watch claim. Visual handoff remains unaccepted, no normal Continue gate.

## Next action
Native package/register rise draft against original4/5 both gears; judge true
pose spacing/proportions/helmet/grade before admitting. Revise and bind interiors,
resolve case/boot seam and floor-art revision in checkpoint, V9 collar/head turn,
normal paired Save/title/new-process Continue, other cardinals and full master/
cross-family set. No commit/export; full goal remains active.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Chronological90pair review recorded;rise jump/case seam unaccepted;raw authored interiors saved;five guides updated.')
