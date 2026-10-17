"""Package a staged fitting/removal candidate from preserved generated art."""

import hashlib

import json

from pathlib import Path

import numpy as np

from PIL import Image, ImageDraw

from scipy.ndimage import map_coordinates, distance_transform_edt



HERE = Path(__file__).resolve().parent

ROOT = HERE.parents[1]

SOURCE = HERE / 'source-v7-muted-patches.png'

MATTE = HERE / 'source-v5-alpha.png'

SCALE = 148 / 406
REVIEW_VERSION = 'material-palette-v13'


def sha(path):

    return hashlib.sha256(path.read_bytes()).hexdigest()



def main():

    from material_grade import grade

    source, material_records = grade(HERE, ROOT)

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

    evidence['material_grade'] = material_records

    evidence['geometry_preservation'] = 'One palette pass from preserved v7 source; unchanged clean matte, registration and pose geometry.'

    (HERE/'checks.json').write_text(json.dumps(evidence,indent=2)+'\n')

    html='<!doctype html><meta charset="utf-8"><title>Veld fitting candidate</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:16px}a{color:#8cc6e7}</style><h1>Veld helmet fitting/removal — material palette review</h1><p>One material pass from the preserved source, using the accepted bare and helmet idle hair and skin palettes. Fixed clip-wide curves with explicit hair/skin masks and a continuous graphite cloth curve. Motion, clean matte, planted boots and exact idle endpoints preserved. Staged for visual review.</p>'

    for key in ['equip-helmet-east','remove-helmet-east']:

        html+=f'<h2>{key}</h2>'

        for height in [208,110,73,36]:html+=f'<img src="{key}-{REVIEW_VERSION}.gif" height="{height}">'

    html+=f'<p><a href="contact-{REVIEW_VERSION}.png">All fitting frames</a> / <a href="accepted-material-comparison-v13.png">Accepted animation comparison</a> / <a href="checks.json">Provenance and checks</a></p><p>Large images are diagnostic. Smaller images approximate standing heights of 82/54/27px. Interior pose continuity and final material matching remain subject to review.</p>'

    (HERE/'index.html').write_text(html,encoding='utf-8')

    print('Staged 8 fitting + 8 reversed removal frames; exact accepted endpoints, clipping and timing checks pass. Runtime unchanged.')



if __name__=='__main__':main()

