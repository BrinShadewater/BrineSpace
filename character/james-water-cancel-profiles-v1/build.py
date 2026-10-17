"""Exact source-index entrances and authored pickup reversal before torch stow."""
from pathlib import Path
import json,os,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
DIRECTIONS=['east','south','west','north'];checks=[];profiles=[];review=[]
def check(ok,msg):checks.append({'passed':bool(ok),'check':msg})
def relative(f):return Path(os.path.relpath(f,P)).as_posix()
for gear in ['bare','helmet']:
 states=[]
 for direction in DIRECTIONS:
  cargo=P.parent/('james-water-cargo-'+direction+'-v1');stow=P.parent/('james-water-torch-stow-'+direction+'-v1')
  sm=json.loads((stow/(gear+'-manifest.json')).read_text())['states'][0]
  cm=json.loads((cargo/(gear+'-manifest.json')).read_text())
  for action,key in [('salvage','work'),('swim-pickup','pickup')]:
   source=next(x for x in cm['states'] if x['id']==action+'-'+direction)
   for index in range(6):
    sequence=list(range(index,-1,-1)) if key=='pickup' else [index]
    donor_files=[cargo/source['frameFiles'][i] for i in sequence]+[stow/f for f in sm['frameFiles'][1:]]
    durations=[50]*len(sequence)+sm['frameDurationsMs'][1:]
    ident='swim-cancel-'+key+'-'+str(index)+'-'+direction
    state={'id':ident,'frameFiles':[relative(f) for f in donor_files],'frameDurationsMs':durations,'loop':False,'waterPoses':[True]*len(donor_files),'waterKinds':['swim']*len(donor_files),'facings':[direction]*len(donor_files),'depthOffsets':[0.0]*len(donor_files),'provenance':{'entrance':source['id'],'entranceIndex':index,'sourceSequence':sequence,'derivation':'Exact visible source entrance; pickup reverses whole selected authored poses to return case before lit-tool pose, then authored extinguish/stow interiors and exact empty swim. No new raster, limb splice or body warp.'}}
    states.append(state)
    check(donor_files[0]==cargo/source['frameFiles'][index],'Exact visible source index '+ident+' '+gear)
    check(not state['loop'] and 400<=sum(durations)<=650,'Finite physical-return-independent clock '+ident+' '+gear)
    check(state['waterPoses']==[True]*len(donor_files),'Prone water contract '+ident+' '+gear)
    for f in donor_files:check(Image.open(f).size==(256,276),'Full donor canvas '+relative(f))
    if key=='pickup':check(sequence==list(range(index,-1,-1)),'Whole selected pickup reversal '+ident+' '+gear)
    profiles.append({'id':ident,'gear':gear,'entranceIndex':index,'sourceState':source['id'],'sourceClockMs':source['frameDurationsMs'],'durationMs':sum(durations),'frameHashes':[hashlib.sha256(f.read_bytes()).hexdigest() for f in donor_files]})
    if gear=='helmet' and key=='pickup' and index==3:
     for j,f in enumerate(donor_files):
      im=Image.open(f).convert('RGBA');board=Image.new('RGB',(720,320),'#303b40');draw=ImageDraw.Draw(board);draw.text((8,8),'James '+direction+' cancelled pickup / whole source '+str(j)+' / indexed source',fill='white');board.paste(im,(30,30),im);small=im.resize((142,153),Image.Resampling.BILINEAR);board.paste(small,(380,105),small);review.append((board,durations[j]+(350 if j in [0,len(donor_files)-1] else 0)))
 (P/(gear+'-manifest.json')).write_text(json.dumps({'name':'James staged indexed exterior cancellation '+gear,'frameWidth':256,'frameHeight':276,'pivot':[128,128],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'selected_runtime_indexed_cancellation','states':states},indent=2)+'\n')
review[0][0].save(P/'review.gif',save_all=True,append_images=[x[0] for x in review[1:]],duration=[x[1] for x in review],loop=0,disposal=2,optimize=False)
report={'checks':len(checks),'failures':sum(not x['passed'] for x in checks),'profiles':profiles,'states':96,'scope':'Exact indexed source/pickup-reverse package contracts, not visual acceptance of all entrances or production saved-clock/Continue/safety proof.'}
(P/'contract-evidence.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['checks','failures','states']}));raise SystemExit(bool(report['failures']))
