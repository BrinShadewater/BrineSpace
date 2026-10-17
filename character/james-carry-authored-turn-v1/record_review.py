from pathlib import Path
from PIL import Image
import hashlib,json,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
for name,root in [('early',r),('late',r),('early-v2',p),('late-v2',p),('early-v3',p)]:
    info=json.loads((p/(name+'-inputs.json')).read_bytes());assert all(hashlib.sha256((root/k).read_bytes()).hexdigest()==h for k,h in info['preCallSha256'].items())
executions={'early':'exec-f5c8d786-cccb-4ead-817f-79aa3b646301','late':'exec-0ad0afc3-10e8-4bf5-b294-b49aea5cad2d','early-v2':'exec-c2f40688-bbac-40a7-b83d-2f1bf36e60b1','late-v2':'exec-29bfff71-5362-4489-8f45-7c22e7de6f6c','early-v3':'exec-a5331a89-5d62-49f6-b3ac-23f3220cc90e'}
for report,version,verdict,findings in [
    ('review.json','v1','rejected-angular-clustering-and-height',[
        'All five raw sources/new raws, whole/upper/legs/station chronology reviewed. Both newly authored intermediate poses copy the middle diagonal too closely, leaving angle clusters and endpoint jumps.',
        'Crowns76all but new soles226 instead224:150height versus148. No whole-body fitting or grade applied.']),
    ('v2-review.json','v2','rejected-wrong-early-yaw',[
        'All new raws and whole/upper/legs/station chronology reviewed. Single South-target early edit turns toward image RIGHT, opposite the intended South-to-West path; never mirrored as a repair.',
        'West-target late pose offers a nearer-profile source candidate but belt-meter details/patch/material vary. Bare source provisional only. Crowns75for new rows versus76master endpoints, common soles224.']),
    ('v3-review.json','v3','staged-repair-needed',[
        'All raw sources/whole/upper/legs/station chronology reviewed. Explicit nose-left/ear-right screen landmarks correct early yaw. Five whole-body poses now provide distinct front-to-left progression and retained two-hand case with planted boots.',
        'Crowns76/74/76/75/76, common soles224. Early head protrudes two native pixels above endpoint crown; late one. Head proportion/position and belt-meter design/material transitions still need source correction before motion acceptance.',
        'Candidate source pose progression only. Intended20/45/70degrees are not measured projections; five images do not prove smooth cadence, paired gear, native lifecycle or master/owner acceptance.'])]:
    path=p/report;data=json.loads(path.read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in data['sourceSha256'].items())
    frames=p/('frames' if version=='v1' else 'frames-'+version)
    for i in [0,2,4]:assert Image.open(frames/f'{i:03}.png').convert('RGBA').tobytes()==Image.open(r/data['sourceFiles'][i]).convert('RGBA').tobytes()
    data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition=verdict,findings=findings,wholeChronologyReviewed=True,upperChronologyReviewed=True,legsChronologyReviewed=True,stationChronologyReviewed=True,reusedEndpointAndMidpointRGBAExact=True,continuouslyWatchedPlayback=False,generationExecutions=executions)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    manifest=p/('candidate-manifest.json' if version=='v1' else version+'-candidate-manifest.json');m=json.loads(manifest.read_bytes());m['status']='unselected_'+verdict;m['review']=report;manifest.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
section='''### James authored carrying turn angle progression — October 2, 2026

Five new built-in raw sources retained in character/james-carry-authored-turn-v1.
Three five-pose bare versions reviewed at whole/upper/legs and82/54/27station
scales. Three-reference v1 clusters both in-betweens around midpoint and grows
soles2pixels; rejected. Single-cardinal v2 early turns wrong way; rejected without
mirroring equipment. Explicit screen nose-left/ear-right landmarks yield v3
distinct front-to-left progression, two-hand case and planted boots. Still staged:
crowns76/74/76/75/76 versus sole224; early head2pixels high, late1, belt-meter/
patch/material details vary. No source/helmet/native/normal/owner acceptance.
Five frozen generation inventories stable; reused endpoint/midpoint RGBA exact.
Three APNGs each decode5exact RGB/duration frames; configured finite800ms versus
preview endpoint600ms hold/replay. Chronology review is not watched cadence proof.

Lesson: degree labels and multiple matching references can copy one favored pose.
Review the complete ordered bodies; nearest-cardinal edits plus absolute screen
landmarks help yaw, but do not certify height/material. Correct head/crown and
single belt-tool identity before helmet/native expansion. Never mirror to repair
wrong yaw or per-pose fit/grade to conceal source drift. Added *.apng to Git LFS
attributes and verified previews/PNG sources use LFS. Five guides updated; full
master/cardinal/context/cross-family goal remains active/incomplete.
Handoff:character/james-carry-authored-turn-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James explicitly authored carrying midpoint and height repair');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James authored South–West carrying turn

## Objective and acceptance
Full master/style/perspective/size/height/proportion/matte James set, then full
cross-family consistency/polish. Active/incomplete. Previous goal turn was progress:
authored midpoint and localized lower-shin height repair, reviewed/documented.

## Accepted decisions and constraints
Common256canvas/148ruler/pivot128224; no per-pose fit/grade or mirrored tools.
Keep normal cap/V9/riseV6/caseV7 until paired source/lifecycle/Continue evidence.
Reserved motion-transfer untouched; explicitly authored source angles replace
failed whole-video spin. Exact angular degrees are intent, not measured projection.

## Current state
prepare/package v1/v2/v3, five raw sources/exact prompts/inventories, three five-pose
frame packs/finite forward and reversed candidate manifests/chronology/APNGs.
V1 angle-cluster/height rejected; v2 wrong early yaw rejected; v3 staged repair needed.
v3-station-preview.apng shows intended bare progression only. No runtime loading.
.gitattributes adds APNG LFS; five guides updated. No profile/Godot/commit/export changes.

## Verification
Five frozen generation inventories/source hashes stable. Reused cardinal endpoints
and midpoint RGBA exact in all versions. All raw/full/upper/legs/station boards
inspected;30APNG RGB/duration checks pass across three versions. V3 distinct yaw
progression, planted boots, case grip retained; crowns76/74/76/75/76, soles224.
Head-height/proportion and belt-meter/patch/material differences remain. Neither
continuous playback nor helmet/native/source lifecycle/master/owner acceptance proved.

## Next action
Correct v3 early high head and late crown against selected South/West masters
without moving successful planted body; stabilize single meter/wrench identity and
case/material across all five bodies. Review complete shortest-path source joins
and cadence before shared helmet, native cargo/room/Continue and versioned admission.
Then all cardinal/context/master checks and full cross-family consistency polish.

## Source provenance
Built-in imagegen. Early/late v1:exec-f5c8d786-cccb-4ead-817f-79aa3b646301,
exec-0ad0afc3-10e8-4bf5-b294-b49aea5cad2d. Early/late v2:
exec-c2f40688-bbac-40a7-b83d-2f1bf36e60b1,exec-29bfff71-5362-4489-8f45-7c22e7de6f6c.
Early v3:exec-a5331a89-5d62-49f6-b3ac-23f3220cc90e.
Saved project raw/prompt pairs:early-raw.png/early-prompt.txt,
late-raw.png/late-prompt.txt,early-v2-raw.png/early-v2-prompt.txt,
late-v2-raw.png/late-v2-prompt.txt,early-v3-raw.png/early-v3-prompt.txt.
''',encoding='utf-8')
print('Three source chronology verdicts closed; five frozen inventories and reused RGBA stable;30APNG checks; five guides/handoff updated.')
