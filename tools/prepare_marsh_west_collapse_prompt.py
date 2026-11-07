"""Freeze West whole-source request after own selected/master inspection."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-collapse-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';guide=json.loads((sources/'guide-provenance.json').read_text())
    for ref in guide['primarySourceFrames']+guide['guideSourceFrames']:assert sha(ROOT/ref['path'])==ref['sha256']
    text=(ROOT/'character/marsh-east-collapse-material-v1/sources/collapse-01.prompt.txt').read_text().strip()
    text=text.replace('EAST/right-facing','WEST/left-facing').replace('East','West')
    text=text.replace('RIGHT','DIRECTION_TMP').replace('LEFT','RIGHT').replace('DIRECTION_TMP','LEFT')
    text=text.replace('32pixels','31pixels').replace('widths to32','widths to31')
    text=text.replace('visible temple hardware','natural bare visible temple/ear').replace('and visible temple plate retain','and natural visible temple/ear retain')
    text+='\n\nWest is independently authored against its OWN left-facing master, never a reflected East sheet. The visible left temple/ear has NO metal implant plate in reference3; the right-temple hardware is on the far side. Do not invent or mirror a metal plate onto the visible side. West hair sweep, face profile and suit equipment retain their own reference details. Older West pose1 stays nearly upright, but author a mild real knee-softening dip of about7 occupied rows rather than an enlarged standing duplicate; all figures remain at the ONE selected147 neutral scale.'
    path=sources/'collapse-01.prompt.txt';assert not path.exists();path.write_text(text+'\n',encoding='utf-8')
    refs=[sources/'selected-west-idle-gait.png',sources/'collapse-pose-guide.png',ROOT/'character/marsh-motion-polish-v1/sources/west-standing-identity-01.png']
    request={'normalAdmission':False,'status':'frozen whole West request before generation','promptSha256':sha(path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],**{k:guide[k] for k in ['primarySourceFrames','guideSourceFrames','selectedIdleOccupiedSize','selectedMetadata']},'transparentBackground':True,'sheetGrid':[6,1],'contract':{'canvas':[184,184],'pivot':[92,172],'standingHeight':148,'durationsMs':[180]*6,'loop':False},'constraints':'Complete independently authored left-facing poses. Own West master, no visible near temple hardware. One selected147 neutral scale; no per-pose fit/body patch/mirror/palette mapping.'}
    (sources/'collapse-01.request.json').write_text(json.dumps(request,indent=2)+'\n')
    print('Frozen West prompt/refs; distinct near temple and left-facing anatomy.')
if __name__=='__main__':main()
