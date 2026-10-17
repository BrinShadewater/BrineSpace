"""Compose independently drawn quarter turns; do not mirror, resize or regrade."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ROUTES={
 'carry-turn-east-west':[('james-cargo-turn-east-south-height-v3','carry-turn-east-south'),('james-cargo-turn-south-west-v1','carry-turn-south-west')],
 'carry-turn-north-south':[('james-cargo-turn-east-north-v1','carry-turn-north-east'),('james-cargo-turn-east-south-height-v3','carry-turn-east-south')],
}
REVERSES={'carry-turn-west-east':'carry-turn-east-west','carry-turn-south-north':'carry-turn-north-south'}
def main():
 hashes={};records={};manifests={}
 for mode in ['bare','helmet']:
  sequences={};timings={};cuts={}
  for key,route in ROUTES.items():
   seq=[];dur=[];neck=[]
   for pack,clip in route:
    folder=ROOT/'character'/pack;m=json.loads((folder/(mode+'-manifest.json')).read_text());st=next(s for s in m['states'] if s['id']==clip);reg=json.loads((folder/'registration.json').read_text());reverse=clip.split('-')[-2:] in [['north','east']]
    poses=list(reversed(range(6))) if reverse else list(range(6))
    source=[(folder/f).relative_to(ROOT).as_posix() for f in st['frameFiles']]
    c=[reg['tracking'][i]['headCutoff'] for i in poses]
    if seq:
     assert Image.open(ROOT/seq[-1]).tobytes()==Image.open(ROOT/source[0]).tobytes(),'Quarter seam is not exact'
     assert neck[-1]==c[0],'Quarter seam head cuts differ'
     dur[-1]+=st['frameDurationsMs'][0];source=source[1:];c=c[1:];d=st['frameDurationsMs'][1:]
    else:d=st['frameDurationsMs']
    seq+=source;dur+=d;neck+=c
   sequences[key]=seq;timings[key]=dur;cuts[key]=neck
  for key,forward in REVERSES.items():sequences[key]=sequences[forward][::-1];timings[key]=timings[forward][::-1];cuts[key]=cuts[forward][::-1]
  m=dict(name='James coherent half carrying turns '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='installed_composed_half_turns_owner_review_pending',states=[])
  records[mode]={}
  for key,seq in sequences.items():
   files=[];rows=[]
   for i,src in enumerate(seq):
    dest=HERE/'frames'/mode/key/f'{i:03d}.png';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/src,dest);rel=dest.relative_to(HERE).as_posix();files.append(rel);sha=hashlib.sha256(dest.read_bytes()).hexdigest();hashes[rel]=sha;rows.append(dict(source=src,sha256=sha,headCutoff=cuts[key][i]))
   records[mode][key]=rows
   m['states'].append(dict(id=key,frameCount=len(seq),frameFiles=files,frameDurationsMs=timings[key],loop=False,facings=[key.split('-')[-1]]*len(seq),waterKinds=['carry']*len(seq),waterPoses=[False]*len(seq),depthOffsets=[0]*len(seq),provenance=dict(derivation='Exact independently drawn quarter frames composed at shared directional pose; duplicate seam merged by summing its holds; reverse exact; no pixel modification',sourceFrames=seq,sourcePixelHashes=[r['sha256'] for r in rows],equipment='Donor selected head angles; below-neck body identity retained')))
  (HERE/(mode+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');manifests[mode]=m
 (HERE/'registration.json').write_text(json.dumps(records,indent=2)+'\n');(HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 boards=[];times=[]
 for st in manifests['bare']['states']:
  key=st['id'];helm=next(s for s in manifests['helmet']['states'] if s['id']==key)
  for i,(bare,helmet) in enumerate(zip(st['frameFiles'],helm['frameFiles'])):
   board=Image.new('RGB',(1000,330),'#303b40');d=ImageDraw.Draw(board);d.text((8,8),'James half carrying turn / '+key+' / bare / helmet / 82px / 54px / 27px',fill='white')
   for j,path in enumerate([bare,helmet]):
    im=Image.open(HERE/path).convert('RGBA');board.paste(im,(j*230,70),im)
    for h,x in [(82,510),(54,725),(27,870)]:
     sc=h/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);board.paste(small,(x+j*(round(256*sc)+8),294-round(224*sc)),small)
   boards.append(board);times.append(st['frameDurationsMs'][i]+(300 if i in [0,len(st['frameFiles'])-1] else 0))
 boards[0].save(HERE/'review.gif',save_all=True,append_images=boards[1:],duration=times,loop=0)
 contact=Image.new('RGB',(2816,1280),'#303b40');d=ImageDraw.Draw(contact)
 for row,key in enumerate(ROUTES):
  for j,mode in enumerate(['bare','helmet']):
   st=next(s for s in manifests[mode]['states'] if s['id']==key)
   for i,path in enumerate(st['frameFiles']):
    im=Image.open(HERE/path).convert('RGBA');contact.paste(im,(i*256,(row*2+j)*320+55),im);d.text((i*256+6,(row*2+j)*320+8),key+' / '+mode+' '+str(i),fill='white')
 contact.save(HERE/'contact.png');(HERE/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James carrying half turns</h1><p>11 exact selected quarter poses, merged seam; 1600ms runtime, review adds endpoint holds. Owner review pending.</p><img src="review.gif"><img src="contact.png">')
 print('4 states / 88 bare and equipped references / 11 poses per half turn / 1600ms')
if __name__=='__main__':main()
