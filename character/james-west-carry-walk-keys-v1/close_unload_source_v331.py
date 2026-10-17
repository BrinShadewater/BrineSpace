from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];motion=p/'north-unload-coherent-motion-v329';o=p/'north-unload-bend-anchor-v331'
im=Image.open(o/'raw.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);im.save(o/'fixed-canvas-source.png')
first=Image.open(r/'character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png').convert('RGBA')
low=Image.open(motion/'frames/bare/062.png').convert('RGBA')
previous=Image.open(p/'north-unload-low-source-v314/fixed-canvas-source.png').convert('RGBA')
ims=[first,im,low,previous];bs=[f.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox() for f in ims]
board=Image.new('RGB',(1536,430),(48,59,64));d=ImageDraw.Draw(board)
for j,(frame,b,label) in enumerate(zip(ims,bs,['Turn entry','New bend331','Video low329','Earlier low314'])):
    x=j*384;board.paste(frame,(x+64,20),frame);d.text((x+5,3),f'{label} {b}',fill='white');pos=x+10
    for h in [82,54,27]:
        n=round(256*h/148);small=frame.resize((n,n),Image.Resampling.LANCZOS);board.paste(small,(pos,420-n),small);pos+=n+6
board.save(o/'source-comparison.png')
inputs=json.loads((o/'inputs.json').read_bytes())
for ref in inputs['refs']:assert hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest()==ref['sha256']
inputs.update(submittedPromptFile='submitted-prompt.txt',submittedPromptSha256=hashlib.sha256((o/'submitted-prompt.txt').read_bytes()).hexdigest(),generationFile='exec-baad9068-f213-4e2b-a93e-4559410d3103.png')
(o/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
report=dict(bounds=bs[1],entryBounds=bs[0],crownChange=bs[1][1]-bs[0][1],soleChange=bs[1][3]-bs[0][3],selected=False,normalChanged=False,nativeRun=False,fullGoalComplete=False,status='rejected_before_native_floor_contact',findings=['shallow bend and muted belt wrench, but soles lifted from entry floor','case wraps broadly outside calves rather than matching original carried prop','head/backpack shape and curved master cloth remain unproven'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
job=json.loads((motion/'generation.json').read_bytes());assert job['status']=='Success'
for name,key in [('first.png','imageSha256'),('last.png','lastImageSha256')]:assert hashlib.sha256((motion/name).read_bytes()).hexdigest()==job[key]
source=json.loads((motion/'source-review.json').read_bytes());assert source['frameCount']==142 and source['checks']==284 and source['failures']==0
source.update(visualDisposition='rejected_for_normal_adoption_material_and_overdeep_bend',rawChronologyPagesViewed=list(range(6)),alphaChronologyPagesViewed=[0,2,5],nativeRun=False)
(motion/'source-review.json').write_text(json.dumps(source,indent=2)+'\n')
files=list(motion.rglob('*.png'))+list(o.glob('*.png'))+[motion/'source.mp4']
raw=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in files)
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=raw,cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
section=f'''### James full unloading clip fidelity review — October 3, 2026

V329 task448620884267478 terminalSuccess/downloaded; all142raw frames at24fps,
5917ms retained, six complete raw chronology boards viewed plus alpha pages0/2/5.
Full-source APNG all142pixels/clocks replay exact:284checks0. Uniform dark48,59,64
alpha/tolerance8/components>=20, whole1/3 registration, no RGB correction/pose fit.
Input controls/source/output evidence retained; normal sources/controllers unchanged.
Top75..130/floor221..223/head25..28; bounding stability does not prove anatomy.
V330 detailed input/middle/exit board confirms belt wrench greys become nearwhite
during bend: fixed belt-region bright achromatic counts0initial to69atframe57.
This is local appearance evidence, not proof of a whole-body grade change. Deep
compression/large crouch and broad floor case persist. REJECT normal adoption;
retain coherent rise as study, no native run or helmet expansion of failed source.

V331 built-in whole-turn-entry bend anchor with original West master material.
Refs/prompts/raw retained; whole1254nearest256 once, no translations or fitting.
New bounds{bs[1]}, entry{bs[0]}; crown change{report['crownChange']}px,
sole change{report['soleChange']}px. Shallow bend/muted wrench but lifted boots,
broader case around calves; rejected before native. Raw and four-source board
H148/82/54/27 viewed. Full goal active; full-set/cross-family fidelity unproven.

Lessons: first/last sources constrain endpoints, not interior knee anatomy or
tool highlight. Check local equipment brightness alongside body/crown/floor.
An explicit intermediate pose also needs support/prop checks before guiding a
temporal clip. Do not body-fit floating poses or expand rejected sources merely
because replay/manifest checks pass. Next viable authored bend must preserve
original foot support and case proportions before full bend/rise generation.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-bend-anchor-v331/HANDOFF.md.
'''
guides=record_guides(r,section,'### James coherent unload source and endpoint pilot — October 3, 2026')
handoff=f'''# Project handoff

Updated: October 3, 2026 · James unloading source fidelity

## Objective and acceptance
Full master-matched James set and whole-family consistency/polish; active/incomplete.

## Accepted decisions and constraints
Original masters, matte curved cloth, fixed support, belt wrench/tablet/forward
torch. No pose fitting, brightness normalization or omitted failed frames.

## Current state
329 video complete, source/142raw/142alpha/full APNG/manifest/reports retained.
330 material/bend diagnosis rejects normal adoption: white wrench and deep bend.
331 whole-source bend anchor rejected for floated feet/broad case. New review/
closeout helpers, exact submitted prompts, full comparisons and five guides.
No normal artwork/controller changes; no Godot probes or owner save operations.

## Verification
284 full-source decoded RGBA/clock checks0;142@24fps/5917ms. All6raw pages,
alpha0/2/5 and material/endpoint board viewed. Local bright tool ROI0->69pixels
at57. 331 source bounds{bs[1]} vsentry{bs[0]}; floor mismatch remains.
Provider/input hashes and{len(files)}LFS media attributes verified. Native not run.
No continuous-playback acceptance claimed. Billing unverified estimateUSD0.28.

## Next action
Author viable moderate bend with exact original boot support and carried-case
proportions before any new temporal trial. Keep rejected source whole. Complete
bend/rise material/anatomy/contact first, then paired helmet/normal adoption.
Full carry/turn/all-family and ordinary lifecycle/interruptions checks remain.
'''
(o/'HANDOFF.md').write_text(handoff)
(motion/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old)
data['wholeUnloadSourceReview']=dict(version=331,videoReview=str((motion/'source-review.json').relative_to(r)),bendReview=str((o/'review.json').relative_to(r)),selected=False,sourceAcceptance=False,normalChanged=False)
data['nextVisualRepair']='Viable moderate full-source unload bend with original planted boot support and original case proportions; whole sequence matte wrench/cloth/anatomy and shared helmet before normal adoption. Full set consistency remains.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(dict(bounds=bs,checks=284,mediaLfs=len(files),guides=guides,selected=False)))
