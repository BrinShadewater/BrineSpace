from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.parent/'bill-rest-east-coherent-v1'
t=(E/'build.py').read_text(encoding='utf-8')
replacements={
"sources/rest-v2.png":"sources/rest-v1.png","bill-seated-east-coherent-v1/frames/sit-down-east/000.png":"bill-seated-south-coherent-v1/frames/sit-down-south/000.png",
"heads=[(211,139),(674,285),(1151,322),(90,749),(572,843),(1086,841)]":"heads=[(345,104),(767,182),(1179,251),(346,651),(769,651),(1179,651)]",
"sx,sy=.28,148/466":"sx,sy=.30,148/436",
"contacts=[None,(854,569),(1419,567),(440,917),(967,911),(1479,911)]":"contacts=[None,(767,511),(1179,522),(346,947),(769,947),(1179,947)]",
"targets=[None,(190,223),(190,223),(190,223),(195,223),(195,223)]":"targets=[None,(128,223),(128,223),(128,223),(128,223),(128,223)]",
"sources/lowering-v3.png":"sources/interiors-v2.png",
"lh=((lx-477)**2+(ly-184)**2<95**2)|((lx-1247)**2+(ly-341)**2<95**2)":"lh=((lx-455)**2+(ly-231)**2<85**2)|((lx-1069)**2+(ly-297)**2<85**2)",
"ruler=[.16,.192]":"ruler=[.16,148/710]",
"contact=[(593,789),(1489,783)][i];target=[(162,223),(190,223)][i]":"contact=[(455,854),(1074,900)][i];target=[(128,223),(128,223)][i]",
"frames=[frames[0]]+interiors+frames[1:]":"frames=[frames[0],interiors[0],frames[1],frames[2],interiors[1],frames[3],frames[4],frames[5]]\nfor record,index in zip(records,[2,3,5,6,7]): record['frame']=index\nfor record,index in zip(lower_records,[1,4]): record['frame']=index",
"frames/lie-down-east":"frames/lie-down-south","name+'-east'":"name+'-south'","['east']":"['south']",
"Bill east generic rest candidate":"Bill south generic rest candidate","bare east candidate":"bare south candidate","bare east rest":"bare south rest",
"exec-7fe0a5e8-739d-4f29-b80a-0e30f113f55a":"exec-64f904ac-5ee3-4209-ab66-ef4b9a6fee9e","exec-be41fd9f-87f5-4fc8-8f54-9f210c2b116a":"exec-cc9665f2-5239-497d-9e0a-9467e3249287",
"'rejectedChoreography':'exec-59db2955-ab5c-46ac-84cf-51c8eb471fe0',":"",
"round((headcenter[1]-224)*65.28/148,4)":"round((headcenter[1]-224)*65.28/148+384*.038,4)"
}
for old,new in replacements.items():assert old in t,old;t=t.replace(old,new)
t=t.replace("mask=masks[name];gain=", "mask=masks[name]\n    if not mask.any() or not authority.any(): continue\n    gain=")
t=t.replace("    gain=np.median(rr[authority],axis=0)/np.median(lr[mask],axis=0)","    if not mask.any() or not authority.any(): continue\n    gain=np.median(rr[authority],axis=0)/np.median(lr[mask],axis=0)")
t=t.replace("rp=(ref[:,:,3]>180)&(ry>100)&", "rp=(ref[:,:,3]>180)&(ry>100)&(ry<125)&(rr[:,:,0]>80)&")
t=t.replace("'burgundy':~head&(raw[:,:,3]>200)&", "'burgundy':~head&(rgb[:,:,0]>70)&(raw[:,:,3]>200)&")
t=t.replace("('burgundy',~lh&(lower[:,:,3]>200)&", "('burgundy',~lh&(lr[:,:,0]>70)&(lower[:,:,3]>200)&")
t=t.replace("lower=np.array(Image.open(lower_path).convert('RGBA'));lr=lower[:,:,:3].astype(float)","lower=np.array(Image.open(lower_path).convert('RGBA'))\nrevision_path=P/'sources/interiors-v3.png';revision=np.array(Image.open(revision_path).convert('RGBA'))\nassert revision.shape==lower.shape\nlower[:,768:]=revision[:,768:]\nlr=lower[:,:,:3].astype(float)")
t=t.replace("(ly-297)**2<85**2", "(ly-350)**2<85**2")
t=t.replace("(1074,900)","(1074,891)")
t=t.replace("'source':'sources/interiors-v2.png'", "'source':'sources/interiors-v2.png' if i==0 else 'sources/interiors-v3.png'")
t=t.replace("'loweringSourceSha256':sha(lower_path)","'loweringSourceSha256':sha(lower_path),'loweringRevisionSha256':sha(revision_path),'recliningCorrectionGeneration':'exec-36d3d557-df4f-417c-b47b-b351486268b2'")
(P/'build.py').write_text(t,encoding='utf-8')
test=(R/'tests/test_bill_rest_north_candidates.gd').read_text(encoding='utf-8').replace('north','south').replace('NORTH','SOUTH')
(R/'tests/test_bill_rest_south_candidates.gd').write_text(test,encoding='utf-8');(R/'tests/test_bill_rest_south_candidates.gd.uid').write_text('uid://w9b8w3m6p2r9v\n')
runner=(R/'tools/run_bill_rest_north_candidate_validation.py').read_text().replace('north','south').replace('NORTH','SOUTH')
(R/'tools/run_bill_rest_south_candidate_validation.py').write_text(runner,encoding='utf-8')
html=(E/'index.html').read_text(encoding='utf-8').replace('east','south').replace('East','South').replace('Equipment, furniture contacts and normal runtime selection remain pending.','Equipment, compatible furniture and normal runtime selection remain pending. Current habitation uses the selected east bunk.')
(P/'index.html').write_text(html,encoding='utf-8')
print('Prepared south fixed-source rest extraction, native fixture/scratch runner and preview')
