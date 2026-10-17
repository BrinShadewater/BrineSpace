from pathlib import Path
import json,os,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
v=json.loads((P/'validate-validation.json').read_text());e=json.loads((P/'validate-evidence.json').read_text());assert v['exitCode']==0 and not v['timedOut'] and e['failures']==0 and 'ERROR:' not in (P/'validate.log').read_text(encoding='utf-8')
material=json.loads((P/'material-evidence.json').read_text());checks=0;changed=0
for row in material['records']:
    src=R/row['source'];assert hashlib.sha256(src.read_bytes()).hexdigest()==material['sourceHashes'][row['source']]
    a=np.array(Image.open(src).convert('RGBA'));b=np.array(Image.open(P/row['frame']).convert('RGBA'))
    assert a.shape==b.shape;checks+=1
    assert np.array_equal(a[:,:,3],b[:,:,3]);checks+=1
    assert np.array_equal(a[:60],b[:60]);checks+=1
    if row['index'] in [0,len([x for x in material['records'] if x['direction']==row['direction'] and x['mode']==row['mode']])-1]:assert np.array_equal(a,b);checks+=1
    changed+=int(np.any(a!=b))
packs={}
for mode in ['bare','helmet']:
    m=json.loads((P/(mode+'-manifest.json')).read_text());packs[mode]=m
    for state in m['states']:
        direction=state['id'].split('-')[-1]
        if state['id'].startswith('inspect-'):base=R/f'character/james-inspect-tablet-v1/{mode}-manifest.json'
        elif state['id'].startswith('interact-'):
            version={'east':'v1','south':'v3','west':'v2','north':'v2'}[direction];folder=f'james-interact-{direction}-matched-{version}' if mode=='bare' else f'james-shared-helmet-interact-{direction}-{version}';base=R/'character'/folder/'manifest.json'
        else:base=R/'character/james-meal-family-v1/helmet-manifest.json'
        bm=json.loads(base.read_text());original=next(s for s in bm['states'] if s['id']==state['id']);assert {k:value for k,value in original.items() if k not in ['frameFiles','provenance']}=={k:value for k,value in state.items() if k not in ['frameFiles','provenance']};checks+=1
        assert all(m[k]==bm[k] for k in ['frameWidth','frameHeight','pivot','standingHeight']);checks+=1
        if not state['id'].startswith(('inspect-','interact-')):state['provenance']['originalPixels']=False
    m['status']='selected_neutral_material_continuity_native_verified_owner_pending'
    (P/(mode+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
material['productionInstalled']=True;material['packageChecks']=checks;material['changedFrames']=changed
(P/'material-evidence.json').write_text(json.dumps(material,indent=2)+'\n',encoding='utf-8')
selection={'status':packs['bare']['status'],'runtimeInstalled':True,'newAuthoredMotions':0,'calibratedSourceFrames':1130,'changedFrames':changed,'bareStates':8,'helmetStates':16,'packageChecks':checks,'nativeChecks':e['checks'],'nativeCaptures':16,'strictProfileUnchanged':v['realProfileUnchanged'],'profileDelta':v['profileDelta'],'scratch':v['scratch'],'alphaAnatomyClocksExact':True,'headHelmetPixelsExact':True,'exactIdleEndpoints':True,'method':'Fixed per-facing pooled neutral suit/equipment material gains; identical calibration for bare and helmet; head/helmet y<60 and warm skin/gold excluded. Mask can include neutral tablet casing, gloves and belt tools. Original source files remain unchanged.','visualScope':'Eight seven-pose original/revised/master boards and four native midpoint views reviewed at148/82/54/27. Complete reference/clock/alpha checks are not all-frame visual/anatomy acceptance.','ownerVisualAcceptance':False,'remaining':['Complete head/perspective/anatomy and motion polish','Real diagnostic arrival/workstation/travel/gear/Continue journeys','Meal contact scale/flip/off-grid/neighbor/crowd contexts'],'priorFailure':'Equipment pack loaded after South larger pivot overrides rejected entire variant; move paired correction before bare contact overrides, retaining validator. Silent following launch engine1 before fixture output unproven cause; preserved, terminal fresh launch engine0.'}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf-8')
a=R/'character/ACTIVE_ASSETS.json';active=json.loads(a.read_text());active['actionOverrides']['branforth-tablet-material-continuity']='character/james-inspect-material-continuity-v1/bare-manifest.json';active['actionOverrides']['branforth-tablet-material-continuity-helmet']='character/james-inspect-material-continuity-v1/helmet-manifest.json';a.write_text(json.dumps(active,indent=2)+'\n',encoding='utf-8')
# Full source-clock paired playback, compared with each facing's exact master.
for direction in ['east','south','west','north']:
    states={mode:next(s for s in m['states'] if s['id']=='inspect-'+direction) for mode,m in packs.items()};views=[]
    for i in range(len(states['bare']['frameFiles'])):
        view=Image.new('RGB',(736,265),'#303b40');d=ImageDraw.Draw(view);d.text((8,8),f'James tablet / {direction} / master and revised / {i}',fill='white')
        for j,mode in enumerate(['bare','helmet']):
            endpoint=Image.open(P/states[mode]['frameFiles'][0]).convert('RGBA');im=Image.open(P/states[mode]['frameFiles'][i]).convert('RGBA');view.paste(endpoint,(j*368,50),endpoint);view.paste(im,(j*368+184,50),im)
        views.append(view)
    ds=states['bare']['frameDurationsMs'];bound=np.rint(np.cumsum([0]+ds)/10).astype(int)*10;views[0].save(P/(direction+'-review.gif'),save_all=True,append_images=views[1:],duration=np.diff(bound).tolist(),loop=0)
note='''

## James tablet neutral material continuity — October 1, 2026

All-pose meal source audit covers24 selected clips/152 references and12 exact
whole registered North/South phase joins. It exposed green-grey suit interiors
against charcoal master/idle endpoints in sealed meal inspection substitutes.
Trace reused sources: actual inspect and interact share this same diagnostic art.
Selected james-inspect-material-continuity-v1 calibrates all1130 paired source
frames with one pooled neutral suit/equipment gain per facing, shared bare/helmet.
All alpha/anatomy/clocks and y<60 head/helmet pixels exact; idle endpoints exact;
original sources retained. Neutral mask can include tablet casing/gloves/belt tools,
while warm skin/gold excluded. Do not equate pooled medians with semantic identity.

Normal loader9332checks/0failures/16 native captures; engines0/no timeout/scratch
APPDATA; strict owner profile guard false,last_session.json only, cause unproven.
Eight7-pose original/revised/master boards and four native midpoint views reviewed
at148/82/54/27. Full six-second source GIFs prepared. Complete-reference numeric
evidence does not prove all-frame anatomy or actual diagnostic travel/gear/Continue.
Bare interact/inspect and helmet interact/inspect/eat/drink substitute keys share
corrected sources; original timing modes preserved, no new authored animation.

First install failed2292checks: helmet validator correctly rejects South equipment
after larger bare contact-pivot overrides. Load the paired material family before
South contact overrides, preserving strict validator. Following launch terminated
engine1 before fixture output, cause unproven; archived. Terminal fresh launch
passes. Do not restart a live unknown job or turn unexplained exit into acceptance.
Other head/anatomy/perspective/motion/material, physical contexts and full-set
cross-family polish remain; full James goal active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James tablet neutral material continuity' not in data:
        encoded=note.encode('utf-8');updated=encoded.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+encoded;temp=path.with_name(path.name+'.tablet-material.tmp');temp.write_bytes(updated);os.replace(temp,path)
handoff=f'''# Project handoff

Updated: October1,2026 · Project: Brine Space · Task: James tablet material continuity

## Objective and acceptance
Full James animation library/master/style/perspective/height/proportion/grade,
then full-set cross-family polish. Goal remains active.

## Accepted decisions and constraints
Matte masters, stable planted body, diagnostics tablet facing actor, wrench belt.
Preserve whole source anatomy and exact idle endpoints; no per-pose grade fitting.

## Current state
New pack calibrates1130 source frames,8bare+16helmet states covering actual
diagnostics/inspection and sealed meal substitutes. Normal grid loader and
ACTIVE_ASSETS selected. Source hashes/recipe/original-revised-master boards and
four paired six-second GIFs saved. Original selected sources unchanged.

## Verification
{checks} package checks: source hashes/size/alpha/head/helmet/endpoints and all
state metadata/clocks exact.9332 normal native checks,0failures,16captures.
Eight7-pose boards and four native midpoint views reviewed. Scratch APPDATA;
strict owner profile guard false,last_session.json only, attribution unproven.
Rejected load order and silent terminal launch retained. Validator preserved.

## Next action
Refresh source inventory/all meal boards and check full diagnostics/head/perspective
motion and actual arrival/workstation/gear/Continue contexts. Other furniture/
crowd/scale/flip/off-grid/neighbor and cross-family polish remain. No owned job live.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
audit=R/'character/james-meal-motion-audit-2026-10-01';archive=audit/'before-tablet-material';archive.mkdir(exist_ok=True)
for f in audit.glob('*'):
    if f.is_file() and f.suffix in ['.png','.gif','.json'] and not (archive/f.name).exists():shutil.copy2(f,archive/f.name)
(audit/'HANDOFF.md').write_text('''# Project handoff

Updated: October1,2026 · Project: Brine Space · Task: Full selected meal pose audit

## Objective and acceptance
Review complete normal meal source motions against masters, then cross-family polish.

## Accepted decisions and constraints
Preserve selected whole directional poses; fixed native ruler; equipment uses
sealed tablet inspection substitutes rather than eating through the visor.

## Current state
All24selected clips/152source references, source-clock GIFs, four all-pose boards
and12 exact whole registered phase joins. Original audit retained under
before-tablet-material. Green interior diagnostics/inspection drift found and
corrected in ../james-inspect-material-continuity-v1, with normal native evidence.

## Verification
Four all-pose boards inspected.152 reference metrics and12 whole joins exact.
Source evidence is not an actual route/workstation/gear or full-set acceptance.

## Next action
Refresh audit to current selected material revision. Continue full head/anatomy/
perspective and motion review, actual contexts and cross-family handoffs.
''',encoding='utf-8')
print(json.dumps({'packageChecks':checks,'nativeChecks':e['checks'],'changedSourceFrames':changed,'fullGoal':'active'}))
