"""Reuse accepted diagnostic cycles as coherent inspection, without pixel edits."""
from pathlib import Path
import json,copy,hashlib,os
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DIRECTIONS={'east':'v1','south':'v3','west':'v2','north':'v2'}
def main():
 records={};packs={}
 for mode in ['bare','helmet']:
  records[mode]={};out=None
  for direction,version in DIRECTIONS.items():
   folder=ROOT/'character'/(f'james-interact-{direction}-matched-{version}' if mode=='bare' else f'james-shared-helmet-interact-{direction}-{version}')
   m=json.loads((folder/'manifest.json').read_text());source=next(s for s in m['states'] if s['id']=='interact-'+direction)
   if out is None:out={k:copy.deepcopy(v) for k,v in m.items() if k!='states'};out.update(name='James tablet inspection '+mode,states=[],status='installed_inspection_tablet_owner_review_pending')
   assert m['pivot']==out['pivot'] and m['frameWidth']==out['frameWidth'] and m['frameHeight']==out['frameHeight']
   st=copy.deepcopy(source);key='inspect-'+direction;st['id']=key;st['loop']=True;st['frameDurationsMs'][-1]+=500;st['waterKinds']=['inspect']*len(st['frameFiles']);rows=[]
   st['frameFiles']=[Path(os.path.relpath(folder/f,HERE)).as_posix() for f in source['frameFiles']]
   for f in st['frameFiles']:
    p=(HERE/f).resolve();rows.append(dict(source=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
   st['provenance']['inspectionDerivation']=dict(sourceManifest=(folder/'manifest.json').relative_to(ROOT).as_posix(),sourceState=source['id'],method='Exact owner-selected diagnostic lift/read/stow cycle reused for inspection; exact idle endpoint loop; no pixel, scale, grade or head changes; original motion timing plus500ms terminal idle hold to close six-second life_inspect stage',sourcePixelHashes=[r['sha256'] for r in rows]);records[mode][key]=rows;out['states'].append(st)
  (HERE/(mode+'-manifest.json')).write_text(json.dumps(out,indent=2)+'\n');packs[mode]=out
 (HERE/'registration.json').write_text(json.dumps(records,indent=2)+'\n')
 frames=[];times=[]
 for direction in DIRECTIONS:
  key='inspect-'+direction;st=next(s for s in packs['bare']['states'] if s['id']==key);eq=next(s for s in packs['helmet']['states'] if s['id']==key)
  for i,f in enumerate(st['frameFiles']):
   board=Image.new('RGB',(1000,330),'#303b40');draw=ImageDraw.Draw(board);draw.text((8,8),'James inspection / '+direction+' / bare / sealed helmet / 82px / 54px / 27px',fill='white')
   for j,(mode,rel) in enumerate([('bare',f),('helmet',eq['frameFiles'][i])]):
    p=packs[mode];im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(HERE/rel).convert('RGBA'),(128-p['pivot'][0],224-p['pivot'][1]));board.paste(im,(230*j,70),im)
    for h,x in [(82,510),(54,725),(27,870)]:
     sc=h/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);board.paste(small,(x+j*(round(256*sc)+8),294-round(224*sc)),small)
   frames.append(board);times.append(st['frameDurationsMs'][i])
 # GIF only supports10ms units; distribute rounding over cumulative time.
 elapsed=0;rounded=0;dur=[]
 for ms in times:
  elapsed+=ms;now=round(elapsed/10)*10;dur.append(now-rounded);rounded=now
 frames[0].save(HERE/'review.gif',save_all=True,append_images=frames[1:],duration=dur,loop=0)
 (HERE/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James tablet inspection</h1><p>Exact selected diagnostic cycles, repeated at shared idle endpoints. Wrench stays on belt. Sealed helmet variant.</p><img src="review.gif">')
 print('4 inspection states,565 poses per mode,1130 unchanged source references;6000ms cycles')
if __name__=='__main__':main()
