from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent
config=P/'anatomy-config.json';before=P/'anatomy-config-before-north-polish.json'
if not before.exists():shutil.copy2(config,before)
c=json.loads(config.read_text());audit=json.loads((P.parent/'james-air-north-v1/recovery-v3-audit.json').read_text())
c['north']['heads'][6:]=audit['heads']
c['north']['recover-air'].update(scale=22/102,ruler='102px visually reviewed rear cranium against22px selected master skull; independent fixed dry source scale',cropFolder='recovery-crops-v3',sourceFile='recover-source-v3.png')
config.write_text(json.dumps(c,indent=2)+'\n')
source=(P/'native-installed.gd').read_text().replace('native-installed-bare-contact.png','native-north-polish-bare-contact.png').replace('native-installed-helmet-contact.png','native-north-polish-helmet-contact.png').replace('JAMES AIR INSTALLED:','JAMES NORTH AIR POLISH:')
(P/'native-north-polish.gd').write_text(source,encoding='utf-8')
source=(P/'native-installed-behaviour.gd').read_text().replace('for d in ["east","south","west","north"]:', 'for d in ["north"]:').replace('installed-behaviour-captures','north-polish-captures').replace('installed-behaviour-evidence.json','north-polish-evidence.json').replace('JAMES AIR INSTALLED BEHAVIOUR:','JAMES NORTH AIR POLISH BEHAVIOUR:')
(P/'native-north-polish-behaviour.gd').write_text(source,encoding='utf-8')
print('Selected master-only North recoveryv3; other seven action rows unchanged')
