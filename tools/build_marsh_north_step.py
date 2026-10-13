"""Package whole authored North shuffle figures; never synthesize body parts."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-north-step-v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', choices=['01', '02', '03', '04', '05', '06'], required=True)
    args = parser.parse_args()
    name = 'north-step-' + args.version
    raw_path = BASE / 'sources' / (name + '.png')
    raw = Image.open(raw_path).convert('RGBA')
    cuts = [round(i * raw.width / 6) for i in range(7)]
    cells = []
    for i in range(6):
        a = np.array(raw.crop((cuts[i], 0, cuts[i+1], raw.height)))
        a[:,:,3] = np.where(a[:,:,3] >= 128, 255, 0)
        a[a[:,:,3] == 0] = 0
        cells.append(Image.fromarray(a))
    idle_path = ROOT / 'character/marsh-v2/frames/bare/idle-north/000.png'
    idle = Image.open(idle_path).convert('RGBA')
    neutral = cells[5].getbbox()
    scale = (idle.getbbox()[3] - idle.getbbox()[1]) / (neutral[3] - neutral[1])
    def contact(im, left):
        a = np.array(im); box = im.getbbox()
        xs = np.indices(a[:,:,3].shape)[1]
        split = (box[0]+box[2])/2
        mask = (a[:,:,3] > 0) & ((xs < split) if left else (xs > split))
        bottom = int(np.where(mask)[0].max())
        return [float(np.median(np.where(mask[bottom-5:bottom+1])[1])), bottom]
    frames = [idle]; extraction = []
    for i, im in enumerate(cells[:5]):
        left = i >= 3
        target = contact(idle, left); source = contact(im, left)
        offset = [round(target[k] - source[k]*scale) for k in range(2)]
        sized = im.resize((round(im.width*scale), round(im.height*scale)), Image.Resampling.BOX)
        a = np.array(sized); a[:,:,3] = np.where(a[:,:,3] >= 128, 255, 0); a[a[:,:,3] == 0] = 0
        frame = Image.new('RGBA', (184,184)); frame.alpha_composite(Image.fromarray(a), offset)
        box = frame.getbbox()
        assert box[0] > 0 and box[1] > 0 and box[2] < 184 and box[3] < 184
        frames.append(frame)
        extraction.append({'cell':i, 'supportSide':'left' if left else 'right', 'sourceContact':source, 'targetContact':target, 'offset':offset, 'bounds':box})
    frames.append(idle)
    output = BASE / ('candidate-' + args.version); output.mkdir(parents=True, exist_ok=True)
    files = []
    for i, frame in enumerate(frames):
        p = output / ('%03d.png' % i); frame.save(p); files.append(p.name)
    manifest = {'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'states':[{'id':'walk-step-north','frameFiles':files,'frameDurationsMs':[120]*7,'loop':False,'facings':['north']*7,'waterKinds':['walk']*7,'waterPoses':[False]*7,'depthOffsets':[0.0]*7}]}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    board = Image.new('RGB',(184*8,230),'#293b40'); draw = ImageDraw.Draw(board)
    for i, frame in enumerate([idle]+frames):
        board.paste(frame,(184*i,25),frame); draw.text((184*i+4,6),'Selected idle' if i==0 else 'Step %d' % (i-1), fill='white')
        draw.line((184*i,197,184*(i+1)-1,197),fill='#829496')
    board.save(output/'comparison.png')
    gif = []
    for frame in frames:
        canvas = Image.new('RGB',(368,368),'#293b40'); big = frame.resize((368,368),Image.Resampling.NEAREST); canvas.paste(big,(0,0),big); gif.append(canvas)
    gif[0].save(output/'step.gif',save_all=True,append_images=gif[1:],duration=[120]*7,loop=0)
    recipe = {'status':'unselected audition; choreography and native acceptance pending','raw':raw_path.relative_to(ROOT).as_posix(),'rawSha256':sha(raw_path),'promptSha256':sha(BASE/'sources'/(name+'.prompt.txt')),'sourceCellBoundaries':cuts,'neutralRulerCell':5,'standingScale':scale,'pivot':[92,172],'standingHeight':148,'extraction':extraction,'grade':'none','alpha':'128 then BOX then128; invisible RGB zero','frameHashes':{p:sha(output/p) for p in files},'limits':'Whole source poses; assumed support-contact alignment is packaging only. No actor travel/controller, natural route, production admission or Continue acceptance.'}
    (output/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    print(args.version, 'seven slots', 'widths', [f.getbbox()[2]-f.getbbox()[0] for f in frames], 'scale', round(scale,5))
if __name__ == '__main__': main()
