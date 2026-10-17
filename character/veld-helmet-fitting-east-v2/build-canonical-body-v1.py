"""Canonical stationary Veld with isolated moving foreground components."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,map_coordinates
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OLD=ROOT/'character/veld-helmet-fitting-east-v1'
VERSION='canonical-body-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def poly(points):
    im=Image.new('L',(184,208));ImageDraw.Draw(im).polygon(points,fill=255);return np.array(im)>0
def ground(path):
    im=Image.new('RGBA',(184,208));im.alpha_composite(Image.open(path).convert('RGBA'),(0,24));return im
def main():
    barepath=ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'
    fittedpath=ROOT/'character/veld-shared-helmet-v1/frames/idle-east/000.png'
    bare=ground(barepath);equipped=ground(fittedpath)
    base=np.array(bare).copy()
    # Only the formerly occluded side below the shoulder uses generated fill.
    # All visible canonical head, torso fittings, belt and lower body stay original.
    under=Image.open(HERE/'body-underlay-source.png').convert('RGBA')
    a=np.array(under)[:,:,3];ys,xs=np.where(a>200)
    scale=148/(ys.max()-ys.min()+1)
    under=under.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).resize((round((xs.max()-xs.min()+1)*scale),148),Image.Resampling.LANCZOS)
    layer=Image.new('RGBA',(184,208));layer.alpha_composite(under,(81,48))
    fill=np.array(layer)
    clear=poly([(81,80),(96,80),(99,100),(99,137),(86,137),(80,117)])
    base[clear]=0
    # Torso side under the moving arm; never transfer generated head/body wholesale.
    fillmask=poly([(89,95),(99,95),(99,137),(88,137)])
    base[fillmask]=fill[fillmask]
    base=Image.fromarray(base)
    # Outer shell and matte are original; generated pixels only empty the aperture.
    raw=Image.open(ROOT/'character/veld-helmet-east-fit-v3/source.png').convert('RGBA')
    empty=Image.open(HERE/'empty-helmet-source.png').convert('RGBA');assert empty.size==raw.size
    aperture=Image.new('L',raw.size)
    ImageDraw.Draw(aperture).polygon([(698,486),(756,437),(889,406),(1010,408),(1091,508),(1115,627),(1114,764),(1085,835),(1019,869),(896,854),(804,810),(725,740),(696,623)],fill=255)
    shell=np.array(raw).copy();inside=np.array(aperture)>0;shell[inside,:3]=np.array(empty)[inside,:3]
    assert np.array_equal(shell[~inside],np.array(raw)[~inside])
    shell=Image.fromarray(shell).crop((270,126,1135,1075)).resize((34,38),Image.Resampling.LANCZOS)
    sp=np.array(shell);rgb=sp[:,:,:3].astype(float)
    neutral=(rgb.max(2)-rgb.min(2)<38)&(rgb.mean(2)>145);neutral[:12,13:22]=False;rgb[neutral]*=.86
    sp[:,:,:3]=rgb.clip(0,255).astype('uint8');shell=Image.fromarray(sp);shell.save(HERE/'empty-helmet-fitted.png')
    fitted=Image.open(ROOT/'character/veld-shared-helmet-v1/fitted-east.png').convert('RGBA')
    # Moving arms extracted from the retained action staging. Helmet/head/body
    # pixels from the rejected candidate are excluded by these explicit polygons.
    polygons=[[],
      [(85,79),(96,76),(108,83),(116,87),(121,84),(128,78),(140,74),(151,81),(154,91),(148,98),(129,103),(115,107),(101,104),(89,98)],
      [(86,79),(96,77),(103,86),(102,97),(110,105),(122,103),(128,108),(125,115),(110,117),(99,112),(92,103),(85,92)],
      [(84,80),(93,76),(102,79),(108,85),(115,76),(118,69),(123,67),(127,70),(127,77),(123,83),(117,91),(109,98),(98,99),(87,93)],
      [(85,79),(94,75),(101,77),(104,73),(102,55),(103,44),(103,36),(110,34),(117,40),(116,49),(117,57),(117,72),(115,85),(106,94),(93,94),(86,87)],
      [(85,84),(86,77),(89,77),(87,73),(88,68),(90,65),(95,65),(99,69),(100,75),(98,79),(104,82),(112,88),(118,93),(119,99),(112,104),(100,105),(88,99),(84,93)],
      [(86,81),(93,79),(103,84),(104,93),(112,92),(113,84),(118,81),(125,85),(126,92),(120,103),(113,108),(103,107),(92,102),(85,92)],[]]
    arms=[]
    for i in range(8):
        if i in [0,7]:arms.append(Image.new('RGBA',(184,208)));continue
        path=HERE/'pose-staging'/f'{i:03}.png'
        if not path.exists():path.parent.mkdir(exist_ok=True);path.write_bytes((OLD/f'frames/equip-helmet-east/{i:03}.png').read_bytes())
        arr=np.array(Image.open(path).convert('RGBA'));mask=poly(polygons[i]);arr[~mask]=0
        if i==4:
            # The arm is fully gloved. Do not retain the rejected face sliver
            # that lay behind its raised forearm in the old staging image.
            region=arr[58:80,108:119,:3].astype(int)
            skin=(region[:,:,0]-region[:,:,1]>15)&(region[:,:,0]-region[:,:,2]>25)
            arr[58:80,108:119][skin]=0
        arms.append(Image.fromarray(arr))
    # One fixed arm-material palette transfer from accepted sleeve pixels.
    ref=np.array(bare)[80:115,85:98,:3].reshape(-1,3).astype(float)
    ref=ref[(ref.max(1)-ref.min(1)<24)&(ref.mean(1)>15)&(ref.mean(1)<125)]
    samples=[]
    for arm in arms:
        a=np.array(arm);r=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(r.max(2)-r.min(2)<24)&(r.mean(2)>15)&(r.mean(2)<125);samples.extend(r[m].mean(1))
    qs=[0,10,25,50,75,90,100];knots=np.percentile(samples,qs);target=np.percentile(ref,qs,axis=0)
    for i,arm in enumerate(arms):
        a=np.array(arm);r=a[:,:,:3].astype(float);m=(a[:,:,3]>0)&(r.max(2)-r.min(2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
        for c in range(3):a[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
        arms[i]=Image.fromarray(a)
    # The accepted science badge is perspective-mapped with the upper arm.
    # This removes the generated white emblem rather than recoloring it.
    patch=np.array(bare)[81:96,85:100].astype(float)
    patch_quads=[None,[(87,79),(99,83),(95,95),(84,90)],[(86,81),(99,81),(100,96),(86,96)],
        [(86,80),(98,84),(95,95),(84,90)],[(85,79),(95,76),(99,87),(88,94)],
        [(85,82),(98,82),(99,96),(85,96)],[(85,83),(98,83),(99,97),(85,97)],None]
    patch_boxes=[None,(86,78,103,96),(86,80,103,98),(86,79,103,97),(85,76,103,96),(85,80,103,99),(85,81,103,99),None]
    for i in range(1,7):
        quad=patch_quads[i];matrix=[];rhs=[]
        for (x,y),(u,v) in zip(quad,[(0,0),(14,0),(14,14),(0,14)]):
            matrix += [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]];rhs += [u,v]
        h=np.linalg.solve(matrix,rhs);yy,xx=np.mgrid[:208,:184];den=h[6]*xx+h[7]*yy+1
        u=(h[0]*xx+h[1]*yy+h[2])/den;v=(h[3]*xx+h[4]*yy+h[5])/den
        arr=np.array(arms[i]);m=poly(quad)
        x0,y0,x1,y1=patch_boxes[i];m[y0:y1,x0:x1]=True
        m &= arr[:,:,3]>200
        for c in range(3):arr[m,c]=map_coordinates(patch[:,:,c],[v[m],u[m]],order=1,mode='nearest').clip(0,255).astype('uint8')
        arms[i]=Image.fromarray(arr)
    outputs=[];masks=[]
    placements={2:(116,82),3:(119,43),4:(102,17)}
    for i in range(8):
        if i in [0,7]:out=bare.copy() if i==0 else equipped.copy()
        else:
            out=base.copy()
            if i>=5:
                # EXACT selected equipped head/collar pixels, not another face repaint.
                out.paste(equipped.crop((79,38,121,83)),(79,38))
            if i in placements:out.alpha_composite(shell,placements[i])
            out.alpha_composite(arms[i])
        outputs.append(out)
    # Stage candidate only, retaining original durations and action cardinality.
    timing=json.loads((OLD/'original-selection.json').read_text())
    manifest={'name':'Veld canonical east fitting/removal study','status':'staged_not_installed_not_owner_accepted','frameWidth':184,'frameHeight':208,'pivot':[92,196],'standingHeight':148,'textureFilter':'linear','precomposed':True,'states':[]}
    palette_sheet=Image.new('RGB',(184*8,208),'#202a30')
    for i,frame in enumerate(outputs):palette_sheet.paste(frame,(184*i,0),frame)
    shared_palette=palette_sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    for state,indices in [('equip-helmet-east',list(range(8))),('remove-helmet-east',list(reversed(range(8))))]:
        folder=HERE/'frames'/state;folder.mkdir(parents=True,exist_ok=True);paths=[];gif=[]
        for j,i in enumerate(indices):
            path=folder/f'{j:03}.png';outputs[i].save(path);paths.append(path.relative_to(HERE).as_posix())
            bg=Image.new('RGB',(184,208),'#202a30');bg.paste(outputs[i],mask=outputs[i])
            gif.append(bg.quantize(palette=shared_palette,dither=Image.Dither.NONE))
        durations=timing[state]['durations'];assert len(durations)==len(paths)
        gif[0].save(HERE/f'{state}-{VERSION}.gif',save_all=True,append_images=gif[1:],duration=durations,loop=0,optimize=False,disposal=2)
        with Image.open(HERE/f'{state}-{VERSION}.gif') as decoded:
            first=None
            for j,i in enumerate(indices):
                decoded.seek(j);pix=np.array(decoded.convert('RGB')).astype(int);a=np.array(outputs[i])[:,:,3]
                if first is None:first=pix.copy()
                assert np.array_equal(pix[139:],first[139:]),('GIF stationary palette changed',state,j)
                outside=(distance_transform_edt(a<200)>2)&(a==0)
                assert np.abs(pix[outside]-[32,42,48]).max()<=3,('decoded glow',state,j)
        manifest['states'].append({'id':state,'frameFiles':paths,'frameCount':8,'frameDurationsMs':durations,'loop':False})
    assert np.array_equal(np.array(outputs[0]),np.array(bare));assert np.array_equal(np.array(outputs[7]),np.array(equipped))
    for i,out in enumerate(outputs):
        a=np.array(out);assert np.array_equal(a[139:],np.array(bare)[139:]),('stationary lower body',i)
        assert not np.any(a[[0,-1],:,3]>20) and not np.any(a[:,[0,-1],3]>20)
        if i in [1,2,3]:assert np.array_equal(a[40:75,80:116],np.array(bare)[40:75,80:116]),('canonical head changed',i)
        if i>=5:assert np.array_equal(a[40:65,80:121],np.array(equipped)[40:65,80:121]),('equipped crown changed',i)
    sheet=Image.new('RGB',(184*8,232),'#202a30');d=ImageDraw.Draw(sheet)
    for i,out in enumerate(outputs):sheet.paste(out,(i*184,24),out);d.text((i*184+4,4),f'fit {i}'+(' exact idle' if i in [0,7] else ''),fill='white')
    sheet.save(HERE/'contact.png')
    heads=Image.new('RGB',(240*8,324),'#202a30');d=ImageDraw.Draw(heads)
    for i,out in enumerate(outputs):crop=out.crop((75,40,135,115)).resize((240,300),Image.Resampling.NEAREST);heads.paste(crop,(i*240,24),crop);d.text((i*240+4,4),str(i),fill='white')
    heads.save(HERE/'heads.png')
    review=Image.new('RGB',(184*8,2*150),'#202a30');d=ImageDraw.Draw(review)
    for i,out in enumerate(outputs):
        small=out.resize((102,115),Image.Resampling.LANCZOS)
        for row,color in enumerate(['#202a30','#bcc0c2']):
            x,y=i*184,row*150;d.rectangle((x,y,x+183,y+149),fill=color)
            review.paste(small,(x+41,y+25),small);d.text((x+4,y+4),f'fit {i}',fill='white' if row==0 else 'black')
    review.save(HERE/'gameplay-dark-light.png')
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    checks={'authority':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [barepath,fittedpath]],'empty_helmet':'Original shell RGB/alpha outside explicit aperture; generated aperture only; accepted fitted size/grade.','body_underlay':'Generated fill restricted to former arm occlusion; canonical visible regions retained.','moving_arm_polygons':polygons,'arm_palette':{'fixed_clip_luma_knots':knots.tolist(),'reference_rgb_knots':target.tolist()},'checks':'8 fitting + 8 removal, original timing, exact idle endpoints, exact lower body rows139+, exact bare heads in first three interior poses, exact equipped crown, no edge clipping','status':'visual review pending; runtime unchanged'}
    checks['generated_inputs']=[{'file':p.name,'sha256':sha(p)} for p in [HERE/'body-underlay-source.png',HERE/'empty-helmet-source.png']]
    checks['accepted_patch']={'source_box':[85,81,100,96],'destination_quads':patch_quads,'old_emblem_coverage_boxes':patch_boxes}
    checks['preview_encoding']={'single_palette_for_both_states':True,'dither':False,'decoded_frames_checked':16,'stationary_lower_body_rgb_exact':True,'exterior_max_channel_error':3}
    checks['geometry_masks']={'arm_clear_polygon':[(81,80),(96,80),(99,100),(99,137),(86,137),(80,117)],'generated_fill_polygon':[(89,95),(99,95),(99,137),(88,137)],'equipped_head_copy_box':[79,38,121,83],'empty_helmet_placements':placements}
    (HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    html='<!doctype html><meta charset="utf-8"><title>Veld canonical fitting</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px;max-width:100%}a{color:#8cc6e7}</style><h1>Veld fitting — canonical body and head</h1><p>Accepted face, brown hair, torso fittings and lower body retained. Accepted helmet shell with an empty carried aperture. Moving arm layers preserve the action staging. Staged for review.</p>'
    for state in ['equip-helmet-east','remove-helmet-east']:
        html+=f'<h2>{state}</h2>'
        for h in [208,110,73,36]:html+=f'<img src="{state}-{VERSION}.gif" height="{h}">'
    html+='<p><a href="contact.png">All frames</a> / <a href="heads.png">Head comparison</a> / <a href="checks.json">Checks</a></p>'
    (HERE/'index.html').write_text(html,encoding='utf-8')
    print('Canonical fitting/removal staged; endpoint, fixed-body/head, timing and clipping checks pass.')
if __name__=='__main__':main()
