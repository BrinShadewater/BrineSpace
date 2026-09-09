# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: interactive station hardware

## Objective and acceptance
Integrate the approved two-row hardware sidebar and connect all eight controls, with animated feedback and saved settings.

## Accepted decisions and constraints
Power stops room production and drone operations; stored reserves remain and crew upkeep continues. Walls/Base hides shells and foundations without changing placement topology. Comms opens the existing compact typewriter popup. Interior lights use the room-light fade; Exterior lights control muted perimeter marker lamps. Sprinklers animate visual spray in powered full rooms, with no resource costs or fire suppression. Pumps gates every room with base water production (currently Tidal Condenser) without changing manual suspension. Doors blocks internal crew routing and holds drone operations; existing airlock safety cycles are separate. A crew member near a threshold prevents locking until clear.

## Current state
Latest finish revision: owner selected darker teal to match the main UI, superseding the olive-gray reference interpretation. Panel and bevels now use dark petrol teal, with cool pale labels and neutral/cool hardware tint; the brushed metal texture and status accents remain. Native hardware checks pass (`output/hardware-dark-teal.log`), with refreshed 1600/960 captures. The 1600 capture was visually inspected.

Latest placement/material revision: Station Controls sits below the inspector and above general Controls. `hardware_panel.gd` adds a stationary fine-grain brushed gunmetal shader behind the hardware, with a gray steel border. Native hardware checks pass and 1600/960 screenshots show the panel fully visible (`output/hardware-gunmetal.log`). Existing opaque asset backing is retained.

Latest owner layout: Walls/Base and Sprinklers use levers, Doors a rocker. Two switch rows now have a 6-pixel gap. Power and Comms artwork both span 156 logical pixels, matching the stacked rows from top artwork to bottom artwork; aspect ratios are preserved with 100/90-wide frames. Small switches remain 82 wide. The sidebar is 504 logical pixels wide, with matching station/hand bounds. This supersedes prior spacing and sizing experiments. Native 1600/960 review and hardware/compact Comms checks pass (`output/hardware-stack*.log`).

New `scripts/hardware_panel.gd` and `scripts/station_hardware.gd`, paired UIDs. Integration in main, grid_canvas, bill_npc and run_save. All controls have focus/hover feedback, endpoint fades and button press displacement; Power supports directional vertical dragging and click/keyboard toggling. These are endpoint transitions, not a newly authored articulated lever animation. Settings persist in optional validated checkpoint data; older saves use defaults. The earlier standalone Comms button is hidden in favor of the speaker hardware.

## Verification
Native hardware fixture covers all eight controls, pumps and manual suspension, power forecasts and reserves, interior light targets, locked crew segments, save/read/restore, legacy saves, malformed-state rejection, comms access, lever drag, two-size bounds, and rendered spray changes over time. Compact Comms regression and power expansion checks pass. Native panel screenshots inspected at 1600x900 and 960x540; evidence under `output/hardware/`. Import succeeds. Existing raw-image import warnings remain; no export was produced.

## Next action
Owner playtest of the panel in normal room building. Native evidence validates integration; owner visual acceptance remains. Long-term pump networks and gameplay fire suppression are outside this pass.
