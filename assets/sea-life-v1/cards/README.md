# BrineSpace card art - batch 3

Accepted September 29: neutral matte outer metal with dark seams and a continuous
2px department-colored inner outline at 6px inset, touching the frame inner edge.
The outline draws above card content so all four sides remain visible. Card and
text geometry are unchanged. Preview: review/frame-closeup-inner-touch-v7.png.

Fifteen PNGs: one 200x284 nine-slice frame, eight 64px department emblems,
five 48px rarity marks and a 200x284 back. Frame/back use preserved built-in
imagegen sources. Tiny emblems and marks are reproducible extensions of the
existing code-native UI symbol language. Exact prompts/geometry and hashes are
recorded in prompts.json, bake.py and manifest.json.

Installed in DraftCard and the existing card-style helper. Department trim and
emblems use the room's existing RoomDatabase.room_color result and existing muted
conversion. The inner stock retains its neutral state-specific fill. Selected,
hovered and unaffordable modulation remains intact. The frame uses 16px slice
margins and the original content margins 8/8/8/7. Card size, text sizes/positions,
cost rows, art windows and row/fan layout stay unchanged. Icons draw alongside
existing labels at 16px/12px. Hallways retain their neutral identity without an
Engineering emblem. Derelict is a condition/category, not a new department.

The card back is wired into the retained pile renderer. The live draw/discard
piles remain hidden, following the later owner decision; no controls restored.
Missing/invalid PNGs warn once per file and retain the old card rendering.

Rebuild: `python assets/sea-life-v1/cards/bake.py` (Pillow/NumPy).
Raster validation: `python assets/sea-life-v1/cards/validate.py`.
Native review: `python tools/check_card_art.py before` before a new revision,
then `python tools/check_card_art.py after`. Fresh scratch APPDATA/LOCALAPPDATA
and owner-profile fingerprints are mandatory. Screen 2 captures at window widths
960/1280/1600/2560 include logical and physical metrics and all text rectangles.
Never overwrite baseline captures merely to make comparison pass.
