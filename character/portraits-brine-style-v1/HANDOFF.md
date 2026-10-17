# Accepted portrait masters

Session closed September 27: see [closeout](../../docs/PORTRAIT_SESSION_CLOSEOUT_2026-09-27.md)
and [matching workflow](../../skills/brinespace-character-pipeline/references/comms-portraits.md).
Safety correction to verification below: the September 26 tests ran without save
isolation and overwrote the owner's comms sidecar. Project instructions record its
restoration from an F8 report zip. Future probes must use scratch APPDATA and
fingerprint the real save folder before/after; do not reuse the old probe as-is.

Updated: 2026-09-26 · Project: Brine Space

## Objective and acceptance
Owner approved the seven BRINE-style portraits and requested installation as profile pictures and preservation as masters. Completed locally.

## Accepted decisions and constraints
Bill, Veld, Branforth, Marsh, Margot, Josh and River PNGs in this folder are the full-resolution masters. BRINE remains character/brine-comms-v14/portrait.png. Preserve these files; future art passes use a new versioned folder. Older source portraits are retained.

## Current state
scripts/architects.gd selects the four crew masters; scripts/companions.gd uses explicit whole paths for the three companion masters. Shared loaders feed profile/selection and applicable comms views. character/installed-portraits.json and this folder's manifest record installation. Exact prompts and reference/output SHA-256 hashes retained. review.html now labels accepted masters and previous images. docs/CURRENT_STATUS.md records owner acceptance. No commit or playable export made.

## Verification
All seven master hashes match the generated reviewed sources; PNGs covered by Git LFS attributes. Native Godot 4.7.2 check passed four crew comms portraits at 1600x900 and 960x540 plus all three companions through their actual portrait loader at 160x170 profile size. Companion sheet and Marsh 960 capture visually inspected: readable, fitting images. Native logs and captures: output/portrait-masters-2026-09-26/. Initial probe incorrectly attempted companion dialogue, rejected by transmit as designed; corrected to test companion portrait loader directly. No gameplay change.

## Next action
No remaining installation work. Restart an already-running game to clear cached portraits. Future executable builds need a fresh export to include the new masters.
