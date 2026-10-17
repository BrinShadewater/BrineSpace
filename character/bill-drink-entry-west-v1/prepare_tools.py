from pathlib import Path
import json,numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;E=P.parent/'bill-drink-entry-east-v1'
a=np.array(Image.open(P/'sources/pickup-size-v3.png'));labs,_=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(labs==k)[0].min()//512,np.where(labs==k)[1].min()))
boxes=[[int(np.where(labs==k)[1].min()),int(np.where(labs==k)[0].min()),int(np.where(labs==k)[1].max()),int(np.where(labs==k)[0].max())] for k in ids]
heads=[[255,boxes[0][1]],[765,boxes[1][1]],[1273,boxes[2][1]],[255,boxes[3][1]],[765,boxes[4][1]],[1273,boxes[5][1]]]
cfg={'sources':{'primary':{'source':'sources/pickup-size-v3.png','generation':'exec-578ba632-4c56-4c26-be0a-77fddf716933','heads':heads,'sourceHeights':[b[3]-b[1]+1 for b in boxes],'count':6,'density':1.08,'fixedRuler':[.28,.313]}},'sequence':[['primary',i] for i in range(5)],'durations':[60,80,100,100,100,80,60],'excludedPrimaryPoses':[5],'sourceCorrections':['distinct short reach v2','equal standing row heights v3']}
(P/'source-rulers.json').write_text(json.dumps(cfg,indent=2)+'\n',encoding='utf-8')
for name in ['build.py','verify.py','build_preview.py']:
 s=(E/name).read_text(encoding='utf-8').replace('east','west').replace('x>np.median(x)','x<np.median(x)').replace('bx>np.median(bx)','bx<np.median(bx)')
 if name=='build.py':
  s=s.replace('from scipy.ndimage import binary_dilation','from scipy.ndimage import binary_dilation\nfrom grade_materials import apply')
  s=s.replace("prepared={key:module.prepare(P/s['source'],s['heads'],s['count'],s['density']) for key,s in cfg['sources'].items()}","prepared={key:apply(module.prepare(P/s['source'],s['heads'],s['count'],s['density']),s,module.IDLE) for key,s in cfg['sources'].items()}")
 if name=='build_preview.py':s=s.replace(".write_text(html.replace('DATA',json.dumps(states)))",".write_text(html.replace('DATA',json.dumps(states)),encoding='utf-8')")
 (P/name).write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_drink_entry_east_candidates.gd').read_text(encoding='utf-8').replace('east','west').replace('BILL DRINK ENTRY EAST','BILL DRINK ENTRY WEST')
s=s.replace('func run():','func run():\n\tprint("BILL DRINK ENTRY WEST profile: "+OS.get_user_data_dir())')
(ROOT/'tests/test_bill_drink_entry_west_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_drink_entry_west_candidates.gd.uid').write_text('uid://j8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_drink_entry_east_candidate_validation.py').read_text(encoding='utf-8').replace('east','west').replace('BILL DRINK ENTRY EAST','BILL DRINK ENTRY WEST')
(ROOT/'tools/run_bill_drink_entry_west_candidate_validation.py').write_text(s,encoding='utf-8')
print(json.dumps({'boxes':boxes,'heights':cfg['sources']['primary']['sourceHeights']}))
