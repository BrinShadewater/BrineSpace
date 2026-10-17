"""Freeze accepted west actions and retain bare art with matching timing."""
import copy
import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'bill-west-actions-coherent-v1'
BARE = HERE.parent/'major-bill-v3/packs/bare-256x256-p128-224'


def main():
    selected = json.loads((SOURCE/'manifest.json').read_text())
    selected.update(name='Bill accepted equipped west actions', status='owner_visual_accepted_2026_09_29')
    hashes = {}
    for state in selected['states']:
        for rel in state['frameFiles']:
            dest = HERE/rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE/rel, dest)
            hashes[rel] = hashlib.sha256(dest.read_bytes()).hexdigest()
    bare = json.loads((BARE/'manifest.json').read_text())
    states = {state['id']: state for state in bare['states']}
    bare['states'] = []
    bare.update(name='Bill retained bare west actions with accepted cadence', status='retained_art_timing_only')
    for selected_state in selected['states']:
        state = copy.deepcopy(states[selected_state['id']])
        assert len(state['frameFiles']) == len(selected_state['frameFiles'])
        state['frameDurationsMs'] = selected_state['frameDurationsMs']
        state['frameFiles'] = ['../major-bill-v3/packs/bare-256x256-p128-224/'+rel for rel in state['frameFiles']]
        state['provenance'] = 'retained bare artwork; timing matched to accepted equipped west'
        bare['states'].append(state)
    for filename,data in [('manifest.json',selected),('bare-timing-manifest.json',bare),('frame-hashes.json',hashes)]:
        (HERE/filename).write_text(json.dumps(data,indent=2)+'\n')
    print('Selected west: 24 equipped frames; four retained bare states retimed')


if __name__ == '__main__':
    main()
