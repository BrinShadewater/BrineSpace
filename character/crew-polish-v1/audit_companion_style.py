"""Read the current companion exports without rebuilding or recolouring them."""
import json
from PIL import Image,ImageDraw
from audit_style import ROOT,REPO,OUT,FONT,SMALL,diagnostic,draw_actor

def main():
    specs=[('margot','margot-polish-v1/manifest.json','margot-polish-v1',['idle-south','walk-south','groom-south','swim-east']),
        ('josh','robot-polish-v1/josh/manifest.json','robot-polish-v1',['idle-south','walk-south','torch-south','powerdown-south']),
        ('river','robot-polish-v1/river/manifest.json','robot-polish-v1',['idle-south','walk-south','scan-south','float-east'])]
    report={};board=Image.new('RGBA',(1000,1000),'#242b2e');draw=ImageDraw.Draw(board)
    draw.text((15,12),'COMPANIONS / same density ruler; distinct physical sizes preserved',font=FONT,fill='white')
    for row,(who,manifest,base,keys) in enumerate(specs):
        path=REPO/'character'/manifest;pack=json.loads(path.read_text());root=REPO/'character'/base
        states={s['id']:s for s in pack['states']};density=set();alpha=0;count=0
        for state in states.values():
            for relative in state['frameFiles']:
                m=diagnostic(root/relative,pack['standingHeight']);density.add(m['pixelsPerWorldUnit']);alpha+=m['partialAlpha'];count+=1
        report[who]=dict(states=len(states),frameReferences=count,pixelsPerWorldUnit=sorted(density),partialAlphaPixels=alpha)
        for col,key in enumerate(keys):
            x=col*250+125;y=55+row*310
            draw.text((col*250+8,y),who+' / '+key,font=SMALL,fill='white')
            source=(root/'manifest.json',pack,states[key])
            draw_actor(board,source,x,y+185,1)
            draw_actor(board,source,x,y+265,65.28/148)
    board.save(OUT/'companions.png')
    (OUT/'companion-metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
