from pathlib import Path
import json
P=Path(__file__).resolve().parent
template=(P.parent/'bill-reading-entry-east-v1/index.html').read_text()
packs={}
order=['sit-down-east','sit-idle-east','read-seated-enter-east','read-seated-east','read-seated-east','read-seated-exit-east','sit-rise-east']
for gear in ['bare','helmet']:
    states={s['id']:s for s in json.loads((P/(gear+'-manifest.json')).read_text())['states']}
    for s in states.values():
        s['frameFiles']=['../../'+f.removeprefix('res://') for f in s['frameFiles']]
    packs[gear]=[states[key] for key in order]
start=template.index('const packs=')+len('const packs=')
end=template.index(';let time=',start)
template=template[:start]+json.dumps(packs)+template[end:]
template=template.replace('Bill east tablet transitions','Bill east seated family').replace('Bill — east tablet transitions','Bill — east seated family')
template=template.replace('Take out tablet, read, put it away. Exact seated/reading endpoint joins and native selected east helmet. Candidate preview; live stage wiring remains pending.', 'Sit, breathe, take out tablet, read, put away and rise. All six actions selected in the normal renderer with exact stage joins. Live east reading activity, interruption/restore and furniture review remain pending.')
(P/'index.html').write_text(template)
print('Built complete east seated family preview')
