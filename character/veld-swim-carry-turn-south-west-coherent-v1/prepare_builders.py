"""One-time contract adaptation; all source poses independently authored."""
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];E=R/'character/veld-swim-carry-turn-east-south-coherent-v1';O=R/'character/veld-swim-turn-south-west-coherent-v1'
assert not (H/'build_bare.py').exists()
s=(E/'build_bare.py').read_text(encoding='utf-8').replace('east-south','south-west').replace('south-east','west-south')
start=s.index(' if i==2:');end=s.index(' b=box(ll==k)',start)
s=s[:start]+s[end:]
s=s.replace("for d in ['east','south']", "for d in ['south','west']").replace('scale=.24;','scale=.21;')
s=s.replace('target=np.array([159,127])*(1-t)+np.array([128,156])*t','target=np.array(anchors[0])*(1-t)+np.array(anchors[1])*t')
s=s.replace("scale=.21;frames=", "anchors=[]\nfor p in refs:\n _,fb,_=masks(np.array(Image.open(p).convert('RGBA')));anchors.append([(fb[0]+fb[2])*.5,fb[3]])\nscale=.21;frames=")
s=s.replace('cargo east/south','cargo south/west')
(H/'build_bare.py').write_text(s,encoding='utf-8')
s=(O/'build_helmet.py').read_text(encoding='utf-8')
s=s.replace('from material import masks','from build_bare import masks,curves').replace('H=Path(__file__).resolve().parent;curves=json.loads((H/"material-fit-v1.json").read_text())["curves"]','H=Path(__file__).resolve().parent')
s=s.replace("source=H/'helmet-source-v2.png'", "source=R/'character/veld-swim-turn-south-west-coherent-v1/helmet-source-v2.png'")
s=s.replace("H/'helmet-source-v1.png'", "R/'character/veld-swim-turn-south-west-coherent-v1/helmet-source-v1.png'")
s=s.replace("H/f'graded-trials/{i:03}.png'", "H/f'frames/bare/swim-carry-turn-south-west/{i+1:03}.png'")
for d in ['south','west']:
 s=s.replace(f'character/veld-water-{d}-coherent-v1/frames/helmet/swim-{d}/000.png',f'character/veld-swim-carry-{d}-coherent-v1/frames/helmet/swim-carry-{d}/000.png')
s=s.replace('swim-turn-','swim-carry-turn-')
# Global state-key adaptation also touched source-family paths: restore exact authority.
s=s.replace('character/veld-swim-carry-turn-south-west-coherent-v1/helmet-source','character/veld-swim-turn-south-west-coherent-v1/helmet-source')
s=s.replace('((bv[:,:,0]>bv[:,:,1]*1.1)|(bv[:,:,1]>bv[:,:,2]*1.25))','((bv[:,:,0]>bv[:,:,1]*1.25)&(bv[:,:,1]>bv[:,:,2]*1.15))')
s=s.replace('oa=np.array(out);protected=~erase;',"oa=np.array(out);Y,X=np.indices((256,256));fg=(ba[:,:,3]>200)&(np.ptp(ba[:,:,:3].astype(float),axis=2)<28)&(Y>=bfb[3])&(X>bfb[0]-10);oa[fg]=ba[fg];out=Image.fromarray(oa);protected=~erase;")
s=s.replace("(H/name).read_bytes()", "(R/'character/veld-swim-turn-south-west-coherent-v1'/name).read_bytes()")
(H/'build_helmet.py').write_text(s,encoding='utf-8')
for name in ['validate.py','check_native.py']:
 s=(E/name).read_text(encoding='utf-8').replace('east-south','south-west').replace('south-east','west-south').replace('east_south','south_west').replace('east/south','south/west')
 (H/name).write_text(s,encoding='utf-8')
target=R/'tools/review_veld_swim_carry_turn_south_west_v1.gd';assert not target.exists()
s=(R/'tools/review_veld_swim_carry_turn_east_south_v1.gd').read_text(encoding='utf-8').replace('east-south','south-west').replace('east_south','south_west').replace('E/S','S/W')
target.write_text(s,encoding='utf-8')
