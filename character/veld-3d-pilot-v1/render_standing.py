"""Standing render study from preserved GLB. Does not edit source mesh/textures."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial.transform import Rotation

ROOT=Path(__file__).resolve().parent
code=(ROOT/'render_walk.py').read_text().split('assert np.max')[0]
# Reuse tested accessor/skinning/raster functions without running walk exports.
ns={'__file__':str(ROOT/'render_walk.py')};exec(code,ns)
OUT=ROOT/'standing-review';OUT.mkdir(exist_ok=True)
# Rotate upper arms in WORLD space while leaving their rest translation intact.
posecode=code[code.index('def pose('):code.index('def render(')]
posecode=posecode.replace("cache[i]=world(parents[i])@m if i in parents else m", """parent=world(parents[i]) if i in parents else np.eye(4)
   if n.get('name') in ['mixamorig:LeftArm','mixamorig:RightArm']:
    sign=-1 if n['name']=='mixamorig:LeftArm' else 1
    delta=Rotation.from_euler('z',sign*76,degrees=True).as_matrix()
    m[:3,:3]=np.linalg.inv(parent[:3,:3])@delta@parent[:3,:3]@m[:3,:3]
   cache[i]=parent@m""")
exec(posecode,ns);v,_=ns['pose']()
assert np.isfinite(v).all()
raw_render=ns['render']
# Four-times raster resolution and a filtered texture mip avoid point-sampling sparkle.
rc=code[code.index('def render('):]
rc=rc.replace('def render(', 'def filtered_render(').replace('xy=np.column_stack(', 'xy=4*np.column_stack(').replace('(184,184)', '(736,736)').replace('(184,184,4)', '(736,736,4)').replace('[183,183]', '[735,735]')
rc=rc.replace('return Image.fromarray(rgb)', 'return Image.fromarray(rgb).resize((184,184),Image.Resampling.LANCZOS)')
exec(rc,ns)
original_texture=ns['tex'].copy()
filtered_texture=np.array(Image.fromarray(original_texture).resize((512,512),Image.Resampling.LANCZOS))
manifest=json.loads((ROOT.parent/'veld-animation-pilot-v12/manifest.json').read_text())
frames={s['id']:ROOT.parent/'veld-animation-pilot-v12'/s['frameFiles'][0] for s in manifest['states']}
panel=Image.new('RGB',(1120,960),'#192127');dr=ImageDraw.Draw(panel)
dr.text((25,15),'VELD / standing art comparison / original 2D pilot versus actual 3D renders',fill='white')
labels=['2D pilot v12','3D point-sampled','3D filtered','3D filtered + proportions']
metrics={}
for row,(direction,angle) in enumerate([('south',0),('east',np.pi/2)]):
 old=Image.open(frames['idle-'+direction]).convert('RGBA')
 ns['tex']=original_texture;a=raw_render(v,angle)
 # Camera elevation 6 degrees: use world-space rotation equivalent to pitched view.
 c,s=np.cos(angle),np.sin(angle);yaw=np.array([[c,0,s],[0,1,0],[-s,0,c]])
 pitch=Rotation.from_euler('x',6,degrees=True).as_matrix()
 vv=v.copy();vv=(vv@yaw.T)@pitch.T
 ns['tex']=filtered_texture;b=ns['filtered_render'](vv,0)
 fuller=v.copy();strength=np.clip((1.5-fuller[:,1])/.22,0,1)
 fuller[:,0]*=1+.14*strength;fuller[:,2]*=1+.25*strength
 head=np.clip((fuller[:,1]-1.43)/.10,0,1)
 fuller[:,0]*=1+.25*head;fuller[:,2]*=1+.20*head
 fuller[:,1]+=head*(fuller[:,1]-1.48)*.10
 fuller=(fuller@yaw.T)@pitch.T;cim=ns['filtered_render'](fuller,0)
 images=[old,a,b,cim]
 for col,im in enumerate(images):
  # One static scale calibration per view for this standing comparison only.
  box=im.getbbox();crop=im.crop(box);scale=148/crop.height
  crop=crop.resize((round(crop.width*scale),148),Image.Resampling.LANCZOS)
  calibrated=Image.new('RGBA',(184,184));calibrated.alpha_composite(crop,((184-crop.width)//2,172-148))
  calibrated.save(OUT/f'{direction}-{col}.png')
  metrics[f'{direction}-{col}']={'uncalibrated_bounds':box,'standing_width':crop.width,'standing_height':148}
  x=col*280+30;y=row*460+55
  dr.text((x,y),labels[col]+' / '+direction,fill='white')
  large=calibrated.resize((368,368),Image.Resampling.NEAREST)
  # Crop empty canvas margins for display, retain calibrated files unchanged.
  display=large.crop((50,30,318,352));panel.paste(display,(col*280+6,y+22),display)
  small=calibrated.resize((56,56),Image.Resampling.LANCZOS);panel.paste(small,(col*280+112,y+360),small)
dr.text((25,938),'Large views 2x. Small figures ~45px. Static pose only; no runtime replacement.',fill='white')
panel.save(OUT/'standing-comparison.png')
(OUT/'settings.json').write_text(json.dumps({'arm_lowering_degrees':76,'camera_elevation_degrees':6,'supersampling':4,'texture_mip':512,'suit_width_multiplier':1.14,'suit_depth_multiplier':1.25,'head_width_multiplier':1.25,'head_depth_multiplier':1.20,'head_height_multiplier':1.10,'notes':'Existing baked colour/shading retained. Fuller-suit variant is a reversible vertex transform, not source mesh edit. Each static comparison calibrated to 148px height; not per-frame animation scaling.','measurements':metrics},indent=2))
print('Saved front/side comparison and eight calibrated sprites.')
