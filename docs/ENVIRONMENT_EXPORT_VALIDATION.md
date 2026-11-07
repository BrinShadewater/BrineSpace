# Environment packaged-build validation

The source preflight now discovers all raster pack folders automatically, prefers
immutable source-ledger.json over derived manifest.json, and stops for missing
ledgers, unregistered PNGs or PNGs outside a pack. The three historical schemas
retain dedicated hash checks. Five discovery tests pass; the current preflight
covers 93 preserved PNGs.

Latest passing build: `output/environment-export-v23/` retains 93 preserved PNGs
and 66 runtime textures. It adds named captures for the wreck field, current shelf
and overgrown edge, alongside eleven habitats and three station resolutions.
See [composed locations](ENVIRONMENT_COMPOSED_SITES.md) for native review and scope.

Previous passing build: `output/environment-export-v22/` verifies 93 preserved PNGs
across twenty-two packs and 66 runtime textures, including the cable reel. Three
station resolutions and eleven habitats pass. The dedicated debris-cable-reel
capture was visually reviewed. Owner approval remains pending.

Previous passing build: `output/environment-export-v21/` verifies 92 preserved PNGs
across twenty-one packs and 65 runtime textures, including ripple sand. Three
station resolutions and eleven habitats pass. The ripple-sand habitat capture
was visually reviewed. Habitat names now come from completed capture calls,
matching the measured per-renderer texture accounting. Owner approval remains pending.

Previous passing build: `output/environment-export-v20/` verifies 91 preserved PNGs
across twenty packs and 64 runtime textures, including pillow basalt. Three
station resolutions and ten habitats pass. The dedicated rocks-pillow-basalt
capture was visually reviewed. Per-renderer counts are recorded in result.json.

Previous passing build: `output/environment-export-v19/` verifies 90 preserved PNGs
across nineteen packs and 63 runtime textures, including low anemones.
The dedicated life-anemones capture from v18 was visually reviewed; v19 reruns
the same capture suite with stronger runtime cache checks. Three station
resolutions and ten habitats pass in an isolated Windows debug export. Source
hashes and dimensions match the export contract. Owner art approval remains
pending. Earlier results below remain historical evidence.

V19 derives its runtime total from 19 checked renderer caches and records each
count in `captures/result.json`. Every dictionary entry must be a nonempty
Texture2D; explicit expected cache sizes remain assertions. The rock surface
is checked separately. This prevents a stale literal total from masquerading
as measured runtime evidence. The result sums to 63 textures.

V11 failed on an intermediate grid/rock/wreck draw-function signature mismatch
during concurrent work. Both renderer sources accepted the sixth argument before
the fresh v12 export. V11 logs remain preserved and are not passing evidence.

Runner reliability: `tools/wait_environment_process.ps1` monitors only the process
started by the export helper, stops it on logged errors or a ten-minute timeout,
and verifies its executable path before termination. Controlled child-process
checks passed for normal exit, a logged script error and timeout. This prevents
the v7 failure mode from leaving a failed fixture running indefinitely. These
runner checks do not constitute a new packaged art verification.

Latest result: `output/environment-export-v8/` verifies 77 PNGs across ten packs
and 53 runtime textures, including a dedicated red-algae capture that was visually
reviewed. Nine habitats, four service groups and three station resolutions remain
covered. V7 failed during concurrent cryo-renderer changes and is not passing
evidence. The current fixture checks the original 19 wrecks by kind, allowing new
cryo wrecks without weakening the original environment invariant. Use a new output
name such as `environment-export-v9` next time.

Current result: `output/environment-export-v6/` extends verification to 76 PNGs,
nine packs and 52 runtime textures. Three station resolutions, nine habitats and
four service groups were captured from the isolated Windows debug executable.
The volcanic-ash habitat capture was visually reviewed. Use a fresh output name
such as `environment-export-v7` for the next check. Older results below are retained.

Latest evidence: `output/environment-export-v5/` verifies 74 PNGs across eight
packs, 50 loaded runtime textures, three station resolutions, eight habitats and
four dedicated service-wreckage group captures. The isolated executable completed
successfully and the exported fallen acoustic receiver capture was visually
reviewed. Earlier v4 evidence covers the shoal addition. Use output name
`environment-export-v6` for the next run to preserve this evidence.

## Earlier baseline

The Windows debug export passed on 2026-09-06 using Godot 4.6.1. Evidence is in
`output/environment-export-v3/`. Only BRINE.exe and BRINE.pck were copied to a new
temporary directory and launched there, independently of the checkout.

- All 69 preserved PNGs across seven packs matched their recorded SHA-256 hashes
  and dimensions inside the package.
- All 46 runtime textures loaded, including eight wreck stages and basalt.
- The fixture captured the station at widths 1280, 1600 and 2560 and all seven
  habitats. Station and iron-seep images from the equivalent v2 run were reviewed.
- Export and runtime exited successfully with no ERROR or SCRIPT ERROR entries.
  Godot still emits raw Image.load export warnings; exact packaged bytes and
  successful decoding are checked explicitly rather than suppressing warnings.

Repeat from the repository with a fresh evidence directory:

```powershell
./tools/validate_environment_export.ps1 -GodotExecutable 'C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe' -OutputName environment-export-v4
```

The helper checks existing source provenance before generating the packaging
contract, preserves its snapshot, exports, records executable/package hashes,
launches the isolated executable, and requires the fixture's completion result.
Its dedicated `environment_validation` feature selects a test startup scene.
The first attempt using `--script` opened the normal title screen instead: do not
treat a successful executable launch alone as fixture execution.

Captures use an absolute writable directory outside the package. Settings and
save paths are isolated. Results are in `captures/result.json`; logs and
`execution.json` accompany them. The helper retains the temporary executable for
inspection. This verifies a Windows debug export, not a release installer,
cross-platform export, or owner approval of the art.
