"""Record source-contact/depth milestone without claiming complete motion."""
from pathlib import Path
import json, hashlib, os
from PIL import Image, ImageDraw
import numpy as np
P=Path(__file__).resolve().parent; R=P.parents[1]
deep=json.loads((P/'native-deep-contact-evidence.json').read_text())
fresh=json.loads((P/'native-fresh-contact-evidence.json').read_text())
assert deep['failures']==fresh['failures']==0
reports=[json.loads((P/f'{name}-validation.json').read_text()) for name in ['native-deep-contact','native-fresh-contact']]
assert all(r['exitCode']==0 and not r['timedOut'] for r in reports)
images=[Image.open(P/'fresh-captures'/name).convert('RGB') for name in ['source-03.png','source-03-foreground.png']]
a,b=map(np.array,images); y,x=np.where(np.any(a!=b,axis=2)); bounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
board=Image.new('RGB',(648,300),'#303b40');d=ImageDraw.Draw(board)
for i,(im,label) in enumerate(zip(images,['Default depth: bowl occluded','Diagnostic +64 depth: bowl visible'])):
 crop=im.crop((160,160,268,250)).resize((324,270),Image.Resampling.NEAREST)
 board.paste(crop,(i*324,30));d.text((i*324+6,8),label,fill='white')
board.save(P/'fresh-counter-contact-review.png')
selection=json.loads((P/'selection.json').read_text())
selection['status']='supported_south_contact_pose_staged_motion_unselected'
selection['deepReachDiagnostic']={
 'source':'deep-contact-source-v4.png','prompt':'deep-contact-prompt-v4.txt',
 'sourceSha256':hashlib.sha256((P/'deep-contact-source-v4.png').read_bytes()).hexdigest(),
 'fixedWholeFigureScale':.13,'bootAnchor':[614,995],
 'deepCandidateChecks':deep['checks'],'freshCandidateChecks':fresh['checks'],
 'nativeContactReview':'fresh-counter-contact-review.png','normalDepthHidesBowl':True,
 'diagnosticDepthOffset':64,'actualDepthChangedPixelsBounds':bounds,
 'productionDepthSelected':False,'motionSelected':False,
 'rejectedRevision3':'deep-contact-source-v3-rejected.png',
 'reasonRevision3Rejected':'Hands/bowl still above boot baseline despite requested forward correction',
 'strictProfileGuards':[r['realProfileUnchanged'] for r in reports],
 'profileDeltas':[r['profileDelta'] for r in reports]}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
note='''

## James South deep reach / depth diagnostic — October 1, 2026

Full James goal remains active. New whole South source v2 is fitted at .15 to a
256/p128,224 plane; 235 native checks pass after fixing capture-directory and
common-pivot endpoint comparisons, but bowl remains behind worktop rear edge.
v3 correction is retained rejected: no useful forward hand projection. Fresh v4
from the master projects bowl beyond toes, whole .13 skull/shoulder ruler and
sole anchor[614,995]. 237 actual-player/native checks pass at supported open prep
contact[48,128]. Same source drawn at normal depth hides bowl; diagnostic +64
world depth shows bowl/wrists on rear worktop. Captures and enlarged pair in
character/james-meal-service-south-open-v1/fresh-counter-contact-review.png.
No limb/body painting, per-part resizing or production installation. This is
one contact pose inserted amongst older reach frames, NOT approved motion.
Depth64 is diagnostic only; select bounded contact depth with the full transition
and nearby props before normal binding. Exact standing/held pixels remain after
common-pivot registration. Both successful engines0/no timeout; scratch APPDATA,
strict owner-profile guards false with last_session.json only, cause unproven.
Earlier fixture7fails and unexplained early engineexit1 retained separately.
Next author whole reach/retract interiors with consistent perspective/ruler,
matte grade, exact standing/held joins and contact-depth timing; then cup,
returns/interruptions/production/Continue and remaining contexts/full-set polish.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
 old=f.read_bytes()
 if b'## James South deep reach / depth diagnostic' in old:continue
 blob=note.encode()+b'\n'+old if f.name=='CURRENT_STATUS.md' else old+note.encode()
 tmp=f.with_name(f.name+'.james-deep-contact.tmp');tmp.write_bytes(blob);os.replace(tmp,f)
handoff=P/'HANDOFF.md';old=handoff.read_text();handoff.write_text(old+note)
print(json.dumps({'deepChecks':deep['checks'],'freshChecks':fresh['checks'],'depthChangedPixelsBounds':bounds,'contactPoseOnly':True,'productionInstalled':False,'goal':'active'}))
