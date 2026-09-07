"""Derive removal motion from authored donning poses, with explicit provenance."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parent
for actor in ['bill','veld','branforth']:
    source=ROOT/'pilot'/f'{actor}-equip-helmet-east'
    base=json.loads((source/'manifest.json').read_text())
    out=ROOT/'pilot'/f'{actor}-remove-helmet-east'; out.mkdir(exist_ok=True)
    files=[]; evidence=[]; previews=[]
    sheet=Image.new('RGB',(1104,230),'#1d252a'); draw=ImageDraw.Draw(sheet)
    for i,source_index in enumerate([5,4,3,2,1,0]):
        path=source/base['states'][0]['frameFiles'][source_index]
        name=f'frame_{i:03}.png'; shutil.copyfile(path,out/name); files.append(name)
        evidence.append({'source':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sourcePose':source_index,'derivation':'reverse pose order; exact frame pixels'})
        im=Image.open(path).convert('RGBA').resize((184,208),Image.Resampling.NEAREST)
        sheet.paste(im,(184*i,22),im)
        preview=Image.new('RGB',(184,208),'#1d252a'); preview.paste(im,(0,0),im); previews.append(preview)
    durations=[140,260,220,220,180,220]
    manifest={'status':'derived_removal_pilot_not_runtime','frameWidth':base['frameWidth'],'frameHeight':base['frameHeight'],'pivot':base['pivot'],'states':[{'id':'remove-helmet-east','frameCount':6,'frameFiles':files,'frameDurationsMs':durations,'loop':False}],'derivation':'Reuses donning frames in reverse order; removal timing authored separately. Ends holding helmet; locker return is not depicted.'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'sources.json').write_text(json.dumps(evidence,indent=2)+'\n')
    draw.text((5,4),actor+' removal / reversed authored poses / ends holding helmet',fill='white'); sheet.save(out/'contact.png')
    previews[0].save(out/'preview.gif',save_all=True,append_images=previews[1:],duration=durations)
print('Three removal pilots derived; visual and runtime review pending')
