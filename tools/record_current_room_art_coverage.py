"""Record the final current-catalog agent review without rewriting ledger history."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "assets/room-facing-rollout/coverage.json"
OLD = '"current_contract_review": "pending-top-down-owner-contract-review"'
NEW = (
    '"current_contract_review": "agent-native-reviewed-current-catalog",\n'
    '      "current_contract_evidence": '
    '"output/owner-asset-completion-audit-2026-09-12/current-catalog/runtime.json"'
)


def main() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 47:
        raise SystemExit(f"Expected 47 pending current-contract gates, found {count}")
    LEDGER.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print("Recorded current native catalog review for 47 room identities")


if __name__ == "__main__":
    main()
