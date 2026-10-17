from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
f=P/'build_contact_player.py';t=f.read_text(encoding='utf-8');t=t.replace('Room crop follows the physical actor; movement is preserved in the recorded coordinates.','Room view is a 2x crop following the physical actor; source view is at 1.5x. Recorded world movement is reported below.');f.write_text(t,encoding='utf-8')
note='''## Bill East synchronized contact review — October 2, 2026

Added reproducible contact-player.html from190 retained exact source/native pairs:
four bare/helmet entry/exit sequences, play/pause, normal/quarter speed, scrub and
single-frame steps. Source uses actual manifest pivot/H148 registration on one
fixed320canvas, displayed1.5x; native is2x actor-following crop with physical world
foot/time/water/state reported. Loop restart is explicitly a review reset, not
an authored handoff. No source/actor/production selection changes or extra Godot run.
Browser verified loading, playback advancing frame/time, pause and exact scrub.

Paused lift at tick81/time1.367s shows lower boot below walking pivot before prone
pose. Actor already swim: pivot is not sufficient evidence of floor penetration
or clearance. Support/contact remains UNACCEPTED until compared with real room
support geometry and buoyancy anchoring. Do not move a swimming figure solely to
make every boot touch a dry walking guide. Browser snapshots prove selected frames
and playback controls, not uninterrupted full-motion visual acceptance.

Next: establish real support plane and expected root during entry/exit, inspect
registered sole clearance and motion, then current-bank Continue and other cardinal
bridges. Full Bill set and cross-family polish remain active/incomplete.
Review:character/bill-land-water-material-east-v4/contact-player.html.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
p=P/'HANDOFF.md';t=p.read_text(encoding='utf-8');t+='\n## Contact review continuation\nAdded build_contact_player.py/contact-player.html and saved browser preview.190paired\nframes retain actual pivot/H148; native2x actor-following/source1.5x. Controls and\nadvancing playback verified in browser, paused ticks78/81 inspected. Tick81 lower\nboot crosses walking pivot while state already swim: actual support plane and\nbuoyancy anchoring must decide clearance; do not force dry registration on swim.\nNo continuous-motion acceptance or new Godot evidence claimed. Next support-plane\naudit, current-bank Continue, other directions/full-family polish. Guidance updated.\n';p.write_text(t,encoding='utf-8')
e=json.loads((P/'review.json').read_text(encoding='utf-8'));e['contactPlayer']={'pairs':190,'sourceZoom':1.5,'nativeCropZoom':2,'browserVerified':['loaded','play advances frame/time','pause','scrub ticks78/81'],'contactAcceptance':'pending actual room support/buoyancy geometry; tick81 lower boot below dry pivot','continuousMotionAccepted':False};(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Recorded contact review finding and support-plane next action.')
