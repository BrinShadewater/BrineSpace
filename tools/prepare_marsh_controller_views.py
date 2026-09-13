"""Register three distinct controller view studies without runtime selection."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main():
    source=BASE/'sources/marsh-role-controller-directions-01.png'
    raw=binary(chroma(source))
    if raw.size!=(2172,724):raise ValueError('Remeasure changed view study')
    output=BASE/'review/marsh-controller-directions-01';output.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1104,208),'#293b40');records=[]
    for index,direction in enumerate(['north','south','west']):
        tile=raw.crop((index*724,0,(index+1)*724,724));box=tile.getbbox()
        scale=148/(box[3]-box[1]);a=np.asarray(tile)
        y,x=np.where(a[box[3]-6:box[3],:,3]>0)
        anchor=float((x.min()+x.max())/2) if direction in ['north','south'] else float(np.median(x))
        dense=binary(tile.resize((round(724*scale),round(724*scale)),Image.Resampling.BOX),True)
        pose=Image.new('RGBA',(184,184));pose.alpha_composite(dense,(round(92-anchor*scale),round(172-(box[3]-1)*scale)))
        pose.save(output/f'{direction}.png')
        ref=Image.open(BASE/f'sources/marsh-role-interact-{direction}-reference-01.png').convert('RGBA')
        sheet.paste(ref,(index*368,24),ref);sheet.paste(pose,(index*368+184,24),pose)
        records.append({'direction':direction,'crop':box,'scale':scale,'support':[anchor,box[3]-1],'pivot':[92,172]})
    labels=ImageDraw.Draw(sheet)
    for index,direction in enumerate(['north','south','west']):
        labels.text((index*368+4,4),direction+' original',fill='white');labels.text((index*368+188,4),direction+' controller',fill='white')
    sheet.save(output/'comparison.png')
    report={'status':'unselected_directional_pose_studies','source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'views':records,'limits':'Standing registration only; full sequences, identity and native occlusion review remain. No helmet equipment.'}
    (output/'registration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
