"""Package whole-figure east actions; no limb or helmet transplantation."""
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_dilation, label

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = HERE / 'sources/actions.png'
IDLE = ROOT / 'bill-shared-helmet-east-matte-v1/frames/idle-east/000.png'


def grade_materials(pixels, mask, top):
    """One fixed source-space grade, with spatially separated face/patch masks."""
    out = pixels.copy()
    rgb = pixels[:, :, :3].astype(float)
    r, g, b = rgb.transpose(2, 0, 1)
    luma = rgb.mean(2)
    yy, xx = np.indices(luma.shape)
    head_y, head_x = np.where(mask & (yy < top+50))
    face_region = (xx > head_x.min()+(head_x.max()-head_x.min())*0.56) & (yy >= top+23) & (yy < top+82)
    valid = pixels[:,:,3] > 0
    warm = np.clip((r-g-8)/14,0,1)*np.clip((r-b-10)/18,0,1)
    skin = valid * face_region * warm * np.clip((luma-55)/25,0,1)
    patch = valid * (~face_region) * (yy >= top+57) * warm
    neutral = valid * (1-np.clip((rgb.max(2)-rgb.min(2)-10)/18,0,1))
    metal = neutral * np.clip((luma-72)/24,0,1)
    shell = neutral * (yy < top+76) * (1-metal) * (1-skin) * (1-patch)
    cloth = neutral * (yy >= top+76) * (1-metal) * (1-patch)
    graded = rgb.copy()
    # Retain shading; change material color, not exposure per pose.
    for weight, target in [
        (cloth, rgb + np.array([1,-1,0]) - 1.5),
        (shell, rgb + 3.5),
        (metal, luma[:,:,None]*1.03 + np.array([10,7,6])),
        (patch, rgb*np.array([0.88,0.95,1.12])),
        (skin, rgb*np.array([0.77,0.88,0.96])),
    ]:
        graded = graded*(1-weight[:,:,None])+target*weight[:,:,None]
    out[:,:,:3] = np.clip(graded,0,255).astype('uint8')
    out[~valid] = 0
    assert np.array_equal(out[:,:,3],pixels[:,:,3])
    # Diagnostic mask: skin green, burgundy red, silver blue, shell/cloth gray.
    diagnostic = np.zeros_like(out)
    diagnostic[:,:,:3] = np.clip(np.stack((patch*255+neutral*45,skin*255+neutral*45,metal*255+neutral*45),axis=2),0,255).astype('uint8')
    diagnostic[:,:,3] = out[:,:,3]
    return out, diagnostic


def main():
    rgba = np.asarray(Image.open(SOURCE).convert('RGBA')).copy()
    labels, _ = label(rgba[:, :, 3] > 180)
    counts = np.bincount(labels.ravel())
    ids = [int(i) for i in range(1, len(counts)) if counts[i] > 10000]
    assert len(ids) == 18, len(ids)
    poses = []
    for ident in ids:
        yy, xx = np.where(labels == ident)
        poses.append((int(yy.min()), int(xx.min()), ident))
    poses.sort()
    ordered = []
    for row in range(3):
        ordered += sorted(poses[row*6:(row+1)*6], key=lambda p: p[1])
    idle = Image.open(IDLE).convert('RGBA')
    # A staged idle color variant keeps the shell grade consistent at endpoints.
    # The installed idle remains untouched; preserve face, visor, lamp and trim.
    idle_rgba = np.asarray(idle).copy()
    yy, xx = np.indices((184,184))
    rgb = idle_rgba[:,:,:3].astype(float)
    luma = rgb.mean(2)
    shell = (yy < 51) & (idle_rgba[:,:,3] > 0) & (luma < 85)
    shell &= ~((xx >= 89) & (yy >= 30))
    shell &= ~((xx >= 99) & (yy < 29))
    idle_rgba[shell,:3] = np.clip(rgb[shell]*0.92,0,255).astype('uint8')
    idle = Image.fromarray(idle_rgba)
    idle.save(HERE/'review-idle-darkened.png')
    ay, ax = np.where(np.asarray(idle)[:, :, 3] > 180)
    first = ordered[0][2]
    sy, sx = np.where(labels == first)
    scale = (ay.max()-ay.min()+1)/(sy.max()-sy.min()+1)
    # The generated source is wider through helmet/legs and slightly taller
    # than the selected idle. Calibrate once for the entire sheet, including
    # crouched poses: never normalize each pose's changing bounds.
    scale_x = scale * 0.85
    scale_y = scale * 0.99
    target_boot = float(np.median(ax[(ay >= ay.max()-6) & (ax > np.median(ax))]))
    target_ground = int(ay.max())
    frames = []
    records = []
    for n, (_, _, ident) in enumerate(ordered):
        mask = labels == ident
        ys, xs = np.where(mask)
        # Keep this component's original soft alpha edge, exclude stray pixels.
        edge = binary_dilation(mask, iterations=2)
        pixels = rgba.copy()
        pixels[~edge] = 0
        pixels, diagnostic = grade_materials(pixels, mask, int(ys.min()))
        if n in (0, 1, 7, 12):
            diagnostic_dir = HERE/'review-masks'
            diagnostic_dir.mkdir(exist_ok=True)
            Image.fromarray(diagnostic).crop((int(xs.min()-3),int(ys.min()-3),int(xs.max()+4),int(ys.max()+4))).save(diagnostic_dir/f'{n:02d}.png')
        # White lamp only: restrict to the top 22 source pixels, above the face.
        rgb = pixels[:, :, :3].astype(float)
        lamp = edge & (np.indices(mask.shape)[0] < ys.min()+22) & (rgb[:,:,0] > rgb[:,:,1]*1.15) & (rgb[:,:,0] > 80)
        light = np.clip(rgb.mean(2)*1.18, 0, 255).astype('uint8')
        pixels[lamp, :3] = light[lamp, None]
        foot = (ys >= ys.max()-10) & (xs > np.median(xs))
        boot_x = float(np.median(xs[foot]))
        x0, y0, x1, y1 = int(xs.min()-3), int(ys.min()-3), int(xs.max()+4), int(ys.max()+4)
        crop = Image.fromarray(pixels).crop((x0,y0,x1,y1))
        crop = crop.resize((round(crop.width*scale_x), round(crop.height*scale_y)), Image.Resampling.LANCZOS)
        dst = Image.new('RGBA', (184,184))
        position = (round(target_boot-(boot_x-x0)*scale_x), round(target_ground-(ys.max()-y0)*scale_y))
        assert position[0] >= 0 and position[1] >= 0
        assert position[0]+crop.width <= 184 and position[1]+crop.height <= 184
        dst.alpha_composite(crop, position)
        frames.append(dst)
        records.append({'sourceCell': n, 'component':ident, 'sourceBox':[x0,y0,x1,y1], 'frontBootX':boot_x, 'position':list(position)})
    # Keep the selected helmet design, but register it to the complete source
    # pose's head position: the authored shoulders/torso sway during the reach.
    # An absolute idle-position lock detached the head from that moving body.
    idle_pixels = np.asarray(idle)
    head_region = np.indices((184,184))[0] < 50
    iy, ix = np.where((idle_pixels[:,:,3] > 200) & head_region)
    idle_center = (int(ix.min())+int(ix.max()))/2
    helmet_registrations = []
    for i,im in enumerate(frames[1:5],start=1):
        authored = np.asarray(im)
        hy, hx = np.where((authored[:,:,3] > 200) & head_region)
        dx = round((int(hx.min())+int(hx.max()))/2-idle_center)
        dy = int(hy.min())-int(iy.min())
        translated = Image.new('RGBA',(184,58))
        translated.paste(idle.crop((0,0,184,58-dy)),(dx,dy))
        # Below the rear shell, keep the authored moving shoulder, never the
        # idle shoulder that previously crossed the raised arm's root.
        helmet_mask = Image.new('L',(184,58))
        polygon = [(72,0),(114,0),(114,51),(110,55),(101,58),
                   (90,55),(82,51),(75,48),(72,43)]
        ImageDraw.Draw(helmet_mask).polygon([(x+dx,y+dy) for x,y in polygon],fill=255)
        band = translated.copy()
        # Restore original shoulders outside the helmet below row 47. Above
        # this band keep transparency to avoid remnants of the generated shell.
        blend = np.asarray(helmet_mask).copy()
        blend[:47] = 255
        band = Image.composite(translated,im.crop((0,0,184,58)),Image.fromarray(blend))
        im.paste(band,(0,0))
        helmet_registrations.append({'frame':i,'offset':[dx,dy],'sourceHeadCenter':(int(hx.min())+int(hx.max()))/2,'method':'translated selected helmet/neck only; authored moving shoulders preserved; shell RGB factor 0.92'})
    (HERE/'helmet-registration.json').write_text(json.dumps(helmet_registrations,indent=2)+'\n')
    chains = {
        'interact-east': [idle, *frames[1:5], idle],
        'kneel-east': [idle, *frames[7:11], frames[12]],
        'repair-east': frames[12:18],
        # Reverse descent retains connected body poses and returns to exact idle.
        'stand-east': [frames[17], *reversed(frames[7:11]), idle],
    }
    old = json.loads((ROOT/'bill-shared-helmet-actions-east-v1/manifest.json').read_text())
    manifest = {k:v for k,v in old.items() if k != 'states'}
    manifest.update(name='Bill whole-figure east action candidate v5', status='owner_review_pending', states=[])
    for state in old['states']:
        state = copy.deepcopy(state)
        key = state['id']
        directory = HERE/'frames'/key
        directory.mkdir(parents=True,exist_ok=True)
        state['frameFiles'] = []
        for i, im in enumerate(chains[key]):
            dest = directory/f'{i:03d}.png'
            im.save(dest)
            state['frameFiles'].append(dest.relative_to(HERE).as_posix())
        state['provenance'] = 'whole-figure generated source; fixed scale; front boot registration; exact selected idle endpoints; stand reverses descent'
        manifest['states'].append(state)
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (HERE/'source-registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scale':scale,'scaleX':scale_x,'scaleY':scale_y,'proportionCorrection':[0.85,0.99],'targetFrontBoot':target_boot,'targetGround':target_ground,'frames':records},indent=2)+'\n')
    sheet = Image.new('RGB',(1104,736),(34,48,56))
    draw = ImageDraw.Draw(sheet)
    for r,(key,images) in enumerate(chains.items()):
        for i,im in enumerate(images):
            sheet.paste(im,(184*i,184*r),im)
            draw.text((184*i+3,184*r+3),f'{key} {i}',fill='white')
    sheet.save(HERE/'contact-sheet.png')
    assert chains['kneel-east'][-1].tobytes() == chains['repair-east'][0].tobytes()
    assert chains['repair-east'][-1].tobytes() == chains['stand-east'][0].tobytes()
    assert chains['interact-east'][0].tobytes() == chains['interact-east'][-1].tobytes() == idle.tobytes()
    print('18 source poses; 24 packaged frames; exact idle and kneel/repair/stand joins; no clipping')


if __name__ == '__main__':
    main()
