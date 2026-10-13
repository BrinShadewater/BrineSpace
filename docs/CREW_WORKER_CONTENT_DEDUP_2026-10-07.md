# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: deduplicated pending crew compression

## Objective and acceptance
Reduce verified redundant worker work and startup time in the exact crew memory
prototype. Preserve all selected art/frame identity/metadata/timing and lifetime.
Full PC/Mac release gates remain open; private evidence is not admission.

## Accepted decisions and constraints
Use existing PNG content SHA256 to share pending compression jobs; separate
frame wrappers/path registrations remain. No worker GPU calls. Limit8 queued jobs,
consume/drain all jobs and clear alias tables. No source/art changes to normal game.

## Current state
Preferred private batch `output/crew-worker-dedup-2026-10-07/batch.gd`, generator
`output/compressed-crew-2026-10-06/build-crew-worker-dedup.py`.
Canonical/content/path maps reconnect alias consumers whichever requests first.
Native alias probe, six startup reports/summary and full consumers under private
artifact root. Worker runners/summarizer support --dedup. All physical player,
Slots/Router/flood adapters restored; no normal provider admitted.

## Verification
Native106 checks/zero failures:prior94 source/metadata/mutation/discard/task checks
plus duplicate PNG aliases in verified scratch, one submitted job per content,
alias-first and canonical-first materialization, exact loaded/early counts and
complete temporary alias-map drain. Source6path/24wrapper fixture retained.

Three native diagnostic initial-game worker/control pairs:all full crew state,
loaded/requested/discarded/source counts, compressed payload, presentation storage
and ready/exit reported texture endpoints equal; six clean logs/exits/router release.
Jobs6,622 ->5,834 (788 fewer,~11.90%); peak8/zero unused/jobs left. One compression
job per unique surviving source. Ready1,082.994MiB/exit80.055MiB unchanged.
Request-to-ready old-worker ->dedup:
- First profiles15,272.120 ->14,656.305ms (OS caches uncontrolled).
- Learned pair1:7,493.625 ->7,254.055ms.
- Learned pair2:7,432.002 ->7,279.624ms.
Learned medians7,462.814 ->7,266.840ms (~195.974ms less). Scene load included.
Warm6s gate still fails. First launch is not certified cold comparison.
Worker CPU compression/bounds totals decrease; warm waits remain~.60-.61s.
Do not sum overlapping worker CPU totals into wall time or claim FPS gain.

Full native selected-bank consumers with dedup batch:
- Veld48,579 checks/390clips/3,186 references.
- James167,285 checks/970clips/11,652 references.
- Marsh20,136 checks/228clips/1,190 references.
Total236,000 checks/1,588clips/16,028 references,zero failures/errors/warnings/leaks.
Every source pixel,size/filter/frame metadata/timing matches normal reference;
30/60/120FPS and1/2/4x playback/pause/snapshot restore,1,080 steps each.
Reading interruption remains separate unchanged earlier fixture; these are source
and consumer checks, not full motion-raster/Studio/hardware/packaged acceptance.
Owner2,936 files unchanged in all probes/startup/consumer lanes; all processes terminal.

## Next action
Prefer dedup worker candidate. Test the full provider in an actual debug=false
maintained export with physically frozen private inputs and isolation, including
startup progress, selected crew/flood/Studio/scene transitions and large station.
Diagnostic scene loading alone costs~2.5s; do not assume that cost persists in
compiled packaged release or mask it by excluding scene load. Profile actual
packaged stage durations before spending more time on small queue tuning.
Larger zoom redraw stall and full release gates remain open.
