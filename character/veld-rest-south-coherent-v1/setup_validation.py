from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];N=P.with_name('veld-rest-north-coherent-v1')
s=(N/'verify_paired.py').read_text(encoding='utf-8').replace('north','south').replace('148/468','148/520').replace('(35,33,4)','(39,35,4)').replace('33/500','35/523').replace("'nativeHelmet':[33,35]","'nativeHelmet':[35,39]")
s=s.replace("head['size'][0] in [32,33] and head['size'][1] in [33,34]","head['size'][0]==35 and head['size'][1] in [29,35,37,38]")
s=s.replace("protected=(xx-cx)**2+(yy-cy)**2>=r['eraseRadius']**2","protected=((xx-cx)**2+(yy-cy)**2>=r['eraseRadius']**2)|(yy>r['eraseYMax'])")
(P/'verify_paired.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_veld_rest_north_candidate.gd').read_text(encoding='utf-8').replace('north','south').replace('NORTH','SOUTH');(R/'tests/test_veld_rest_south_candidate.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_veld_rest_north_candidate.py').read_text(encoding='utf-8').replace('north','south').replace('NORTH','SOUTH');(R/'tools/run_veld_rest_south_candidate.py').write_text(s,encoding='utf-8')
print('South source/pitch/collar protection and native player checks prepared.')
