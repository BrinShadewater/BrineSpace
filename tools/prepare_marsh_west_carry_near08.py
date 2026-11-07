"""Freeze vertical foreground thigh and low dark far heel recovery."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-west-carry-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=ROOT/'character/marsh-west-carry-material-v1/near-07-unselected/near-passing.png';guide=S/'near-08-whole-near-guide.png';Image.open(source).convert('RGBA').resize((736,736),Image.Resampling.NEAREST).save(guide)
text=(S/'near-07.prompt.txt').read_text().replace('ReferenceONE whole successful NEAR-contact supplies exact near/far leg identity,crate/hand support','ReferenceONE whole NEAR-support guide supplies exact near/far leg identity,crate/hand support, but both thighs/rear leg are TOO EXTENDED and need compact passing recovery')
text=text.replace('LIGHT FOREGROUND NEAR thigh nearly vertical/slightly FORWARD LEFT,foreground NEAR knee LEFT of darker far knee.','LIGHT FOREGROUND NEAR THIGH hangs STRAIGHT VERTICALLY DOWN FROM HIP,not diagonally forward LEFT. Put foreground NEAR knee directly BELOW the pelvis,just LEFT of the darker far knee. Move light foreground supporting SHIN and flat boot directly UNDER THE PELVIS to eliminate the contact-like forward-reaching thigh. Preserve anatomical limb lengths; change whole joint arrangement rather than shrink the leg.')
text=text.replace('DARKER BACKGROUND FAR thigh/knee low immediately RIGHT of near knee; bend DARK FAR knee in low walking heel recovery','DARKER BACKGROUND FAR THIGH also hangs nearly VERTICAL,not extended backward: dark FAR knee low just RIGHT of near knee. Bend the DARK FAR knee strongly in low walking heel recovery')
text=text.replace('no high knee/deep crouch or shortened anatomical limb','no high knee/deep crouch or shortened anatomical limb. Complete compact passing pose, foreground light thigh VERTICAL under hip, dark rear thigh nearly VERTICAL and only its CALF folds behind RIGHT. Do not preserve the guide extended thigh diagonals')
p=S/'near-08.prompt.txt';assert not p.exists();p.write_text(text,encoding='utf-8');g=json.loads((S/'guide-provenance.json').read_text());refs=[guide,S/'selected-idle0-only.png',ROOT/g['originalOwnMaster']['path']]
(S/'near-08.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation; not started','promptSha256':sha(p),'orderedReferences':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in refs],'sourceFrames':[{'path':source.relative_to(ROOT).as_posix(),'sha256':sha(source)}],'sheetGrid':[2,1],'transparentBackground':True},indent=2)+'\n')
print('Frozen near passing with vertical light supporting thigh and low dark heel recovery; generation not started.')
