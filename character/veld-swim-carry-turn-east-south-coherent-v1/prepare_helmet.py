from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];O=R/'character/veld-swim-turn-east-south-coherent-v1'
assert not (H/'build_helmet.py').exists()
s=(O/'build_helmet.py').read_text(encoding='utf-8')
s=s.replace('from fit_material_trials import masks,curves','from build_bare import masks,curves')
s=s.replace("source=H/'helmet-source-v1.png'","source=R/'character/veld-swim-turn-east-south-coherent-v1/helmet-source-v1.png'")
s=s.replace("character/veld-water-east-coherent-v1/frames/helmet/swim-east/000.png","character/veld-swim-carry-east-coherent-v1/frames/helmet/swim-carry-east/000.png")
s=s.replace("character/veld-water-south-coherent-v1/frames/helmet/swim-south/000.png","character/veld-swim-carry-south-coherent-v1/frames/helmet/swim-carry-south/000.png")
s=s.replace("H/f'graded-trials/{i:03}.png'","H/f'frames/bare/swim-carry-turn-east-south/{i+1:03}.png'")
s=s.replace('swim-turn-','swim-carry-turn-')
# Preserve cargo pixels in front of the chin; components remain reviewed ordinary-turn sources.
s=s.replace('oa=np.array(out);protected=~erase;',"oa=np.array(out);Y,X=np.indices((256,256));fg=(ba[:,:,3]>200)&(np.ptp(ba[:,:,:3].astype(float),axis=2)<28)&(Y>=bfb[3])&(X>bfb[0]-10);oa[fg]=ba[fg];out=Image.fromarray(oa);protected=~erase;")
(H/'build_helmet.py').write_text(s,encoding='utf-8')
