from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
rows=[];atlas=Image.new('RGBA',(768,768))
for i in range(9):
    key='carry-east' if i<6 else 'pickup-east';index=i if i<6 else i-5
    file=R/'character/james-cargo-material-joined-v1/frames/bare'/key/(str(index).zfill(3)+'.png')
    box=(110,61,174,125) if i<6 else [(143,86,207,150),(147,101,211,165),(135,70,199,134)][i-6]
    crop=Image.open(file).convert('RGBA').crop(box).resize((256,256),Image.Resampling.NEAREST)
    atlas.alpha_composite(crop,((i%3)*256,(i//3)*256));rows.append({'cell':i,'key':key,'index':index,'source':file.relative_to(R).as_posix(),'crop':box,'presentationScale':4})
atlas.save(P/'head-closeup-target.png')
master=Image.open(P/'east-idle-master-reference.png').convert('RGBA').crop((60,10,124,74)).resize((256,256),Image.Resampling.NEAREST);master.save(P/'head-closeup-master.png')
(P/'head-closeup-layout.json').write_text(json.dumps({'cells':rows,'status':'isolated nine-head authoring study; not selected; crop contains collar/upper chest, not semantic head mask','masterCrop':[60,10,124,74],'scale':4},indent=2))
print('Nine registered head/neck closeups prepared; presentation4x, no production changes.')
