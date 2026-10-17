from pathlib import Path
P=Path(__file__).resolve().parent;N=P.with_name('veld-rest-north-coherent-v1')
s=(N/'build_helmet.py').read_text(encoding='utf-8').replace('north','south').replace("COMP=R/'character/veld-shared-helmet-v1/fitted-south.png'","COMP=R/'character/veld-shared-helmet-south-v1/fitted-helmet.png'")
s=s.replace('NECKS=[[254,122],[768,244],[1267,354],[254,827],[768,878],[1268,878]]','NECKS=[[282,113],[768,302],[1244,303],[290,681],[768,681],[1248,681]]').replace("source_anchors=[[256,606],[768,611],[1275,158],[1792,157]]","source_anchors=[[276,610],[817,610],[1358,610],[1901,608]]").replace('anchor=[16,32]','anchor=[17,36]').replace("'nativeAnchor':[16,32]","'nativeAnchor':[17,36]")
s=s.replace('exec-8a06b411-a4b4-40b6-a58b-a371e667f50b','exec-31af3da4-070c-4260-8dcd-c0989461a04b').replace('33native pixels /500opaque authored upright width','35native pixels /523opaque authored upright width').replace('rear helmet candidate','front helmet candidate').replace('rear face hidden',"closed' if i>=4 else 'open").replace("'expression':'closed' if i>=4 else 'open'","'expression':'closed' if i>=4 else 'open'").replace('authored backward depth projection','authored front backward depth projection')
a=s.index('    target=np.array(native)');b=s.index('    source_anchors=',a)
s=s[:a]+'''    target=np.array(native);solid=raw[:,:,3]>180;q=[0,15,35,55,75,90,100]
    polygons=[[(178,285),(350,285),(390,344),(375,440),(329,499),(218,499),(171,438),(150,348)],[(716,342),(916,342),(949,402),(928,475),(871,514),(763,514),(708,471),(689,409)],[(1251,287),(1468,287),(1501,361),(1473,451),(1425,496),(1292,493),(1236,445),(1219,366)],[(1795,301),(2017,301),(2051,356),(2030,433),(1974,492),(1836,492),(1780,436),(1769,368)]]
    face=Image.new('1',(raw.shape[1],raw.shape[0]));d=ImageDraw.Draw(face)
    for poly in polygons:d.polygon(poly,fill=1)
    rv=raw[:,:,:3].astype(float);tv=target[:,:,:3].astype(float)
    warm=solid&(rv[:,:,0]>1.12*rv[:,:,1])&(rv[:,:,1]>1.15*rv[:,:,2]);blue=solid&(rv[:,:,2]>1.2*rv[:,:,0])&(rv[:,:,2]>1.1*rv[:,:,1]);face=np.array(face,dtype=bool)
    yy,xx=np.indices(target.shape[:2]);twarm=(target[:,:,3]>180)&(tv[:,:,0]>1.12*tv[:,:,1])&(tv[:,:,1]>1.15*tv[:,:,2]);tface=(xx>=10)&(xx<=25)&(yy>=15)&(yy<=29)
    tblue=(target[:,:,3]>180)&(tv[:,:,2]>1.2*tv[:,:,0])&(tv[:,:,2]>1.1*tv[:,:,1])
    masks={'skin':warm&face,'hair':warm&~face,'visor':blue,'hardware':solid&~warm&~blue};targets={'skin':twarm&tface,'hair':twarm&~tface,'visor':tblue,'hardware':(target[:,:,3]>180)&~twarm&~tblue}
    graded=raw.copy();curves={}
    for name,mask in masks.items():
        authority=targets[name];assert mask.sum()>30 and authority.sum()>3,(name,int(mask.sum()),int(authority.sum()))
        knots=np.percentile(rv[mask].mean(1),q);palette=np.percentile(tv[authority],q,axis=0)
        for c in range(3):graded[mask,c]=np.interp(rv[mask].mean(1),knots,palette[:,c]).clip(0,255).astype('uint8')
        curves[name]={'knots':knots.tolist(),'targets':palette.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(authority.sum())}
'''+s[b:]
s=s.replace("'grade':{'knots':knots.tolist(),'targets':palette.tolist(),'scope':'one pooled atlas luma-to-masterRGB curve before fitting'}","'grade':{'materials':curves,'facePolygons':polygons,'scope':'one pooled semantic curve per material before fitting'}")
(P/'build_helmet.py').write_text(s,encoding='utf-8');print('South authored-depth processing prepared.')
