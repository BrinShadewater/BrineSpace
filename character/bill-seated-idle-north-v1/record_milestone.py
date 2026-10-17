from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
note='''
Bill north seated breathing candidate — September30,2026: two gear states/12refs,
four authored interior poses plus exact seated transition entry/closure, fixed
source ruler [.214,.251],960ms loop, native rear helmet/body preservation.
37 package and83 native checks pass; native82 contact reviewed;2,914 real non-log
files unchanged. Initial loop fixture used finite elapsed API; corrected to actual
cosmetic player.frame; rejected interval retained. Runtime unchanged. Actual chair
contact, interrupted life stages, reading and remaining life/rest coverage pending.
Evidence: character/bill-seated-idle-north-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill north seated breathing staged — September30,2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
with installed.open('a',encoding='utf-8') as f:f.write(note)
files=['sources/seated-breathing-v1.png','sources/prompt.txt','build.py','bare-manifest.json','helmet-manifest.json','registration.json','verification.json','contact-sheet.png']
evidence={'status':'staged_candidate','generator':'exec-18f46aa3-a499-4db4-a8e7-f9c2b4229716','hashes':{s:hashlib.sha256((P/s).read_bytes()).hexdigest() for s in files},'native':json.loads((ROOT/'output/bill-seated-idle-north-candidate-native-v1/validation.json').read_text(encoding='utf-8')),'scope':'native candidate loader/playback;real furniture/runtime installation pending'}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
print('Recorded north seated breathing candidate milestone')
