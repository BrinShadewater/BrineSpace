from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'upper-donor-v32';out.mkdir(exist_ok=True)
base=p/'leg-bridge-v20/candidate.png'
donor=r/'character/james-cargo-return-bridges-v1/frames-v9/bare/000.png'
walk=p/'master-head-review-v16/bare-000.png'
standing=r/'character/james-carry-headcaps-v1/frames/004.png'
crop=[64,96,208,240];admission=[88,110,166,169]
refs=[]
for f,label in [(base,'target'),(donor,'actual-pose-guide'),(walk,'following-walk-pose'),(standing,'case-master')]:
    dst=out/(label+'.png');Image.open(f).convert('RGBA').crop(crop).resize((576,576),Image.Resampling.LANCZOS).save(dst);refs.append(dst)
prompt='''Use case: precise-object-edit. Edit Image1, a transparent James carrying sprite crop. Image1 owns the matte clothing, character size, retained legs, hands and graphite carrying case. Image2 is an ACTUAL existing chronological transition pose: use its narrower shoulder/chest profile and close-to-body elbow/forearm placement as the anatomy guide for this one upper-body pose. Copy the anatomical shoulder-to-waist arrangement visible in Image2, rather than inventing an abstract fractional turn. Image3 is the immediately following walking pose. Image4 is the standing case and material authority.
Change only the upper torso, arms and carried case area in Image1 so his shoulder and chest align above his already narrowed profile hips. Pull the near elbow closer to his ribs and show the side of his chest like Image2. Preserve Image1 knees, shins, boots and stance. The case must remain centered at Image1 existing waist position: do not push it forward/left, enlarge it or lower it. Keep the same compact graphite rectangular box, four dull silver corner latches, panel construction and two glove grips from Image1/Image4. Use Image2 only for human anatomy, not its old case design or old shiny/purple grade. Keep muted charcoal matte fabric, muted mustard panels, subdued metal highlights. No bright outline, no glossy finish, no purple, no new black shadow patches, no floating gloves, no case intersecting abdomen. The high belt meter remains on the belt and occluded by the glove; the wrench stays holstered. Same framing and transparent background; no ground shadow. All four references are identical144x144 native crops enlarged4x. Return precisely the same square crop and scale. This is one transition sprite, not a sheet. No added text or background.'''
pf=out/'prompt.txt';pf.write_text(prompt+'\n',encoding='utf-8')
files=[base,donor,walk,standing,Path(__file__),pf]+refs
(out/'inputs.json').write_text(json.dumps(dict(baseFile=base.relative_to(r).as_posix(),donorSource=donor.relative_to(r).as_posix(),crop=crop,admissionRegion=admission,references=[f.relative_to(r).as_posix() for f in refs],preCallSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}),indent=2)+'\n')
print('V32 actual-pose upper-body guide prepared; original head and retained legs protected.')
