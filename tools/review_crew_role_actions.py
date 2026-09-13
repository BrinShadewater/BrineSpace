"""Export selected role-action evidence without changing any runtime pack."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
PACKS={'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}

def main():
    output=ROOT/'character/crew-action-detail-v2/review/role-action-inventory'
    output.mkdir(parents=True,exist_ok=True)
    report=[]
    for actor,folder in PACKS.items():
        root=ROOT/'character'/folder
        catalog=json.loads((root/'catalog.json').read_text())
        rows=[]
        for relative in catalog['body']:
            path=root/relative;manifest=json.loads(path.read_text())
            for state in manifest['states']:
                if state['id'].rsplit('-',1)[0] not in ['interact','repair']:continue
                frames=[];hashes=[]
                pivot=manifest['pivot']
                for frame in state['frameFiles']:
                    im=Image.open(path.parent/frame).convert('RGBA')
                    canvas=Image.new('RGBA',(256,288));canvas.alpha_composite(im,(round(128-pivot[0]),round(210-pivot[1])))
                    frames.append(canvas);hashes.append(hashlib.sha256(canvas.tobytes()).hexdigest())
                rows.append((state['id'],frames))
                report.append({'actor':actor,'state':state['id'],'manifest':path.relative_to(ROOT).as_posix(),'frames':len(frames),'uniqueNormalizedFrames':len(set(hashes)),'durationsMs':state['frameDurationsMs'],'hashes':hashes})
        rows.sort(key=lambda row:row[0])
        sheet=Image.new('RGB',(256*max(len(row[1]) for row in rows),312*len(rows)),'#293b40')
        for row,(key,frames) in enumerate(rows):
            for column,frame in enumerate(frames):sheet.paste(frame,(column*256,row*312+24),frame)
        labels=ImageDraw.Draw(sheet)
        for row,(key,frames) in enumerate(rows):labels.text((4,row*312+4),key,fill='white')
        sheet.save(output/f'{actor}-contact.png')
    (output/'inventory.json').write_text(json.dumps({'status':'selected-state inventory, not visual acceptance','states':report},indent=2)+'\n')
    print(json.dumps([{k:v for k,v in row.items() if k in ['actor','state','frames','uniqueNormalizedFrames']} for row in report]))

if __name__=='__main__':main()
