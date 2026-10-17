"""Compose opposite carrying turns from authored quarters, retaining planted joins."""
from pathlib import Path
import copy,hashlib,json
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
QUARTERS=['east-south','south-west','west-north','north-east']
ROUTES=[['east','south','west'],['south','west','north'],['west','north','east'],['north','east','south']]

def main():
 hashes={};provenance={};counts={}
 for kind in ['bare','helmet']:
  states=[];lookup={}
  for pair in QUARTERS:
   folder=HERE.parent/f"bill-carry-turn-{'helmet-' if kind=='helmet' else ''}{pair}-v1"
   pack=json.loads((folder/'manifest.json').read_text())
   assert pack['pivot']==[128,224] and pack['standingHeight']==148
   for original in pack['states']:
    s=copy.deepcopy(original);s['frameFiles']=[(folder/f).relative_to(HERE.parent).as_posix() for f in s['frameFiles']]
    lookup[s['id']]=s
    exported=copy.deepcopy(s);exported['frameFiles']=['../'+f for f in s['frameFiles']];states.append(exported)
  for route in ROUTES:
   first=lookup['carry-turn-'+'-'.join(route[:2])];second=lookup['carry-turn-'+'-'.join(route[1:])]
   sources=first['frameFiles']+second['frameFiles'][1:]
   assert (HERE.parent/first['frameFiles'][-1]).read_bytes()==(HERE.parent/second['frameFiles'][0]).read_bytes(),'Cardinal loaded midpoint must be exact'
   times=first['frameDurationsMs'][:];times[-1]+=second['frameDurationsMs'][0];times+=second['frameDurationsMs'][1:]
   key='carry-turn-'+route[0]+'-'+route[2];files=[];records=[]
   for i,source in enumerate(sources):
    path=HERE/'frames'/kind/key/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((HERE.parent/source).read_bytes());file=path.relative_to(HERE).as_posix();files.append(file)
    hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest();records.append({'file':file,'source':'../'+source})
   state={'id':key,'frameFiles':files,'frameDurationsMs':times,'loop':False,'water':False,'facings':first['facings']+second['facings'][1:],'provenance':'two clockwise authored quarters;exact loaded midpoint merged,combined hold retained;no new art or mirroring'}
   assert len(files)==11 and sum(times)==1600
   states.append(state);provenance[kind+'/'+key]={'route':route,'frames':records,'mergedSource':second['frameFiles'][0],'durationMs':1600,'runtimeTimingChangePending':True}
  manifest={'name':f'Bill {kind} full dry carry-turn candidate matrix','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_owner_visual_review','states':states}
  if kind=='helmet':manifest['equipment']='diving-helmet'
  (HERE/f'{kind}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');counts[kind]={'states':len(states),'quarterStates':8,'halfStates':4}
 (HERE/'half-turn-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
 (HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 (HERE/'coverage.json').write_text(json.dumps({'counts':counts,'installed':False,'nativePlayback':False,'ownerAcceptance':False,'quarterDurationMs':800,'halfDurationMs':1600,'legacyRuntimeHalfDurationMs':680},indent=2)+'\n')
 review=Image.new('RGB',(1536,2048),(29,43,51));draw=ImageDraw.Draw(review)
 gameplay=Image.new('RGB',(600,720));gd=ImageDraw.Draw(gameplay)
 for row,(kind,pair) in enumerate([(k,p) for k in ['bare','helmet'] for p in QUARTERS]):
  folder=HERE.parent/f"bill-carry-turn-{'helmet-' if kind=='helmet' else ''}{pair}-v1";pack=json.loads((folder/'manifest.json').read_text());state=pack['states'][0]
  gd.rectangle((0,row*90,600,row*90+89),fill=(29,43,51) if row<4 else (218,225,224))
  for i,file in enumerate(state['frameFiles']):
   im=Image.open(folder/file).convert('RGBA');review.paste(im,(i*256,row*256),im)
   s=82/148;sample=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS);gameplay.paste(sample,(i*100+50-round(128*s),row*90+87-round(224*s)),sample)
  draw.text((8,row*256+8),kind+' '+pair,fill='white')
 review.save(HERE/'quarter-matrix.png');gameplay.save(HERE/'gameplay-matrix.png')
 print('Built 24 candidate states:16 quarter/8 half across bare+helmet;88 derived half-frame references;1600ms retains quarter pacing')
if __name__=='__main__':main()
