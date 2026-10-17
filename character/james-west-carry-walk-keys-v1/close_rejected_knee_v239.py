from pathlib import Path
import hashlib,json,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'knee-material-phase30-v239';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:
 assert all(sha(r/f)==h for f,h in d[group].items())
assert sha(out/'prompt.txt')==d['promptSha256']
ledger=json.loads((p/'material-repair-progress.json').read_bytes())
assert all('lower-material-phase30-v205' in ledger['states'][30]['candidateSources'][gear]['file'] for gear in ['bare','helmet'])
evidence=dict(disposition='rejected_before_packaging_and_native',execution='013c2056-5534-4ec7-9a55-61fe040be867',rawSha256=sha(out/'raw.png'),reviewed=['edit-target.png','master-metal-reference.png','raw.png'],findings=['Generated knee fitting has two prominent brass fasteners absent from target and transfers plate design from material reference.', 'Fitting orientation and surrounding quilt/strap construction drift; exact target landmarks are not preserved.', 'Candidate not packaged, not native tested, not selected; original restored knee and phase30 V205 unchanged.'],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
(out/'review.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
section='''### James knee material reference contamination rejected - October3,2026

V239 phase30 knee edit raw visually reviewed and rejected BEFORE packaging/native.
Two prominent brass fasteners and changed fitting construction transferred from
the original-master material sample despite geometry-only constraints. Prompt,
target, references and raw hashes frozen; current selected V205 and restored
original knee remain unchanged. No new native or motion acceptance claimed.
Lesson: a reference containing conspicuous fasteners can contaminate component
design even when labelled material-only. Choose a material patch without distinct
hardware motifs and explicitly preserve component construction as well as joint
coordinates. Do not admit added details merely because the outer alpha survives.
Remaining: knee finish continuity, current full49 moving grade/master proportions/
contact/seam, normal cargo integration and all-family consistency/polish.
Evidence: character/james-west-carry-walk-keys-v1/knee-material-phase30-v239/review.json.
'''
guides=record_guides(r,section,'### James carrying opening lower finish phases0 to3')
(out/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nActive full animation objective incomplete. Next use a motif-free material reference for the same restored knee.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in out.glob('*.png')]
a=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert all(a[i+2]==b'lfs' for i in range(0,len(a)-1,3))
print(json.dumps(dict(rejected=239,selectedPhase30=205,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
