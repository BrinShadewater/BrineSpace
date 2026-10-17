"""One reproducible palette pass, starting before the stacked v8-v12 edits."""
import json
import numpy as np
from PIL import Image, ImageDraw

# Coordinates in the original 384x512 cells. These are material boundaries,
# not warm/neutral RGB guesses; bright skin and desaturated hair stay included.
HAIR = [
 [(139,111),(148,100),(157,101),(163,80),(181,65),(208,63),(230,76),(235,92),(218,90),(202,101),(191,112),(188,131),(168,136),(147,128)],
 [(144,116),(153,105),(162,106),(168,84),(186,70),(214,68),(237,82),(240,99),(221,96),(207,108),(195,118),(193,137),(174,141),(152,134)],
 [(146,120),(155,109),(166,110),(172,88),(191,77),(219,77),(240,91),(243,104),(226,102),(212,114),(202,122),(198,143),(177,146),(156,140)],
 [(145,120),(152,108),(165,110),(171,87),(189,76),(216,76),(239,87),(241,102),(224,99),(210,111),(200,120),(197,141),(177,145),(152,137)],
 [(134,139),(141,132),(148,132),(147,121),(155,109),(173,97),(193,95),(197,104),(191,124),(176,139),(167,153),(155,163),(139,158)],
 [],[],[]]
SKIN = [
 [(187,103),(197,102),(216,91),(223,89),(231,100),(234,111),(232,114),(235,120),(231,128),(230,139),(213,139),(202,133),(194,125),(187,123)],
 [(193,109),(204,108),(223,98),(230,96),(236,108),(238,119),(237,122),(239,128),(236,136),(235,144),(219,146),(207,139),(199,132),(193,130)],
 [(201,117),(211,114),(227,104),(234,104),(241,113),(243,124),(246,128),(241,131),(243,136),(239,142),(239,150),(221,151),(209,143),(202,137)],
 [(199,113),(211,111),(226,101),(234,100),(240,111),(242,122),(244,125),(240,128),(242,134),(238,140),(238,148),(221,150),(208,140),(200,134)],
 [(174,136),(181,132),(185,137),(181,145),(176,146)],
 [(219,119),(229,112),(235,111),(240,120),(243,132),(241,137),(244,141),(239,147),(238,154),(224,154),(216,144),(213,136)],
 [(217,124),(228,119),(233,119),(239,127),(241,138),(240,141),(243,145),(238,151),(237,157),(224,157),(217,149),(213,139)],
 [(218,123),(229,118),(235,119),(240,128),(243,137),(240,140),(244,144),(239,151),(238,156),(223,155),(216,147),(214,137)]]
# Silver headband crosses the hair. Exclude the actual strip, not every gray hair.
BANDS = [ [(166,108),(214,87),(220,92),(173,117)],
 [(172,113),(221,94),(227,98),(178,122)],
 [(178,120),(227,99),(233,104),(184,127)],
 [(177,118),(225,96),(232,101),(183,125)],
 [(158,144),(188,127),(188,134),(161,151)], [],[],[]]

# Coordinate review of the preserved v7 source (not later generated edits).
for i,(dx,dy) in enumerate([(0,0),(0,7),(2,14),(-32,14)]):
    HAIR[i]=[(x+dx,y+dy) for x,y in HAIR[0]] if i else HAIR[0]
    SKIN[i]=[(x+dx,y+dy) for x,y in SKIN[0]] if i else SKIN[0]
    BANDS[i]=[(x+dx,y+dy) for x,y in BANDS[0]] if i else BANDS[0]
SKIN[5]=[(216,106),(223,97),(233,93),(238,102),(241,113),(239,117),(244,120),(239,125),(238,133),(225,135),(217,127),(215,116)]
SKIN[6]=[(216,116),(223,107),(233,103),(238,112),(241,123),(239,127),(244,130),(239,135),(238,143),(225,145),(217,137),(215,126)]
SKIN[7]=SKIN[6]

def shape(polygons):
    result=np.zeros((1024,1536),bool)
    for i,poly in enumerate(polygons):
        if not poly: continue
        im=Image.new('L',(384,512));ImageDraw.Draw(im).polygon(poly,fill=255)
        result[(i//4)*512:(i//4+1)*512,(i%4)*384:(i%4+1)*384]=np.array(im)>0
    return result

def grade(here,root):
    original=np.array(Image.open(here/'source-v7-muted-patches.png').convert('RGBA'))
    original[:,:,3]=np.array(Image.open(here/'source-v5-alpha.png'))[:,:,3]
    rgb=original[:,:,:3].astype(float); lum=rgb.mean(2)
    hair=shape(HAIR)&~shape(BANDS)&(original[:,:,3]>0)
    skin=shape(SKIN)
    extra=[[],[],[],[],[(223,118),(231,120),(233,131),(231,135),(237,139),(231,143),(232,150),(221,153),(218,143)],[],[],[]]
    skin |= shape(extra)
    skin &= original[:,:,3]>0
    # Keep eye/lip ink rather than lifting it into a skin highlight.
    skin &= lum>45
    idle=np.array(Image.open(root/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png').convert('RGBA'))
    refhair=np.zeros((184,184),bool); refhair[25:35,89:110]=True;refhair[35:43,84:94]=True
    refskin=np.zeros((184,184),bool); refskin[35:45,104:112]=True
    equipped=np.array(Image.open(root/'character/veld-shared-helmet-v1/frames/idle-east/000.png').convert('RGBA'))
    refglass=np.zeros((184,184),bool);refglass[35:44,105:113]=True
    warm=(equipped[:,:,0].astype(int)-equipped[:,:,2].astype(int))>25
    reference={'hair':idle[refhair&(idle[:,:,3]>240),:3], 'skin':idle[refskin&(idle[:,:,3]>240),:3],
               'skin_through_glass':equipped[refglass&warm&(equipped[:,:,3]>240),:3]}
    out=original.copy(); records={}
    # Fit a SINGLE pooled-source tonal curve for each material. All frames use
    # the identical LUT and the accepted idle's RGB palette, never pose exposure.
    through_glass=skin.copy();through_glass[:512]=False;through_glass[512:,:384]=False
    for name,mask in [('hair',hair),('skin',skin&~through_glass),('skin_through_glass',through_glass)]:
        sample=lum[mask&(original[:,:,3]>240)]
        q=np.array([0,5,15,30,50,70,85,95,100])
        x=np.percentile(sample,q)
        colors=np.percentile(reference[name],q,axis=0)
        for c in range(3):out[mask,c]=np.interp(lum[mask],x,colors[:,c]).clip(0,255).astype('uint8')
        records[name]={'pooled_source_luma_knots':x.tolist(),'reference_rgb_knots':colors.tolist(),'pixels':int(mask.sum())}
    # A continuous cloth curve includes sleeve highlights. Preserve silver,
    # science blue and brass, and exclude helmets/head/patch boundaries.
    cloth=np.zeros(lum.shape,bool)
    helmets=[None,None,(198,150,295,270),(199,25,305,150),(165,0,285,95),(139,50,270,162),(139,50,275,165),(139,50,280,168)]
    patches=[(151,160,193,200),(158,150,199,190),(161,169,204,207),(151,148,198,190),(153,162,198,204),(157,164,200,208),(165,174,209,218),(170,174,214,217)]
    for i in range(8):
        oy,ox=(i//4)*512,(i%4)*384
        m=(rgb[oy:oy+512,ox:ox+384].max(2)-rgb[oy:oy+512,ox:ox+384].min(2)<24)&(lum[oy:oy+512,ox:ox+384]<125)
        m[:145]=False;m[335:]=False
        for box in [patches[i],helmets[i]]:
            if box:
                x0,y0,x1,y1=box;m[y0:y1,x0:x1]=False
        cloth[oy:oy+512,ox:ox+384]=m
    cloth &= ~(hair|skin|shape(BANDS))&(original[:,:,3]>0)
    knots=[0,25,40,60,80,100,125]; targets=[0,19,31,46,57,69,90]
    val=np.interp(lum[cloth],knots,targets)
    out[cloth,:3]=np.clip(val[:,None]+np.array([0,0,2]),0,255).astype('uint8')
    records['cloth']={'input_luma':knots,'output_luma':targets,'pixels':int(cloth.sum())}
    out[out[:,:,3]==0,:3]=0
    assert np.array_equal(original[:,:,3],out[:,:,3])
    visible=original[:,:,3]>0
    assert np.array_equal(original[visible&~(hair|skin|cloth)],out[visible&~(hair|skin|cloth)])
    maskview=np.zeros_like(out);maskview[:,:,3]=original[:,:,3]
    maskview[visible,:3]=rgb[visible]*.22
    maskview[hair,:3]=[145,79,30];maskview[skin,:3]=[237,150,100];maskview[cloth,:3]=[65,95,170]
    Image.fromarray(maskview).save(here/'material-masks-v13.png')
    records['source']='source-v7-muted-patches.png';records['palette_references']=['character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png','character/veld-shared-helmet-v1/frames/idle-east/000.png']
    records['scope']='Fixed pooled clip LUTs; explicit per-pose masks; unchanged alpha and outside-material RGB. No per-frame normalization.'
    (here/'material-grade-v13.json').write_text(json.dumps(records,indent=2)+'\n')
    return Image.fromarray(out),records
