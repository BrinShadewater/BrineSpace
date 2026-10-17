# Survey Probe animation handoff
Updated: 2026-09-26
## Objective and acceptance
Owner requested a more top-down south launcher and four directional animations: loaded, launch, empty, return.
## Accepted decisions and constraints
Charcoal Robotics equipment, muted cyan, painted prop style. Standalone visual work, no gameplay changes. Previous four-wall study retained as history.
## Current state
components-source.png is a new imagegen atlas with separate launcher/probe artwork per cardinal direction. prompt.txt preserves exact prompt; manifest.json records source SHA256, crops, component scales and timing. No direction is bitmap-rotated or mirrored.
index.html offers four synchronized 13-second loops, pause, scrub, restart and speed controls. Four animated WebP exports each contain 195 frames at 15 fps. Browser animation interpolates continuously.
South now shows the bed from above. Probe translates into the concealed tube and reverses into the cradle on return. Fixed art stays unchanged between loaded and empty states.
## Verification
verify_export.py passed: all assets loaded, no browser errors, loaded/empty difference in all directions, pixel-identical loop endpoints. loaded-review.png and states-contact.png reviewed visually. South clipping adjusted to conceal probe behind near collar.
## Remaining work
Owner visual acceptance. This is a motion study, not final game-ready directional geometry: pipe placement and fin silhouette still vary by view; shared world scale and room-wall occlusion need native calibration. Hatch articulation and external ocean travel are not animated. No game files or owner layouts changed.


## Status-light revision
Added fixed caged yellow beacon and probe-attached blinking status light in all directions. Automatic preview uses yellow docked and blue underway; selector also demonstrates red stopped and manual states. Probe light uses the same tube clipping as probe. Beacon has 16 pulses per 13-second loop (0.8125 seconds) to preserve seamless repetition; probe blink is 1 second. Canvas overlays preserve source artwork. Four WebP exports rebuilt; loop and browser checks passed. Previous HTML preserved as index-before-lights.html.

## Circular prelaunch beacon revision
Owner requested circular yellow strobe before launch. Replaced fixed pulsing cage with round amber lens and rotating bright arc, 0.8-second revolution. Active only at 0.4–2 seconds, two revolutions before launch; dark during travel, empty and return states. Probe status light retained. Four animation exports rebuilt. Visual screenshot reviewed; isolated checks confirm rotation, exact period, and inactive states; existing loop/browser checks passed.
