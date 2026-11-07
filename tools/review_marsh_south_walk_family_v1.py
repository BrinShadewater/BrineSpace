"""Package six coherent whole-pose edits, preserving native contract and alpha."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/marsh-south-walk-family-detail-v1'
INV = ROOT / 'character/marsh-selected-normal-audit-2026-10-03-post-north-walk/inventory.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
d = json.loads(INV.read_text())
frozen = json.loads((OUT / 'references.json').read_text())
assert sha(INV) == frozen['inventory']['sha256']
for entry in [d['catalog'], *d['orderedBodyManifests']]:
    assert sha(ROOT / entry['path']) == entry['sha256']
originals, revised, records = [], [], []
for slot, entry in enumerate(d['states']['walk-south']['frames']):
    source = ROOT / entry['path']
    assert sha(source) == entry['sha256']
    old = Image.open(source).convert('RGBA')
    rawpath = OUT / f'phase-{slot:03}.raw.png'
    raw = Image.open(rawpath).convert('RGBA')
    assert raw.width == raw.height
    frame = raw.resize((184, 184), Image.Resampling.LANCZOS)
    registration=None
    if slot==1:
        unregistered=OUT/'001.unregistered.png';frame.save(unregistered)
        arr=np.asarray(frame);assert not arr[-1,:,3].any()
        shifted=Image.new('RGBA',(184,184));shifted.paste(frame,(0,1))
        registered=np.asarray(shifted)
        assert np.array_equal(registered[1:],arr[:-1])
        assert int((registered[:,:,3]>0).sum())==int((arr[:,:,3]>0).sum())
        registration={'wholeRgbaTranslation':[0,1],'unregisteredSha256':sha(unregistered),'outgoingAlphaZero':True,'allSurvivingRgbaExact':True,'nonzeroAlphaPixelsUnchanged':True,'reason':'Recover original sole level; retain explicit1pixel crown residual without anatomy fitting.'}
        frame=shifted
    path = OUT / f'{slot:03}.png'
    frame.save(path)
    a, b = np.asarray(old)[:, :, 3] >= 128, np.asarray(frame)[:, :, 3] >= 128
    bounds = lambda m: Image.fromarray(m.astype('uint8') * 255).getbbox()
    ob, bb = bounds(a), bounds(b)
    records.append({'slot': slot, 'original': entry, 'rawPath': rawpath.relative_to(ROOT).as_posix(),
        'rawSha256': sha(rawpath), 'rawCanvas': list(raw.size), 'frameSha256': sha(path),
        'framePath': path.relative_to(ROOT).as_posix(), 'originalOpaqueBounds': ob, 'opaqueBounds': bb,
        'heightRatio': (bb[3]-bb[1])/(ob[3]-ob[1]), 'crownDisplacement': bb[1]-ob[1],
        'soleDisplacement': bb[3]-ob[3], 'opaqueIoU': int((a & b).sum())/int((a | b).sum()),
        'registration': registration,
        'method': 'Single whole-canvas184/raw-width resampling; generated alpha preserved. Phase1-only wholeRGBA Y+1, all pixels survive; no pose fit/pivot move/anatomy splice/recolour.',
        'reviewed': False, 'normalAdmission': False})
    originals.append(old)
    revised.append(frame)
board = Image.new('RGB', (6*184, 6*214), '#293b40')
draw = ImageDraw.Draw(board)
def place(im, col, row, label, pivot=(92, 172)):
    dx, dy = round(92-pivot[0]), round(172-pivot[1])
    board.paste(im, (col*184+dx, row*214+25+dy), im)
    draw.text((col*184+3, row*214+3), label, fill='white')
master = Image.open(ROOT / frozen['master']['path']).convert('RGBA')
master_rgb=np.asarray(master)[:,:,:3]
non_matte=~((master_rgb[:,:,0]>200)&(master_rgb[:,:,2]>200)&(master_rgb[:,:,1]<100))
master_bounds=Image.fromarray(non_matte.astype('uint8')*255).getbbox()
factor = 147/(master_bounds[3]-master_bounds[1])
master = master.resize((round(master.width*factor), round(master.height*factor)), Image.Resampling.LANCZOS)
board.paste(master, (31, 25+round(172-(master_bounds[3]-1)*factor)), master)
draw.text((3, 3), 'original master', fill='white')
idle = d['states']['idle-south']
place(Image.open(ROOT/idle['frames'][0]['path']).convert('RGBA'), 1, 0, 'own idle')
for col,direction in enumerate(['east','west','north'],2):
    place(Image.open(ROOT/f'character/marsh-v2/supplemental/{direction}-walk-polish-v1/000.png').convert('RGBA'), col, 0, f'selected {direction}0')
for slot in range(6):
    place(originals[slot], slot, 1, f'current walk /{slot}')
    place(revised[slot], slot, 2, f'family revision /{slot}')
for row, key in enumerate(['walk-start-south', 'idle-south', 'run-south'], 3):
    state = d['states'][key]
    for slot, entry in enumerate(state['frames']):
        assert sha(ROOT/entry['path']) == entry['sha256']
        place(Image.open(ROOT/entry['path']).convert('RGBA'), slot, row, f'{key} /{slot}', state['pivot'])
board.save(OUT/'family-joins-native.png')
# Exact head neighborhoods for diagnosis only; never used as replacement art.
head = Image.new('RGB', (6*170, 3*110), '#293b40')
hd = ImageDraw.Draw(head)
for row, images in enumerate([originals, revised, [Image.open(ROOT/idle['frames'][0]['path']).convert('RGBA')]*6]):
    for slot, im in enumerate(images):
        crop = im.crop((50, 12, 135, 57)).resize((170, 90), Image.Resampling.NEAREST)
        head.paste(crop, (170*slot, 110*row+20), crop)
        hd.text((170*slot+3, 110*row+3), ['current', 'revision', 'ownidle'][row]+f' /{slot}', fill='white')
head.save(OUT/'heads-2x.png')
durations = d['states']['walk-south']['state']['frameDurationsMs']
# APNG review media with exact authored durations and no frame-bound fitting.
rgb = []
for im in revised:
    bg = Image.new('RGBA', (184,184), '#293b40');bg.alpha_composite(im);rgb.append(bg)
rgb[0].save(OUT/'walk-review.png', save_all=True, append_images=rgb[1:], duration=durations, loop=0, disposal=0, blend=0)
state = dict(d['states']['walk-south']['state'])
state['frameFiles'] = ['res://' + (OUT / f'{i:03}.png').relative_to(ROOT).as_posix() for i in range(6)]
states=[state];aliases=[]
for phase in range(6):
    key='walk-stop-phase%d-south'%phase
    old=d['states'][key];s=dict(old['state']);s['frameFiles']=['res://'+x['path'] for x in old['frames']]
    s['frameFiles'][0]=state['frameFiles'][phase];states.append(s)
    aliases.append({'key':key,'slot':0,'walkingPhase':phase,'oldFrame':old['frames'][0],'unchangedLaterFrames':old['frames'][1:]})
old=d['states']['walk-start-south'];s=dict(old['state']);s['frameFiles']=['res://'+x['path'] for x in old['frames']];s['frameFiles'][4]=state['frameFiles'][4];states.append(s)
aliases.append({'key':'walk-start-south','slot':4,'walkingPhase':4,'oldFrame':old['frames'][4],'unchangedEarlierFrames':old['frames'][:4]})
(OUT/'manifest.json').write_text(json.dumps({'pivot':[92,172],'standingHeight':148,'states':states},indent=2)+'\n')
(OUT/'transition-aliases.json').write_text(json.dumps({'normalAdmission':False,'records':aliases,'method':'Exact walking duplicates proven before edits; stage six stop0aliases and start4alias while keeping other transition drawings and timing.'},indent=2)+'\n')
(OUT/'review.json').write_text(json.dumps({'scope':'Six-phase whole-pose family study; normal selection unchanged; held/native-density/head review and APNG media do not establish native/cadence acceptance.',
    'records': records, 'durationsMs': durations, 'masterDisplayScale':factor,'masterForegroundDisplayBounds':master_bounds,'masterDisplayMethod':'Fixed147/sourceMasterForegroundHeight display ruler; magenta retained in unpainted reference, no candidate pose fitting.', 'normalAdmission':False,
    'boards':[{'path':p.relative_to(ROOT).as_posix(), 'sha256':sha(p), 'reviewed':False} for p in [OUT/'family-joins-native.png', OUT/'heads-2x.png']],
    'fullGoalComplete':False}, indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['slot','opaqueBounds','heightRatio','crownDisplacement','soleDisplacement','opaqueIoU']} for r in records]))

stop_board=Image.new('RGB',(6*184,12*214),'#293b40');sd=ImageDraw.Draw(stop_board)
for phase in range(6):
    old=d['states']['walk-stop-phase%d-south'%phase]
    for row,version in [(phase*2,'original'),(phase*2+1,'proposed')]:
        for slot,entry in enumerate(old['frames']):
            im=revised[phase] if version=='proposed' and slot==0 else Image.open(ROOT/entry['path']).convert('RGBA')
            stop_board.paste(im,(slot*184,row*214+25),im);sd.text((slot*184+3,row*214+3),f'p{phase} {version} stop/{slot}',fill='white')
stop_board.save(OUT/'phase-stop-joins-native.png')
closing=Image.new('RGB',(8*184,3*214),'#293b40');cd=ImageDraw.Draw(closing)
for col,phase in enumerate([5,0,1,2,3,4,5,0]):
    for row,im in [(0,originals[phase]),(1,revised[phase]),(2,revised[phase])]:
        cd.text((col*184+3,row*214+3),f'phase{phase} '+['original','proposed','fixed station density'][row],fill='white')
        if row<2:closing.paste(im,(col*184,row*214+25),im)
        else:
            factor=65.28/148;small=im.resize((round(184*factor),round(184*factor)),Image.Resampling.LANCZOS)
            closing.paste(small,(col*184+92-round(92*factor),row*214+25+172-round(172*factor)),small)
closing.save(OUT/'closing-join-station.png')
