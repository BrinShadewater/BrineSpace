from pathlib import Path
import hashlib,json,shutil
P=Path(__file__).resolve().parent;D=P.parent/'standing-step-video-v3-dark'
assert not (P/'generation.json').exists()
for name in ['master-input.png','whole-source-reference.png','registered-reference.png']:
 shutil.copyfile(D/name,P/name)
record=json.loads((D/'input-record.json').read_text(encoding='utf-8'))
assert hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest()==record['inputSha256']
record['conditioningChange']='Byte-identical dark-background original-native plate from trial448589965386249. Only motion prompt changes to slow load-bearing walk with persistent boot support and explicit finite timeline. No art/density/background edit.'
(P/'input-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
prompt='Locked orthographic camera, full EAST/right-facing pixel-art game sprite, exactly the reference character and small case. Preserve her native pixel texture, small head, body proportions, matte neutral charcoal suit, brown bun, skin and equipment colours. Uniform dark blue-black background RGB12,18,24. Animate ONE slow, careful, weight-bearing carrying walk cycle in place, NOT running, hopping or floating. One boot must remain planted and bear her weight at every instant; both boots are never airborne together. Keep her original ground level and fixed horizontal position. 0-1 seconds: stand exactly as shown. 1-3 seconds: smaller far foot takes one low short step, while the near foot stays on the ground supporting her. Transfer weight smoothly onto the far foot. 3-5 seconds: larger near foot takes one low short step while the far foot stays on the ground supporting her. 5-6 seconds: settle into the exact original feet-together standing pose. Slow continuous heel-to-toe support, natural hip/knee motion and small coordinated torso bob. No extra steps, fast cycling, high knees, crossed legs, skating, teleporting or dissolves. Arms hold the heavy case steadily. No head growth, suit recolouring, glossy lighting, white rim, floor graphics, shadows, text or extra props. Static camera and identical start/end pose.'
(P/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
assert len(prompt)<=2000
print(json.dumps({'inputSHA256':record['inputSha256'],'identicalDarkInput':True,'promptCharacters':len(prompt),'estimatedUSD':.28,'billingVerified':False}))
