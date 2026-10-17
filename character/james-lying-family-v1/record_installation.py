from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent update '+str(path))
 tmp.replace(path)
entry='''## James directional lying family installed - 2026-09-30

Installed12 ordinary lie-down/sleep/get-up states, bare/shared-helmet,144 references.
Four independent helmet pitch sources fitted at one calibrated shell scale per
direction; widths35/39/35/33 east/south/west/north. Body outside head edit regions
exact, standing arrivals exact accepted masters, rises reversed, sleep joins shared.
864 packaging checks,744 actual installed-loader checks and794 retained-berth
checks PASS, zero failures; scratch profiles unchanged.36 native q0 north berth
captures reviewed for bare/helmet, using explicit retained room artwork. Current
hab's separately installed east bunk remains its active profile. No all-layout or
continuous full-set polish claim. North breathing uses quiet neutral pending a
coherent source. Runtime inventory:68 retained bare states. Next: swimming/tread
start/stop and turns, then salvage/distress/recovery/death and cross-family polish.
See docs/JAMES_LYING_HANDOFF_2026-09-30.md and family/native-berth-contact.png.

'''
lesson='''

### James helmet shell calibration and retained berth evidence - 2026-09-30

Measure standing shell width above shoulder panels: including shoulders inflated
lying helmets from native35/33 to41/39px. Use one master-calibrated shell scale for
all independently authored pitched heads per direction; no per-frame size fitting.
Erase the owned cranial shape rather than a wide rectangular region that cuts the
collar/shoulder and leaves a floating shell. Review the whole fit after preserving
body pixels outside its recorded head region; exact exterior pixels alone do not
prove a sensible neck join. The final fit retains native shell widths35/39/35/33.
An explicit retained whole-room berth fixture can establish ordinary north pillow
contact through normal chooser/approach and the real renderer without changing
current station art. Label that scope: it does not prove current bunk or every
layout/facing. Evidence: docs/JAMES_LYING_HANDOFF_2026-09-30.md.
'''
for rel,text,prepend in [('docs/CURRENT_STATUS.md',entry,True),('docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',entry,False),('docs/ASSET_PIPELINE_AND_WORKFLOW.md',lesson,False),('docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',lesson,False),('skills/brinespace-character-pipeline/references/crew-consistency.md',lesson,False)]:
 path=R/rel
 if text.splitlines()[0].encode() not in path.read_bytes() if prepend else (b'James helmet shell calibration and retained berth evidence - 2026-09-30' not in path.read_bytes() if text==lesson else b'## James directional lying family installed - 2026-09-30' not in path.read_bytes()):atomic(path,lambda b,t=text.encode(),p=prepend:t+b if p else b+t)
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if b'James helmet shell calibration and retained berth evidence - 2026-09-30' not in path.read_bytes():atomic(path,lambda b:b+lesson.encode())
path=P/'selection.json'
def selected(b):
 m=json.loads(b);m['checks'].update(nativeInstalledLoader=744,nativeRetainedBerth=794,nativePairedCandidate=794);m['helmetSourceProvenance']='helmet-source-origins.json';m['nativeScope']='Actual installed loader all144 slots; retained whole-room q0 north berth, bare/helmet, normal approach,36 captures; other layouts not claimed';return (json.dumps(m,indent=2)+'\n').encode()
atomic(path,selected)
path=R/'character/james-animation-coverage-2026-09-30/audit.py'
atomic(path,lambda b:b.replace(b'Current next work:12 ordinary directional lying/sleeping/get-up states.',b'Current next work: swimming/tread, water start/stop and turns, then cargo/salvage/distress/recovery/death. All12 ordinary directional lying/sleeping/get-up states are now installed in both modes; actual144-slot loader and retained q0 north berth reviewed. North breathing remains a quiet neutral pending a coherent source.'))
print('Installed lying milestone, inventory next steps and pipeline/skill lessons recorded')
