from pathlib import Path
import copy, json, hashlib, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

P = Path(__file__).resolve().parent
R = P.parent.parent
SOURCE = R / 'character/james-diagnostics-edge-matte-v30/bare-manifest.json'
CANON = R / 'character/krusher-james-canonical-v1'
for name in ['frames/interact-north', 'masks', 'review', 'native']:
    (P / name).mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
m = json.loads(SOURCE.read_text())
state = copy.deepcopy(next(s for s in m['states'] if s['id'] == 'interact-north'))
head_path = CANON / 'sources/north-head-native.png'
head = Image.open(head_path).convert('RGBA')
yy, xx = np.indices((184, 184))
h = np.array(head)
hy, hx = np.where((h[:, :, 3] > 150) & (np.indices(h.shape[:2])[0] >= head.height - 5))
head_axis = head.width // 2
head_paths = {'rear': 'character/krusher-james-canonical-v1/sources/north-head-native.png', 'turn1': 'character/krusher-north-head-turn-v1/six-view-1.png', 'turn2': 'character/krusher-north-head-turn-v1/six-view-2.png', 'turn3': 'character/krusher-north-head-turn-v1/six-view-3.png', 'turn4': 'character/krusher-north-head-turn-v1/six-view-4.png', 'turn5': 'character/krusher-north-head-turn-v1/six-view-5.png'}
heads = {key: Image.open(R / path).convert('RGBA') for key,path in head_paths.items()}
def head_view(i):
    if i <= 5 or i >= 131: return 'rear'
    if i <= 10 or i >= 127: return 'turn1'
    if i <= 15 or i >= 124: return 'turn2'
    if i <= 20 or i >= 121: return 'turn3'
    if i <= 26 or i >= 118: return 'turn4'
    return 'turn5'

def registration(a):
    top = int(np.where((a[:, :, 3] > 180) & (yy < 44) & (xx > 70) & (xx < 110))[0].min())
    ys, xs = np.where((a[:, :, 3] > 180) & (yy >= top) & (yy < top + 19) & (xx > 70) & (xx < 110))
    return top, round((int(xs.min()) + int(xs.max())) / 2)

reference = np.array(Image.open(R / state['frameFiles'][0][6:] if state['frameFiles'][0].startswith('res://') else SOURCE.parent / state['frameFiles'][0]).convert('RGBA'))
base_top, base_axis = registration(reference)
target = np.array([82., 124., 128.])
luma = np.array([.2126, .7152, .0722])
records, outputs, originals, files, errors = [], [], [], [], []
checks = 0
for i, relative in enumerate(state['frameFiles']):
    source = (R / relative[6:] if relative.startswith('res://') else SOURCE.parent / relative).resolve()
    original = Image.open(source).convert('RGBA')
    a = np.array(original)
    top, axis = registration(a)
    dy = top - base_top
    collar = (yy >= 45 + dy) & (yy < 54 + dy)
    collar &= a[:, :, 3] > 0
    # The North tablet stays below the head region. Protect its cool grey surface.
    head_edit = (yy < 54 + dy) & (~collar) & ((xx < 108) | ((xx < 112) & (yy < 45 + dy)))
    layer = a.copy()
    layer[head_edit] = 0
    image = Image.fromarray(layer)
    view = head_view(i)
    head = heads[view]
    anchor = [axis - head.width // 2, 45 + dy - head.height]
    image.paste(head, tuple(anchor))
    b = np.array(image)
    b[collar] = a[collar]
    rgb = b[:, :, :3].astype(float)
    yellow = (rgb[:, :, 0] > rgb[:, :, 2] * 1.15) & (rgb[:, :, 1] > rgb[:, :, 2] * 1.12) & (rgb[:, :, 0] > 35) & (rgb[:, :, 1] > rgb[:, :, 0] * .65)
    marking = yellow & (b[:, :, 3] > 0) & (~head_edit) & (yy >= 44 + dy) & (yy < 85 + dy) 
    gain = np.minimum(1.15, (rgb @ luma) / (target @ luma))
    colours = np.rint(gain[:, :, None] * target).astype('uint8')
    b[marking, :3] = colours[marking]
    allowed = head_edit | marking
    checks += 3
    if not np.array_equal(a[~allowed], b[~allowed]): errors.append('protected:' + str(i))
    if not np.array_equal(a[54 + max(dy, 0):, :, 3], b[54 + max(dy, 0):, :, 3]): errors.append('body-alpha:' + str(i))
    src_rgb=a[:,:,:3].astype(float)
    tablet=(xx>=108)&(xx<135)&(yy>=48)&(yy<100)&(a[:,:,3]>0)&(src_rgb.mean(2)>65)&(np.max(src_rgb,axis=2)-np.min(src_rgb,axis=2)<14)&(src_rgb[:,:,2]>=src_rgb[:,:,0])
    if not np.array_equal(a[tablet],b[tablet]):errors.append('tablet:'+str(i))
    file = f'frames/interact-north/{i:03}.png'
    out = Image.fromarray(b)
    out.save(P / file)
    mask = f'masks/{i:03}-allowed.png'
    Image.fromarray(allowed.astype('uint8') * 255).save(P / mask)
    tablet_mask=f'masks/{i:03}-tablet.png'
    Image.fromarray(tablet.astype('uint8')*255).save(P/tablet_mask)
    marking_mask = f'masks/{i:03}-markings.png'
    Image.fromarray(marking.astype('uint8') * 255).save(P / marking_mask)
    records.append({'source': source.relative_to(R).as_posix(), 'sourceHash': sha(source), 'output': file, 'outputHash': sha(P / file), 'mask': mask, 'markingMask': marking_mask, 'tabletMask': tablet_mask, 'headView': view, 'headPaste': anchor, 'headShift': [axis - base_axis, dy], 'markingPixels': int(marking.sum())})
    files.append(file); outputs.append(out); originals.append(original)
state['frameFiles'] = files
out_m = copy.deepcopy(m)
out_m['states'] = [state]
out_m['name'] = 'Krusher Dom / North tablet lift read stow'
out_m['status'] = 'Six-view head turn candidate; temporal review pending; selected James utility base'
out_m['identity'] = json.loads((CANON / 'bare-manifest.json').read_text())['identity']
(P / 'bare-manifest.json').write_text(json.dumps(out_m, indent=2) + '\n', encoding='utf-8')
idle_path = CANON / 'frames/bare/idle-north/000.png'
idle = np.array(Image.open(idle_path).convert('RGBA'))
endpoints = {name: int(np.any(np.array(outputs[i]) != idle, axis=2).sum()) for name, i in [('start', 0), ('return', len(outputs) - 1)]}
checks += 2
if any(endpoints.values()): errors.append('canonical idle endpoint mismatch')
report = {'checks': checks, 'errors': errors, 'sourceManifest': SOURCE.relative_to(R).as_posix(), 'sourceManifestHash': sha(SOURCE), 'headSource': head_path.relative_to(R).as_posix(), 'headSourceHash': sha(head_path), 'canonicalIdle': idle_path.relative_to(R).as_posix(), 'canonicalIdleHash': sha(idle_path), 'endpointPixelDifferences': endpoints, 'records': records, 'headViewScope': 'Six authored views at a common extraction scale, source pose bands; source micro-pitch not independently reconstructed', 'scope': 'Full source motion preserved outside head/marking masks, source clocks retained, central cool grey tablet surface protected; no normal selection'}
report['headSources'] = {name: {'path': path, 'sha256': sha(R / path)} for name, path in head_paths.items()}
(P / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
font = lambda n: ImageFont.truetype(str(R / 'assets/fonts/BarlowSemiCondensed-Regular.ttf'), n)
sheet = Image.new('RGB', (1600,650), '#272b2e'); d = ImageDraw.Draw(sheet)
d.text((24,12), 'KRUSHER DOM / NORTH TABLET ACTION / JAMES UTILITY SUIT', font=font(30), fill='white')
for col, i in enumerate([0, 18, 68, 136]):
    tile = outputs[i].resize((368,368), Image.Resampling.NEAREST); sheet.paste(tile,(col*400,65),tile)
    d.text((col*400+18,435), f'Frame {i}', font=font(24), fill='white')
    small = outputs[i].resize((92,92),Image.Resampling.LANCZOS);sheet.paste(small,(col*400+145,485),small)
d.text((24,605), 'Source lift/read/stow / 137 poses / 5.5 seconds / no reversed lift or deleted frames',font=font(23),fill='#bdcdd0')
sheet.save(P/'review/key-poses.png')
outputs[0].save(P/'review/action.png',save_all=True,append_images=outputs[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
video=P/'review/action-preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','800x600','-framerate','60','-i','-','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
ends=np.cumsum(state['frameDurationsMs'])
for j in range(math.ceil(ends[-1]*60/1000)):
    i=min(int(np.searchsorted(ends,j*1000/60,side='right')),len(ends)-1)
    board=Image.new('RGB',(800,600),'#272b2e');d=ImageDraw.Draw(board);d.text((20,12),'KRUSHER DOM / NORTH TABLET ACTION',font=font(30),fill='white')
    for col,(label,im) in enumerate([('James source',originals[i]),('Krusher candidate',outputs[i])]):
        d.text((25+col*390,52),label,font=font(23),fill='white');tile=im.resize((368,368),Image.Resampling.NEAREST);board.paste(tile,(10+col*390,83),tile);small=im.resize((92,92),Image.Resampling.LANCZOS);board.paste(small,(150+col*390,453),small)
    d.text((20,557),'5.5s source clock / tablet and glove motion retained',font=font(23),fill='#bdcdd0');proc.stdin.write(board.tobytes())
proc.stdin.close();assert proc.wait()==0
print(json.dumps({'frames':len(records),'checks':checks,'errors':errors,'endpointPixelDifferences':endpoints,'videoBytes':video.stat().st_size}));assert not errors
