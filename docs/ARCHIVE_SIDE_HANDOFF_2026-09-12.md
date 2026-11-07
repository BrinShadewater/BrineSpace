# Data Archive side-art handoff

Updated: 2026-09-12. Project: Brine Space.

## Objective and acceptance
Continue all-room directional art improvements, addressing owner dislike of side elevations. Wall equipment must face inward and fit its host; native review is required.

## Accepted decisions and constraints
Low overhead companions with matte department materials. Preserve original sources, functional inventory, doorway clearance and central equipment. Newly authored east may mirror west.

## Current state
Selected assets/archive-directional-v1/side-overhead.png in four east/west cartridge/index registrations; previous registrations and exact prompt preserved. Five cartridge drawers, two screens/keyboards, one reader. Source has verified alpha. Split-wall registration now carries optional operating_screens; split draw reuses room_asset_library.draw_operating_screens, extracted from the existing library draw path. data_archive_view marks screen-bearing banks animated so retained rendering advances telemetry.

## Verification
Both native powered side views and retained west reviewed. All baseline prop metadata and q0/q2 RGB remain identical; existing q0 card retained. Six direct/retained captures exit 0; eight isolated screen cases across east/west and both renderers change with power and time. 176 layouts and existing 20 variant regressions pass 20260912-150747-headless. Evidence: assets/archive-directional-v1/side-overhead-review.json and output/archive-overhead-2026-09-12.

## Next action
Continue other room side-camera repairs. Actual station pause and owner aesthetic acceptance remain open. No export or commit.
