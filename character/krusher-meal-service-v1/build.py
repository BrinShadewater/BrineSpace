"""Identity conversion once per source pose, reused by all indexed returns."""
import copy,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import binary_fill_holes,binary_closing
P=Path(__file__).resolve().parent;R=P.parent.parent;C=R/'character/krusher-james-canonical-v4';M=R/'character/krusher-meal-family-v1'
inventory=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text());new_sources=json.loads((R/'character/krusher-complete-animation-v1/meal-service-unique-sources.json').read_text());new_order={h:i for i,h in enumerate(new_sources)}
known={r['sourceHash']:r for r in json.loads((M/'provenance.json').read_text())['records'] if r['gear']=='bare'}
family={k:v for k,v in inventory['resolved']['bare'].items() if k.startswith(('meal-','cup-'))};yy,xx=np.indices((256,256));target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722]);records={};checks=0
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
canonical=json.loads((C/'bare-manifest.json').read_text());result={'name':'Krusher Dom meal service and returns','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'candidate-not-installed','identity':canonical['identity'],'states':[]}
# (source head bottom, pitched source index; None denotes upright)
south_fit={9:(103,None),10:(116,0),11:(163,1),12:(173,2),13:(173,2),14:(161,1),15:(118,0),16:(174,2),17:(144,0),18:(118,0)}
images={}
for key,resolved in family.items():
 mp=R/resolved['manifest'].removeprefix('res://');profile=resolved['profile'];state=copy.deepcopy(resolved['state']);files=[]
 for relative in state['frameFiles']:
  source=((R/relative.removeprefix('res://')) if relative.startswith('res://') else mp.parent/relative).resolve();h=sha(source)
  if h not in records:
   im=Image.open(source).convert('RGBA');pad=Image.new('RGBA',(256,256));offset=(round(128-profile['pivot'][0]),round(224-profile['pivot'][1]));pad.alpha_composite(im,offset);a=np.array(pad);rgb=a[:,:,:3].astype(float);direction=key.rsplit('-',1)[1];head_source=None;anchor=None
   if h in known:
    k=known[h];out=np.array(Image.open(M/k['output']).convert('RGBA'));allowed=np.array(Image.open(M/k['allowedMask']))>0;head_source=R/k['headSource'];anchor=k['headPaste'];method='Exact reuse of checked meal-family pose'
   else:
    j=new_order[h];out=a.copy()
    if j in (0,9):
     idle=next(s for s in canonical['states'] if s['id']=='idle-'+direction);endpoint=Image.new('RGBA',(256,256));endpoint.alpha_composite(Image.open(C/idle['frameFiles'][0]).convert('RGBA'),(36,52));out=np.array(endpoint);allowed=np.any(a!=out,axis=2);method='Exact canonical-v4 bare idle endpoint'
    else:
     if direction=='north':
      zone=(a[:,:,3]>180)&(xx>=110)&(xx<148)&(yy<93);top=int(yy[zone].min());head_bottom=96+(top-76);crown=zone&(yy<top+16);axis=round((int(xx[crown].min())+int(xx[crown].max()))/2);head_source=R/'character/krusher-bill-base-test-v2/sources/north-head-native.png';pitch=None
     else:
      head_bottom,pitch=south_fit[j];top=head_bottom-30
      skin=(a[:,:,3]>180)&(xx>=116)&(xx<144)&(yy>=head_bottom-20)&(yy<head_bottom)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb.mean(2)>40)
      axis=round((int(xx[skin].min())+int(xx[skin].max()))/2)
      head_source=R/f'character/krusher-south-bow-heads-v1/head-{pitch}.png'
     head=Image.open(head_source).convert('RGBA');anchor=[axis-head.width//2,head_bottom-head.height];headbounds=(xx>=axis-14)&(xx<axis+15)&(yy>=top-2)&(yy<head_bottom)
     if direction=='north':
      old_head=headbounds&(yy<head_bottom-2);rear_collar=(yy>=head_bottom-5)&((xx<axis-9)|(xx>axis+9));old_head&=~rear_collar
     else:
      # Skin, brown hair and goggles form the original skull; neutral grey collar
      # and backpack remain behind it. Fill only internal holes in that silhouette.
      warm=(rgb[:,:,0]>rgb[:,:,1]*1.025)&(rgb[:,:,0]>rgb[:,:,2]*1.035)
      old_head=binary_fill_holes(binary_closing(headbounds&warm&(a[:,:,3]>100)))&headbounds
     layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(anchor));ha=np.array(layer);identity=old_head|(ha[:,:,3]>60)
     out[old_head]=0;visible=ha[:,:,3]>60;out[visible]=ha[visible]
     yellow=(rgb[:,:,0]>rgb[:,:,2]*1.15)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65)
     if direction=='north':suit=(yy>=96)&(yy<141)
     else:
      # Department patches follow shoulder/backpack positions in the bow.
      # Central utility belt/food/cup pixels are excluded by the lateral mask.
      body_top=int(yy[(a[:,:,3]>180)&(xx>104)&(xx<151)].min())
      suit=(yy>=body_top+8)&(yy<head_bottom+12)&((xx<axis-10)|(xx>axis+10))
      suit|=(yy>=head_bottom)&(yy<head_bottom+16)&(xx>=axis-9)&(xx<=axis+9)
     marking=yellow&suit&(a[:,:,3]>0)&(~identity);gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8');out[marking,:3]=colour[marking];allowed=identity|marking;method='Source whole-body/utensils with fitted identity and upper suit markings'
   assert np.array_equal(a[~allowed],out[~allowed]);checks+=1
   # The bottom of the original body, utensils and boots remains unchanged.
   protected_from=190 if direction=='south' and h not in known and new_order[h] not in (9,) else 141
   assert np.array_equal(a[protected_from:],out[protected_from:]);checks+=1
   q=P/f'poses/{h[:20]}.png';q.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(q);mask=f'masks/{h[:20]}.png';(P/'masks').mkdir(exist_ok=True);Image.fromarray(allowed.astype('uint8')*255).save(P/mask)
   records[h]={'source':source.relative_to(R).as_posix(),'sourceHash':h,'output':q.relative_to(P).as_posix(),'outputHash':sha(q),'sourcePadding':list(offset),'allowedMask':mask,'headSource':head_source.relative_to(R).as_posix() if head_source else None,'headHash':sha(head_source) if head_source else None,'headPaste':anchor,'method':method,'protectedFromRow':protected_from,'newSourceIndex':new_order.get(h)};images[h]=Image.fromarray(out)
  files.append(records[h]['output'])
 state['frameFiles']=files;state['provenance']={'bodyReuse':'Selected James whole meal service poses, original clocks/events and indexed-return chronology','identity':'Krusher cardinal/rear heads and authored pitched South heads','deduplication':'Each identical source SHA256 transforms once; all action/return occurrences share its exact output'};result['states'].append(state)
(P/'bare-manifest.json').write_text(json.dumps(result,indent=2)+'\n');(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':list(records.values()),'sourceStates':{key:{'manifest':v['manifest'],'sha256':sha(R/v['manifest'].removeprefix('res://'))} for key,v in family.items()}},indent=2)+'\n')
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22);board=Image.new('RGB',(1500,1120),'#242c31');d=ImageDraw.Draw(board);d.text((15,10),'KRUSHER DOM / NEW MEAL SERVICE POSES / JAMES UTILITY BODY',font=font,fill='white')
for h,j in new_order.items():
 x=j%6*250;y=45+j//6*260;im=images[h];tile=im.resize((220,220),Image.Resampling.NEAREST);board.paste(tile,(x+5,y),tile);d.text((x+8,y+220),f'Source {j:02}',font=font,fill='#cadcde')
board.save(P/'new-poses-sheet.png');print(json.dumps({'states':len(result['states']),'references':sum(len(s['frameFiles']) for s in result['states']),'uniquePoses':len(records),'newPoses':len(new_order),'checks':checks,'errors':[]}))
