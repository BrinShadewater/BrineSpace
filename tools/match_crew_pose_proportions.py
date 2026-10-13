"""Conservative fixed horizontal proportion trials; retain vertical gait and timing."""
from pathlib import Path
import json, re
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates

SRC=Path('character/crew-idle-size-match-v1')
OUT=Path('character/crew-pose-match-v1'); OUT.mkdir(exist_ok=True)
# Head / shoulder / waist widths. Deliberately smaller than silhouette ratios:
# arm swing and equipment are not anatomical width measurements.
SETTINGS={
 'bill': {'south':(1,1,1.025),'east':(.94,1,1),'north':(.95,1.035,1.025),'west':(.91,1,1)},
 'veld': {'south':(1,.985,.97),'east':(1.035,1.05,1.04),'north':(1,1,.975),'west':(1,1.02,1.025)},
 'branforth': {'south':(1,1,1),'east':(.97,1.06,1.06),'north':(1,1,1),'west':(.98,1.06,1.06)}
}
sheet=Image.new('RGB',(1104,880),'#303b40'); draw=ImageDraw.Draw(sheet)
reports={}; tracks=[]
yy,xx=np.indices((184,184),dtype=float)
for col,who in enumerate(SETTINGS):
 m=json.loads((SRC/who/'manifest.json').read_text())
 ir=Path('character/crew-idle-match-v1')/who
 im=json.loads((ir/'manifest.json').read_text())
 for row,d in enumerate(['south','east','north','west']):
  s=next(s for s in m['states'] if s['id']=='walk-'+d)
  idle=next(s for s in im['states'] if s['id']=='idle-'+d)
  factors=SETTINGS[who][d]; files=[]; clipped=0
  for n,f in enumerate(s['frameFiles']):
   a=np.array(Image.open(SRC/who/f).convert('RGBA'))
   top=int(np.where(a[:,:,3]>127)[0].min()); dy=yy-top
   # Follow only the crown translation; coefficients never vary by frame.
   cx=float(np.median(xx[(a[:,:,3]>127)&(dy<10)]))
   sc=np.interp(dy,[0,16,27,38,51,65,85,100],[factors[0],factors[0],1,factors[1],factors[1],factors[2],1,1])
   center=np.where(dy<27,cx,92.)
   sx=center+(xx-center)/sc
   if factors==(1,1,1): b=a.copy()
   else:
    v=a.astype(float)/255;v[:,:,:3]*=v[:,:,3:4]
    b=np.stack([map_coordinates(v[:,:,k],[yy,sx],order=1,mode='constant') for k in range(4)],axis=2)
    alpha=b[:,:,3:4];b[:,:,:3]=np.divide(b[:,:,:3],alpha,out=np.zeros_like(b[:,:,:3]),where=alpha>0)
    b=np.clip(np.rint(b*255),0,255).astype('uint8');b[dy>=85]=a[dy>=85]
   assert np.array_equal(a[dy>=85],b[dy>=85])
   clipped+=int(np.any(b[[0,-1],:,3]>127) or np.any(b[:,[0,-1],3]>127))
   rel=f'frames/walk-{d}/{n:03}.png';dest=OUT/who/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);files.append(rel)
   if n==0:
    ii=Image.open(ir/idle['frameFiles'][0]).convert('RGBA');bi=Image.fromarray(b)
    sheet.paste(ii,(col*368,row*220+25),ii);sheet.paste(bi,(col*368+184,row*220+25),bi)
    draw.text((col*368+5,row*220+3),f'{who} {d}: idle / proportion trial',fill='white')
  old=s['provenance'];s['frameFiles']=files;s['provenance']={'source':str(SRC/who),'previous':old,'horizontalProportions':factors,'verticalCoordinatesUnchanged':True}
  reports[f'{who}-{d}']={'frames':len(files),'headShoulderWaistWidthFactors':factors,'clippedFrames':clipped,'lowerLegPixelsExact':True,'timingUnchanged':True}
  tracks.append(dict(label=who.title()+' '+d,row=row,col=col,idle='../crew-idle-match-v1/'+who+'/'+idle['frameFiles'][0],idleFiles=['../crew-idle-match-v1/'+who+'/'+f for f in idle['frameFiles']],idleDurations=idle['frameDurationsMs'],files=[who+'/'+f for f in files],durations=s['frameDurationsMs']))
 (OUT/who/'manifest.json').write_text(json.dumps(m,indent=2))
sheet.save(OUT/'contact.png');(OUT/'validation.json').write_text(json.dumps(reports,indent=2))
html=(SRC/'index.html').read_text();html=re.sub(r'const tracks=.*?;let ready=',lambda _: 'const tracks='+json.dumps(tracks)+';let ready=',html)
html=re.sub(r'<title>.*?</title>','<title>Crew pose proportion matching</title>',html)
html=html.replace('Idle size and Bill skin matching','Crew pose proportion matching')
html=re.sub(r'<p>.*?</p>','<p>Idle left; proportion trial right. Conservative head and torso width adjustments, with unchanged vertical motion and timing. Preview only.</p>',html,count=1)
(OUT/'index.html').write_text(html)
print(json.dumps({'clips':len(reports),'frames':sum(r['frames'] for r in reports.values()),'clipped':sum(r['clippedFrames'] for r in reports.values()),'runtimeChanged':False}))
