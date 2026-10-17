"""Add living and held-death fresh Continue without changing the running suites."""
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
fresh=(R/'tests/test_veld_bunk_selected_approach.gd').read_text(encoding='utf-8')
normal=fresh[fresh.index('\t# Production selection only;'):fresh.index('\treturn game',fresh.index('\t# Production selection only;'))]
s=(R/'tests/test_veld_bunk_body_resume.gd').read_text(encoding='utf-8').replace('test_veld_bunk_body_resume','test_veld_bunk_selected_continue').replace('veld-bunk-body-resume-v1','veld-bunk-selected-continue-v1')
a=s.index('\tgame.grid_view.veld_player.load_manifest',s.index('func fresh'));b=s.index('\treturn game',a);s=s[:a]+normal+s[b:]
assert 'load_manifest(' not in s and 'load_equipment_manifest(' not in s
(R/'tests/test_veld_bunk_selected_continue.gd').write_text(s,encoding='utf-8')
(R/'tests/test_veld_bunk_selected_continue.gd.uid').write_text('uid://d0evbknsela6\n',encoding='utf-8')
t=(R/'tools/run_veld_bunk_body_resume.py').read_text(encoding='utf-8').replace('test_veld_bunk_body_resume','test_veld_bunk_selected_continue').replace('veld-bunk-body-resume-v1','veld-bunk-selected-continue-v1')
anchor="    inputs+=list((ROOT/'character/veld-bunk-body-master-v1/frames').rglob('*.png'))"
t=t.replace(anchor,"    inputs+=[ROOT/'scripts/grid_canvas.gd',ROOT/'scripts/crew_sprite_player.gd',ROOT/'character/ACTIVE_ASSETS.json']\n    inputs+=list((ROOT/'character/veld-bunk-early-fall-v1/frames').rglob('*.png'))\n    inputs+=[ROOT/'character/veld-bunk-early-fall-v1/bare-manifest.json',ROOT/'character/veld-bunk-early-fall-v1/helmet-manifest.json']\n"+anchor)
(R/'tools/run_veld_bunk_selected_continue.py').write_text(t,encoding='utf-8')
print('Eight normal living/held-death disk Continue cases prepared separately')
