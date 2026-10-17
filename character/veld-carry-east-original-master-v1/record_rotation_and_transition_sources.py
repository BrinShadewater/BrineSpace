"""Record rotation ambiguity and two complete rejected transition sources."""
from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'continuous-video-v3-white'
title='## Veld East rotation ambiguity and transition-source rejects — October 3, 2026'
note='''## Veld East rotation ambiguity and transition-source rejects — October 3, 2026

Added independent native148 rigid boot rotation+translation, uniform/paced,27
observed phases each.74 native paired lower-body comparisons prove identical gear
pixels for the complete first cycle. Rotation improves matching beyond flat stance,
but first support24->25 abruptly jumps0 to-40deg and fitted toe shifts about23px
despite NCC0.87. Overlay suggests a different overlapping boot, INVALID physical
identity/contact inference. Two corrected sole-marker overlays reviewed; initial
second-boot marker extended beyond actual toe, retained invalid first diagnostic.
Corrected markers remain material reference points, not measured floor contacts.
High correlation does not establish foot identity. Full contacts still unaccepted.

New builtin whole-source start/stop atlasd6b09dfb-3571-48a7-b3eb-bd432af7cd7a
saved with exact prompt/references: twelve poses/2x6. One first standing ruler:
heights145-148, head27-29, stop final standing146 vs original148. Equal-cell slicing
included neighbouring boot fragment; whole-component gutters remove it. Full
same-scale original comparisons reviewed; pair rejected for final head/body fidelity.
Separate single-row stop0709e962-2866-471f-b130-f55b5ed87aa1 uses only original
high-resolution held/gait refs, no low-density video guide. ONE global atlas
resample matched final standing148: body147-148/head28-29/floor222-223/no clipping.
Closer height consistency but still enlarged head vs original26-27; rejected final
identity. Both complete sources/prompts/registrations retained; no native tests,
helmet packaging, endpoint substitutions or normal selector adoption for rejects.

Lessons: two-row source consistency must be checked independently per row against
original proportions. Component gutters preserve complete figures; equal-grid
crop is not proof of unclipped geometry. Resample entire atlas ONCE at the common
ruler, then slice, avoiding per-cell width rounding. A standing148 ruler does not
prove head/body ratio. Do not normalize head/anatomy to rescue drifting sources.
Latent brown RGB under alpha0 is not visible background; inspect actual alpha
before declaring glow. Raw RGBA preserved and only exported alpha0 RGB cleared.

Next prove a representative independent WHOLE-POSE transition from the unchanged
original held master before another multi-pose atlas, then dense start/stop/exact
joins. Gait full near/far contact/rotation/overlap/temporal wrap, final master grade,
North contact repair, full original action/direction/furniture, ordinary controller/
save/menu Continue and cross-library polish remain. No live generation remains,
no runtime selectors changed. Full goal active/incomplete.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.

'''
for name,verdict in [('rotating-boot-audit.json','Initial second-boot toe annotation was beyond actual toe; invalid sole calibration. Rotation also permits high-score boot identity switches during overlap. Source and native captures unchanged.'),('rotating-boot-audit-v2.json','Corrected original sole-anchor grid and both uniform/paced rotation overlays inspected. Boot A24->25 angle0->-40 and fitted toe jump~23px at high NCC; likely switches to overlapping boot. Not full semantic foot/contact proof. Corrected sole material points are interior reference pixels, not independent floor contact landmarks.')]:
    data=json.loads((V/name).read_text(encoding='utf-8'));data['visualReview']=verdict;(V/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
data=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
data['rotationContactStudy']={'reports':['continuous-video-v3-white/rotating-boot-audit.json','continuous-video-v3-white/rotating-boot-audit-v2.json'],'pairedNativeLowerBodyChecks':74,'status':'Rotation matches improve; high-score overlap identity ambiguity unresolved','verdict':'First support24->25 jumps0->-40deg and toe~23px despite0.87NCC. Physical boot continuity unproven; no final contact/stride admission. Initial second-boot sole marker beyond real toe corrected separately, original diagnostic retained.'}
items=[('d6b09dfb-3571-48a7-b3eb-bd432af7cd7a','start-stop-source-v1','raw-start-stop-v1.png','Rejected final pair:12pose two-row atlas head27-29/body145-148; final stop standing146 vs original148, neighbour boot fragment caught and corrected component gutters. No anatomy repair, packaging/native test or normal admission.'),('0709e962-2866-471f-b130-f55b5ed87aa1','stop-source-v2','raw-stop-v2.png','Rejected final identity: single-row six stop keys with high-resolution originals only. Entire atlas single resample matched final standing148; body147-148/head28-29 vs original26-27/floor222-223/no clipping. Proportion drift persists; no packaging/native admission.')]
existing={g['id'] for g in data['generations']}
for ident,folder,raw,verdict in items:
    entry={'id':ident,'folder':folder,'raw':f'{folder}/{raw}','prompt':f'{folder}/prompt.txt','rawSHA256':hashlib.sha256((P/folder/raw).read_bytes()).hexdigest(),'references':['../veld-east-held-original-master-v1/raw-held-v1.png','raw-gait-v2.png'],'status':'Completed; rejected for final artwork','verdict':verdict}
    if folder=='start-stop-source-v1':entry['references'].append('continuous-video-v3-white/clip-frames/bare/018.png')
    if ident not in existing:data['generations'].append(entry)
    (P/folder/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
(P/'EXECUTIONS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('''
## Latest rotation/source-authoring milestone
audit_rotating_boots.py and corrected v2/report/overlays added from existing native
captures.74 paired native lower-body pixel comparisons0; all first-cycle gear body
identical. Initial sole B marker too far beyond toe, corrected by native source-grid
inspection; original reject retained. Boot A24->25 highNCC0.87 rotates0->-40deg,
toe jumps~23px: likely different overlapping boot, not proof of push-off contact.
Whole source start/stopd6b09dfb-3571-48a7-b3eb-bd432af7cd7a saved under
start-stop-source-v1:12poses2x6; reject final identity head27-29/body145-148/stop final
standing146vs148. Equal grid captured neighbour fragment; whole-component gutters
remove it (v1 preserved). Source ratios still drift. Stop0709e962-2866-471f-b130-f55b5ed87aa1
saved under stop-source-v2:6 one-row original-only keys, global atlas resample final
standing148/body147-148/head28-29/floor222-223; reject enlarged head vs original26-27.
Exact prompts/raw RGBA/registrations/master boards/verdicts retained, no native or
normal adoption. No live generation remains. Next prove an independent whole-pose
transition against original held master before expanding another atlas. No local
head/body resizing or endpoint substitution to conceal drifting intermediate art.
Full near/far contact/roll/overlap and original-master starts/stops remain, plus
North gait, all action/direction/furniture/controller/save/library polish.
''')
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(P/'record_rotation_and_transition_sources.py'),'exec'))
print('Rotation ambiguity and both terminal source rejects recorded; full goal remains active.')
