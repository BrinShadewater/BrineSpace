from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw

P=Path(__file__).resolve().parent;R=P.parents[2]
V5=P.parent/'west-carry-master-match-v5'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Manually reviewed heel/sole windows on boot-contact-detail.png. Restrict to
# the supporting boot; a full lower-body box would mix the raised swing foot.
boxes=[(80,219,130,226),(90,219,135,227),(115,219,152,227),(80,219,122,227),(90,219,131,227),(125,219,158,227)]
stride=.07351351351351351;density=148.;height_fraction=.17
root_native_per_pose=stride*density/height_fraction/6
records=[];bindings={};ims=[]
for i,box in enumerate(boxes):
 p=V5/f'frames/bare/{i:03}.png';im=Image.open(p).convert('RGBA');ims.append(im);bindings[p.relative_to(R).as_posix()]=sha(p)
 x0,y0,x1,y1=box;a=np.array(im);y,x=np.where(a[y0:y1,x0:x1,3]>128);assert len(x)
 heel=float(x.max()+x0);floor=int(y.max()+y0)
 records.append({'slot':i,'supportLeg':'near' if i<3 else 'far','reviewedSoleWindow':box,'heelRightContourX':heel,'floorAlpha128':floor,'rootNativeX':-i*root_native_per_pose,'worldHeelNativeX':heel-i*root_native_per_pose})
halves=[]
for begin in [0,3]:
 rows=records[begin:begin+3];xs=[r['worldHeelNativeX'] for r in rows]
 halves.append({'supportLeg':rows[0]['supportLeg'],'observedSlots':[begin,begin+1,begin+2],'worldHeelContourSpreadNative':max(xs)-min(xs),'scope':'Opaque right sole contour proxy, not tracked anatomical landmark or full stance acceptance'})
board=Image.new('RGB',(1680,680),'#202a30');d=ImageDraw.Draw(board)
for i,im in enumerate(ims):
 x=(i%3)*560;y=(i//3)*340;shift=-root_native_per_pose*(i%3)
 # Fixed world ruler, runtime-equivalent translation. No change to source art.
 zoom=2;render=im.resize((512,512),Image.Resampling.NEAREST)
 px=round(x+100+shift*zoom);py=y-160;board.paste(render,(px,py),render)
 d.line((x,y+288,x+559,y+288),fill='#728792')
 heel=records[i]['worldHeelNativeX']+root_native_per_pose*(3 if i>=3 else 0)
 xx=round(x+100+heel*zoom);d.line((xx,y+250,xx,y+302),fill='#ffb954')
 baseline=records[0 if i<3 else 3]['heelRightContourX'];bx=round(x+100+baseline*zoom)
 d.line((bx,y+225,bx,y+310),fill='#60bcc4')
 d.text((x+6,y+8),f'Pose {i}, root shift {shift:.2f}px; support {records[i]["supportLeg"]}',fill='white')
 d.text((x+6,y+318),'Cyan: initial sole heel. Gold: current heel contour.',fill='white')
board.save(P/'world-contact-comparison.png')
report={'method':'Consumer scale cell_size*0.17/standingHeight; root advances one sixth declared stride between equal holds. Supporting sole windows visually reviewed.','strideDistanceCells':stride,'nativeRootTravelPerCycle':stride*density/height_fraction,'nativeRootTravelPerPose':root_native_per_pose,'records':records,'halfStanceDiagnostics':halves,'noSourceArtChanged':True,'physicalAcceptance':False,'limitations':['Discrete six-pose holds produce intra-hold sliding','Sole contour changes with articulation; this is a proxy, not anatomical tracking','Not native NPC route/arrival or fully observed stance/loop'],'bindings':bindings}
(P/'CONTACT_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps({'rootNativePerPose':root_native_per_pose,'heels':[r['heelRightContourX'] for r in records],'stanceDiagnostics':halves}))
