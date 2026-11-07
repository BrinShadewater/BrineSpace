# Crew portrait communications

The live game now has a bottom-centered portrait transmission panel. It uses the approved 256x272 concept-sheet crops at a 224x238 UI slot, linear-filtered, rather than enlarged 32x34 gameplay portraits. Bill, Veld and Branforth retain their existing identities. These are static portraits with revealed text, not video, lip sync or voice audio.

Controls: Reveal text, Next transmission when queued, and Close transmission. Menu > Crew Comms reopens the latest message or supplies an initial channel greeting. The panel hides behind the pause menu, and reading does not alter the simulation pause state. Close dismisses the current queue. Pending messages are capped at eight and session history at thirty; history is not saved to disk.

First paid construction of Pressure Control, Listening Post or Crew Hab triggers a transmission once per game scene. Speakers use the selected architect, preferring present Veld for Listening Post and present Branforth for Pressure Control. Fixture/free placement does not automatically transmit. scripts/crew_comms.gd exposes transmit(speaker_id, text, optional_dedup_key) for later authored events.

Validation: tests/test_crew_comms.gd covers all three native portraits at 1600x900 and 960x540, fitting bounds, invalid speaker rejection, reveal, duplicate suppression, dismissal and replay. tests/playtest_crew_comms.gd exercises the construction event handler and replay inside the native main scene. Both pass. Agent inspected the small-window portrait preview and output/crew-comms/in-game.png. No portrait source pixels were changed. No voiced or animated-face assets were produced.

## Smaller station-view panel and BRINE revision

The panel now fits within grid_scroll bounds with a 16-unit inset, up to 660x246 logical units, and a 156x166 portrait slot. Native 1600/960 checks assert containment in the station viewport, excluding the HUD/card bar/inspector. Text reveals one character every 75ms, with 180ms comma/colon/semicolon pauses and 360ms sentence pauses. Reveal remains optional. BRINE has a new generated portrait based on her retained brown-bob/blue-eye identity; native dimensions/hash and exact prompt are in character/brine-comms-v1. The BRINE button opens her channel; an empty Comms history also defaults to BRINE. Portrait remains static.

## Context, history and pacing

BRINE greets the player on the first active observation after startup. Ambient messages have a 45-second global cooldown and per-scene event keys. Critical reserve messages require reserve <=2 AND a negative projected cycle delta; unused zero reserves do not trigger warnings. Newly active crew get identity-specific wake lines. Leaving the three authored room activities while the host remains powered can produce a completion/rest comment, once per actor/activity. Discovery dialogue is hooked only after meta.discover_synergy succeeds and reveals no undiscovered recipe names. Existing built-room messages remain.

The history dropdown browses the latest thirty displayed transmissions in this scene without adding replay duplicates. This is session history, not a persistent conversation archive. Slow/Normal/Fast changes typewriter timing; the selected speed is stored in user://comms_preferences.cfg. Slow remains 75ms per ordinary character. The compact panel remains within the station viewport at 1600 and 960 widths.

Validation: tests/test_comms_context.gd passes greeting, warning deduplication/cooldown, wake, completed activity, history and speed checks with controlled state. Native tests/playtest_crew_comms.gd passes presentation, speaker/replay, slow reveal and station-view containment. Source scripts remain paired with Godot UIDs. No dialogue voices, new character art or game-economy effects are added in this revision.

## Persistent archive and reliable completion events

The latest thirty displayed messages now persist beside the active run-save path as <run_save_path>.comms.json. This supersedes the session-only history limitation above. Writes use a temporary file and rename; malformed/unsupported archives are left intact and disable further archive writes for that scene. Playback does not duplicate entries. Fixture paths inherit isolated run-save paths or explicit output paths.

Crew completion chatter now follows an explicit event emitted only when the existing activity timer finishes normally. Interrupted actions do not emit it. The comms observer can defer completion messages across the ambient cooldown and still deduplicates each actor/activity. No gameplay reward or save-schema fields were added for these transient events.

Archive tests cover disk reload, replay without duplicates, replacement, thirty-entry cap and malformed-file preservation. Context tests cover interruption without false completion. Crew activity tests exercise the natural completion emission and power-interruption negative control in addition to the existing approach/facing checks.


## Opening conversation and click-to-talk

Fresh loops now queue BRINE, the selected architect, and a first objective: connect a power-producing room through matching doors. Continue retains the short greeting without the tutorial sequence. In-scene restarts reset conversation event keys and replay the introduction for the new selected architect; the bounded archive is retained.

With no blueprint selected, hover a living crew member for a talk cursor/name and click to open their approved portrait and current activity. Right-click clears blueprint selection using the existing controls. Two reply buttons become available after the text is revealed: Needs attention? ranks declining essential reserves by projected cycles remaining; This room? reads the definition of the actor's current room. Questions retain pending station reports and append to the existing archive. These are authored/contextual replies, without dialogue rewards or hidden recipe disclosure.

Critical reserve transmissions use a muted amber border and PRIORITY heading; history preserves that cue. The panel hides behind gameplay-blocking overlays and expands to 278 logical units high when replies are visible, inside the station viewport. Portrait sources and gameplay economy are unchanged.

Verification: tests/test_comms_conversation.gd passed in native Godot for the opening, Continue flag, three crew hit targets, construction input precedence, replies, queued-report retention, priority cue, overlay hiding and 1600/960 panel containment. Agent reviewed output/crew-conversation/talk-960.png. The final headless rerun additionally tests the actual in-scene restart hook. Existing context, archive and native portrait regression checks pass. Native logs retain existing raw room-image export warnings; this is local runtime evidence, not packaged acceptance. New test UIDs are generated by editor import.


## Contact picker and queue polish

The comms action row now offers Contact crew..., listing BRINE and only active living architects. Menu > Crew Comms provides access without locating sprites or deselecting a blueprint. The list refreshes when opened and selection revalidates availability. Switching to BRINE now preserves pending reports, matching crew conversations. Urgent messages are inserted ahead of routine queued messages in arrival order, without replacing the current message. The eight-message cap is retained. Close retains its existing dismiss-current-and-queue behavior.

The opening objective is shortened for the compact panel. Extended native conversation checks cover contact filtering, selecting Bill/BRINE, restoring available contacts, stable urgent ordering, no reading interruption and queue retention. Native 1600/960 containment, contextual events and archive regressions pass (output/comms-contacts*.log). Agent reviewed the refreshed 960 screenshot. Existing raw-image loading warnings remain; no packaged build was produced.


## Close/resume inbox and advice navigation

Close now minimizes instead of discarding the conversation queue, superseding the earlier Close behavior above. A station-view Resume comms button shows the number of queued messages. Reading position is retained while hidden; menus and journal overlays also hide the inbox. Explicit loop reset still discards transient messages. This is scene-local retention, not disk persistence of unread reports.

Resource advice offers Station Health after reveal. It opens the existing journal tab and retains the conversation for return, using the journal's normal pause restoration. Native checks cover resume/queue count, stable reveal position, health navigation and small/large window containment. The milestone and remaining owner cadence review are recorded in CREW_COMMS_HANDOFF_2026-09-08.md.


## Distinct crew dialogue

scripts/crew_dialogue.gd now owns authored greetings, steady/declining resource assessments and five room opinions per character. Bill emphasizes practical crew concerns, Veld evidence and uncertainty, and Branforth equipment and connections. BRINE Core, Pressure Control, Listening Post, Crew Hab and Salvage Workshop have three distinct opinions each. Other rooms retain their existing definition text. These opinions do not claim that equipment is currently operating or change any game state.

The caller still supplies current activity and the resource with the shortest projected reserve duration. Numeric amounts are unchanged by speaker choice. The dialogue fixture verifies 15 room lines, live activity substitution, numeric report values and fallback; the native conversation fixture verifies different replies for all three actors and the existing small-window containment. Owner writing review remains separate from these checks.


## Room status and locate action

This room? now snapshots the same observed status and next-cycle economy forecast used by the inspector. The two values are labeled separately, including the initial awaiting-cycle state, and asking again refreshes them. Authored opinions remain separate from operating claims. A Locate room action focuses the discussed cell/type through the existing diagnostic navigation and minimizes comms. A missing room or changed type disables the stale action. Archive reload retains prose but does not reconstruct old actionable room context.

Native conversation checks pass with suspension forecast, locate behavior and expanded panel containment at 1600/960. Agent reviewed the 960 screenshot. The final headless check adds stale context rejection. No economy rules, room art or packaged builds change.


## Owner-directed compact popup (supersedes expanded UI)

The popup is now 520x170 logical units with a 96x108 portrait and only Next/X. Contact, history, speed, room-status and reply controls are absent from its visible UI. Slow text remains; five seconds after completion the next queued message starts, or the popup hides. X preserves the current message for the dedicated side-panel COMMS button; a new incoming event reopens the popup. The floating inbox is retired. Native compact-popup checks and visual review are recorded in the latest comms handoff.
