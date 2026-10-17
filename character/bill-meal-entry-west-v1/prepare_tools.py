from pathlib import Path
import json,numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;E=P.parent/'bill-meal-entry-east-v1'
a=np.array(Image.open(P/'sources/pickup-v1.png'));labs,_=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(labs==k)[0].min()//512,np.where(labs==k)[1].min()))
boxes=[[int(np.where(labs==k)[1].min()),int(np.where(labs==k)[0].min()),int(np.where(labs==k)[1].max()),int(np.where(labs==k)[0].max())] for k in ids]
heads=[[328,boxes[0][1]],[779,boxes[1][1]],[1224,boxes[2][1]],[328,boxes[3][1]],[779,boxes[4][1]],[1224,boxes[5][1]]]
cfg={'sources':{'primary':{'source':'sources/pickup-v1.png','generation':'exec-d8af5a0e-44fd-4973-8cbe-3bc1f07e8b97','heads':heads,'sourceHeights':[b[3]-b[1]+1 for b in boxes],'count':6,'density':1.0,'fixedRuler':[.29,.332]}},'sequence':[['primary',i] for i in range(5)],'durations':[60,80,100,100,100,80,60],'excludedPrimaryPoses':[5]}
(P/'source-rulers.json').write_text(json.dumps(cfg,indent=2)+'\n',encoding='utf-8')
for name in ['build.py','verify.py','build_preview.py']:
 s=(E/name).read_text(encoding='utf-8').replace('east','west').replace('x>np.median(x)','x<np.median(x)').replace('bx>np.median(bx)','bx<np.median(bx)')
 if name=='build_preview.py':s=s.replace(".write_text(html.replace('DATA',json.dumps(states)))",".write_text(html.replace('DATA',json.dumps(states)),encoding='utf-8')")
 (P/name).write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_meal_entry_east_candidates.gd').read_text(encoding='utf-8').replace('east','west').replace('BILL MEAL ENTRY EAST','BILL MEAL ENTRY WEST')
(ROOT/'tests/test_bill_meal_entry_west_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_meal_entry_west_candidates.gd.uid').write_text('uid://i8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_meal_entry_east_candidate_validation.py').read_text(encoding='utf-8').replace('east','west').replace('BILL MEAL ENTRY EAST','BILL MEAL ENTRY WEST')
(ROOT/'tools/run_bill_meal_entry_west_candidate_validation.py').write_text(s,encoding='utf-8')
print(json.dumps({'boxes':boxes,'heights':cfg['sources']['primary']['sourceHeights']}))
