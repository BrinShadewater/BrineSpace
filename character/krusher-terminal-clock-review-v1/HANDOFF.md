# Project handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: Krusher reusable body trial

## Objective and acceptance
Test existing crew body reuse for Krusher Dom, System Administrator, with matte muted cyan AI & Robotics markings. Match source scale, animation timing and registration; keep this candidate available for review.

## Accepted decisions and constraints
Bill supplies this trial's body. Bare and helmet west terminal poses share the same lower body. Preserve the original models and normal game selection. Other base families need their own compatibility checks.

## Current state
This folder adds a standalone continuous-clock Godot review of character/krusher-terminal-gear-pair-v1. It changes no artwork or game controller. native/review.gd preloads textures and selects poses using one uninterrupted elapsed timeline for three 2,480 ms cycles. run_native.py isolates APPDATA. validate_clock.py checks schedule, pose selection, rendered body binding and owner file preservation.

## Verification
Godot 4.7.2 exited successfully: 57 paired pose events over three cycles. 465 checks passed, zero errors. Total finish overrun 7.679 ms; maximum selection latency 16.044 ms and draw latency 32.647 ms. All 2,930 fingerprinted owner files unchanged. Captured typing and release poses visually inspected; bare/helmet body alignment remains consistent. First-cycle captures are in review/native; later cycles record timestamps without capture stalls.

## Next action
Review complete locomotion cycles for attachment and glove contact. Continuous source timing is verified here; artistic motion acceptance and actual station/controller integration remain separate work. No normal selectors changed.
