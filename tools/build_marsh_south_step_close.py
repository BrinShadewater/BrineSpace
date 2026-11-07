"""Package source05's complete closing figure; retain candidate04 otherwise."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw
from rebuild_bill_art import binary
from build_marsh_south_start import sole

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-south-step-v1'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    request_path = BASE / 'sources/step-05.request.json'
    raw_path = BASE / 'sources/step-05.raw.png'
    req = json.loads(request_path.read_text())
    assert sha(raw_path) == req['rawSha256']
    assert sha(BASE / 'sources/step-05.prompt.txt') == req['promptSha256']
    for ref in req['orderedReferences'] + req['guideSources']:
        assert sha(ROOT / ref['path']) == ref['sha256']
    raw = Image.open(raw_path).convert('RGBA')
    cuts = [(0, 0, raw.width // 2, raw.height), (raw.width // 2, 0, raw.width, raw.height)]
    cells = [binary(raw.crop(cut)) for cut in cuts]
    box = cells[1].getbbox()
    scale = 148 / (box[3] - box[1])
    previous = BASE / 'candidate-04'
    out = BASE / 'candidate-05'
    out.mkdir(exist_ok=True)
    idle = Image.open(previous / '000.png').convert('RGBA')
    retained = []
    for index in [0, 1, 2, 3, 4, 6]:
        src = previous / f'{index:03d}.png'
        (out / src.name).write_bytes(src.read_bytes())
        retained.append({'slot': index, 'wholeSource': src.relative_to(ROOT).as_posix(), 'sha256': sha(src)})
    records = []
    for index, cell in enumerate(cells):
        dense = binary(cell.resize((round(cell.width * scale), round(cell.height * scale)), Image.Resampling.BOX))
        support = True if index == 0 else None
        target, anchor = sole(idle, support), sole(dense, support)
        offset = [round(target[0] - anchor[0]), round(target[1] - anchor[1])]
        frame = Image.new('RGBA', (184, 184))
        frame.alpha_composite(dense, offset)
        assert np.count_nonzero(np.array(frame)[:, :, 3]) == np.count_nonzero(np.array(dense)[:, :, 3]), 'whole figure clipped'
        name = ['005.png', 'ruler.png'][index]
        frame.save(out / name)
        bounds = frame.getbbox()
        records.append({'file': name, 'sourceCell': cuts[index], 'commonNeutralScale': scale, 'wholeTranslation': offset, 'bounds': bounds, 'width': bounds[2] - bounds[0], 'height': bounds[3] - bounds[1], 'contacts': [sole(frame, True), sole(frame, False)], 'sha256': sha(out / name)})
    (out / 'manifest.json').write_bytes((previous / 'manifest.json').read_bytes())
    recipe = {'status': 'unselected complete closing correction; visual/contact review pending', 'normalAdmission': False, 'rawPath': raw_path.relative_to(ROOT).as_posix(), 'rawSha256': sha(raw_path), 'requestSha256': sha(request_path), 'commonNeutralScale': scale, 'retainedWholeSources': retained, 'records': records, 'grade': 'none; alpha128, one neutral-ruler BOX scale and complete-figure integer translation; no anatomy edits, mirror or per-pose fit', 'rootDenseAtHoldStart': [0, 0, 0, 0, 13, 13, 13], 'nominalWorldTravel': 13 * 65.28 / 148, 'limits': 'Source03 lift/plant, source04 reach, source05 close audition. Physical root, controller, safety, Continue and normal admission remain unimplemented.'}
    (out / 'recipe.json').write_text(json.dumps(recipe, indent=2) + '\n')
    frames = [Image.open(out / f'{i:03d}.png').convert('RGBA') for i in range(7)]
    board = Image.new('RGB', (184 * 8, 245), '#293b40')
    draw = ImageDraw.Draw(board)
    for i, frame in enumerate(frames + [Image.open(out / 'ruler.png')]):
        board.paste(frame, (184 * i, 40), frame)
        draw.text((184 * i + 3, 4), ['exact idle0', 'exact idle1', 'retained lift', 'retained reach', 'retained plant', 'NEW close', 'exact idle0', 'new neutral ruler'][i], fill='white')
        draw.text((184 * i + 3, 20), str([sole(frame, True), sole(frame, False)]), fill='#c3d8d3')
    board.save(out / 'comparison.png')
    frames[0].save(out / 'source-motion.apng', save_all=True, append_images=frames[1:], duration=[120] * 7, loop=0, disposal=1, blend=0)
    print(json.dumps({'commonScale': scale, 'widths': [r['width'] for r in records], 'contacts': [r['contacts'] for r in records], 'normalAdmission': False}))

if __name__ == '__main__':
    main()
