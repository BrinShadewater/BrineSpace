"""Package pickup candidates with an exact existing donning endpoint."""
from pathlib import Path
import json,hashlib,argparse
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--candidate', choices=['01','02','05','06','07'], help='Defaults to the currently selected source for the actor')
parser.add_argument('--actor', choices=['bill','veld','branforth'], default='bill')
args=parser.parse_args()
actor=args.actor
candidate=args.candidate or {'bill':'07','veld':'01','branforth':'02'}[actor]
versions={'bill':{'05':'v2','06':'v3','07':'v4'},'veld':{'01':'v1'},'branforth':{'01':'v1','02':'v2'}}
if candidate not in versions[actor]: parser.error(f'Candidate {candidate} has no measured registration for {actor}')
source=ROOT/f'generated/{actor}-pickup-helmet-east-candidate-{candidate}.png'
raw=Image.open(source).convert('RGBA');data=np.array(raw);rgb=data[:,:,:3].astype(np.int16)
data[(rgb[:,:,0]>rgb[:,:,1]+35)&(rgb[:,:,2]>rgb[:,:,1]+35)]=0
clean=Image.fromarray(data);mask=(data[:,:,3]>0).sum(axis=0)>3
edges=np.diff(np.r_[False,mask,False].astype(int));groups=[(int(a),int(b)) for a,b in zip(np.where(edges==1)[0],np.where(edges==-1)[0]) if b-a>25]
assert len(groups)==6
version=versions[actor][candidate]
pack=ROOT/f'revisions/{actor}-pickup-helmet-east-{version}';pack.mkdir(exist_ok=True)
factor=raw.width/2048;scale=74/({'bill':392,'veld':408,'branforth':368}[actor]*factor)
feet={'bill':[(194,562),(499,562),(833,562),(1172,562),(1487,562)],
      'veld':[(194,563),(522,563),(866,563),(1200,563),(1525,563)],
      'branforth':[(175,546),(486,546),(806,546),(1188,546),(1535,546)]}[actor]
if actor=='branforth' and candidate=='02': feet=[(175,546),(486,546),(804,546),(1180,546),(1527,546)]
if actor=='bill' and candidate=='07':
    scale=74/(381*factor)
    feet=[(177,540),(511,540),(857,540),(1193,540),(1537,540)]
registrations=[];frames=[]
for i,((left,right),(fx,fy)) in enumerate(zip(groups,feet)):
    box=clean.crop((left,0,right,raw.height)).getbbox();crop=(left+box[0],box[1],left+box[2],box[3]);body=clean.crop(crop)
    body=body.resize((round(body.width*scale),round(body.height*scale)),Image.Resampling.BOX);a=np.array(body);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;body=Image.fromarray(a)
    pos=(round(46-(fx*factor-crop[0])*scale),round(98-(fy*factor-crop[1])*scale))
    assert pos[0]>0 and pos[1]>0 and pos[0]+body.width<92 and pos[1]+body.height<104
    frame=Image.new('RGBA',(92,104));frame.alpha_composite(body,pos);frames.append(frame);registrations.append({'crop':crop,'footSource':[fx*factor,fy*factor],'paste':pos})
endpoint=ROOT/f'pilot/{actor}-equip-helmet-east/frame_000.png';frames.append(Image.open(endpoint).convert('RGBA'))
sheet=Image.new('RGB',(1104,208),'#1d252a')
for i,frame in enumerate(frames):
    frame.save(pack/f'frame_{i:03}.png');large=frame.resize((184,208),Image.Resampling.NEAREST);sheet.paste(large,(184*i,0),large)
sheet.save(pack/'contact.png')
manifest={'status':'candidate_not_integrated','frameWidth':92,'frameHeight':104,'pivot':[46,98],'states':[{'id':'pickup-helmet-east','frameFiles':[f'frame_{i:03}.png' for i in range(6)],'frameDurationsMs':[140,180,160,180,180,160],'loop':False}]}
(pack/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(pack/'registration.json').write_text(json.dumps({'source':source.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'frames':registrations,'endpointSource':endpoint.relative_to(ROOT).as_posix(),'endpointSha256':hashlib.sha256(endpoint.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
print('Five pickup poses plus exact donning endpoint packaged; visual join review required')
