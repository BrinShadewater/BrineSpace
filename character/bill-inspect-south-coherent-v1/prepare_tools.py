from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;N=P.parent/'bill-inspect-north-coherent-v1'
for name in ['build.py','verify.py','build_review.py']:
    text=(N/name).read_text().replace('north','south')
    if name=='build.py':
        text=text.replace("B=P.parent/'bill-seated-south-coherent-v1'","B=P.parent/'bill-seated-loops-south-v1'")
        text=text.replace("module.prepare(source,heads,6,cfg['density'])","module.prepare(source,heads,cfg['density'])")
        text=text.replace('dx=17-head.width/2;dy=6-head.height/2','dx=18-head.width/2;dy=8-head.height/2').replace('hy+31','hy+35')
        text=text.replace("'excludedSourcePoses':[3,4,5]","'excludedSourcePoses':sorted(set(range(6))-set(cfg['sourcePoses']))")
        text=text.replace('three independent upright poses ping-pong;slot5 copies exact slot0;no per-pose scaling','explicit authored source sequence;slot5 copies exact slot0;no per-pose scaling')
    if name=='verify.py':
        text=text.replace("<=2,'Upright crown range within two native pixels'","<=3,'Upright crown range within three native pixels'")
        text=text.replace("r['sourcePoses']==[0,1,2,1,0] and r['excludedSourcePoses']==[3,4,5],'Three authored upright poses; compressed bottom poses excluded'","r['sourcePoses']==cfg['sourcePoses'] and r['excludedSourcePoses']==sorted(set(range(6))-set(cfg['sourcePoses'])),'Explicit authored source sequence and exclusions'")
        text=text.replace("==3,'Three distinct authored inspection poses'",">=3,'At least three distinct authored inspection poses'")
    if name=='build_review.py':
        text=text.replace('Rear standing inspection. The reader and working gloves are naturally occluded in front of the torso; bent elbows remain connected.','Front standing inspection. Two connected gloves support a small diagnostic reader below the chest panels.').replace('native rear helmet','native front helmet')
    (P/name).write_text(text)
test=(ROOT/'tests/test_bill_inspect_north_candidates.gd').read_text().replace('north','south').replace('NORTH','SOUTH')
(ROOT/'tests/test_bill_inspect_south_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_inspect_south_candidates.gd.uid').write_text('uid://f7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_inspect_north_candidate_validation.py').read_text().replace('north','south').replace('NORTH','SOUTH')
(ROOT/'tools/run_bill_inspect_south_candidate_validation.py').write_text(runner)
print('Prepared south grade/native helmet and isolated source-player fixture')
