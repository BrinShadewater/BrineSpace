from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.parent/'bill-rest-east-coherent-v1'
t=(E/'build.py').read_text(encoding='utf-8')
replacements={
'east':'west',
'heads=[(211,139),(674,285),(1151,322),(90,749),(572,843),(1086,841)]':'heads=[(254,104),(866,278),(1414,311),(421,768),(958,857),(1466,857)]',
'sx,sy=.28,148/466':'sx,sy=.31,148/446',
'contacts=[None,(854,569),(1419,567),(440,917),(967,911),(1479,911)]':'contacts=[None,(600,512),(1110,513),(110,928),(565,922),(1080,922)]',
'targets=[None,(190,223),(190,223),(190,223),(195,223),(195,223)]':'targets=[None,(66,223),(66,223),(66,223),(61,223),(61,223)]',
'lh=((lx-477)**2+(ly-184)**2<95**2)|((lx-1247)**2+(ly-341)**2<95**2)':'lh=((lx-499)**2+(ly-188)**2<95**2)|((lx-1327)**2+(ly-375)**2<95**2)',
'ruler=[.16,.192]':'ruler=[.18,148/710]',
'contact=[(593,789),(1489,783)][i];target=[(162,223),(190,223)][i]':'contact=[(477,799),(1167,799)][i];target=[(94,223),(66,223)][i]',
'exec-7fe0a5e8-739d-4f29-b80a-0e30f113f55a':'exec-36d899f3-d63d-41a3-acea-dfe64d0e7634',
'exec-be41fd9f-87f5-4fc8-8f54-9f210c2b116a':'exec-0b7db075-2467-454c-947b-5a9148d4703a',
'exec-59db2955-ab5c-46ac-84cf-51c8eb471fe0':'exec-65530fef-1e27-42bc-af11-6a237d6ff68f',
'round((headcenter[1]-224)*65.28/148,4)':'round((headcenter[1]-224)*65.28/148+384*.038,4)',
'(rx>115)':'(rx>108)&(rx<132)',
'rp=(ref[:,:,3]>180)&(ry>100)&':'rp=(ref[:,:,3]>180)&(ry>100)&(ry<125)&(rr[:,:,0]>80)&',
"'burgundy':~head&(raw[:,:,3]>200)&":"'burgundy':~head&(rgb[:,:,0]>70)&(raw[:,:,3]>200)&",
"('burgundy',~lh&(lower[:,:,3]>200)&":"('burgundy',~lh&(lr[:,:,0]>70)&(lower[:,:,3]>200)&",
}
for old,new in replacements.items():assert old in t,old;t=t.replace(old,new)
t=t.replace('mask=masks[name];gain=','mask=masks[name]\n    if not mask.any() or not authority.any(): continue\n    gain=')
t=t.replace('    gain=np.median(rr[authority],axis=0)/np.median(lr[mask],axis=0)','    if not mask.any() or not authority.any(): continue\n    gain=np.median(rr[authority],axis=0)/np.median(lr[mask],axis=0)')
t=t.replace('frames=[frames[0]]+interiors+frames[1:]','frames=[frames[0]]+interiors+frames[1:]\nfor row,index in zip(lower_records,[1,2]):row["frame"]=index\nfor row,index in zip(records,[3,4,5,6,7]):row["frame"]=index')
(P/'build.py').write_text(t,encoding='utf-8')
test=(R/'tests/test_bill_rest_north_candidates.gd').read_text(encoding='utf-8').replace('north','west').replace('NORTH','WEST')
(R/'tests/test_bill_rest_west_candidates.gd').write_text(test,encoding='utf-8');(R/'tests/test_bill_rest_west_candidates.gd.uid').write_text('uid://y9b8w3m6p2r9v\n')
runner=(R/'tools/run_bill_rest_north_candidate_validation.py').read_text().replace('north','west').replace('NORTH','WEST')
(R/'tools/run_bill_rest_west_candidate_validation.py').write_text(runner,encoding='utf-8')
html=(E/'index.html').read_text(encoding='utf-8').replace('east','west').replace('East','West').replace('Equipment, furniture contacts and normal runtime selection remain pending.','Equipment, compatible furniture and normal runtime selection remain pending. Current habitation uses the selected east bunk.')
(P/'index.html').write_text(html,encoding='utf-8')
print('Prepared west rest extraction, native fixture/UID, scratch runner and preview')
