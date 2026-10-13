"""Diagnose shared-ruler East profile widths and request a whole-source correction."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-retained-gesture-material-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    paths={'own':ROOT/'character/marsh-v2/frames/bare/idle-east/000.png',
           'neutral':BASE/'east03-unselected/neutral-ruler.png',
           'gesture0':BASE/'east03-unselected/gesture-00.png'}
    diagnostics={}
    for key,path in paths.items():
        a=np.array(Image.open(path).convert('RGBA'));regions={}
        for name,y0,y1 in [('head',25,58),('torso',58,99),('pelvis',99,121),('legs',121,159),('boots',159,174)]:
            y,x=np.where(a[y0:y1,:,3]>80);assert len(x)
            regions[name]={'rows':[y0,y1],'span':[int(x.min()),int(x.max()+1)],'width':int(x.max()+1-x.min())}
        diagnostics[key]={'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'regions':regions}
    (BASE/'inputs/east04-region-widths.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
    prompt='''Edit SECOND image, five East-facing Marsh whole figures in one horizontal row on transparent background. FIRST image is exact current East idle enlarged3x, primary silhouette/perspective/material reference. The current upper body already matches it closely: head27vs28px, torso30vs30, pelvis26vs26 at runtime scale. Preserve the current SECOND head, face, bare near LEFT temple, shoulder/torso, compact bent-glove gestures and muted matte ivory/sage/charcoal materials; do not widen or shrink upper body. Correct the lower-leg and boot silhouettes of ALL FIVE whole figures to FIRST: current neutral lower-leg span28px instead of own23px, boot span32px instead of own28px. Repaint proper strict East-profile lower legs and planted boots with slimmer calves/shins and narrower near/far boot projection/spacing as FIRST. Do not make two side-by-side broad legs or big round toe boots. Match the narrow natural overlapping East profile legs and boot stance in FIRST, with exact ceramic knee/shin plates and charcoal undersuit boundaries. Keep all figures about the SAME full occupied height, identical leg lengths and whole-body scale, planted boots baseline. All face viewer RIGHT in elevated East camera, near LEFT temple BARE; far RIGHT temple implant is hidden, no visible near metal. Keep first four original compact BOTH bent forearms and closed broad gloves near chest/waist, fifth neutral arms down. Maintain connected whole knees/legs/feet/wrists; no detached parts, local patch collage, mirroring, new equipment/helmet/prop, pointing or palm-out gesture, extra figure, second row, labels/background/shadows/grid/checkerboard. Return FIVE complete WHOLE figures, uncropped with generous transparent margins. This is a whole-source perspective/proportion correction, not per-pose scale fitting.'''
    refs=[BASE/'inputs/east-own-idle-3x.png',BASE/'sources/east-gesture-03.png']
    r={'prompt':prompt,'transparent_background':True,'referenced_image_paths':[str(p) for p in refs],
       'references':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],
       'diagnostics':diagnostics,'scope':'Whole-source East lower-leg/boot silhouette correction at unchanged upper-body scale. Unselected retained gesture.'}
    request=BASE/'sources/east-gesture-04.request.json';assert not request.exists()
    request.write_text(json.dumps(r,indent=2)+'\n');(BASE/'sources/east-gesture-04.prompt.txt').write_text(prompt)
    print('East04: measured upper match, lower-leg/boot projection mismatch; whole-source correction prepared')
if __name__=='__main__':main()
