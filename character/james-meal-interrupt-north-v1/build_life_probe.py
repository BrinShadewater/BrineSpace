from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
source=(R/'tests/test_crew_life_rooms.gd').read_text()
source=source.replace('check(npc.stage in ["life_sleep","life_seated","observation_read"],id+" settled")','print("LIFE SETTLE STATE ",JSON.stringify({"room":id,"rotation":q,"actor":actor,"initial":initial,"stage":npc.stage,"timer":npc.timer,"tabletSequence":npc.tablet_reading_sequence()}));check(npc.stage in ["life_sleep","life_seated","observation_read"],id+" settled")')
source=source.replace('if initial=="observation_sit":check(npc.stage=="observation_rise",id+" reader rises on interruption")','if initial=="observation_sit":print("LIFE INTERRUPT STATE ",JSON.stringify({"room":id,"rotation":q,"actor":actor,"stage":npc.stage,"timer":npc.timer,"tabletSequence":npc.tablet_reading_sequence()}));check(npc.stage=="observation_rise",id+" reader rises on interruption")')
(P/'native-life-probe.gd').write_text(source)
print('Created temporary-state probe of existing72-case fixture; no runtime edits')
