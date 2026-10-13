"""Freeze passing correction with a visually explicit whole selected gait pose."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    pose=ROOT/'character/marsh-south-walk-material-v1/candidate-02/003.png'
    guide=BASE/'right-support-selected-walk3.png'
    Image.open(pose).convert('RGBA').resize((736,736),Image.Resampling.NEAREST).save(guide)
    prompt='''Create a transparent pixel-art SOURCE SHEET of TWO COMPLETE full-body front/SOUTH Marsh figures, separated by generous transparent space. Reference1 selected idle/walk is PRIMARY for fitted adult build, unchanged head/collar/chest size, equipment, native drawing density, camera and warm matte ivory/sage/slate materials. Reference2 is a single selected walking pose: COPY ITS LEG SIDE ARRANGEMENT exactly for figure1. In reference2 the long supporting leg and planted boot are on the VIEWER RIGHT, while the shorter bent/lifted leg is on VIEWER LEFT. Do not exchange these legs or mirror the character. Reference3 original master supplies adult blond face/hair and right-temple implant on viewer LEFT. Same elevated FRONT camera as selected walking reference2.

Figure1: a complete running PASSING/COMPRESSION pose developed from reference2. Keep reference2's viewer-RIGHT supporting boot planted and its viewer-LEFT foot lifted. Bend the supporting knee gently so the body dips slightly, bring the lifted knee forward beneath the pelvis without lifting it high. Running torso leans forward mildly; both elbows naturally bent, arms passing toward neutral in opposite swing. The leg SIDE arrangement must be exactly reference2: full boot on viewer RIGHT reaches the floor, viewer LEFT foot is visibly above it and closer under the pelvis. Whole connected adult shoulders, arms/hands, torso, pelvis, knees/ankles/feet; no isolated limb patches, duplicated legs or detached hands. Maintain reference1 compact adult head and equipment anatomy at unchanged scale.

Figure2: neutral standing arms down, same body as selected idle, a ruler for ONE shared drawing scale. Selected neutral occupied58wide by147high native pixels in184square canvas with pivot92/172, metadatastandingHeight148. These are calibration numbers, not text to print. All figures share ONE neutral scale. Do not separately fit figure1 to147high. Keep warm ivory suit/boot UPPERS, charcoal SOLES/gloves, slate joints and muted sage shoulders/beltpouches. Crisp warm restrained pixel clusters, matte finish, no cyan/blue grade, thicker head, glossy highlights or new equipment. Actual transparent background, no floor/shadow/text/labels/magenta/effects. TWO COMPLETE whole figures, wide gutters, no mirroring or patched anatomy.'''
    path=BASE/'passing-05.prompt.txt';assert not path.exists();path.write_text(prompt+'\n',encoding='utf-8')
    refs=[BASE/'selected-south-idle-gait.png',guide,ROOT/'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png']
    req={'normalAdmission':False,'status':'frozen before generation; single selected walk3 visually explicit leg-side guide','promptSha256':sha(path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],'poseGuideSource':{'path':pose.relative_to(ROOT).as_posix(),'sha256':sha(pose),'operation':'complete RGBA nearest4x, no art changes'},'sheetGrid':[2,1],'transparentBackground':True,'constraints':'Complete pose plus neutral, single147-occupied neutral scale, no per-pose fit/mirror/limb patches/recolour.'}
    (BASE/'passing-05.request.json').write_text(json.dumps(req,indent=2)+'\n')
    print('Frozen exact05 request and selected walk3 whole-pose guide.')
if __name__=='__main__':main()
