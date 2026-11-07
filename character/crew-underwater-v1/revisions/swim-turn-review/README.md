# Swim turn comparison

Rebuild with `python character/crew-underwater-v1/build_swim_turn_review.py`. Twelve sheets cover six normalized stroke fractions, bare and helmeted, for all three actors and four directions. Current selection comes from `revisions/current-swim-coverage.json`; selected source hashes are checked. Images share a 2× scale and registered anchor, with full canvas extents retained. `sources.json` identifies each selected frame.

Inspected helmet phase 3: Branforth north shows unusually prominent boots and stronger foreshortening relative to his other directions. North/south body projection differs for the other crew too. Equal gait phase does not correct source camera/anatomy. Correct the directional source while preserving body scale, then rebuild helmet fitting and full-stroke clearance. Do not shrink the whole actor to improve a comparison or route test. No continuous turning acceptance is claimed.
