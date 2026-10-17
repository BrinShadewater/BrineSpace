from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'james-meal-pickup-south-v1/native-candidate.gd').read_text()
source=source.replace('const OUT := "res://character/james-meal-pickup-south-v1/"','const OUT := "res://character/james-meal-service-south-open-v1/"')
source=source.replace('"library/sp-galley-2":[60.0,80.0],"library/sp-galley-4":null','"library/sp-galley-2":null,"library/sp-galley-4":null,"library/sp-generated-counter-galley-prep":[0.0,126.0]')
source=source.replace('native-candidate-evidence.json','native-contact-evidence.json')
source=source.replace('Fixture-only custom bought counter moved to[60,80], second counter omitted; no owner layout edit.', 'Dedicated in-memory open prep counter at[0,126], North-only raised-backboard counters omitted. Registered open counter supports both service sides; no owner layout edit.')
source=source.replace('npc.rebuild(game);npc.dead=false;', 'npc.rebuild(game);var prep:Dictionary=npc.geometry[cell].props.filter(func(prop):return prop.id=="library/sp-generated-counter-galley-prep")[0];check(Rect2(-184,-184,368,368).encloses(prep.rect),"Open prep counter floor footprint wholly inside hull");print("OPEN PREP RECT ",prep.rect," COLLISION ",prep.get("collision",[]));npc.dead=false;')
source=source.replace('JAMES SOUTH BOWL CANDIDATE','JAMES SOUTH OPEN COUNTER CONTACT')
(P/'native-contact.gd').write_text(source)
print('Supported open-counter South contact fixture prepared; old bowl candidate remains a contact diagnostic only.')
