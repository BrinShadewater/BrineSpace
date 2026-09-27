from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/room-risers-v4'
data=json.loads((PACK/'panel-decorations.json').read_text())
paths={v[k] for v in data['rooms'].values() for k in ['left','right','center','ocean_left','ocean_right','ocean_center']}
paths.update('res://'+str(p.relative_to(ROOT)).replace('\\','/') for p in (PACK/'panel-expansion/masters').glob('*.png'))
sizes={
'analog_clock':([24,24],[28,28]),'digital_clock':([49,21],[55,24]),
'com_handset':([19,28],[23,37]),'com_panel':([28,27],[36,35]),
'emergency_box':([26,28],[34,38]),'alarm_beacon':([17,27],[21,34]),
'key_rack':([43,27],[51,33]),'tool_rack':([43,28],[55,38]),
'pressure_gauge':([35,28],[44,38]),'picture_botanical':([19,28],[28,43]),
'picture_ocean':([41,28],[53,38]),'poster_diver':([16,28],[25,46]),
'poster_marine':([16,28],[24,46]),'notice_board':([49,28],[65,39]),
'wall_calendar':([22,28],[28,38]),'oxygen_masks':([44,28],[48,36]),
'wall_planter':([29,28],[43,45]),'vent_fan':([26,28],[34,36]),
'station_map':([46,28],[63,41]),'sample_display':([53,28],[63,36]),
'reinforced_access_panel':([57,28],[65,33]),'status_display_wide':([62,26],[66,28]),
'monitor_single':([25,28],[34,40]),'monitor_dual':([45,28],[58,37]),
'ocean_window_panoramic':([66,28],[75,30]),'ocean_window_medium':([53,28],[67,36]),
'ocean_window_tall':([17,28],[31,54])}
profiles={}
for path in sorted(paths):
 p=ROOT/path.removeprefix('res://'); im=Image.open(p).convert('RGBA'); alpha=np.array(im.getchannel('A'))
 mask=alpha>=128
 if any(folder in path for folder in ['/panel-expansion/','/square-fittings/','/polish-v1/']):
  labels,n=ndimage.label(mask); counts=np.bincount(labels.ravel());counts[0]=0; mask=labels==counts.argmax()
 yy,xx=np.nonzero(mask); x,y,right,bottom=int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)
 w,h=right-x,bottom-y
 anchor=[round(float(np.clip(((xx-x).mean()+.5)/w,.35,.65)),4),round(float(np.clip(((yy-y).mean()+.5)/h,.35,.65)),4)]
 side,center=([32,28],[66,60]) if p.stem.startswith('square_') else sizes.get(p.stem,([66,28],[72,35]))
 profiles[path]={'region':[x,y,w,h],'anchor':anchor,'side_size':side,'center_size':center,'source_size':list(im.size),'source_pixels_per_world_at_side_height':round(h/side[1],2),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'style_review':'candidate_new' if any(folder in path for folder in ['/panel-expansion/','/square-fittings/','/polish-v1/']) else 'retained_existing','perspective':'front-facing north-wall fitting; never rotate into floor space'}
(PACK/'fitting-profiles.json').write_text(json.dumps(profiles,indent=2)+'\n',encoding='utf-8')
print(f'{len(profiles)} fittings registered with visible bounds, optical anchors, per-slot size limits and source hashes')
