from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;E=P.parent/'bill-drink-east-coherent-v1'
a=np.array(Image.open(P/'sources/drink-v1.png'));labs,_=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(labs==k)[0].min()//512,np.where(labs==k)[1].min()))
boxes=[[int(np.where(labs==k)[1].min()),int(np.where(labs==k)[0].min()),int(np.where(labs==k)[1].max()),int(np.where(labs==k)[0].max())] for k in ids]
heads=[[353,boxes[0][1]],[771,boxes[1][1]],[1187,boxes[2][1]],[353,boxes[3][1]],[771,boxes[4][1]],[1187,boxes[5][1]]]
cfg={'source':'sources/drink-v1.png','generation':'exec-72c69b7d-af88-488c-bb02-67d3589de1f4','heads':heads,'sourceHeights':[b[3]-b[1]+1 for b in boxes],'fixedRuler':[.29,.3395],'density':.98,'sequence':[0,1,2,3,4,5,0],'durations':[140,120,140,180,140,120,120]}
(P/'source-rulers.json').write_text(json.dumps(cfg,indent=2)+'\n',encoding='utf-8')
s=(E/'build.py').read_text(encoding='utf-8').replace('east','west').replace('x>np.median(x)','x<np.median(x)').replace('bx>np.median(bx)','bx<np.median(bx)')
(P/'build.py').write_text(s,encoding='utf-8')
(P/'verify.py').write_text((E/'verify.py').read_text(encoding='utf-8').replace('east','west'),encoding='utf-8')
(P/'index.html').write_text((E/'index.html').read_text(encoding='utf-8').replace('east','west'),encoding='utf-8')
s=(ROOT/'tests/test_bill_drink_east_candidates.gd').read_text(encoding='utf-8').replace('east','west').replace('BILL DRINK EAST','BILL DRINK WEST')
(ROOT/'tests/test_bill_drink_west_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_drink_west_candidates.gd.uid').write_text('uid://h8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_drink_east_candidate_validation.py').read_text(encoding='utf-8').replace('east','west').replace('BILL DRINK EAST','BILL DRINK WEST')
(ROOT/'tools/run_bill_drink_west_candidate_validation.py').write_text(s,encoding='utf-8')
print(json.dumps({'boxes':boxes,'heights':cfg['sourceHeights']}))
