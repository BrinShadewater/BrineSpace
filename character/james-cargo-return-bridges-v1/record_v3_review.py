from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
package=json.loads((p/'package-v3-evidence.json').read_bytes());native=json.loads((p/'native-v3-evidence.json').read_bytes())
assert package['outsideWindowExactChecks']==358440 and native['checks']==18 and native['failures']==0
for name in ['package-west-bridge-v3','validate-west-bridge-v3']:
 guard=json.loads((p/(name+'-validation.json')).read_bytes());assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
refs=json.loads((p/'reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in refs['sources'])
def atomic(path,new):
 old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review={'selected':False,'fullGoalComplete':False,'visualBridgeAcceptance':False,
 'reviewed':['west-bridge-generated-v3.png','west-bridge-endpoint-review-v3.png','west-bridge-station-review-v3.png'],
 'improvements':['Original head/shared-shell and lower-leg pixels outside recorded torso/hip rectangle retained exactly in all6sources.','Both gears use exactly identical generated torso/hip rectangle; eliminated independent undersized generated helmet.','Case and arm adjustment now progresses rather than repeating a fixed destination stance.'],
 'remaining':['Third pose tilts/lifts the case beyond the level unload entrance, so final join is not accepted.','Rectangular shoulder/collar and hip boundaries still require motion review; outside-window equality does not prove anatomical continuity.','Final floor-case/standing handoff and actual finite return controller/safety/Continue remain open.'],
 'nativePlayerChecks':18,'outsideWindowExactChecks':358440,'method':'Built-in imagegen v3 source; native deterministic shared350bare-ruler/217pixel cell resize, recorded80,110,84,69torso/hip rectangle on original sources. No per-frame grade, reflection or head rescale.'}
(p/'study-review-v3-evidence.json').write_text(json.dumps(review,indent=2)+'\n')
section='''## James original-registered West grip bridge v3 — October 2, 2026

Third built-in source sheet/prompt retained. New unselected paired v3 study uses
only its bare coherent torso/hip drawings inside recorded rectangle80,110,84,69;
original selected turn endpoint supplies every other pixel. Six frames, native
358440outside-window full-RGBA comparisons pass. Original head/shell/lower-leg
regions outside rectangle retained; not a semantic head/body mask claim. Paired
torso rectangles exact, removing independently undersized generated helmet.
Shared raw bare ruler350 to nominal148, rounded217cell extraction/recorded anchors;
no per-frame grading, scale fitting or body reflection.

Staged native CrewSpritePlayer18checks0fail: all6source-clock bindings, p128224/H148
and paired rectangular torso identity. Package and player engine0/no timeout,
whole owner profile unchanged under separate scratch profiles. Exact six original
reference hashes unchanged. No prelaunch broad input freeze or world acceptance.
All6registered full/reduced source comparisons reviewed. Original helmet scale
and feet retained, grip change now progressive. Final pose tilts/lifts case beyond
level unload entrance; final join remains FAILED. Shoulder/collar/hip boundaries
require motion review despite exact protected pixels. Both v3 manifests unselected.

Lesson: reuse original gear pixels and one generated paired body region where
coherent source geometry allows it; reject rectangle seams that disrupt anatomy.
Pixel protection cannot certify a good motion join. Specify case orientation and
height against the real final source; gradual movement can still overshoot.
Next level final-grip correction, shoulder/hip and paired native motion review,
floor-case/standing and controller safety/ordinary Continue. Full James master,
all cardinal contexts and cross-family polish objective active/incomplete.
Evidence: character/james-cargo-return-bridges-v1/study-review-v3-evidence.json and
west-bridge-endpoint-review-v3.png. Built-in prompt: west-bridge-prompt-v3.txt.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes()
 if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West grip bridge v3

## Objective and acceptance
Full James master/style/perspective/size/height/proportion/matte set, then
cross-family polish. Full objective active/incomplete; bridge not accepted.

## Accepted decisions and constraints
Original masters/shared shell govern. Retain head/feet outside recorded torso/hip
rectangle; one paired body region. Exact pixel guards do not prove body continuity.

## Current state
Third built-in sheet/prompt, native package-v3 sixframes under frames-v3,
paired *-manifest-v3.json remain unselected. Original head/shell/feet outside
80,110,84,69 retained; progressive hand/case poses. Final pose overshoots level
unload entrance. Full/reduced boards reviewed; five guides updated.
Earlier rawv1/v2 and v2package retained. Actual power interruption still snaps.

## Verification
358440protected RGBA comparisons,18staged player checks0fail; both engine0,
scratch whole owner profile unchanged. Six native selected-clock pixels/pivots/
rulers and paired torso rectangles exact. Six original reference hashes unchanged.
No semantic body mask, complete anatomical/motion acceptance, world/controller
repair, cargo-floor handoff, safety or return Continue. No broad input freeze.

## Next action
Correct final case angle/height to level unload source, review shoulder/hip
joins and paired native motion. Then floor-case/standing handoff, actual finite
controller return, needs/emergency priority and ordinary Continue. Other cardinal
contexts/West tablet edges and full master/cross-family polish remain open.
No commit/export.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('V3 progressive paired torso study recorded; final level-case and motion joins remain open; five guides updated.')
