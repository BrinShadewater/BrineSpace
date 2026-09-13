"""Reconcile facing ledger with a freshly exported RoomDatabase catalog.

Read-only audit. Stages and evidence references are declarations, not visual
acceptance. This reports unresolved language rather than promoting entries.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def audit(catalog, ledger):
    expected = {r['id'] for r in catalog}
    rows = ledger['rooms']
    counts = Counter(r['room'] for r in rows)
    stages = Counter()
    review_candidates = []
    missing_directions = []
    contract_reviews = Counter()
    missing_contract_evidence = []
    for row in rows:
        contract_reviews[row.get('current_contract_review', 'unspecified')] += 1
        if row.get('current_contract_review') == 'agent-native-reviewed-current-catalog' and not row.get('current_contract_evidence'):
            missing_contract_evidence.append(row['room'])
        for direction in ['north', 'east', 'south', 'west']:
            entry = row.get('directions', {}).get(direction)
            if not entry:
                missing_directions.append([row['room'], direction])
                continue
            stage = entry.get('stage', 'unspecified')
            stages[stage] += 1
            # Nested notes may describe unfinished host fit despite a reviewed stage.
            text = json.dumps(entry).lower()
            flags = [word for word in ['pending', 'missing', 'uninstalled', 'requires-',
                     'repair-required', 'inventory-other', 'reverted', 'library'] if word in text]
            if flags:
                review_candidates.append(dict(room=row['room'], direction=direction,
                                       stage=stage, flags=flags))
    return dict(catalog_count=len(expected), ledger_count=len(rows),
                missing_rooms=sorted(expected-set(counts)),
                unexpected_rooms=sorted(set(counts)-expected),
                duplicate_rooms=sorted(k for k,v in counts.items() if v>1),
                missing_directions=missing_directions,
                stage_counts=dict(sorted(stages.items())), review_candidates=review_candidates,
                current_contract_counts=dict(sorted(contract_reviews.items())),
                missing_current_contract_evidence=sorted(missing_contract_evidence),
                owner_feedback=ledger.get('latest_owner_side_feedback',''),
                limitations='Declared stages and text flags only. Candidates include negated/historical wording and need manual review; absence of flags is not acceptance. No visual, route, state, source-hash or owner acceptance inferred.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', required=True, type=Path)
    parser.add_argument('--ledger', type=Path, default=ROOT/'assets/room-facing-rollout/coverage.json')
    parser.add_argument('--out', required=True, type=Path)
    args=parser.parse_args()
    result=audit(json.loads(args.catalog.read_bytes()), json.loads(args.ledger.read_bytes()))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print(f"Catalog {result['catalog_count']}; ledger {result['ledger_count']}; textual review candidates {len(result['review_candidates'])}")
    for key in ['missing_rooms','unexpected_rooms','duplicate_rooms','missing_directions',
                'missing_current_contract_evidence']:
        print(f'{key}: {result[key]}')
    print(f"current_contract_counts: {result['current_contract_counts']}")
    print('This is inventory reconciliation, not completion or visual acceptance.')

if __name__ == '__main__':
    main()
