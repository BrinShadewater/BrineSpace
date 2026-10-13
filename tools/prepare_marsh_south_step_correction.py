"""Freeze two complete pose corrections; markers are reference diagrams only."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-step-v1/sources'
PROMPT='''Draw exactly THREE separate COMPLETE pixel-art figures of the same South/front-facing Marsh android, in ONE horizontal row on transparent alpha. Figure1 corrects the reaching pose, Figure2 corrects the closing pose, Figure3 is the neutral standing ruler. Reference1 is the actual selected South idle/gait: PRIMARY camera, proportion, material, drawing scale and grade authority. Reference2 is an annotated WHOLE-POSE motion guide: green markers show desired sole positions, its existing reaching/closing boot positions are incorrect. Reference3 is face/temple-hardware/suit identity authority. No markers, text, floor, halo or shadow in the output.

Keep the exact reference1 adult male stocky physique, narrow fitted ivory/sage suit, collar/chest rectangle/two harness straps/belt pouches, dark gloves, ivory knees/shins/ankles/BOOT UPPERS with only thin dark soles. Same short blond hair, neutral face and visible silver temple hardware. Total body width including arms is58 units per148 units standing height, not a bulky60–65unit variant. Head size, hand/arm width, chest/hip/leg proportions match selected idle. One consistent whole-body scale and warm matte subdued ivory/olive grade across all three; no per-pose scaling, horizontal squashing, body mirroring, isolated anatomy patches or extra limbs. Slight elevated frontal game camera, all heads/fingers/boot tips inside generous gutters.

Figure1 REACH: boot on IMAGE LEFT, under visible temple hardware side, extends SOUTH/toward viewer. The other IMAGE RIGHT boot stays flat and planted. Place left boot farther DOWN and OUTWARD than guide1: about6units BELOW the planted right sole, with27units separation between sole centers at148unit height. Right sole at reference-stance right position; left sole directly under the left hip rather than tucked inward under center. In the guide's184px coordinates desired left sole78.5,176 versus right105.5,170. These coordinates describe proportions and foot placement, NOT a diagram to draw. Left leg modestly reaches forward, toe/heel articulated naturally; it is airborne, not a high knee or crossed leg. Redraw the complete body coherently over the right support.

Figure2 CLOSE: left-image boot remains flat planted at the NEW forward line, same left support as guide's middle planted pose. The trailing right-image boot comes FORWARD and OUTWARD almost to neutral, no new left step. RIGHT boot sole only2units above/behind the left sole and27units to its right at148unit scale. Guide3's old right boot is12units high and10.5units too far inward; do not preserve that defect. Desired left sole78.5,170/right105.5,168 in184px proportional guide. Right foot moves DOWN and RIGHT toward the idle's right boot position; right knee gently flexed and toe slightly lifted. Both feet remain beneath their respective hips, no crossing. LEFT boot stays planted exactly; whole upper body shifts naturally but no direction change.

Figure3 NEUTRAL RULER: exact selected reference1 neutral standing posture, both soles level with27units between centers at148unit standing height, shoulders/head/collar/harness/hips matching selected idle. This ruler establishes ONE common extraction scale for all figures. Same head, dark glove silhouettes and ivory boot material. Final pose should read as the same Marsh, not a newly designed character.

Essential: Figure1 leading LEFT boot appears LOWER than right by6units; Figure2 trailing RIGHT boot closes almost level and stays on its OWN right side, while LEFT support does not move. Each is a coherent complete body. Do not return the existing tucked-in feet or alternating walking poses.'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    refs=['character/marsh-south-step-v1/candidate-03/003.png','character/marsh-south-step-v1/candidate-03/004.png','character/marsh-south-step-v1/candidate-03/005.png']
    board=Image.new('RGBA',(184*3,235),(41,59,64,255));draw=ImageDraw.Draw(board)
    for i,path in enumerate(refs):
        board.alpha_composite(Image.open(ROOT/path).convert('RGBA'),(184*i,45))
        draw.text((184*i+4,4),['Reach: too high/inward','Retained planted support','Close: too high/inward'][i],fill='white')
        targets=[[(78.5,176),(105.5,170)],[(78.5,170)],[(78.5,170),(105.5,168)]][i]
        for x,y in targets:
            x+=184*i;y+=45;draw.ellipse((x-3,y-3,x+3,y+3),outline='#5ff1a4',width=1)
        draw.text((184*i+4,21),'GREEN: desired sole',fill='#5ff1a4')
    guide=BASE/'reach-close-guide-04.png';board.resize((board.width*4,board.height*4),Image.Resampling.NEAREST).save(guide)
    ordered=['character/marsh-south-step-v1/sources/idle-gait-reference.png',guide.relative_to(ROOT).as_posix(),'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png']
    pp=BASE/'step-04.prompt.txt';rp=BASE/'step-04.request.json';assert not pp.exists() and not rp.exists()
    pp.write_text(PROMPT,encoding='utf-8')
    rp.write_text(json.dumps({'status':'frozen before whole-figure reaching/closing correction','normalAdmission':False,'promptSha256':sha(pp),'orderedReferences':[{'path':p,'sha256':sha(ROOT/p)} for p in ordered],'guideSources':[{'path':p,'sha256':sha(ROOT/p)} for p in refs],'desiredSheetGrid':[3,1],'transparentBackground':True,'targetSolesDense':{'reach':[[78.5,176],[105.5,170]],'close':[[78.5,170],[105.5,168]]}},indent=2)+'\n')
    print('Source04 prompt and3ordered references frozen; whole-figure reach/close plus neutral ruler.')
if __name__=='__main__':main()
