from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'james-death-family-v1/native-restore.gd').read_text().replace('const OUT := "res://character/james-death-family-v1/"','const OUT := "res://character/james-west-water-death-polish-v1/"')
s=s.replace('for d in ["east","south","west","north"]:', 'for d in ["west"]:').replace('for medium in ["dry","flooded"]:', 'for medium in ["flooded"]:')
s=s.replace('32 actual scratch RunSave','4 actual scratch RunSave').replace('16 selected states/gear cases','2 selected West-water gear cases').replace('and16 native terminal captures','and2 native terminal captures').replace('JAMES DEATH DISK RESTORE:','JAMES WEST WATER DEATH DISK RESTORE:').replace('failures;32 actual checkpoint phases','failures;4 actual checkpoint phases')
(P/'native-restore.gd').write_text(s)
print('Prepared actual installed West-water mid/terminal disk restore in both modes')
