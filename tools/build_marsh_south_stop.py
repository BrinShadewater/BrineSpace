"""Package a whole-figure South stop study; never alter normal art."""
from pathlib import Path
import hashlib
import json
import argparse
import shutil
import numpy as np
from PIL import Image, ImageDraw
from rebuild_bill_art import binary
from build_marsh_south_start import sole

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-south-stop-v1'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stage_shared_stop(phase, source_phase, version):
    source = BASE / f'candidate-{version}/phase-{source_phase}'
    out = BASE / f'candidate-{version}/phase-{phase}'
    out.mkdir(parents=True, exist_ok=True)
    gait = ROOT / f'character/marsh-south-walk-material-v1/candidate-02/{phase:03d}.png'
    (out/'000.png').write_bytes(gait.read_bytes())
    for file in ['001.png', '002.png', '003.png', '004.png', 'ruler.png']:
        shutil.copyfile(source/file, out/file)
    manifest = json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    manifest['states'][0]['id'] = f'walk-stop-phase{phase}-south'
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    frames = [Image.open(out/f'{i:03d}.png').convert('RGBA') for i in range(5)]
    recipe = {'status':'shared whole-pose source study; visual review pending',
              'sourceBank':source.relative_to(ROOT).as_posix(),
              'sourceRecipeSha256':sha(source/'recipe.json'),
              'gaitPath':gait.relative_to(ROOT).as_posix(), 'gaitSha256':sha(gait),
              'newAuthoredInteriors':0, 'sharedAuthoredInteriors':3,
              'grade':f'none; byte-exact authored phase{source_phase} bank, no anatomical/palette changes',
              'frameHashes':{f'{i:03d}.png':sha(out/f'{i:03d}.png') for i in range(5)},
              'contacts':[[sole(frame,True),sole(frame,False)] for frame in frames],
              'limits':'Staged source only. Same recovering-foot side; near-contact phases2/5 have2dense sole-depth settle at entry. No controller/native/save admission; full-family width/detail/terminal seam polish pending.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n',encoding='utf-8')
    board=Image.new('RGB',(184*6,220),'#293b40');draw=ImageDraw.Draw(board)
    for i,frame in enumerate(frames+[Image.open(out/'ruler.png')]):
        board.paste(frame,(184*i,30),frame)
        draw.text((184*i+4,6),f'exact gait{phase}' if i==0 else 'exact idle' if i==4 else 'ruler' if i==5 else f'shared interior{i}',fill='white')
    board.resize((board.width*2,board.height*2),Image.Resampling.NEAREST).save(out/'comparison-2x.png')
    frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[80]*5,loop=0,disposal=1,blend=0)
    print(json.dumps({'sharedAuthoredInteriors':3,'newAuthoredInteriors':0,'contacts':recipe['contacts']}))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', choices=['01', '02', '03', '04', '05', '06', '07'], default='07')
    parser.add_argument('--phase', type=int, choices=range(6), default=4)
    parser.add_argument('--shared-phase0', action='store_true', help='Stage phase1/2 using the authored phase0 source06 recovery bank')
    parser.add_argument('--shared-phase3', action='store_true', help='Stage phase5 using the authored phase3 source01 recovery bank')
    args = parser.parse_args()
    if args.shared_phase0:
        assert args.phase in [1, 2] and args.version == '06' and not args.shared_phase3
        stage_shared_stop(args.phase, 0, '06')
        return
    if args.shared_phase3:
        assert args.phase == 5 and args.version == '01'
        stage_shared_stop(5, 3, '01')
        return
    assert args.phase == 4 or args.phase == 0 and args.version in ['01', '02', '03', '04', '05', '06'] or args.phase == 1 and args.version in ['01', '02'] or args.phase == 3 and args.version == '01', 'source not authored'
    raw_path = BASE / f'sources/stop-phase{args.phase}-{args.version}.raw.png'
    raw = Image.open(raw_path).convert('RGBA')
    cells, cuts = [], []
    columns, rows = (3, 2) if args.version == '01' and args.phase == 4 else (4, 1)
    for row in range(rows):
        for col in range(columns):
            cut = [round(col*raw.width/columns), round(row*raw.height/rows),
                   round((col+1)*raw.width/columns), round((row+1)*raw.height/rows)]
            if args.phase == 1:
                # Source01 reflowed its figures. Inspected gutters supersede equal cells.
                boundaries = [0, 590, 1020, 1450, raw.width]
                cut = [boundaries[col], 0, boundaries[col+1], raw.height]
            cells.append(binary(raw.crop(cut))); cuts.append(cut)
    gait_path = ROOT / f'character/marsh-south-walk-material-v1/candidate-02/{args.phase:03d}.png'
    idle_path = ROOT / ('character/marsh-south-idle-material-v1/candidate-01/000.png' if args.phase in [0, 1, 3] or args.version in ['04','05','06','07'] else 'character/marsh-v2/frames/bare/idle-south/000.png')
    gait = Image.open(gait_path).convert('RGBA')
    idle = Image.open(idle_path).convert('RGBA')
    neutral_index = len(cells)-1
    box = cells[neutral_index].getbbox()
    scale = 148 / (box[3]-box[1])
    out = BASE / f'candidate-{args.version}/phase-{args.phase}'; out.mkdir(parents=True, exist_ok=True)
    frames, records = [gait], []
    for index, cell in enumerate(cells):
        dense = binary(cell.resize((round(cell.width*scale), round(cell.height*scale)), Image.Resampling.BOX), True)
        # Only translate complete figures; phase0 reverses the supporting side.
        late = index >= (1 if args.phase in [0, 1, 3] else 3 if args.version == '01' else 1 if args.version in ['05','06','07'] else 2)
        left = not late if args.phase in [0, 1] else late
        target = sole(idle if late else gait, left)
        anchor = sole(dense, left)
        offset = [round(target[0]-anchor[0]), round(target[1]-anchor[1])]
        frame = Image.new('RGBA', (184, 184)); frame.alpha_composite(dense, offset)
        assert np.count_nonzero(np.array(frame)[:,:,3]) == np.count_nonzero(np.array(dense)[:,:,3]), 'whole figure clipping'
        path = out / ('ruler.png' if index == neutral_index else f'{index+1:03d}.png')
        frame.save(path)
        if index < neutral_index: frames.append(frame)
        mask = np.array(frame)[:,:,3] > 0; mask[50:] = False
        hy, hx = np.where(mask)
        records.append({'cell': cuts[index], 'wholeFigureOffset': offset,
                        'supportSide': 'viewer-left' if left else 'viewer-right',
                        'supportTarget': target, 'bounds': frame.getbbox(),
                        'leftSole': sole(frame, True), 'rightSole': sole(frame, False),
                        'headAlphaCentroid': [float(hx.mean()), float(hy.mean())],
                        'sha256': sha(path)})
    frames.append(idle)
    files = []
    for index, frame in enumerate(frames):
        path = out / f'{index:03d}.png'; frame.save(path); files.append(path.name)
    # Endpoints are exact source files, including their original PNG encoding.
    (out/files[0]).write_bytes(gait_path.read_bytes())
    (out/files[-1]).write_bytes(idle_path.read_bytes())
    manifest = {'frameWidth':184, 'frameHeight':184, 'pivot':[92,172], 'standingHeight':148,
                'states':[{'id':f'walk-stop-phase{args.phase}-south', 'frameFiles':files,
                           'frameDurationsMs':[80]*len(frames), 'loop':False, 'facings':['south']*len(frames),
                           'waterKinds':['walk']*len(frames), 'waterPoses':[False]*len(frames), 'depthOffsets':[0.0]*len(frames)}]}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    recipe = {'status':'unselected study; visual/contact acceptance pending',
              'rawSha256':sha(raw_path), 'sharedNeutralScale':scale, 'neutralCell':neutral_index,
              'gaitPath':gait_path.relative_to(ROOT).as_posix(), 'gaitSha256':sha(gait_path),
              'idlePath':idle_path.relative_to(ROOT).as_posix(), 'idleSha256':sha(idle_path),
              'grade':'none', 'cells':records,
              'frameHashes':{file:sha(out/file) for file in files},
              'limits':'Whole figures only; no independent anatomy/scale edits. Source support targets are a study, not a validated root/controller. No native, arbitrary phase, safety, save, title Continue or normal admission.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n', encoding='utf-8')
    board=Image.new('RGB',(184*(len(frames)+1),220),'#293b40'); draw=ImageDraw.Draw(board)
    for index, frame in enumerate(frames+[Image.open(out/'ruler.png')]):
        board.paste(frame,(184*index,30),frame)
        label = f'exact gait{args.phase}' if index == 0 else 'exact idle' if index == len(frames)-1 else 'ruler' if index == len(frames) else f'interior{index}'
        draw.text((184*index+4,6),label,fill='white')
    board.resize((board.width*2,board.height*2),Image.Resampling.NEAREST).save(out/'comparison-2x.png')
    frames[0].save(out/'source-motion.apng', save_all=True, append_images=frames[1:], duration=[80]*len(frames), loop=0, disposal=1, blend=0)
    print(json.dumps({'scale':scale,'bounds':[frame.getbbox() for frame in frames],
                      'contacts':[[sole(frame,True),sole(frame,False)] for frame in frames]}))

if __name__ == '__main__':
    main()
