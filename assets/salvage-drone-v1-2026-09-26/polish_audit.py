"""Native-size and source-density evidence; no source artwork modifications."""
from build_full import R,SPECS,rig,GLASS
from PIL import Image,ImageDraw
import hashlib,json,numpy as np

order=['north','northeast','east','southeast','south','southwest','west','northwest']
board=Image.new('RGBA',(1000,840),'#17272e');draw=ImageDraw.Draw(board);rows=[]
draw.text((16,12),'SALVAGE / shared 0.34 scale / dark and light backgrounds',fill='white')
for i,h in enumerate(order):
 base,body,*rest=rig(h,SPECS[h]);meta=rest[-1]
 assert np.array_equal(np.array(base),np.array(body(0,0))),h
 assert meta['scale']<1,h
 a=np.array(base);box=base.getchannel('A').point(lambda x:255 if x>128 else 0).getbbox()
 rgb=a[:,:,:3].astype(float);cyan=(a[:,:,3]>240)&(rgb[:,:,1]>rgb[:,:,0]*1.15)&(rgb[:,:,2]>rgb[:,:,0]*1.15)
 rows.append({'heading':h,'sourceToLibraryScale':meta['scale'],'libraryPixelsPerWorldUnit':1/.34,'viewportDiameterLibrary':GLASS,'opaqueBounds':box,'nativeFootprint':[round((box[2]-box[0])*.34,2),round((box[3]-box[1])*.34,2)],'cyanMedianRGB':np.median(rgb[cyan],axis=0).tolist(),'sourceSha256':hashlib.sha256((R/'sources'/SPECS[h]['file']).read_bytes()).hexdigest()})
 x=i%4*250;y=40+i//4*395;draw.text((x+12,y),h.upper(),fill='white')
 small=base.resize((174,174),Image.Resampling.LANCZOS)
 board.alpha_composite(small,(x+35,y+15));draw.rectangle((x+3,y+200,x+246,y+385),fill='#c2c5bd')
 board.alpha_composite(small,(x+35,y+205))
board.save(R/'review/polish-native-directions.png')
result={'sameWorldScale':.34,'noSourceUpscaling':True,'allRestingFramesPixelExact':True,'notes':'RGB summaries are diagnostics, not visual identity acceptance. Native footprints vary with perspective; do not normalize silhouettes to equal boxes.','headings':rows}
(R/'review/polish-density.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'headings':len(rows),'libraryPixelsPerWorldUnit':round(1/.34,4),'sourceScaleRange':[min(x['sourceToLibraryScale'] for x in rows),max(x['sourceToLibraryScale'] for x in rows)],'restPoseParity':'8/8 exact','nativeFootprints':[x['nativeFootprint'] for x in rows]}))
