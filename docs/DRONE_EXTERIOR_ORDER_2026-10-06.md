# Project handoff

Updated: October 6, 2026 · BrineSpace · Exterior palette ordering prerequisite

## Objective and acceptance
Preserve surrounding draw order while preparing the lossless drone storage
prototype for actual 40-room integration. Whole-station performance remains open.

## Accepted decisions and constraints
Normal source/art/settings unchanged. Isolated profile verified before writes;
all 2,936 owner non-log files unchanged. No export or normal admission.

## Current state
Private `output/drone-coordinate-2026-10-06/exterior-order/` copies the ordered
session provider. Adds line command slots and a RefCounted adapter so actual
`scripts/drone_dust.gd` draws into the same ordered sequence as body/wheels/cargo/
effects/lamp. No shadowing native CanvasItem methods. Generator at
`output/drone-coordinate-2026-10-06/prepare-exterior-order.py`.

Inspection of current grid confirms harvest/construction precede drones, dust
must precede each individual body, and admin lines/survey follow the fleet.
Simply adding body children beneath the existing parent would change this order.

## Verification
Native Godot 4.7.2 Compatibility, RTX 4070 Ti: 74 checks, zero failures/errors,
72 exact raster pairs. Actual current dust and full drone drawing; effects quality
0/1/2, reduced motion on/off, nearest/linear, zero/one/two overlapping drones,
two mining frames including active effect frame, loaded second drone, fractional
translation/nonuniform parent scale. Contrasting crossing lines before/after
the fleet establish surrounding command order. Empty/fewer actors hide stale slots.
Both palette/fallback exercised; last owner exit clears copied cache. Clean exit.
Results/log/owner fingerprints retained in private directory.

These are boundary sentinel lines, not actual harvest/construction/admin/survey
art. Dust is deliberately forced beside mining frames to test order; this does
not certify gameplay's drive eligibility or full station behavior. No FPS,
station memory, preparation cost, packaged release or Mac claim.

## Next action
Integrate a physical grid/Main/40-room fixture using separate ordered exterior
sections or complete command capture. Preserve actual transforms, per-drone
dust/body order, post-fleet effects and scene ownership. Measure extra nodes,
commands/material allocations and upload/frame/memory costs against baseline.
Raw binary indices remain disposable fixture assets; release encoding/hash checks,
linear residency policy, other atlas families and all release gates remain open.
