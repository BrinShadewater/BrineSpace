# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: private bay scope safety and actual return lifecycle

## Objective and acceptance
Continue all performance, bug and PC/Mac readiness requirements; keep scope private until full relevant behavioral and repeated native/visual evidence supports admission. Preserve clocks, selected art and owner data. No itch action.

## Accepted decisions and constraints
Scope eligibility/fallback unchanged from accepted private experiment. Normal runtime source unchanged this turn. Actor checkpoint tests are not full RunSave/Continue certification; short mission lifecycle is not the required two-hour native soak.

## Current state
Private D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/bay-safety/{test.gd,run.py,result.json,owner.json}; bay-return-runtime/ contains independent actual bootstrap, identical private source/overrides, extended adapter and reports. Production source scope/mission changes still unadmitted. Earlier paired136ms result remains single-pair evidence.

## Verification
Safety matrix72 checks/zero failures, isolated headless. Exact route/failure parity against frozen full mission implementation: boarding/return lock eligible; approach/unload/open station/fire/outside endpoint full; hardware locks/room locks/blocked target scoped failure falls back full. Successful approach/unload now use their actual intended targets, not wet-bay boarding target. Scope request reset; partial signature invalidated; full fallback graph size/signature current. Incremented layout geometry revision clears sentinel obsolete cache (revision test, not actual moved-prop visual acceptance). Serialized actor checkpoint validates, preserves route/position/reservation and restores a full graph with scope request default -1; no scope field saved. Ordinary subsequent full rebuild restores exact global point map and signature. Pause/power loss preserve mission clocks/state. Demolishing bay releases reservation and marks partial graph stale; explicit subsequent full rebuild recovers remaining station. No normal Main input/playable demolition certificate. First65-check evidence retained.

Extended native actual debug=false1080p candidate:40rooms/four crew/three naturally dispatched missions, idle1/2/4x1,000 measured frames each (3,000 total), uncapped/focused. All three complete approach/seal/flood/boarding/launch/outbound/work/return/disembark/exit_bay/drain/unload/idle. Two scoped crossings per pilot,1,319 nodes each, ZERO fallbacks. At final settled state every assignment empty and all four actors have full occupied-cell geometry. Logs clean/error/warning/leak/missing-art guards pass. Compiled NPC and mission hashes checked; same canonical/private source inputs. Reports candidate.json, identity-candidate.json, owner-candidate.json; resolved scratch profiles guarded, owner2,936 files unchanged; adapters restored, all handles terminal.

Extended-run frame means45.410/44.272/44.167 ms; p9552.651/51.522/55.816; maxima113.384/124.919/171.821. Different longer fixture, no matched baseline or FPS acceptance. Largest4x frame653: crew89,371us/step90,110us/engine wait81,693us; simultaneous drone uploads289,013,760 bytes. Another4x frame905128.710ms: crew89,646us/step90,350us/wait38,339us/no uploads. Early1x frame974113.384ms: step1,347us/wait112,009us/uploads240,844,804 bytes. CPU rebuild and upload/wait costs remain separately reproducible. Rendering timing disabled/unavailable. Peak2,346.502MiB, exit228.259MiB, uploads4,074; longer run changes exposure, no storage improvement claim.

## Next action
Actual early recall/cancellation during scoped crossing and full RunSave/Continue lifecycle still need scoped-candidate checks. Actual moved/deleted props and engine focus/pause timing, all simulation/frame rates and repeated reverse-order native pairs/visual checks remain before admission. Instrument scoped rebuild stages to distinguish cold local graph geometry from full graph restoration at return/unload; pursue measured reductions and avoid merely delaying gameplay. Drone upload/capture stalls and ordinary drawing still block60FPS. Full original nine packaged bugs, Windows/Mac frozen exports/audits, texture/loading/endurance and target hardware/signing remain open.
