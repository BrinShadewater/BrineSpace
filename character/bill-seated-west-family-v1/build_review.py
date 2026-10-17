from pathlib import Path
import json
P=Path(__file__).resolve().parent
template=(P.parent/'bill-reading-entry-west-v1/index.html').read_text()
packs={}
order=['sit-down-west','sit-idle-west','read-seated-enter-west','read-seated-west','read-seated-west','read-seated-exit-west','sit-rise-west']
for gear in ['bare','helmet']:
    states={s['id']:s for s in json.loads((P/(gear+'-manifest.json')).read_text())['states']}
    for s in states.values():
        s['frameFiles']=['../../'+f.removeprefix('res://') for f in s['frameFiles']]
    packs[gear]=[states[key] for key in order]
start=template.index('const packs=')+len('const packs=')
end=template.index(';let time=',start)
template=template[:start]+json.dumps(packs)+template[end:]
template=template.replace('Bill west tablet transitions','Bill west seated family').replace('Bill — west tablet transitions','Bill — west seated family')
template=template.replace('Take out tablet, read, put it away. Exact seated/reading endpoint joins and native selected west helmet. Candidate preview; live stage wiring remains pending.', 'Sit, breathe, take out tablet, read, put away and rise. All six actions selected in the normal renderer with exact stage joins. Live west reading activity, interruption/restore and furniture review remain pending.')
(P/'index.html').write_text(template)
print('Built complete west seated family preview')
