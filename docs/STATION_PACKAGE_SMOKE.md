# Checkout-independent station asset smoke test

This is a local PCK dependency test, **not a standalone release export**. No
export preset or installed export template was found during this pass. Do not
treat this evidence as Windows distribution, installer, or release acceptance.

`tools/package_station_fixture.gd` follows quoted res:// dependencies from the
real project and underwater station fixture, includes dynamic animation folders,
and records each packaged file's SHA-256 in a sidecar manifest. It refuses an
existing destination. It is not a general GDScript dependency parser: dynamically
constructed paths outside the included folders still require explicit coverage.

## Observed result

- V1 contained raw images but omitted imported resource dependencies. Rooms drew,
  yet RichTextLabel card cost icons failed to load. The fixture printed PASS
  despite resource errors: its assertions did not cover this failure.
- V2 includes raw image bytes **and** available `.import` remaps and their compiled
  dependencies. The package contains 1,544 files. Generated imports remain local,
  ignored source-control files; packaging them does not mean committing them.
- Ran V2 with `--main-pack` from an empty temporary directory outside the checkout,
  using the real station fixture and its isolated save. Exit code 0; no ERROR or
  SCRIPT ERROR entries; 1,616 narrow-floor path samples and all four rotations pass.
- Inspected the packaged station capture: room art, connected narrow hulls,
  character, complete draft silhouettes and resource icons are present.
- Evidence: `output/station-package-v2.pck.json`, `output/station-package-v2.log`,
  and 85 PNGs under `output/station-package-v2-captures/`.

Raw `Image.load` export warnings remain. This test proves the explicitly packaged
source files are readable, not that default editor export rules include them.
Preserve runtime raw-PNG loading; a future release preset must retain those bytes
and be tested using the actual exported executable. Do not hide these warnings
and claim release compatibility.

## Reproduce

Run Godot headless in the checkout with `--script
res://tools/package_station_fixture.gd -- --package=<new absolute .pck path>`.
Then launch Godot from an empty external directory with `--main-pack <pack path>
--script res://tests/playtest_underwater_station.gd --log-file <absolute log>
-- --capture-dir=<new absolute capture directory>`.

Always inspect the entire log as well as exit status and fixture assertions.
Do not publish the pack; NOTICE.md rights still apply.
