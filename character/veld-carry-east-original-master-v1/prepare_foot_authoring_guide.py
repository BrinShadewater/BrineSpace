"""Whole master enlargement and annotation only; never replacement body artwork."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'forward-lift-guide-v1';D.mkdir(exist_ok=True)
source=R/'character/veld-east-held-original-master-v1/frames/bare/000.png';im=Image.open(source).convert('RGBA');large=im.resize((1024,1024),Image.Resampling.NEAREST);large.save(D/'original-native-master-4x.png')
guide=Image.new('RGB',(1024,1024),(32,43,49));guide.paste(large,(0,0),large);d=ImageDraw.Draw(guide)
# Mark projected boot contact positions without changing source files or anatomy.
near=(125*4,222*4);far=(143*4,218*4)
d.line((240,920,near[0],near[1]),fill=(108,197,232),width=3);d.ellipse((near[0]-5,near[1]-5,near[0]+5,near[1]+5),outline=(108,197,232),width=2)
d.text((40,920),'NEAR foreground boot: keep original position and shape',fill=(108,197,232))
d.line((760,820,far[0],far[1]),fill=(237,174,103),width=3);d.ellipse((far[0]-5,far[1]-5,far[0]+5,far[1]+5),outline=(237,174,103),width=2)
d.text((670,780),'FAR boot behind: lift slightly UP',fill=(237,174,103));d.text((670,805),'then slightly RIGHT; never LEFT',fill=(237,174,103))
d.line((far[0],far[1]-8,far[0]+16,far[1]-24),fill=(237,174,103),width=3);d.line((far[0]+16,far[1]-24,far[0]+4,far[1]-24),fill=(237,174,103),width=3);d.line((far[0]+16,far[1]-24,far[0]+16,far[1]-12),fill=(237,174,103),width=3)
guide.save(D/'foot-role-authoring-guide.png')
(D/'GUIDE.json').write_text(json.dumps({'appearanceAuthority':source.relative_to(R).as_posix(),'originalSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'enlargement':'Whole unchanged native256RGBA enlarged4x nearest, no regional/art/colour edits.','annotationRole':'Foot identity and tiny requested displacement guide ONLY. Lines/labels/circles are authoring annotations and must not appear in output. Native/original raw master remains sole appearance authority.','purpose':'Disambiguate original near foreground boot versus far screen-right boot after forward-lift wording produced trailing recovery pose.','scope':'Guide only, not new pose, calibrated heel/contact evidence or completed animation.'},indent=2)+'\n',encoding='utf-8');print('Original-only whole native enlargement and explicit foot-role guide saved.')
