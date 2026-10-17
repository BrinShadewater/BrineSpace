from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];DIRS=['east','south','west','north']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    bindings={};checks=0
    for gear in ['bare','helmet']:
        states=[]
        for direction in DIRS:
            source=R/f'character/veld-rest-{direction}-coherent-v1';m=json.loads((source/f'{gear}-manifest.json').read_text())
            br=json.loads((source/'bare-registration.json').read_text());gr=json.loads((source/'helmet-registration.json').read_text())
            r=br['frames'][-1];center=[r['position'][j]+(br['heads'][-1][j]-r['box'][j])*br['fixedRuler'] for j in range(2)]
            if gear=='helmet':
                h=gr['frames'][-1];center=[h['componentPosition'][j]+h['componentSize'][j]/2 for j in range(2)]
            offset=[round((center[j]-[128,224][j])*65.28/148+(14.592 if j==1 else 0),6) for j in range(2)]
            for entry in m['states']:
                entry=entry.copy();entry['frameFiles']=['res://'+(source/f).relative_to(R).as_posix() for f in entry['frameFiles']]
                if entry['id'].startswith('sleep-'):entry['restHeadOffset']=offset
                for f in entry['frameFiles']:
                    path=R/f.removeprefix('res://');assert Image.open(path).size==(256,256);bindings[f]=sha(path);checks+=1
                states.append(entry)
            for name in [f'{gear}-manifest.json','bare-registration.json','helmet-registration.json','paired-verification.json']:
                bindings[(source/name).relative_to(R).as_posix()]=sha(source/name)
        manifest={'name':f'Veld cardinal generic rest {gear} selected family','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'selected_runtime','states':states}
        if gear=='helmet':manifest['equipment']='diving-helmet'
        (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (P/'source-bindings.json').write_text(json.dumps({'normalSelection':True,'frameReferences':checks,'uniqueFrames':48,'states':24,'bindings':bindings,'restHeadOffsetUnits':'world pixels at CELL384 * .17 /148; anatomical bare or component helmet center including14.592world draw lift; furniture integration proof distinct'},indent=2)+'\n')
    board=Image.new('RGB',(1536,2160),'#202a30');d=ImageDraw.Draw(board)
    for i,direction in enumerate(DIRS):
        source=R/f'character/veld-rest-{direction}-coherent-v1'
        for gi,gear in enumerate(['bare','helmet']):
            m=json.loads((source/f'{gear}-manifest.json').read_text())
            for slot,f in enumerate(m['states'][0]['frameFiles']):
                im=Image.open(source/f).convert('RGBA');at=(slot*256,(i*2+gi)*270+16);board.paste(im,at,im);d.text((at[0]+6,at[1]-16),f'{direction} {gear} {slot}',fill='white')
    board.save(P/'cardinal-contact-sheet.png');print(json.dumps({'states':24,'references':checks,'uniqueFrames':48,'normalSelection':True}))
if __name__=='__main__':main()
