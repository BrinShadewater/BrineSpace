from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.with_name('veld-rest-east-coherent-v1')
s=(E/'review_scale.py').read_text(encoding='utf-8').replace('east','north').replace('contact_x=[229,699,1160,221,769,1280]','contact_x=[254,767,1270,254,768,1268]').replace('target_x=[130,130,130,130,130,130]','target_x=[128,128,128,128,128,128]')
# ASCII labels keep deterministic review text legible across Windows codepages.
s=s.replace("f'Raw pose{i-1} — ungraded'","f'Raw pose{i-1} - ungraded'").replace("f'Raw pose{i-1} â€” ungraded'","f'Raw pose{i-1} - ungraded'")
(P/'review_scale.py').write_text(s,encoding='utf-8')
s=(E/'build_bare.py').read_text(encoding='utf-8').replace('east','north').replace('East rest','North rest')
s=s.replace('HEADS=[[215,113],[765,311],[1135,346],[99,778],[577,871],[1089,872]]','HEADS=[[254,79],[768,195],[1267,310],[254,833],[768,923],[1268,923]]')
s=s.replace('rh=(rx>=117)&(rx<155)&(ry>=74)&(ry<106)','rh=(rx>=117)&(rx<144)&(ry>=76)&(ry<104)')
a=s.index('    # Anatomical face windows');b=s.index('    graded=raw.copy()',a)
s=s[:a]+'''    # Rear cameras own shaded ear/neck skin. Bright brown crown is not face.
    boxes=[[215,79,224,103],[286,79,296,104],[727,200,736,224],[800,200,810,224],[1227,311,1238,337],[1295,311,1306,337],[211,828,225,852],[284,828,298,852],[738,860,799,881],[720,932,731,955],[804,932,815,955],[1238,860,1299,881],[1220,932,1231,955],[1304,932,1315,955]]
    face=np.zeros(raw.shape[:2],bool)
    for x0,y0,x1,y1 in boxes:face[y0:y1,x0:x1]=True
    warm=sm['skin']|sm['hair'];sm['skin']=warm&face;sm['hair']=warm&~face
    rv=ref[:,:,:3].astype(float)
    rear_ears=((rx>=116)&(rx<=119)&(ry>=89)&(ry<=94))|((rx>=137)&(rx<=140)&(ry>=89)&(ry<=94))
    rear_ears&=(ref[:,:,3]>160)&(rv[:,:,0]>rv[:,:,1]*1.10)&(rv[:,:,1]>rv[:,:,2]*1.10)
    rwarm=rm['skin']|rm['hair'];rm['skin']=rear_ears;rm['hair']=rwarm&~rear_ears
'''+s[b:]
s=s.replace("'facePolygons':polygons","'skinWindows':boxes")
(P/'build_bare.py').write_text(s,encoding='utf-8')
s=(E/'index.html').read_text(encoding='utf-8').replace('east','north').replace('East','North').replace('79 packaging and 102 player checks pass.','Packaging and native player review pending.').replace('Overall native runner retains a profile-guard failure.','').replace('veld-helmet-fitting-north-v2/frames/equipped-idle-north','veld-shared-helmet-v1/frames/idle-north')
s=s.replace('canonical helmet hardware and closed eyes in the final poses','canonical rear hardware with authored depth pitch and hidden sleeping face').replace('final closed-eye pose','final rear sleeping pose')
(P/'index.html').write_text(s,encoding='utf-8')
print('Prepared independent north geometry/material processing.')
