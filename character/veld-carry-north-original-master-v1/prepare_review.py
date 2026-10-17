from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'character/veld-cargo-north-original-master-v3/prepare_review.py').read_text().replace('veld-cargo-north-original-master-v3','veld-carry-north-original-master-v1')
s=s.replace(".replace('282','172')", ".replace('282','282')").replace(".replace('12 chronological boards','6 chronological boards')", ".replace('12 chronological boards','12 chronological boards')")
s=s.replace(".replace(\"['unload-north', 'pickup-north', 'carry-start-north', 'carry-stop-north', 'carry-north', 'idle-north']\",\"['unload-north','pickup-north','idle-north']\")",'')
s='\n'.join(line for line in s.split('\n') if not line.startswith("html=html.replace('<option"))
start=s.index("for gear in ['Bare','Helmet']:");end=s.index("(P/'index.html').write_text",start)
s=s[:start]+s[end:]
s=s.replace('Veld North original cargo repair','Veld North original carry family').replace('Veld North - original cargo repair','Veld North - original carry family')
s=s.replace('paired-unload.png','paired-gait-held.png')
s=s.replace('Whole-source North cargo repair restores quilt detail and wider standing legs against the original master. Shared helmet and exact resting endpoint retained. Original charcoal suit material refined; older held/gait/turn joins remain open. Staged only.','Original-master North carry gait now shares the repaired cargo body/material and whole helmet. Pickup/start/carry/stop/idle endpoints agree. Start/stop ramps derive from whole gait poses; turn joins and gameplay review remain open.')
s=s.replace("sorted(P.glob('prompt-unload-*.txt'))","sorted(P.glob('prompt-gait-*.txt'))").replace('32 distinct poses','60 distinct poses')
exec(compile(s,str(P/'prepare_review.py'),'exec'),{'__file__':str(P/'prepare_review.py')})
