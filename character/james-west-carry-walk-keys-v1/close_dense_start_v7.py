from pathlib import Path
from PIL import Image
import json,hashlib,subprocess,os,uuid
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];phases=[1,2,3,4,5,6,7,9,10,11]
def digest(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
def stable(d,k):assert all(digest(r/f)==v for f,v in d[k].items())
planfile=p/'dense-walk-v6-plan.json';plan=json.loads(planfile.read_bytes());assert digest(r/plan['sourceManifest'])==plan['sourceManifestSha256']
durations=plan['state']['frameDurationsMs'];assert sum(durations)==1680 and set(durations)=={20,30,40} and sum(durations[:13])==430
for i in plan['remainingAuthoredPhases']:stable(json.loads((p/f'walk{i:02d}-dense-carry-v6-inputs.json').read_bytes()),'preCallSha256')
for i in phases:
    n=f'walk{i:02d}-dense-carry-v6';inputs=json.loads((p/f'{n}-inputs.json').read_bytes());a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{n}.png').convert('RGBA'));mask=np.ones(a.shape[:2],bool);mask[104:169,88:166]=False;assert mask.sum()==60466 and np.array_equal(a[mask],b[mask])
    f=p/f'{n}-review.json';d=json.loads(f.read_bytes());assert d['rawSha256']==digest(p/f'{n}-raw.png')
    d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_low_squat_case_temporal_drift' if i==3 else 'provisional_original_pose_carrying_source',findings=['Raw individually/detail and chronological13pose full/upper/four station boards reviewed. Original60466outside upper pixels exact; headabove104/legsbelow169kept, hips/chest inside admission may change.','Case3lower/flatter vs2/4rejected; case/latch/grip and exposed amber/silver meter portions vary across adjacent drafts, temporal hardware identity/material continuity still pending.','Actual original donor per phase; no repeated-key fake49frame bank. No complete continuous loop/helmet/native/room/Continue/owner acceptance.']);save(f,d)
n='walk03-contact-v7';inputs=json.loads((p/f'{n}-inputs.json').read_bytes());stable(inputs,'preCallSha256');a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{n}.png').convert('RGBA'));mask=np.ones(a.shape[:2],bool);mask[116:161,88:151]=False;assert mask.sum()==62701 and np.array_equal(a[mask],b[mask])
f=p/f'{n}-review.json';d=json.loads(f.read_bytes());assert d['rawSha256']==digest(p/f'{n}-raw.png');d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_case_top_raised_temporal_repair',findings=['Raw/detail and changed chronological full/upper/station0boards reviewed. Low top raised vs rejected3; connected grips retained,62701outside exact. Exact case/latch/contact/material/hidden-tool continuity not yet accepted.','Five unchanged revised boards byte-identical to previously inspected full7/upper7/station4/8/12; prior evidence reused.']);save(f,d)
for version in (6,7):
    f=p/f'dense-start-v{version}-review.json';d=json.loads(f.read_bytes());stable(d,'sourceSha256');assert d['fullWalkDurationsMs']==durations
    d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,findings=['Chronological2full/2upper/4station boards inspected; revised3changed views inspected and5unchanged boards verified byte-identical. All13outside60466original upper exact.','Original selected full-clock1680ms with20/30/40ms frame durations; initial13pose slice430ms. Prior uniform49x40ms wording was inaccurate and is superseded.','Case-height/latch/grip/material and authentic exposed meter portions still vary; phase3v6rejected, v7provisional. 31additional interiors not yet generated; complete gait/helmet/native/context acceptance pending.']);save(f,d)
components=json.loads((p/'dense-start-v6-components.json').read_bytes());assert all(len(d['candidate'])==1 for d in components)
namespace={'__file__':str(p/'audit_case_components_v5.py')};exec((p/'audit_case_components_v5.py').read_text().split('results=[]')[0],namespace);c=namespace['components'](p/'walk03-contact-v7.png');assert len(c)==1
preview=json.loads((p/'dense-start-v7-preview.json').read_bytes());stable(preview,'sourceSha256');assert preview['previewSha256']==digest(p/'dense-start-v7-preview.apng')
plan.update(status='ten_generated_reviewed_initial_slice_provisional',generatedPhases=phases,notYetGeneratedPhases=[i for i in plan['remainingAuthoredPhases'] if i not in phases],fullGoalComplete=False);save(planfile,plan)
rasters=[f.relative_to(r).as_posix() for f in p.iterdir() if f.suffix in ('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],input=b'\0'.join(s.encode('utf-8') for s in rasters)+b'\0',cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
save(p/'dense-start-v7-checks.json',{'all41PreparedInputsStable':True,'tenOriginalOutside60466Exact':True,'derivedOutside62701Exact':True,'thirteenOriginalUpperGuards':True,'tenAndDerivedSingleAlpha128Components':True,'actualFullClockMs':1680,'sliceClockMs':430,'decodedPreviewFramesExact':13,'rastersLfs':len(rasters),'normalChanged':False,'nativeRun':False,'fullGoalComplete':False})
section='''### James West carrying chronological initial slice and actual variable timing — October 2, 2026

41distinct original walk poses prepared for remaining carrying upper authorship;
10generated1..7/9..11now join prior0/8/12to form consecutive13pose initial slice.
All10raws individually/details and2full/2upper/4station boards reviewed. Ten60466
outside original upper admission exact; actual headsabove104/legsbelow169retained,
hips/chest inside edit may change. No repeated sparse keys masquerading as49frames.
Case3v6lower/flatter than2/4REJECTED. New bounded3v7raises top/contact,62701outside
exact; raw/detail/changed full/upper/station reviewed,5unchanged boards byte-identical
and prior inspection reused. No detached alpha128components in10plus revised3.
Case/latch/grip/material and exposed amber/silver meter portions still vary; original
device attachment/occlusion needs temporal validation, not blanket invisibility.
Actual selected manifest has49VARIABLE20/30/40ms frames,total1680ms. Prior uniform
40ms wording inaccurate; selected duration array governs. Initial13poses430ms.
Review-only APNG retains13decoded source frames/timing plus600ms terminal viewer
hold;1030ms repeats are not a game loop or continuous/native cadence acceptance.
All41prepared input inventories stable, source guards/raw hashes/LFS verified.
31interiors not yet generated; no complete gait/helmet/normal/native/save/owner
acceptance. Lesson: read actual selected durations, then review adjacent poses at
native density; static key agreement cannot certify rigid-case/tool continuity.
Next reconcile initial case/tool consistency and complete remaining genuine motion
sources, full loop/helmet/joins/rooms/interruptions/Continue/versioned adoption.
Full James set/polish incomplete. Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West carrying reference case and connected-grip family');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James carrying motion

## Objective and acceptance
Full master-matched James animation set, then full cross-family polish. Incomplete.

## Accepted decisions and constraints
Actual selected49variable20/30/40ms frames,total1680ms govern cadence; older40ms
uniform wording inaccurate. Original camera/density/pivot/anatomical tools/matte
style retained; no fitting/warping or repeated-key fake motion. Standing carry
local3is provisional, not new owner-locked master. Normal bindings unchanged.

## Current state
41actual-donor targets prepared,10generated1..7/9..11. Prior keys0/8/12complete
13consecutive430ms source slice.3v6case low/squat rejected, bounded3v7improved
but provisional. Case/latch/grip/material/meter exposure still varies.31additional
interiors ungenerated. Review APNG13frames+600ms terminal viewer hold, not full gait.
Raw/prompt/frozen inventories/failed sources retained; five guides updated.

## Verification
11new raws/details and initial2full/2upper/4station boards inspected. Revised3
changed views reviewed,5unchanged boards byte-identical/reused.41prepared hashes
stable; ten60466upper/one62701local and13original60466guards pass, components
connected,13APNGdecoded frames/clocks exact, raster LFS verified. No temporal/native/
full loop/helmet/room/Continue/owner acceptance or normal/profile changes.

## Next action
Reconcile adjacent rigid-case/tool consistency, generate remaining31genuine source
phases, then full cycle/helmet/joins/rooms/interruptions/fresh Continue/versioned
normal adoption. Full remaining cardinals/families and polish stay in scope.
''',encoding='utf-8')
print(f'Ten authored interiors+one local correction reviewed;13consecutive sources,31missing,clock1680ms. {len(rasters)}LFS rasters; five guides/handoff updated. Full goal incomplete.')
