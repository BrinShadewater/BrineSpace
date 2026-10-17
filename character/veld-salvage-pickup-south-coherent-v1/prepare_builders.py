"""One-time contract adaptation; source artwork is independently authored south."""
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parents[1]; E=R/'character/veld-salvage-pickup-east-coherent-v1'
assert not (H/'build.py').exists(), 'Do not overwrite reviewed south recipes'
s=(E/'build.py').read_text(encoding='utf-8').replace('east','south')
s=s.replace('head=(y<fb[3])&(x>fb[0]-h*1.15)&(x<fb[2]+h*.12);body=(~head)&(x<fb[2])&(a[:,:,3]>200)', 'head=(y>fb[1]-h*2.5)&(y<fb[3])&(x>(fb[0]+fb[2])*.5-h*1.5)&(x<(fb[0]+fb[2])*.5+h*1.5);body=(~head)&(y<fb[3])&(a[:,:,3]>200)')
start=s.index('masterpath='); end=s.index("for role in",start)
s=s[:start]+"masterpath=R/'character/veld-water-master-audit-v1/fitted-swim-south-head.png';head=Image.open(masterpath).convert('RGBA');ha=np.array(head);v=ha[:,:,:3].astype(float);skin=(ha[:,:,3]>150)&(v[:,:,0]>90)&(v[:,:,0]>v[:,:,1]*1.18)&(v[:,:,1]>v[:,:,2]*1.1);hl,hn=label(skin);hz=np.bincount(hl.ravel());hfb=box(hl==1+np.argmax(hz[1:]));hp=(111,156-(hfb[3]-1));clear=(113,hp[1]-3,143,158)\n"+s[end:]
s=s.replace('raw.shape[0]/3','raw.shape[0]/2').replace('round(159-fb[2]*scale),round(127-fb[3]*scale)','round(128-(fb[0]+fb[2])*.5*scale),round(156-fb[3]*scale)')
s=s.replace('helmet.alpha_composite(head,hp)\n', "helmet.alpha_composite(head,hp)\n  before=np.array(bare);after=np.array(helmet);y,x=np.indices((256,256));v=before[:,:,:3].astype(float);foreground=(before[:,:,3]>200)&(np.ptp(v,axis=2)<25)&(y>=154)&(y<166)&(x>=111)&(x<146);after[foreground]=before[foreground];helmet=Image.fromarray(after)\n")
(H/'build.py').write_text(s,encoding='utf-8')
for name in ['validate.py','check_native.py']:
    (H/name).write_text((E/name).read_text(encoding='utf-8').replace('east','south'),encoding='utf-8')
fixture=R/'tools/review_veld_salvage_pickup_east_coherent_v1.gd'
target=R/'tools/review_veld_salvage_pickup_south_coherent_v1.gd'
assert not target.exists()
target.write_text(fixture.read_text(encoding='utf-8').replace('east','south'),encoding='utf-8')
# Native fixture UID is supplied by Godot on first run; keep it paired.
