# Department door preview

Authored rim: ocean-hatch-rim.png is a new transparent painted steel capsule
with rounded bevel, perimeter gasket and four fasteners. Source 2172x724;
registered region [147,228,1879,266]. Exact prompt and preserved original path
are in ocean-hatch-rim-prompt.json. diving-room.js maps it onto the moving top
plane (56x7 units) and directional overhead leaves. Full-open browser view and
JS syntax checked. Original generated pixels preserved.

Full chamber swim route: inner endpoint y=190; outer endpoint (-70,-115).
The north opening now clears the cap and riser, and its ocean background draws
before the diver. This fixes the swimmer disappearing behind the aperture fill.
Tests include inner endpoint/return and crossing assertions; browser views checked
at 7.0 seconds (mid-chamber) and 8.8 seconds (visible through the hatch).

North view now retains the riser with an upright hatch face and outward rigid
leaf projection. The outside swimmer waits at (70,-115) relative to the threshold,
away from both the physical swing and its visible projection. The cycle test
also checks a 24-unit actor envelope against the moving door segment.

Latest cycle supersedes the earlier inward/16-second study: outward swing in the
room and four overhead views. airlock-cycle.js implements a 30-second preview:
flood/equalize, open, swim out, close, reopen, swim in, seal, drain, stand.
Water is a separate chamber-only overlay. Swimming persists through sealing and
drainage. Timeline scrub added. Run node assets/door-polish-v3/check-airlock-cycle.cjs:
3,001 samples pass crossing, equalization, seal-before-drain and swim-until-dry.
Browser closing/draining/dry states inspected. Production logic is unchanged.

Diving-room fitting: diving-room.html uses the saved native airlock room capture
as a static room backdrop with the hatch at the north chamber/hull connection, with separate production seabed artwork and
helmeted Bill walk/swim frames from diver-preview.json. diving-room.js draws
recessed seals, threshold grating, moving leaf and foreground jamb lips separately.
The 16-second exit/return cycle waits for a fully open leaf before crossing and
closes only once Bill is back inside. Four rotated passage studies preserve
character facing. 6,404 rotationally equivalent temporal clearance samples pass;
browser assets load, JS syntax passes, main room and directional views reviewed.
This is a browser composition over a captured room, not native gameplay integration
or a production airlock flooding/equalization simulation. The stationary crew
member in the room capture remains part of that backdrop. Saves are not accessed.

Top-down hatch follow-up: ocean-hatch-top.png is a separately generated overhead
master (1774x887, true alpha), not a rotated elevation. hatches-top.js registers
the leaf at 72 units, separates fixed end jambs and rotates the leaf inward 90
degrees around its hinge. Four quarter-turn views show north/east/south/west
ocean boundaries with correctly rotated room sides. Dedicated open/close/play
and scrub controls. Exact prompt and original location: ocean-hatch-top-prompt.json.
JavaScript syntax checked; all four open and closed browser views inspected.
These are fitting studies, not installed native gameplay art.

Ocean-exit follow-up: ocean-hatch-interior.png and ocean-hatch-exterior.png are
matching closed single-leaf pressure hatch faces, with reversed hinge sides.
They are presented separately in review.html, with hatches.js rendering a fixed
frame, rotating locking wheel and rigid hinged leaf projection. Dedicated open,
close, autoplay and scrub controls operate both reverse faces. Browser opening
and closing endpoints visually checked; JavaScript syntax checked. Native room
fitting and overhead companions remain pending. Exact prompts and alpha/dimension/hash evidence are in ocean-hatch-prompts.json
and ocean-hatch-manifest.json. Both source images are 1254 square with actual alpha.

Eight new families: Operations, Engineering, Science, Life Support, Recreation,
Anomaly, Robotics and Airlock. Each has a raised and overhead RGBA master (16 PNGs).
BRINE and the three corridor shapes retain the approved V2 neutral art.
Open review.html through the local server for synchronized motion and room captures.

catalog.json maps all 47 rooms, using current room_database categories, with an
Airlock override. All source paths are whole res:// paths. Overhead low_y offsets
register the generated leaves to the same 72-unit opening. Fixed frames and eased
rigid sliding use the approved V2 mechanism in tools/preview_door_art.gd.

Generated with the built-in image generator using the approved V2 masters as
references. Exact prompts: prompts.json. Original generation locations:
generation-sources.json. PNGs retain transparency and use Git LFS.

Validation: native 47-room capture, walking clearance and four corridor rotations
passed; 0 clearance failures; no script errors. Session:
output/riser-room-preview/session-800e849deb2d45d2b0e70c7e4718be2d.
Owner save fingerprints unchanged. All nine families visually reviewed in the
gallery, plus native context contact sheet covering the eight new families.

Preview only. Production selection, cross-department shared doorway policy and
gameplay animation integration remain outside this approved scope.

