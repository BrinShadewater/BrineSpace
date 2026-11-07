"""Freeze complete West first-dip correction without per-pose body fitting."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-collapse-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    prompt='''Transparent pixel-art source sheet, TWO COMPLETE separated Marsh figures in one horizontal row with wide transparent gutter. EXACT WEST/LEFT-facing adult male android from selected reference1. Reference1 is PRIMARY authority for adult head/torso/limb proportions, narrow fitted side silhouette, warm ivory/sage matte grade and elevated side camera. Reference2 original West standing master controls identity, hair sweep, suit/harness/shoulder/pouch details and natural visible temple/ear. No metal plate on the visible near temple; right-temple hardware is on FAR side. Magenta background must not appear.

LEFT figure: a gentle dry mechanical first collapse dip, knees flex moderately and hips lower, torso pitches forward slightly while head stays aligned with neck; complete connected arms flex naturally at elbows, gloved hands fall near thighs. It must be a real mild LOWERED articulated pose, not almost-neutral knees angled backward. At shared master density, target about140occupied rows versus147standing: about7rows lost through knee/hip articulation, not scaling the figure. Adult head and equipment stay master-sized; fitted limbs/torso don't thicken. This is not a deep squat or kneeling pose. Always facing LEFT, natural weight over complete ivory boot uppers and dark soles. Preserve complete shoulders/elbows/hands and connected hips/knees/ankles/feet.

RIGHT figure: exact selected West neutral standing ruler from reference1, occupied31wide by147high in184canvas with declared148height. ONE common drawing scale for BOTH complete figures based on this neutral. No per-pose fitting, enlarged head, equalized silhouette heights, reflected East character or camera turning. Preserve warm matte ivory fabric/guards, sage shoulders/pouches, slate joint bands, full dark gloves, dark boot soles, blond swept hair, bare near temple/ear. Restrained crisp warm pixel clusters, no broad new outlines, shiny/cyan lights or cold blue grade. Actual transparency, no floor/cast shadow, no text/labels. DRY: no coolant/puddle/smoke/sparks. Complete whole figures, never limb patches.'''
    path=BASE/'soften-02.prompt.txt';assert not path.exists();path.write_text(prompt+'\n',encoding='utf-8')
    refs=[BASE/'selected-west-idle-gait.png',ROOT/'character/marsh-motion-polish-v1/sources/west-standing-identity-01.png']
    request={'normalAdmission':False,'status':'frozen whole mild West first-dip correction before generation','promptSha256':sha(path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],'transparentBackground':True,'sheetGrid':[2,1],'target':'Articulated mild140row dip at147row selected neutral common scale; do not force sampled bounds or separately fit pose. Replace complete first figure only; four later source01 figures unchanged.'}
    (BASE/'soften-02.request.json').write_text(json.dumps(request,indent=2)+'\n')
    print('Frozen two complete West figures for articulated milder dip.')
if __name__=='__main__':main()
