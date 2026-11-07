# Project handoff

Updated: September 29, 2026 · Project: BrineSpace · Task: card artwork batch 3

## Objective and acceptance
Deliver frame, department emblems, rarity marks and back in the maintained matte
painted style. Owner accepted the final frame treatment on September 29.

## Accepted decisions and constraints
Neutral painted metal at the outer edge, with visible charcoal seams and lighter
raised surfaces. Continuous 2px department-colored inner outline begins at 6px
inset and touches the metal's inner edge. Draw above content so it remains visible.
Colors follow existing room/state styling; unavailable art retains flat fallback.
Logical card 200x284; slice corners16; content margins8/8/8/7 unchanged. Emblems16px,
rarity12px. Hallways stay neutral; Derelict is a condition/category. Removed pile
controls stay hidden; delivered back uses only the retained renderer.

## Current state
15 PNGs, two immutable imagegen sources, prompts, deterministic bake/manifest,
raster validator and native review under assets/sea-life-v1/cards. Refinements in
scripts/card_art.gd, the card-style hunk of scripts/main.gd, tests/test_card_art.gd
and review/build_closeup.py. Existing integration in scripts/draft_card.gd.
Accepted preview: review/frame-closeup-inner-touch-v7.png. Release manifest refreshed;
no executable export. Previous close-ups preserve iteration evidence.

## Verification
75 raster/deterministic rebake checks passed after the final source-art revision.
35 runtime checks pass: output/card-art-20260929-211139. Exact card/text geometry
and native visual review at 960/1280/1600/2560 widths pass: -211148. Card drag passes:
-205817; hand backdrop passed: -201811. Owner profile fingerprints unchanged.
Original baseline retained: -200834. Card-binding parity's 28 newer room-ID failures
are an existing parser limitation; this art work does not change room bindings.

## Next action
Frame visual acceptance complete. Session closed on codex/sea-life-art-closeout;
see docs/ART_SESSION_CLOSEOUT_2026-09-29.md for commit scope and checks. Next batch
is screen-effect maps only when requested. Concurrent shared changes are excluded.
