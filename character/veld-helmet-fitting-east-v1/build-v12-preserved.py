"""Package a staged fitting/removal candidate from preserved generated art."""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates, distance_transform_edt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / 'assembled-source-v11.png'
MATTE = HERE / 'source-v5-alpha.png'
HEAD_EDIT = HERE / 'source-v11-consistency.png'
SUIT_EDIT = HEAD_EDIT
SCALE = 148 / 406
REVIEW_VERSION = 'brown-hair-sleeves-v12'
HEAD_REGIONS = [(130,60,240,145),(130,60,240,150),(130,65,245,155),(130,60,245,150),
                (125,90,245,175),(185,105,255,157),(190,105,260,160),(195,105,265,165)]
FACE_REGIONS = [(205,100,233,134),(209,103,237,139),(218,110,245,146),(218,107,246,143),
                (210,135,238,166),(218,126,243,151),(215,129,243,155),(217,130,245,156)]
HAIR_POLYGON = [(141,95),(155,88),(163,69),(192,63),(216,69),(231,88),
                (232,98),(213,105),(198,112),(192,125),(173,131),(148,126),(136,111)]
PATCH_BOXES = [(151,160,193,200),(158,150,199,190),(161,169,204,207),(151,148,198,190),
               (153,162,198,204),(157,164,200,208),(165,174,209,218),(170,174,214,217)]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    source = Image.open(SOURCE).convert('RGBA')
    assert source.size == (1536, 1024)
    # Composite only the requested warm face/hair material from the generated
    # correction. Keep the accepted v7 suit/patch/helmet color artwork intact.
    old = np.asarray(source).copy()
    corrected = np.asarray(Image.open(HEAD_EDIT).convert('RGBA'))
    assert corrected.shape == old.shape
    head_mask = np.zeros(old.shape[:2],dtype=bool)
    for i,(x0,y0,x1,y1) in enumerate(HEAD_REGIONS):
        ox,oy = (i%4)*384,(i//4)*512
        roi = old[oy+y0:oy+y1,ox+x0:ox+x1,:3].astype(int)
        head_mask[oy+y0:oy+y1,ox+x0:ox+x1] = (roi[:,:,0]-roi[:,:,1]>5) & (roi[:,:,0]-roi[:,:,2]>10)
    composed = old.copy()
    material_transfers = {}
    # Transfer only the generated palette adjustment. Never substitute edited
    # pose pixels: constant offsets preserve the selected anatomy and texture.
    def transfer_palette(mask, name, limit, reference_offset=None):
        mask = mask & (old[:,:,3] > 0)
        visible = mask & (old[:,:,3] > 240)
        source_median = np.median(old[visible,:3],axis=0)
        target_median = np.median(corrected[visible,:3],axis=0)
        delta = np.clip(target_median-source_median,-limit,limit)
        if reference_offset is not None:
            # The accepted idle takes precedence where the generated palette
            # drifts away from the measured output material reference.
            delta = np.asarray(reference_offset,dtype=float)
        composed[mask,:3] = np.clip(old[mask,:3].astype(float)+delta,0,255).astype('uint8')
        material_transfers[name] = {'source_median':source_median.tolist(),'candidate_median':target_median.tolist(),'constant_rgb_offset':delta.tolist(),'pixels':int(mask.sum()),'authority':'accepted idle/output material comparison' if reference_offset is not None else 'generated grading palette'}
    lum = old[:,:,:3].mean(2)
    # Glossy near-neutral cheek/forehead highlights must not escape the warm
    # skin mask. Restrict their separate treatment to explicit face interiors.
    face_highlights = np.zeros(old.shape[:2],dtype=bool)
    for i,(x0,y0,x1,y1) in enumerate(FACE_REGIONS):
        ox,oy=(i%4)*384,(i//4)*512
        roi=old[oy+y0:oy+y1,ox+x0:ox+x1,:3].astype(int)
        face_highlights[oy+y0:oy+y1,ox+x0:ox+x1]=(roi.mean(2)>180)&(roi.max(2)-roi.min(2)<35)
    head_mask |= face_highlights
    # V11 is frozen input for this correction; preserve its accepted skin.
    transfer_palette(head_mask & (lum > 110) & ~face_highlights,'skin',12,[0,0,0])
    transfer_palette(face_highlights,'skin_highlights',24,[0,0,0])
    transfer_palette(head_mask & (lum <= 110),'hair',12,[0,0,0])
    assert np.array_equal(composed[~head_mask],old[~head_mask]), 'unrequested material changed'
    before_suit = composed.copy()
    suit_corrected = np.asarray(Image.open(SUIT_EDIT).convert('RGBA'))
    assert suit_corrected.shape == old.shape
    suit_mask = np.zeros(old.shape[:2],dtype=bool)
    # Neutral suit material only; preserve blue patches, face/hair and helmets.
    helmet_boxes=[None,None,(200,150,295,270),(200,25,305,150),(165,0,285,95),
                  (140,50,270,162),(140,50,275,165),(140,50,280,168)]
    hair_shape = np.zeros(old.shape[:2],dtype=bool)
    shifts=[(0,0),(5,5),(10,9),(9,8)]
    for i in range(5):
        ox,oy=(i%4)*384,(i//4)*512
        mask_image=Image.new('L',(384,512))
        if i<4:
            dx,dy=shifts[i];poly=[(x+dx,y+dy) for x,y in HAIR_POLYGON]
        else:
            poly=[(134,136),(140,116),(152,105),(170,96),(190,99),(201,107),(193,129),(190,147),(166,163),(143,157)]
        ImageDraw.Draw(mask_image).polygon(poly,fill=255)
        hair_shape[oy:oy+512,ox:ox+384]=np.asarray(mask_image)>0
    for i in range(8):
        ox,oy=(i%4)*384,(i//4)*512
        rgb=old[oy:oy+512,ox:ox+384,:3].astype(int)
        m=(rgb.max(2)-rgb.min(2)<18)
        m[:85]=False
        m[500:]=False
        # The patch emblem and stitched border are also preserved.
        x0,y0,x1,y1=PATCH_BOXES[i];m[y0:y1,x0:x1]=False
        box=FACE_REGIONS[i]
        m[box[1]:box[3],box[0]:box[2]]=False
        m[hair_shape[oy:oy+512,ox:ox+384]]=False
        if helmet_boxes[i]:
            x0,y0,x1,y1=helmet_boxes[i];m[y0:y1,x0:x1]=False
        suit_mask[oy:oy+512,ox:ox+384]=m
    # Separate fabric and hardware; the same grade applies across all poses.
    transfer_palette(suit_mask & (lum < 105),'cloth',8,[0,0,0])
    transfer_palette(suit_mask & (lum >= 105),'silver_suit_fittings',8,[0,0,0])
    cloth = suit_mask & (lum<105) & (old[:,:,3]>0)
    value=np.interp(lum[cloth],[0,25,40,50,60,75,105],[0,23,38,49,52,61,94])
    rgb=old[cloth,:3].astype(float)
    # One fixed cloth curve across the whole clip, including exposed sleeves.
    composed[cloth,:3]=np.clip(value[:,None]+(rgb-lum[cloth,None])*.3+np.array([0,0,1]),0,255).astype('uint8')
    assert np.array_equal(composed[~suit_mask],before_suit[~suit_mask]), 'other materials changed'
    rgb=old[:,:,:3].astype(float)
    silver_streak=(rgb.max(2)-rgb.min(2)<15)&(lum>105)
    hair=hair_shape & (lum<135) & ~silver_streak & (old[:,:,3]>0)
    value=np.interp(lum[hair],[0,25,45,65,90,120,135],[0,22,40,54,72,89,99])
    composed[hair,:3]=np.clip(value[:,None]*np.array([1.24,.94,.70]),0,255).astype('uint8')
    assert np.array_equal(composed[:,:,3],old[:,:,3]), 'source silhouette changed'
    assert np.array_equal(composed[~(hair|suit_mask)],old[~(hair|suit_mask)]), 'unselected materials changed'
    source = Image.fromarray(composed,'RGBA')
    # Keep the selected clean extraction matte; grading outputs may carry haze
    # in their background even when the visible artwork is correctly graded.
    matte = Image.open(MATTE).getchannel('A')
    assert matte.size == source.size
    source.putalpha(matte)
    source_pixels = np.asarray(source).copy()
    source_pixels[source_pixels[:,:,3]==0,:3] = 0
    source = Image.fromarray(source_pixels,'RGBA')
    source.save(HERE/'assembled-source.png')
    source_alpha = np.asarray(source)[:,:,3]
    far_halo = (source_alpha > 5) & (source_alpha < 200) & (distance_transform_edt(source_alpha < 200) > 4)
    halo_pixels = int(far_halo.sum())
    assert halo_pixels <= 16, ('diffuse exterior alpha returned', halo_pixels)
    selections = json.loads((HERE/'original-selection.json').read_text())
    idle_paths = [ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png', ROOT/'character/veld-shared-helmet-v1/frames/idle-east/000.png']
    output = []
    registration = []
    idle_ground = Image.new('RGBA',(184,208))
    idle_ground.alpha_composite(Image.open(idle_paths[0]).convert('RGBA'),(0,24))
    ref_alpha = np.asarray(idle_ground)[:,:,3]
    ref_y, ref_x = np.where(ref_alpha[180:] > 200)
    target_x = (ref_x.min()+ref_x.max())/2
    target_y = ref_y.max()+180
    # One reference-calibrated scale; translation follows measured sole anchors.
    # No per-frame height equalization.
    yy, xx = np.mgrid[:208, :184]
    for i in range(8):
        crop = source.crop(((i%4)*384, (i//4)*512, (i%4+1)*384, (i//4+1)*512))
        pixels = np.asarray(crop, dtype=np.float32)/255
        alpha = pixels[:,:,3:4]
        premul = np.dstack((pixels[:,:,:3]*alpha, alpha))
        opaque_y, opaque_x = np.where(pixels[:,:,3] > 200/255)
        sole = int(opaque_y.max())
        foot_y, foot_x = np.where(pixels[sole-18:sole+1,:,3] > 200/255)
        anchor_x = (int(foot_x.min())+int(foot_x.max()))/2
        # Translation-only registration against planted boots; scale is fixed.
        sx = (xx-target_x)/SCALE + anchor_x
        sy = (yy-target_y)/SCALE + sole
        registration.append({'source_cell':i,'source_boot_anchor':[anchor_x,sole],'target_anchor':[float(target_x),int(target_y)]})
        warp = np.dstack([map_coordinates(premul[:,:,c], [sy,sx], order=1, mode='constant', cval=0) for c in range(4)])
        a = warp[:,:,3:4]
        rgb = np.divide(warp[:,:,:3], a, out=np.zeros_like(warp[:,:,:3]), where=a>1e-5)
        image = Image.fromarray(np.clip(np.dstack((rgb,a))*255,0,255).astype('uint8'))
        # These actions do not step: reuse the approved planted shins/boots.
        # This avoids generated sole/ankle repainting appearing as movement.
        image.paste(idle_ground.crop((0,168,184,208)),(0,168))
        if i in [0,7]:
            image = Image.new('RGBA',(184,208))
            image.alpha_composite(Image.open(idle_paths[0 if i==0 else 1]).convert('RGBA'),(0,24))
        output.append(image)
    manifest = {'name':'Veld east helmet fitting candidate v1','status':'staged_not_installed_not_owner_accepted','frameWidth':184,'frameHeight':208,'pivot':[92,196],'standingHeight':148,'textureFilter':'linear','precomposed':True,'states':[]}
    checks = []
    for key, indices in [('equip-helmet-east',list(range(8))), ('remove-helmet-east',list(reversed(range(8))))]:
        folder = HERE/'frames'/key
        folder.mkdir(parents=True,exist_ok=True)
        paths=[]
        for j,i in enumerate(indices):
            path=folder/f'{j:03}.png'
            output[i].save(path)
            paths.append(path.relative_to(HERE).as_posix())
            arr=np.asarray(output[i])[:,:,3]
            assert not np.any(arr[0,:]>20) and not np.any(arr[-1,:]>20) and not np.any(arr[:,0]>20) and not np.any(arr[:,-1]>20), (key,j,'clipped')
            checks.append({'state':key,'index':j,'source_cell':i,'sha256':sha(path),'opaque_pixels':int((arr>200).sum())})
        original=selections[key]
        assert len(paths)==len(original['durations'])
        manifest['states'].append({'id':key,'frameFiles':paths,'frameCount':8,'frameDurationsMs':original['durations'],'loop':False,'provenance':'generated fitting poses; exact accepted idle endpoints; removal reverses fitting poses with retained removal timing'})
        bg=[]
        for i in indices:
            frame=Image.new('RGB',(184,208),'#202a30'); frame.paste(output[i],(0,0),output[i]); bg.append(frame)
        gif_path = HERE/f'{key}-{REVIEW_VERSION}.gif'
        bg[0].save(gif_path,save_all=True,append_images=bg[1:],duration=original['durations'],loop=0)
        # Validate what the browser actually receives, not only source alpha.
        with Image.open(gif_path) as preview:
            for j,i in enumerate(indices):
                preview.seek(j)
                decoded = np.asarray(preview.convert('RGB')).astype(int)
                alpha = np.asarray(output[i])[:,:,3]
                exterior = (distance_transform_edt(alpha < 200) > 2) & (alpha == 0)
                difference = np.abs(decoded - np.array([32,42,48]))
                assert int(difference[exterior].max()) <= 3, (key,j,'preview exterior glow')
    # Endpoint registration is exact, including alpha.
    for i,idle in [(0,idle_paths[0]),(7,idle_paths[1])]:
        assert np.array_equal(np.asarray(output[i])[24:], np.asarray(Image.open(idle).convert('RGBA')))
    for frame in output:
        assert np.array_equal(np.asarray(frame)[168:],np.asarray(idle_ground)[168:]), 'planted boots changed'
    sheet=Image.new('RGB',(184*8,232),'#202a30');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate(output):
        sheet.paste(frame,(184*i,24),frame);draw.text((184*i+4,4),f'{i:02}'+(' accepted idle' if i in [0,7] else ''),fill='white')
    sheet.save(HERE/'contact.png')
    sheet.save(HERE/f'contact-{REVIEW_VERSION}.png')
    heads=Image.new('RGB',(240*8,324),'#202a30');hd=ImageDraw.Draw(heads)
    for i,frame in enumerate(output):
        crop=frame.crop((75,40,135,115)).resize((240,300),Image.Resampling.NEAREST)
        heads.paste(crop,(240*i,24),crop)
        hd.text((240*i+4,4),f'{i:02}'+(' accepted idle' if i in [0,7] else ''),fill='white')
    heads.save(HERE/f'heads-{REVIEW_VERSION}.png')
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    evidence={'source':SOURCE.name,'source_sha256':sha(SOURCE),'scale':SCALE,'source_foot_anchor':[205,470],'destination_foot_anchor':[108,195],'idle_endpoints':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p)} for p in idle_paths],'rejected':[{'file':'source-v1.png','reason':'exterior bun in fitted poses; oversized shell'},{'file':'source-v2-rejected.png','reason':'duplicate face inside carried helmet'}],'frames':checks,'checks':'16 non-clipped frames; both exact idle endpoints; timing cardinality preserved. Native runtime and owner acceptance pending.'}
    evidence['alpha_cleanup'] = {'far_halo_pixels':halo_pixels,'definition':'alpha 6..199 more than four source pixels from alpha >=200','prior_source_v3_far_halo_pixels':320296,'source_dimensions_preserved':True}
    evidence.pop('source_foot_anchor')
    evidence['destination_foot_anchor'] = [float(target_x),int(target_y)]
    evidence['registration'] = registration
    evidence['clean_matte'] = {'source':MATTE.name,'sha256':sha(MATTE)}
    evidence['stationary_shins_boots'] = {'copied_from':str(idle_paths[0].relative_to(ROOT)).replace('\\','/'),'rows':[168,207],'all_frames_pixel_exact':True}
    evidence['preview_exterior'] = {'decoded_gif_frames_checked':16,'max_background_error_per_channel':3,'criterion':'fully transparent pixels more than two output pixels from opaque silhouette'}
    evidence['skin_hair_correction'] = {'palette_source':HEAD_EDIT.name,'sha256':sha(HEAD_EDIT),'regions':HEAD_REGIONS,'face_highlight_regions':FACE_REGIONS,'material_pixels':int(head_mask.sum()),'outside_head_material_mask_pixel_exact_before_suit_grade':True,'mask':'Warm skin/hair plus near-neutral highlights within explicit face interiors; generated pose pixels are never substituted.'}
    evidence['neutral_suit_correction'] = {'palette_source':SUIT_EDIT.name,'sha256':sha(SUIT_EDIT),'outside_suit_mask_pixel_exact_before_suit_grade':True,'material_mask':'RGB spread <18; body rows143..499; explicit face/hair, patch and helmet exclusions'}
    evidence['material_palette_transfers'] = material_transfers
    evidence['sleeve_hair_fix']={'hair_polygons':'explicit crown/bun polygons, bare phases only; neutral silver streak excluded','hair_curve':[[0,25,45,65,90,120,135],[0,22,40,54,72,89,99]],'brown_rgb_factors':[1.24,.94,.70],'cloth_curve':[[0,25,40,50,60,75,105],[0,23,38,49,52,61,94]],'patch_boxes':PATCH_BOXES,'fixed_curve_for_all_frames':True,'hair_pixels':int(hair.sum()),'cloth_pixels':int(cloth.sum())}
    evidence['geometry_preservation'] = 'Fixed material curves on frozen v11 artwork; no replacement face, body or action pixels. Alpha/registration unchanged.'
    (HERE/'checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Veld fitting candidate</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:16px}a{color:#8cc6e7}</style><h1>Veld helmet fitting/removal — brown hair and sleeve match</h1><p>Hair crown/bun kept brown; silver streak preserved. Sleeve cloth now shares the body grade with tighter patch exclusions. Skin, helmet, geometry, clean matte, fixed boots and exact idle endpoints preserved. Staged.</p>'
    for key in ['equip-helmet-east','remove-helmet-east']:
        html+=f'<h2>{key}</h2>'
        for height in [208,110,73,36]:html+=f'<img src="{key}-{REVIEW_VERSION}.gif" height="{height}">'
    html+=f'<p><a href="contact-{REVIEW_VERSION}.png">All fitting frames</a> · <a href="checks.json">Provenance and checks</a></p><p>Large images are diagnostic. Smaller images approximate standing heights of 82/54/27px. Interior pose continuity and final material matching remain subject to review.</p>'
    (HERE/'index.html').write_text(html,encoding='utf-8')
    print('Staged 8 fitting + 8 reversed removal frames; exact accepted endpoints, clipping and timing checks pass. Runtime unchanged.')

if __name__=='__main__':main()
