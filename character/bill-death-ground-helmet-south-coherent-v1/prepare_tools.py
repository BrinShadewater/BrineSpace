from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];N=P.parent/'bill-death-ground-helmet-north-coherent-v1'
cfg={'generation':'exec-cad07484-a967-44cd-a49a-4533e1a6d26e','helmetRuler':[.30,.31],'sourceBoxes':[[210,56,334,194],[708,94,828,229],[1196,140,1309,246],[210,587,334,699],[710,598,827,694],[1202,599,1320,695]],'sourceNecks':[[766,227],[1255,241],[266,699],[768,693],[1261,697]]}
s=(N/'build.py').read_text(encoding='utf-8').replace('north','south').replace('rear','front').replace('prone','supine')
s='\n'.join('cfg='+repr(cfg) if line.startswith('cfg=') else line for line in s.splitlines())+'\n'
s=s.replace("idle=DONOR/", "ref_skin=(ref[:,:,3]>180)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2])&(rgb.mean(2)>65);first_skin=(first[:,:,3]>180)&(fr[:,:,0]>1.12*fr[:,:,1])&(fr[:,:,1]>1.14*fr[:,:,2])&(fr.mean(2)>65);skin_gain=np.median(rgb[ref_skin],axis=0)/np.median(fr[first_skin],axis=0)\n idle=DONOR/")
s=s.replace("im=Image.fromarray(head)", "skin=(head[:,:,3]>0)&(hr[:,:,0]>1.12*hr[:,:,1])&(hr[:,:,1]>1.14*hr[:,:,2])&(hr.mean(2)>65);head[skin,:3]=np.clip(hr[skin]*skin_gain,0,255).astype('uint8');im=Image.fromarray(head)")
s=s.replace("'curveInput':curve.tolist()", "'skinGain':skin_gain.tolist(),'curveInput':curve.tolist()")
(P/'build.py').write_text(s,encoding='utf-8')
for name in ['verify.py','index.html']:
 s=(N/name).read_text(encoding='utf-8').replace('north','south').replace('rear','front').replace('[.35,.36]','[.30,.31]');(P/name).write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_death_ground_helmet_north_candidates.gd').read_text(encoding='utf-8').replace('north','south').replace('BILL DEATH GROUND HELMET NORTH','BILL DEATH GROUND HELMET SOUTH')
(ROOT/'tests/test_bill_death_ground_helmet_south_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_death_ground_helmet_south_candidates.gd.uid').write_text('uid://s8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_helmet_north_candidate_validation.py').read_text(encoding='utf-8').replace('north','south').replace('BILL DEATH GROUND HELMET NORTH','BILL DEATH GROUND HELMET SOUTH')
(ROOT/'tools/run_bill_death_ground_helmet_south_candidate_validation.py').write_text(s,encoding='utf-8')
