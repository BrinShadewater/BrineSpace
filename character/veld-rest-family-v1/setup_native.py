from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_veld_rest_south_candidate.gd').read_text(encoding='utf-8').replace('veld-rest-south-coherent-v1','veld-rest-family-v1').replace('test_veld_rest_south_candidate','test_veld_rest_family_candidate').replace('VELD SOUTH REST CANDIDATE','VELD REST FAMILY CANDIDATE')
a=s.index('\tp.load_manifest');b=s.index('\tvar all_frames:=[]',a)
s=s[:a]+'''\tp.load_manifest(PACKS.bare)
\tcheck(p.load_equipment_manifest("diving-helmet",PACKS.helmet),"Full paired family loads")
\tfor direction in ["east","south","west","north"]:
\t\tcheck(p.frames.has("lie-down-"+direction),"Authored cardinal present")
'''+''.join('\t'+line if line.strip() else line for line in s[b:s.index('\tprint(',b)].splitlines(keepends=True))+s[s.index('\tprint(',b):]
s=s.replace('"lie-down-south"','"lie-down-"+direction').replace('"get-up-south"','"get-up-"+direction').replace('"sleep-south"','"sleep-"+direction').replace('=="south"','==direction').replace('"south",clock','direction,clock').replace('"south",17.43','direction,17.43').replace('action+"-south"','action+"-"+direction')
s=s.replace('var s:Dictionary=m.states[0]','var s:Dictionary={}\n\t\t\tfor entry in m.states:\n\t\t\t\tif entry.id=="lie-down-"+direction:s=entry')
s=s.replace('PACKS[gear].get_base_dir().path_join(s.frameFiles[i])','s.frameFiles[i]')
s=s.replace('"res://output/veld-rest-south-candidate-v1/native-contact.png"','"res://output/veld-rest-family-candidate-v1/native-"+direction+".png"')
(R/'tests/test_veld_rest_family_candidate.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_veld_rest_south_candidate.py').read_text(encoding='utf-8').replace('veld-rest-south-candidate-v1','veld-rest-family-candidate-v1').replace('test_veld_rest_south_candidate','test_veld_rest_family_candidate').replace('VELD SOUTH REST CANDIDATE','VELD REST FAMILY CANDIDATE')
s=s.replace("'native-contact.png'","'native-east.png','native-south.png','native-west.png','native-north.png'")
s=s.replace("(O/'native-east.png','native-south.png','native-west.png','native-north.png').exists()","all((O/f'native-{d}.png').exists() for d in ['east','south','west','north'])")
(R/'tools/run_veld_rest_family_candidate.py').write_text(s,encoding='utf-8');print('Cardinal paired family actual-player fixture prepared.')
