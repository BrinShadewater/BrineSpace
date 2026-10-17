from pathlib import Path
import json
P=Path(__file__).resolve().parent;V=P/'continuous-video-v2'
data=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
data['videoGradeTrial'].update(status='Success; rejected for final artwork',verdict='All141 raw frames reviewed, fixed-reference extraction and same-scale original comparison. Explicit no-purple wording did not preserve neutral/olive-grey cloth. Raw later motion remains plum-purple. Body147-152/head26-27/floor223-225 under unchanged source scale/offset; no per-frame normalization. No loop, helmet pack or native test admitted for V2. No live generation remains.')
(P/'EXECUTIONS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
raw=json.loads((V/'raw-review/review.json').read_text(encoding='utf-8'))
raw['visualReview']={'coverage':'All141 raw frames inspected in six chronological boards; native unchanged-scale raw32/raw48 compared with starting key, original-guided held and true original empty body.','verdict':'Reject for final material fidelity. Explicit no-purple prompt still shifts source neutral/olive-grey suit toward plum. Connected walking trial retained as evidence, not accepted motion/colour/loop. Alpha chronology boards not separately all inspected; all raw chronology was.'}
(V/'raw-review/review.json').write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('''
## Grade trial terminal verdict

Task448379855364450 Success,141 raw frames downloaded and all six raw chronology
boards reviewed. Same fixed extraction:147-152body/26-27head/223-225floor.
Same-scale original comparison confirms plum cloth drift persists despite explicit
no-purple wording. Rejected for final artwork; no selected loop or native admission.
Both videos retained; no live paid job remains. Do not issue repeated prompt-only
video retries for the same demonstrated grade failure. Next compare a different
whole-source authoring/colour-preservation approach using the neutral V2 keys and
masters; retain full two-step kinematics/contact requirement, not a short easy loop.
All action/direction coverage, start/stop and ordinary integration remain in scope.
''')
note='''## Veld East video grade trial rejected — October 3, 2026

Grade-preservation task448379855364450 completed,141 raw frames/all six raw
chronology boards inspected, same fixed-reference extraction and five-figure
original-master comparison. Added explicit neutral/olive-grey/no-purple wording
still yields plum cloth absent from unchanged starting key/held/true empty masters.
V2 rejected for final art:147-152body/26-27head/223-225floor; no selected loop or
native admission. Both source videos/prompts/ledgers retained, no live job remains.
Earlier native V1 motion sweep2299checks0 remains valid diagnostic playback evidence,
not final colour or complete rigid-foot acceptance. No normal selector changes.

Lesson: explicit colour-preservation prose alone did not solve two demonstrated
video grade failures. Keep the matched whole source and reject the video drift;
do not spend on uncontrolled prompt-only retries or conceal it with body-region
patches. Next investigate a different whole-source authoring/colour-preservation
approach, retaining both complete footsteps/physical contact rather than accepting
a smaller easy loop. Source/temporal/native/master fidelity are separate evidence.
Full scope remains active/incomplete: original-faithful gait/start/stop, North foot
contact repair, full original action/direction set, controller/save integration and
cross-library polish. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.

'''
template=(P/'record_native_milestone.py').read_text(encoding='utf-8');start=template.index('title=');end=template.index('paths=[')
script=template[:start]+'title='+repr(note.splitlines()[0])+'\nnote='+repr(note)+'\n'+template[end:]
(P/'record_grade_milestone.py').write_text(script,encoding='utf-8')
exec(compile(script,str(P/'record_grade_milestone.py'),'exec'),{'__file__':str(P/'record_grade_milestone.py')})
print('Grade trial terminal rejection recorded; no live generation remains.')
