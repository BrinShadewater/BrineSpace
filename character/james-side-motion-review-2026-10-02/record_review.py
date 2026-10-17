from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
before=json.loads((P/'inputs-before.json').read_bytes())
changed=[p for p,h in before.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
a=np.array(Image.open(P/'east-carry-head-edit-target.png').convert('RGBA'))
raw=Image.open(P/'unselected-head-study.png').convert('RGBA');b=np.array(raw.resize((768,512),Image.Resampling.LANCZOS))
mask=np.zeros(a.shape[:2],bool)
for row in range(2):
    for col in range(3):mask[row*256+65:row*256+112,col*256+115:col*256+165]=True
diff=np.any(a!=b,2);alpha=a[:,:,3]!=b[:,:,3]
report={'reviewedSourceSlots':380,'reviewedBoards':32,'frozenInputs':len(before),'changedInputs':changed,'rawStudySize':raw.size,'targetSize':[768,512],'normalizedAlphaChangedPixels':int(alpha.sum()),'normalizedRGBAChangedOutsideDiagnosticHeadWindows':int((diff&~mask).sum()),'studySelected':False,'diagnosticWindowScope':'Broad rectangular head/neck windows, not semantic segmentation. Normalization is comparison only, never an installed source.','scope':'Complete source board review, not uninterrupted video/native task/furniture acceptance.'}
(P/'review-evidence.json').write_text(json.dumps(report,indent=2))
section=f'''## James side carry and West tablet complete source review — October 2, 2026

`character/james-side-motion-review-2026-10-02` resolves current catalog plus
ordered overrides; all380selected slots viewed in32boards: East/West carry,
pickup and unload, West inspection, both gears. Exact148 ruler and pivot
registration, no rescale/source edits. All{len(before)}frozen inputs unchanged.
Fourteen constructed source-clock GIFs retain each slot; boards were reviewed,
not uninterrupted browser/native video or natural task chains.

East bare carry head/cheek/skull looks larger than the idle master across gait and
interior pickup/unload poses; helmet overlays hide this underlying proportion
drift. Shoulder/torso construction also needs pose review before narrowing it.
West carrying is closer to its master; no blanket height/whole-body rescale is
justified. West tablet154poses per gear keep a compact reading posture and return,
with edge-on tablet toward face; hand/key-green residue remains a local issue.
Do not apply the East tablet positional mask to the opposite-facing artwork.

Built-in six-pose East head repair study retained with exact master/target/prompt.
Raw{raw.width}x{raw.height} vs target768x512; normalized alpha changes{int(alpha.sum())}
pixels and RGBA outside broad diagnostic head windows{int((diff&~mask).sum())}.
It redraws body/boots/case and adds surrounding haze, so remains wholly unselected.
No candidate manifests/runtime selection, native test or owner profile access.

Lesson: shared-helmet consistency can conceal bare-head anatomy drift. Review
bare and equipped sources together with directional idle; compare pickup/held/
gait/unload as one family and preserve shared pose identity across aliases.
Exact ruler metadata and a source-clock preview do not establish anatomy or
motion acceptance. Generated head-only prompts still require outside-region
and alpha evidence before admission.
Next coherent East cargo head/neck correction across shared poses, including
pickup/unload and turn joins; preserve original body/cargo registration and
paired helmet. West hand-edge material cleanup separately. Full-set context and
cross-family master/polish goal remains active/incomplete; no commit/export.
'''
def atomic(path,data):
    original=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
    assert path.read_bytes()==original,str(path)+' concurrent change';os.replace(tmp,path)
for rel in ['docs/CURRENT_STATUS.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    path=R/rel;original=path.read_bytes();add=section.encode()
    atomic(path,add+b'\n'+original if rel.endswith('CURRENT_STATUS.md') else original+b'\n\n'+add)
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');atomic(path,path.read_bytes()+b'\n\n'+section.encode())
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October2,2026 · Project: {R} · Task: James side cargo/West tablet review

## Objective and acceptance
Complete James set, then all-family master/style/perspective/proportions/material
polish. Current full goal incomplete; this is complete selected source review.

## Accepted decisions and constraints
Exact current masters/ordered selection; torch repairs/tablet diagnostics/wrench
on belt. Original registered body/cargo/helmet/clocks remain authoritative.

## Current state
New380source-slot/32board comparison and14source-clock GIFs; no production edits.
East bare cargo head drift found through pickup/gait/unload. West tablet hand-edge
residue identified. Generated six-head study rejected for body/alpha drift.

## Verification
All32boards viewed; all{len(before)}frozen inputs unchanged. Generated raw and
normalized geometry/alpha comparison retained; no native runs/profile access.
No continuous video, natural task or final owner acceptance claim.

## Next action
Coherent East cargo head/neck repair across shared pickup/held/gait/unload and
turn joins; preserve body/crate/helmet. West local hand-edge correction separately.
''')
print(json.dumps(report))
