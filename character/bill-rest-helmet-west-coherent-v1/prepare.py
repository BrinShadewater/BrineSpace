from pathlib import Path
import shutil,json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.parent/'bill-rest-helmet-east-coherent-v1';D=P.parent/'bill-seated-helmet-west-coherent-v1';A=P.parent/'bill-death-ground-helmet-south-lateral-v1'
S=P/'sources';S.mkdir(parents=True,exist_ok=True)
for source,name in [(D/'sources/canonical-head.png','canonical-head.png'),(A/'sources/canonical-closed-eyes.png','authored-closed-eyes.png'),(A/'sources/closed-eyes-v1.png','closed-eyes-v1.png'),(A/'sources/prompt-closed-eyes-v1.txt','prompt-closed-eyes-v1.txt')]:shutil.copy2(source,S/name)
original=Image.open(S/'canonical-head.png').convert('RGBA');out=np.array(original);donor=Image.open(S/'authored-closed-eyes.png').convert('RGBA')
eye=np.array(donor.crop((13,18,17,21)).resize((3,3),Image.Resampling.LANCZOS))
out[16:19,6:9,:3]=eye[:,:,:3]
Image.fromarray(out).save(S/'canonical-closed-eye.png')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(P/'closed-eye-registration.json').write_text(json.dumps({'generation':'exec-0b1ad8c7-6822-4afb-816d-f4980cb3c9fe','sourceSha256':sha(S/'closed-eyes-v1.png'),'donorSha256':sha(S/'authored-closed-eyes.png'),'canonicalSha256':sha(S/'canonical-head.png'),'resultSha256':sha(S/'canonical-closed-eye.png'),'sourceBox':[13,18,17,21],'targetBox':[6,16,9,19],'changedPixels':int(np.any(out!=np.array(original),axis=2).sum()),'alphaExact':bool(np.array_equal(out[:,:,3],np.array(original)[:,:,3])),'scope':'9 RGB pixels from authored front-left closed eyelid, native west shell/alpha unchanged'},indent=2)+'\n',encoding='utf-8')
t=(E/'build.py').read_text().replace('east','west')
t=t.replace('necks=[(469,245),(1224,394),(658,327),(1136,374),(115,803),(613,855),(1127,853)]','necks=[(526,278),(1355,459),(881,321),(1422,357),(432,818),(922,860),(1432,860)]')
t=t.replace('centers=[(477,184),(1247,341),(674,285),(1151,322),(90,749),(572,843),(1086,841)]','centers=[(499,188),(1327,375),(866,278),(1414,311),(421,768),(958,857),(1466,857)]')
t=t.replace('angles=[-5,-5,-5,-15,-40,-90,-90]','angles=[5,5,5,15,40,90,90]').replace('dx=19-head.width/2','dx=16-head.width/2')
t=t.replace('erase=local&warm','erase=local&(bare[:,:,3]>0)')
t=t.replace('pos=[round(neck[0]-anchor[0]),round(neck[1]-anchor[1])];hx,hy=centers[i-1];center=', 'pos=[round(neck[0]-anchor[0]),round(neck[1]-anchor[1])]\n        if i==7:pos=records[-1]["position"].copy()\n        hx,hy=centers[i-1];center=')
(P/'build.py').write_text(t,encoding='utf-8')
t=(P.parent/'bill-rest-helmet-south-coherent-v1/verify.py').read_text().replace('south','west')
start=t.index("check(r['frames'][-1]['componentPose']")
end=t.index("(P/'verification.json')")
t=t[:start]+'''check(r['frames'][-1]['closedEye'] and r['frames'][-2]['closedEye'],'authored closed sleep eyes')
check(r['frames'][-1]['position']==r['frames'][-2]['position'],'sleep helmet position held')
check(m['states'][-1]['restHeadOffset']==bm['states'][-1]['restHeadOffset'],'paired resting head reference')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=np.array(Image.open(P/'sources/canonical-head.png'));after=np.array(Image.open(P/'sources/canonical-closed-eye.png'))
mask=np.zeros(before.shape[:2],dtype=bool);mask[16:19,6:9]=True
check(np.array_equal(before[~mask],after[~mask]),'native hardware exact outside authored eyelid')
check(np.array_equal(before[:,:,3],after[:,:,3]),'canonical alpha exact')
''' +t[end:]
(P/'verify.py').write_text(t,encoding='utf-8')
(P/'prepare_validation.py').write_text((P.parent/'bill-rest-helmet-north-coherent-v1/prepare_validation.py').read_text(encoding='utf-8').replace('north','west').replace('NORTH','WEST').replace('v9b8w3m6p2r9v','z9b8w3m6p2r9v'),encoding='utf-8')
print('Prepared west paired helmet fitting with bounded authored closed eyelid')
