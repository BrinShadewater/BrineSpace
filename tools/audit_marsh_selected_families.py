"""Current ordered catalog inventory and complete source family boards; no acceptance inference."""
from pathlib import Path
import hashlib,json,math,argparse
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-selected-family-audit-2026-10-02'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def resolve(manifest,path):return ROOT/path.removeprefix('res://') if path.startswith('res://') else (manifest.parent/path).resolve()
def main():
    global OUT
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='character/marsh-selected-family-audit-2026-10-02')
    parser.add_argument('--overlay-list',help='Project-relative ordered private manifest list, preserving individual metadata')
    args=parser.parse_args();OUT=ROOT/args.output
    catalog=ROOT/'character/marsh-v2/catalog.json';ordered=json.loads(catalog.read_text())['body'];selected={};manifests=[];images={};overrides=[]
    normal_count=len(ordered);overlay_path=None
    if args.overlay_list:
        overlay_path=ROOT/args.overlay_list
        ordered=ordered+['res://'+n.removeprefix('res://') for n in json.loads(overlay_path.read_text())['manifests']]
    for name in ordered:
        manifest=resolve(catalog,name);data=json.loads(manifest.read_text());manifests.append({'path':manifest.relative_to(ROOT).as_posix(),'sha256':sha(manifest)})
        for state in data['states']:
            key=state['id'];paths=[resolve(manifest,p) for p in state['frameFiles']]
            assert len(paths)==len(state['frameDurationsMs']) and all(t>0 for t in state['frameDurationsMs'])
            if key in selected:overrides.append({'key':key,'from':selected[key]['manifest'],'to':manifest.relative_to(ROOT).as_posix()})
            frames=[]
            for path in paths:
                image=images.setdefault(path,Image.open(path).convert('RGBA'));bounds=image.getbbox();assert bounds is not None
                frames.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'canvas':list(image.size),'bounds':list(bounds),'occupiedSize':[bounds[2]-bounds[0],bounds[3]-bounds[1]],'edgeContact':bounds[0]==0 or bounds[1]==0 or bounds[2]==image.width or bounds[3]==image.height})
            selected[key]={'manifest':manifest.relative_to(ROOT).as_posix(),'manifestSha256':sha(manifest),'pivot':data['pivot'],'standingHeight':data.get('standingHeight',74),'durationsMs':state['frameDurationsMs'],'loop':state['loop'],'frames':frames,'artAcceptance':'Not established by inventory/metrics; consult scoped visual/moving evidence.'}
    OUT.mkdir(exist_ok=True);families={}
    for key,state in selected.items():
        action,direction=key.rsplit('-',1) if '-' in key else (key,'')
        family=action if direction in ['east','west','north','south'] else key
        families.setdefault(family,[]).append(key)
    board_records=[]
    for family,keys in sorted(families.items()):
        keys=sorted(keys);extent=[]
        for key in keys:
            s=selected[key]
            for f in s['frames']:
                b=f['bounds'];p=s['pivot'];extent.append((b[0]-p[0],b[1]-p[1],b[2]-p[0],b[3]-p[1]))
        left=math.ceil(max(-b[0] for b in extent))+12;right=math.ceil(max(b[2] for b in extent))+12
        above=math.ceil(max(-b[1] for b in extent))+34;below=max(0,math.ceil(max(b[3] for b in extent)))+12
        width=max(184,left+right);height=above+below;rows=sum(math.ceil(len(selected[k]['frames'])/6) for k in keys)
        board=Image.new('RGB',(width*6,height*rows),'#293b40');draw=ImageDraw.Draw(board);row=0
        for key in keys:
            s=selected[key];p=s['pivot']
            for i,f in enumerate(s['frames']):
                im=images[ROOT/f['path']];x=i%6*width;y=(row+i//6)*height
                draw.text((x+3,y+3),key+' '+str(i)+' / '+str(s['durationsMs'][i])+'ms',fill='white')
                draw.text((x+3,y+17),'occupied%s / H%s'%(f['occupiedSize'],s['standingHeight']),fill='#a4d4c3')
                px=x+left-round(p[0]);py=y+above-round(p[1]);b=f['bounds']
                assert x<=px+b[0] and px+b[2]<=x+width and y+30<=py+b[1] and py+b[3]<=y+height,'registered figure clipped'
                board.paste(im,(px,py),im)
            row+=math.ceil(len(s['frames'])/6)
        path=OUT/(family+'-contact.png');board.save(path);board_records.append({'family':family,'keys':keys,'file':path.name,'sha256':sha(path),'visualReviewed':False})
    report={'catalogSha256':sha(catalog),'orderedBodyManifests':manifests,'bodyManifests':len(ordered),'selectedStates':len(selected),'selectedSlots':sum(len(s['frames']) for s in selected.values()),'uniqueSourcePaths':len({f['path'] for s in selected.values() for f in s['frames']}),'states':selected,'overrides':overrides,'boards':board_records,'fullGoalComplete':False,'limits':'Current ordered last-state-wins source inventory and whole-figure common-pivot boards only. Source timing recorded, not gameplay distance cadence. No new native/motion/art acceptance. Older runtime-contract not reused; underlying artwork/current hashes inspected. Missing cardinal variants are not automatically missing runtime requirements.'}
    report.update(normalBodyManifestCount=normal_count,privateOverlayList=args.overlay_list,privateOverlayListSha256=sha(overlay_path) if overlay_path else None,normalAdmission=False)
    (OUT/'inventory.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Current Marsh selected family inventory</title><style>body{background:#182b30;color:#dae8e2;font:16px system-ui;margin:24px}img{max-width:100%;image-rendering:pixelated}</style><h1>Marsh current selected family inventory</h1><p>Complete source boards and timing at common registered foot anchors. Coverage and metrics do not establish master or motion acceptance. <a href="inventory.json">Ordered selection/hashes and scope</a></p>'+''.join('<h2>'+r['family']+'</h2><img src="'+r['file']+'">' for r in board_records),encoding='utf-8')
    print(json.dumps({'bodyManifests':len(ordered),'selectedStates':len(selected),'selectedSlots':report['selectedSlots'],'familyBoards':len(board_records),'edgeContactStates':[k for k,s in selected.items() if any(f['edgeContact'] for f in s['frames'])],'standingRulers':sorted({s['standingHeight'] for s in selected.values()})}))
if __name__=='__main__':main()
