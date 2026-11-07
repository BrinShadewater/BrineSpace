# Security Policy

BrineSpace is an offline single-player Godot prototype. It has no server, no accounts, no telemetry, and no network calls, so the realistic security surface is small.

## Reporting

If you do find something — a malicious file path in a save, an unsafe resource load, a dependency concern — please report it privately through GitHub Security Advisories on this repository rather than opening a public issue.

Please do not open a public issue for anything you believe is exploitable.

## Scope

In scope: the game code and its build/export configuration.

Out of scope: the Godot engine itself (report upstream), and anything requiring an attacker to already have write access to the player's machine.