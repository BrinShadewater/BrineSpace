from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.parent/'bill-rest-east-coherent-v1'
t=(E/'build.py').read_text(encoding='utf-8')
replacements={
"sources/rest-v2.png":"sources/rest-v1.png","bill-seated-east-coherent-v1/frames/sit-down-east/000.png":"bill-seated-north-coherent-v1/frames/sit-down-north/000.png",
"heads=[(211,139),(674,285),(1151,322),(90,749),(572,843),(1086,841)]":"heads=[(308,69),(771,178),(1241,217),(302,638),(769,650),(1249,650)]",
"sx,sy=.28,148/466":"sx,sy=.31,148/425",
"contacts=[None,(854,569),(1419,567),(440,917),(967,911),(1479,911)]":"contacts=[None,(771,468),(1241,472),(302,972),(769,973),(1249,973)]",
"targets=[None,(190,223),(190,223),(190,223),(195,223),(195,223)]":"targets=[None,(128,223),(128,223),(128,223),(128,223),(128,223)]",
"sources/lowering-v3.png":"sources/lowering-v2.png",
"lh=((lx-477)**2+(ly-184)**2<95**2)|((lx-1247)**2+(ly-341)**2<95**2)":"lh=((lx-461)**2+(ly-279)**2<70**2)|((lx-1065)**2+(ly-378)**2<70**2)",
"ruler=[.16,.192]":"ruler=[.19,.23]",
"contact=[(593,789),(1489,783)][i];target=[(162,223),(190,223)][i]":"contact=[(463,820),(1065,820)][i];target=[(128,223),(128,223)][i]",
"frames/lie-down-east":"frames/lie-down-north","name+'-east'":"name+'-north'","['east']":"['north']",
"Bill east generic rest candidate":"Bill north generic rest candidate","bare east candidate":"bare north candidate","bare east rest":"bare north rest",
"exec-7fe0a5e8-739d-4f29-b80a-0e30f113f55a":"exec-c1d5b892-cc6b-4e4d-b663-69ffa565e67d","exec-be41fd9f-87f5-4fc8-8f54-9f210c2b116a":"exec-7086cca6-bbee-4926-a7e6-6434e82339ff",
"'rejectedChoreography':'exec-59db2955-ab5c-46ac-84cf-51c8eb471fe0',":"",
"(ry>=76)&(ry<85)":"(ry>=76)&(ry<94)"
}
for old,new in replacements.items():assert old in t,old;t=t.replace(old,new)
t=t.replace("mask=masks[name];gain=", "mask=masks[name]\n    if not mask.any() or not authority.any(): continue\n    gain=")
t=t.replace("    gain=np.median(rr[authority],axis=0)/np.median(lr[mask],axis=0)","    if not mask.any() or not authority.any(): continue\n    gain=np.median(rr[authority],axis=0)/np.median(lr[mask],axis=0)")
t=t.replace("rp=(ref[:,:,3]>180)&(ry>100)&", "rp=(ref[:,:,3]>180)&(ry>100)&(ry<125)&(rr[:,:,0]>80)&")
t=t.replace("'burgundy':~head&(raw[:,:,3]>200)&", "'burgundy':~head&(rgb[:,:,0]>70)&(raw[:,:,3]>200)&")
t=t.replace("('burgundy',~lh&(lower[:,:,3]>200)&", "('burgundy',~lh&(lr[:,:,0]>70)&(lower[:,:,3]>200)&")
t=t.replace("round((headcenter[1]-224)*65.28/148,4)","round((headcenter[1]-224)*65.28/148+384*.038,4)")
(P/'build.py').write_text(t,encoding='utf-8')
test=(R/'tests/test_bill_rest_east_candidates.gd').read_text(encoding='utf-8').replace('bill-rest-east-coherent-v1','bill-rest-north-coherent-v1').replace('BILL REST EAST','BILL REST NORTH').replace('bill-rest-east-candidate-native-v1','bill-rest-north-candidate-native-v1').replace('bill-seated-east-coherent-v1','bill-seated-north-coherent-v1').replace('sit-down-east','sit-down-north').replace('sleep-east','sleep-north').replace('lie-down-east','lie-down-north').replace('get-up-east','get-up-north').replace('"east"','"north"')
test=test.replace('check(row[0].has_meta("crew_rest_head_offset"),"Rest head anchor exposed")','check(row[0].has_meta("crew_rest_head_offset"),"Rest head anchor exposed")\n\t\t\tcheck(row[0].get_meta("crew_rest_head_offset")==Vector2(state.restHeadOffset[0],state.restHeadOffset[1]),"Exact north resting head anchor including render lift")')
(R/'tests/test_bill_rest_north_candidates.gd').write_text(test,encoding='utf-8');(R/'tests/test_bill_rest_north_candidates.gd.uid').write_text('uid://t9b8w3m6p2r9v\n')
runner=(R/'tools/run_bill_rest_east_candidate_validation.py').read_text().replace('bill-rest-east-candidate-native-v1','bill-rest-north-candidate-native-v1').replace('test_bill_rest_east_candidates.gd','test_bill_rest_north_candidates.gd').replace('BILL REST EAST','BILL REST NORTH')
(R/'tools/run_bill_rest_north_candidate_validation.py').write_text(runner,encoding='utf-8')
html=(E/'index.html').read_text(encoding='utf-8').replace('east','north').replace('East','North')
(P/'index.html').write_text(html,encoding='utf-8')
print('Prepared north fixed-source rest extraction, native fixture/scratch runner and preview')
