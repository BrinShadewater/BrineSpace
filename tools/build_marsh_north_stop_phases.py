"""Stage stop entries with exact selected outgoing gait poses for all six phases."""
from pathlib import Path
import json,hashlib,os,argparse
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-stop-v1'
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--polished',action='store_true');parser.add_argument('--both-polished',action='store_true');args=parser.parse_args()
    output=BASE/('phase-bank-v3' if args.both_polished else 'phase-bank-v2' if args.polished else 'phase-bank-v1');output.mkdir(parents=True,exist_ok=True)
    current=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    bank=[];records=[];board=Image.new('RGB',(920,220*6),'#293b40');draw=ImageDraw.Draw(board)
    for phase in range(6):
        family=BASE/(('candidate-09' if args.polished or args.both_polished else 'candidate-05') if phase<3 else 'candidate-12' if args.both_polished else 'candidate-06')
        # Near-neutral contact phases go straight into two-foot settlement rather
        # than introducing a fresh lifted leg. Repeated rows are deliberate holds.
        paths=[ROOT/current['walk-north']['files'][phase]]
        if phase in [2,5]:paths += [family/'003.png',family/'003.png',ROOT/current['idle-north']['files'][0]]
        else:paths += [family/f'{i:03d}.png' for i in [1,2,3]]
        paths += [ROOT/current['idle-north']['files'][0]]
        key=f'walk-stop-p{phase}-north'
        bank.append({'id':key,'frameFiles':[os.path.relpath(p,output).replace('\\','/') for p in paths],'frameDurationsMs':[80]*5,'loop':False,'facings':['north']*5,'waterKinds':['walk']*5,'waterPoses':[False]*5,'depthOffsets':[0.0]*5})
        records.append({'key':key,'gaitSlot':phase,'family':family.name,'contactPhase':phase in [2,5],'sources':[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]})
        for i,p in enumerate(paths):
            im=Image.open(p).convert('RGBA');board.paste(im,(184*i,220*phase+26),im)
            draw.text((184*i+3,220*phase+5),f'Gait{phase} / stop{i}',fill='white')
            draw.line((184*i,220*phase+198,184*(i+1)-1,220*phase+198),fill='#829496')
    manifest={'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'states':bank}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    admitted=args.both_polished and '../marsh-north-stop-v1/phase-bank-v3/manifest.json' in json.loads((ROOT/'character/marsh-v2/catalog.json').read_text())['body']
    (output/'sources.json').write_text(json.dumps({'normalAdmission':admitted,'status':'selected normal North stops; dated production evidence records verification scope' if admitted else 'staged phase source joins; root/arrival/controller/Continue pending','phases':records},indent=2)+'\n')
    board.save(output/'comparison.png')
    print('Staged six phase-specific stops/30source references, exact six gait entries and idle endpoints; no new raster or normal admission')
if __name__=='__main__':main()
