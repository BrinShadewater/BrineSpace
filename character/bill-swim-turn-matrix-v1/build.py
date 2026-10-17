"""Compose full basic-swim turn coverage from independently authored quarters."""
from pathlib import Path
import copy,hashlib,json
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
QUARTERS=['east-south','south-west','west-north','north-east']
ROUTES=[['east','south','west'],['south','west','north'],['west','north','east'],['north','east','south']]

def main():
 hashes={};provenance={}
 for kind in ['bare','helmet']:
  states=[];lookup={}
  for pair in QUARTERS:
   folder=HERE.parent/f"bill-swim-turn-{'helmet-' if kind=='helmet' else ''}{pair}-v1"
   pack=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
   assert pack['pivot']==[128,128] and pack['standingHeight']==148
   for original in pack['states']:
    s=copy.deepcopy(original);s['frameFiles']=['../'+(folder/f).relative_to(HERE.parent).as_posix() for f in s['frameFiles']]
    lookup[s['id']]=s;states.append(s)
  for route in ROUTES:
   first=lookup['swim-turn-'+'-'.join(route[:2])];second=lookup['swim-turn-'+'-'.join(route[1:])]
   assert (HERE/first['frameFiles'][-1]).read_bytes()==(HERE/second['frameFiles'][0]).read_bytes(),'exact common swimming endpoint'
   sources=first['frameFiles']+second['frameFiles'][1:]
   times=first['frameDurationsMs'][:];times[-1]+=second['frameDurationsMs'][0];times+=second['frameDurationsMs'][1:]
   key='swim-turn-'+route[0]+'-'+route[2];files=[];records=[]
   for i,source in enumerate(sources):
    path=HERE/'frames'/kind/key/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((HERE/source).read_bytes());file=path.relative_to(HERE).as_posix();files.append(file)
    hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest();records.append({'file':file,'source':source})
   s={'id':key,'frameFiles':files,'frameDurationsMs':times,'loop':False,'facings':first['facings']+second['facings'][1:],'waterKinds':['swim']*11,'waterPoses':[True]*11,'depthOffsets':[0]*11,'provenance':'two clockwise authored quarters;exact common endpoint merged with combined hold;no mirroring or new raster art'}
   assert len(files)==11 and sum(times)==1280
   states.append(s);provenance[kind+'/'+key]={'route':route,'frames':records,'mergedSource':second['frameFiles'][0],'durationMs':1280}
  manifest={'name':f'Bill {kind} complete basic-swim turn matrix','frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'installed_runtime_reviewed','states':states}
  if kind=='helmet':manifest['equipment']='diving-helmet'
  (HERE/f'{kind}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
  board=Image.new('RGB',(2816,1024),(29,43,51));d=ImageDraw.Draw(board)
  for row,state in enumerate(states[-4:]):
   d.text((5,row*256+5),state['id'],fill='white')
   for col,file in enumerate(state['frameFiles']):
    im=Image.open(HERE/file).convert('RGBA');board.paste(im,(col*256,row*256),im)
  board.save(HERE/f'{kind}-half-contact.png')
 for file,data in [('half-turn-provenance.json',provenance),('frame-hashes.json',hashes)]:
  (HERE/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 print('Built 12 routes per gear:8quarter640ms/4half1280ms;exact common midpoints')
if __name__=='__main__':main()
