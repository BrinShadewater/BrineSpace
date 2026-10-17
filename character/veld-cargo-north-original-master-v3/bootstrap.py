from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;B=P.with_name('veld-cargo-north-original-master-v2')
assert not (P.parents[1]/'output/veld-cargo-north-original-master-v3/validation.json').exists(),'Bootstrap is one-time preparation; preserve frozen native inputs.'
for name in ['register_source.py','build.py','prepare_native.py','prepare_review.py']:
    s=(B/name).read_text().replace('veld-cargo-north-original-master-v2','veld-cargo-north-original-master-v3').replace('raw-unload-v4.png','raw-unload-v5.png').replace('cvldcargonorthorig2','cvldcargonorthorig3')
    if name=='prepare_review.py':
        start=s.index("(P/'EXECUTIONS.json').write_text")
        end=s.index("print('Two all-pose",start)
        s=s[:start]+s[end:]
        s=s.replace('Suit shading and older held/gait/turn joins still need refinement; staged only.','Original charcoal suit material refined; older held/gait/turn joins remain open. Staged only.')
    (P/name).write_text(s)
shutil.copy2('C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-0f892780-36fc-409c-b74a-c8612798926a.png',P/'raw-unload-v5.png')
print('New North material interval prepared; previous evidence preserved.')
