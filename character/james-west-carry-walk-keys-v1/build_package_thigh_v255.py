from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_knee_v240.py').read_text(encoding='utf-8').replace('knee-material-phase30-v240','thigh-construction-phase12-v255').replace('(40,40)','(96,96)').replace('knee-detail-review.png','thigh-detail-review.png').replace('Original restored knee','Original diagonal thigh').replace('[29,30,31,32]','[11,12,13,14]').replace('if phase==30','if phase==12')
s=s.replace("mask=np.zeros((256,256),bool);x0,y0,x1,y1=d['admissionRectangle'];mask[y0:y1,x0:x1]=True;mask&=np.array(opaque)>0", "admission=Image.new('L',(256,256));ImageDraw.Draw(admission).polygon([tuple(xy) for xy in d['admissionPolygon']],fill=255);mask=np.array(admission)>0;mask&=np.array(opaque)>0")
s=s.replace('outsideRectangleExact=True','outsidePolygonExact=True')
(p/'package_thigh_v255.py').write_text(s,encoding='utf-8')
