# Expedition reward count handoff

Updated: 2026-10-23 / Project: BrineSpace

## Objective and acceptance
Owner requested rapid ticking numbers with a small landing sparkle and a rewarding,
slot-machine-like feel, within the existing terminal interface.

## Accepted decisions and constraints
Short accelerating-feel count followed by eased landing, lightly staggered figures,
stronger Data landing. Controls remain available. Respect reduced motion and zero
rewards; no reward, game-artwork or simulation animation changes. No extra sound added.

## Current state
- scripts/reward_count.gd (+ UID): label-owned bounded count, reserved final width,
  exact landing, brightness pulse and mint/gold drawn sparkles. Maximum duration
  about 1.4 seconds including the hero's delay and landing. Hidden labels and reduced
  motion settle immediately. Nodes stop processing on completion and die with labels.
- scripts/expedition_report.gd and main.gd: reveal starts once after report text
  scaling; hero and five expedition figures animate. Spendable balance stays factual;
  progression return refreshes state without restarting the reveal.
- tests/test_reward_count.gd (+ UID): monotonic/no-overshoot counts, small and large
  values, exact final text, normal brightness restoration, zero, reduced motion and
  mid-reveal hide/preferences changes.
- tests/test_expedition_report_native.gd: intermediate count, landing sparkle,
  unchanged recorded payout, reduced-motion initial report and existing UI/purchase
  coverage. tests/index.json includes numeric test in expedition-report group.

## Verification
- Numeric headless PASS: output/test-runs/20261023-132944-headless.
- Final native PASS: output/test-runs/20261023-133039-native; clean log.
- Counting and landing captures reviewed in output/expedition-reward-count-20261023;
  normal, compact 130%, details and empty failure captures also produced. Landing
  capture deliberately advances the hero while smaller figures continue naturally.
- Scoped whitespace check passed. Runner isolated APPDATA for every Godot test.
  Protection receipts D:/bs-tutorial-20261021/ending-count-before.json and
  ending-count-after.json: 2,971 owner profile files unchanged; signed ZIP unchanged.

## Next action
Owner timing/feel review during a natural expedition ending. Source changes only.
