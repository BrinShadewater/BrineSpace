# Source and generation record

The owner-approved identity is `sources/mining-approved-v10.png`, copied from
`C:/Users/Alex/Desktop/BrineSpace Clean Prop Exports/drone-animation-bases/approved-v10/sources/mining-base.png`.
The visual bible and the polished Construction south pose informed material,
camera and scale. A compact front drill was added for the mining action.
All generated sources remain preserved; selected files are hashed in manifest.json.

Imagegen was used for source generation and revisions. The following records
summarize the editing instructions, not verbatim prompt transcripts:

| Local source | Generation ID | Instruction/result |
| --- | --- | --- |
| south-v1.png | exec-02a1d342-5d0f-4db3-85df-2e6834a13676 | Preserve the four-wheel Mining identity and overhead/shallow-front view; add a compact stowed drill; no hovering or propellers. Cyan too bright. |
| south-v2-material-rejected.png | exec-aa814792-0d1b-4de1-89e7-9023515708c1 | Transfer muted room-prop materials; rejected because it made the chassis blue and too worn. |
| south-v3.png | exec-b60df78b-849b-4160-9f81-4ba30f1a6e0d | Reduce cyan saturation and white highlights; retain gray steel and the existing geometry. |
| south-v4.png | exec-0c97e69f-507c-47fb-8bdc-637d8b378481 | Remove only the small rear roof vent to leave a clean separate-lamp position. Selected south source. |
| cardinals-v1-rejected.png | exec-6453dc2f-fe7b-44b4-b369-9454a2533a65 | Four cardinal views. Rejected: east/west tyres did not turn with the chassis. |
| east-west-v2.png | exec-29473254-d29e-41a2-81ef-37574da12a79 | Correct side views: all four tyre rolling axes follow the horizontal body direction. Selected both cells. |
| north-v2.png | exec-8e118a08-033e-4ca5-beb6-252c17f87553 | Full north-facing rover, drill at far end, blank rear roof at near end. Selected. |
| diagonals-v1.png | exec-728bf508-69ba-40cf-93c1-2b3bc9bd8499 | Four independent diagonal views. Superseded because central bodies were too long. |
| diagonals-v2-extra-tools-rejected.png | exec-1e325852-4c88-4390-aaf0-87856a39a06d | Shorten central bodies while preserving wheelbase; selected SE/SW only. NE/NW had erroneous extra rear drills. Filename records sheet-level rejection, not rejection of the two selected cells. |
| diagonals-v3-selective.png | exec-0aa39db0-dc03-408b-bbd7-496b2b17a004 | Replace NE/NW extra rear drills with gray caps. Selected NE/NW only; SE incorrectly lost its front drill. |

No whole-sprite rotations or mirrored views were used. Python performs alpha
component isolation, proportional registration, local tyre/drill articulation,
effect rendering, atlas assembly and review exports. Generated views retain some
illustrative variation; these are review candidates, not a measured 3D model.

Completion supplement reuses the generated ore-only frame at
`assets/drone-motion-v2-2026-09-26/cargo/job-collect-south/090.png`. The isolated
alpha bounds are reduced to an 18-pixel-high fragment and composited along the
front tool/processing-bay axis. Its source hash is recorded under `completion`
in manifest.json. Cargo, status emission and body remain separate layers. Power
states reuse stationary chassis pixels; acceleration/deceleration reuse the
registered rolling frames. No additional vehicle designs were generated.
