"""Bind new pose studies to actual retained route-boundary source phases."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
CAP=R/'character/bill-floor-case-north-v1/flood-navigation-captures'
rows=json.loads((R/'output/bill-floor-case-flood-navigation-v1/records.json').read_text())['records']
meta=json.loads((R/'output/bill-flood-source-registration-v1/metadata.json').read_text())
times=[60,90,100,100,90,60]
def registered(row,gear):
 file=CAP/(row['name']+'-source.png');im=Image.open(file).convert('RGBA');sha=hashlib.sha256(im.tobytes()).hexdigest()
 matches=[m for m in meta[sha] if m['gear']==gear and m['key']==row['state']+'-'+row['direction']]
 assert matches
 profiles={(tuple(m['pivot']),m['standingHeight'],tuple(m['size'])) for m in matches};assert len(profiles)==1
 pivot,height,size=profiles.pop();assert height==148 and size==im.size
 pos=[round(160-pivot[0]),round(224-pivot[1])];out=Image.new('RGBA',(320,320));out.alpha_composite(im,pos)
 assert out.crop((pos[0],pos[1],pos[0]+im.width,pos[1]+im.height)).tobytes()==im.tobytes()
 return out,dict(capture=file.relative_to(R).as_posix(),captureSHA256=hashlib.sha256(file.read_bytes()).hexdigest(),decodedSHA256=sha,normalMatches=matches,record=row,position=pos)
def main():
 plans=[];sections=[]
 for label,gear,study in [('bare','','bill-land-water-east-v3'),('helmet','diving-helmet','bill-land-water-helmet-east-v1')]:
  group=sorted([x for x in rows if x['name'].startswith(label+'-') and x['name'].endswith('-candidate')],key=lambda x:x['tick'])
  boundaries=[(a,b) for a,b in zip(group,group[1:]) if a['medium']!=b['medium']];assert len(boundaries)==2
  for a,b in boundaries:
   enter=b['medium']=='flooded';name=label+('-enter' if enter else '-leave');key='land-swim-east' if enter else 'swim-land-east'
   assert a['direction']==b['direction']=='east'
   start,sa=registered(a,gear);end,sb=registered(b,gear)
   originals=[Image.open(R/f'character/{study}/frames/{key}/{i:03}.png').convert('RGBA') for i in range(6)]
   poses=[start]+originals[1:5]+[end]
   files=[]
   for i,im in enumerate(poses):
    file=P/f'frames/{name}/{i:03}.png';file.parent.mkdir(parents=True,exist_ok=True);im.save(file);files.append(dict(file=file.relative_to(P).as_posix(),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),seconds=times[i]/1000))
   poses[0].save(P/f'{name}.png',save_all=True,append_images=poses[1:],duration=times,loop=0,disposal=0,blend=0)
   with Image.open(P/f'{name}.png') as apng:
    assert apng.n_frames==6
    for i,im in enumerate(poses):apng.seek(i);assert apng.convert('RGBA').tobytes()==im.tobytes()
    assert sum(apng.seek(i) or apng.info['duration'] for i in range(6))==500
   board=Image.new('RGB',(1920,360),'#182932');d=ImageDraw.Draw(board)
   for i,im in enumerate(poses):board.paste(im,(i*320,25),im);d.text((i*320+4,5),('Actual last captured '+a['state'] if i==0 else 'Actual first captured '+b['state'] if i==5 else 'Authored interior '+str(i)),fill='white')
   board.save(P/f'{name}-board.png')
   seam=Image.new('RGB',(1280,360),'#182932');d=ImageDraw.Draw(seam)
   for i,(title,im) in enumerate([('Study original start',originals[0]),('Actual captured start',start),('Study original end',originals[-1]),('Actual captured end',end)]):seam.paste(im,(i*320,25),im);d.text((i*320+4,5),title,fill='white')
   seam.save(P/f'{name}-endpoint-review.png')
   plans.append(dict(id=name,gear=gear,rows=files,originalStudy=study,key=key,sourceBoundary=[sa,sb],timelineMs=500,APNGDecodeExact=True,endpointReplacementExact=True,interiorsUnchanged=True,root=[160,224],standingHeight=148,sourceStudyOnly=True))
   sections.append(f'<h2>{name}</h2><p>Captured ticks {a["tick"]} → {b["tick"]}; last/first 30Hz samples, not exact 60Hz handoff.</p><img src="{name}-endpoint-review.png"><img src="{name}-board.png"><img src="{name}.png">')
 (P/'phase-evidence.json').write_text(json.dumps(dict(plans=plans,normalSelected=False,nativeBridgePlayed=False,scope='Actual original route source samples bind entrance/exit phase audit. Authored interiors unchanged. New 500ms montage does not replay original world positions, elapsed route or prove collision/support; endpoint substitution is not gait admission.'),indent=2)+'\n',encoding='utf-8')
 (P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill phase-boundary audit</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Bill East — actual walking/swimming source-phase comparison</h1><p>Source-only audit. Four interiors plus exact last/first captured original route sources. A new 500ms montage, not a native replay. Separate bare/helmet walking clocks and terminal phase need staged runtime coordination. Collision, support, interruption and Continue pending.</p>'+''.join(sections),encoding='utf-8')
 print('Four captured-phase boundary plans; 24 exact APNG frames/500ms each; original endpoints and four interiors protected.')
if __name__=='__main__':main()
