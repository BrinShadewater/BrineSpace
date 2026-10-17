"""Reuse the authored mid-rise drawing; leave every source file unchanged."""
INDICES = [0, 1, 2, 3, 4, 2, 5]
DURATIONS = [80, 100, 100, 90, 40, 40, 70]

def add_midrise(state):
    assert state['id'] == 'unload-north' and state['frameCount'] == 6
    for field in ['frameFiles', 'facings', 'waterKinds', 'waterPoses', 'depthOffsets']:
        assert len(state[field]) == 6
        state[field] = [state[field][i] for i in INDICES]
    state['frameCount'] = 7
    state['frameDurationsMs'] = DURATIONS.copy()
    poses = state['provenance']['sourcePoses']
    state['provenance']['sourcePoses'] = [poses[i] for i in INDICES]
    state['provenance']['derivation'] = 'Reversed pickup with existing mid-rise reused before standing; exact idle/carry endpoints,520ms; no new artwork'
    state['provenance']['returnTiming'] = 'Original80ms shallow-rise hold split40+40 between shallow and existing mid-rise'
    return state
