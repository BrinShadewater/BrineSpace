"""Freeze materialized tracked sources, export a playable Windows debug build,
and run acceptance against that immutable PCK with isolated user data.

Usage: python tools/build_integrated_acceptance.py prepare OUTPUT --godot EXE
       python tools/build_integrated_acceptance.py build OUTPUT --godot EXE
       python tools/build_integrated_acceptance.py test OUTPUT --only title
All evidence is retained; an existing test directory is never overwritten.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
_VERIFIED_FILES = {}
FIXTURES = {
    "title": ("tests/test_title_screen.gd", "TITLE SCREEN: PASS", []),
    "architects": ("tests/test_architect_selection.gd", "ARCHITECT SELECTION PASS", []),
    "recovery": ("tests/test_architect_recovery.gd", "ARCHITECT RECOVERY PASS", []),
    "save": ("tests/test_run_save.gd", "SAVE GAME: PASS", []),
    "menus": ("tests/test_menu_recovery.gd", "MENU RECOVERY: PASS", []),
    "airlock": ("tests/test_airlock.gd", "AIRLOCK PASS", []),
    "fleet": ("tests/test_drone_fleet.gd", "Drone fleet state-machine tests passed", []),
    "drone_jobs": ("tests/test_drone_jobs.gd", "DRONE JOBS PASS", []),
    "battery": ("tests/test_drone_battery.gd", "DRONE BATTERY PASS", []),
    "harvest": ("tests/test_finite_harvest.gd", "FINITE HARVEST PASS", []),
    "operations": ("tests/test_station_operations.gd", "STATION OPERATIONS: PASS", []),
    "navigation": ("tests/test_station_navigation.gd", "STATION NAVIGATION PASS", []),
    "yield_save": ("tests/test_battery_passage_probe.gd", "BATTERY CONCURRENT YIELD:", ["--save-during-yield"]),
    "crew": ("tests/test_crew_polish.gd", "CREW POLISH: PASS", []),
    "paid_mining": ("tests/playtest_paid_opening.gd", "PAID OPENING PASS", []),
    "paid_salvage": ("tests/playtest_paid_opening.gd", "PAID OPENING PASS", ["--kind=salvage"]),
    "catalog": ("tools/review_decoration_integration.gd", "DECORATION INTEGRATION PASS: 40", []),
}
MANIFESTS = ["rooms/production-ten/manifest.json", "rooms/whole-room/export-manifest.json",
             "rooms/underwater/batch-two/export-manifest.json", "rooms/underwater/gravity-loom/manifest.json",
             "rooms/underwater/routing-export-manifest.json", "rooms/production-ten/construction-manifest.json"]


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def unchanged_digest(path):
    # Hash once per suite process; rehash if size or modification time changes.
    # summarize() performs a fresh full hash after the complete suite.
    stat = path.stat()
    key = (str(path.resolve()), stat.st_size, stat.st_mtime_ns)
    if key not in _VERIFIED_FILES: _VERIFIED_FILES[key] = digest(path)
    return _VERIFIED_FILES[key]


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def install_dispatch(source, output):
    """Export templates cannot run --script. Keep fixtures as persistent root Nodes.

    Persistence matters: Save/Continue and title tests change current_scene.
    Only SceneTree access/lifecycle is adapted; assertion bodies remain intact.
    """
    adapter = '''extends Node
var root: Window:
\tget: return get_tree().root
var current_scene: Node:
\tget: return get_tree().current_scene
\tset(value): get_tree().current_scene = value
var process_frame: Signal:
\tget: return get_tree().process_frame
func create_timer(seconds: float) -> SceneTreeTimer: return get_tree().create_timer(seconds)
func quit(code: int = 0) -> void: get_tree().quit(code)
'''
    generated = source / "tests/runtime_generated/acceptance"
    records = []
    for name in FIXTURES:
        path = generated / (name + ".gd")
        original = path.read_text(encoding="utf-8")
        assert original.startswith("extends SceneTree"), name
        transformed = original.replace("extends SceneTree", adapter, 1).replace("func _init()", "func _ready()", 1).replace("func _initialize()", "func _ready()", 1)
        path.write_text(transformed, encoding="utf-8")
        records.append({"path":path.relative_to(source).as_posix(),"sha256":digest(path)})
    dispatch = '''extends Node
func _ready() -> void: call_deferred("launch")
func launch() -> void:
\tvar fixture := ""
\tvar expected := ""
\tfor arg in OS.get_cmdline_user_args():
\t\tif arg.begins_with("--acceptance-fixture="): fixture = arg.trim_prefix("--acceptance-fixture=")
\t\tif arg.begins_with("--acceptance-userdata-root="): expected = arg.trim_prefix("--acceptance-userdata-root=")
\tif fixture.is_empty():
\t\tget_tree().change_scene_to_file("res://scenes/title_screen.tscn")
\t\treturn
\tvar actual := OS.get_user_data_dir().replace("\\\\", "/")
\tprint("ACCEPTANCE USER DATA: ", actual)
\tif expected.is_empty() or not actual.begins_with(expected.replace("\\\\", "/") + "/"):
\t\tpush_error("Acceptance user data is not isolated: " + actual)
\t\tget_tree().quit(1)
\t\treturn
\tDirAccess.make_dir_recursive_absolute("user://acceptance")
\tif fixture == "isolation":
\t\tprint("ISOLATION PASS")
\t\tget_tree().quit()
\t\treturn
\tvar path := "res://tests/runtime_generated/acceptance/" + fixture + ".gd"
\tif fixture == "tour": path = "res://tests/runtime_generated/station.gd"
\tif fixture == "environment": path = "res://tests/playtest_environment_package.gd"
\tvar script = load(path)
\tif script == null:
\t\tpush_error("Cannot load acceptance fixture: " + path)
\t\tget_tree().quit(1)
\t\treturn
\tget_tree().root.add_child(script.new())
'''
    (generated / "entry.gd").write_text(dispatch, encoding="utf-8")
    (generated / "entry.tscn").write_text('[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://tests/runtime_generated/acceptance/entry.gd" id="1"]\n[node name="AcceptanceEntry" type="Node"]\nscript = ExtResource("1")\n', encoding="utf-8")
    project = source / "project.godot"
    project.write_text(project.read_text().replace('run/main_scene="res://scenes/title_screen.tscn"', 'run/main_scene="res://tests/runtime_generated/acceptance/entry.tscn"'), encoding="utf-8")
    presets = source / "export_presets.cfg"
    presets.write_text(presets.read_text().replace('export_files=PackedStringArray(', 'export_files=PackedStringArray("res://tests/runtime_generated/acceptance/entry.tscn",'), encoding="utf-8")
    write_json(output / "runtime-node-bridges.json", records)


def run_logged(command, cwd, directory, label, timeout=300, env=None):
    stdout, stderr = directory / (label + ".log"), directory / (label + ".err")
    if stdout.exists() or stderr.exists():
        raise RuntimeError("Evidence exists; choose a fresh label: " + label)
    started = time.monotonic()
    print("START " + label, flush=True)
    with stdout.open("w", encoding="utf-8") as out, stderr.open("w", encoding="utf-8") as err:
        process = subprocess.Popen(command, cwd=cwd, env=env, stdout=out, stderr=err,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            code = -1
    text = stdout.read_text(encoding="utf-8", errors="replace") + stderr.read_text(encoding="utf-8", errors="replace")
    errors = re.findall(r"^.*(?:SCRIPT ERROR:|ERROR:|Assertion failed).*$", text, re.M)
    result = {"command": command, "exit_code": code, "seconds": round(time.monotonic()-started, 2),
              "engine_errors": errors, "timed_out": code == -1, "pass": code == 0 and not errors}
    write_json(directory / (label + ".result.json"), result)
    print(f"END {label}: {'PASS' if result['pass'] else 'FAIL'} ({result['seconds']}s)", flush=True)
    return result, text


def prepare(output, godot):
    output.mkdir(parents=True, exist_ok=False)
    source = output / "source"
    source.mkdir()
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    paths = [p for p in paths if p]
    # Include this new harness before it is committed; preserve actual working bytes.
    if "tools/build_integrated_acceptance.py" not in paths:
        paths.append("tools/build_integrated_acceptance.py")
    records = []
    for relative in sorted(paths):
        original = ROOT / relative
        with original.open("rb") as f:
            if f.read(48).startswith(b"version https://git-lfs.github.com/spec/"):
                raise RuntimeError("LFS pointer: " + relative)
        target = source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, target)
        records.append({"path": relative, "sha256": digest(target), "size": target.stat().st_size})
    write_json(output / "source-checkpoint.json", {
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip(),
        "working_diff": subprocess.check_output(["git", "diff", "--"], cwd=ROOT).decode(),
        "files": records,
    })
    print(f"Frozen {len(records)} materialized source files", flush=True)
    generated = source / "tests/runtime_generated/acceptance"
    generated.mkdir(parents=True, exist_ok=True)
    adaptations = []
    for name, (relative, _, _) in FIXTURES.items():
        text = (source / relative).read_text(encoding="utf-8")
        # SceneTree scripts remain SceneTree scripts, including across scene changes.
        text = text.replace("res://output/", "user://acceptance/")
        if name == "catalog":
            text = text.replace("capture.save_png(row.card)", 'capture.save_png("user://acceptance/decoration-integration/%s-q0-off.png" % row.id)')
            text = text.replace('"res://rooms/decoration-integration/%s-%d.png"', '"user://acceptance/decoration-integration/%s-%d.png"')
            # Keep every state render as evidence, not only powered frames.
            text = text.replace('if live: assert(capture.save_png("user://acceptance/decoration-integration/%s-q%d.png"%[row.id,q])==OK)',
                                'assert(capture.save_png("user://acceptance/decoration-integration/%s-q%d-%s.png"%[row.id,q,live])==OK)')
        target = generated / (name + ".gd")
        target.write_text(text, encoding="utf-8")
        adaptations.append({"source": relative, "generated": target.relative_to(source).as_posix(),
                            "sha256": digest(target), "change": "Evidence destinations only; catalog keeps both power states"})
    write_json(output / "fixture-adaptations.json", adaptations)
    # Runtime card selection is centralized in the latest decoration manifest.
    # Reconcile staged validation consumers, preserving historical source manifests.
    cards = json.loads((source / "rooms/decoration-integration/manifest.json").read_text())["rooms"]
    selected = {row["id"]: row for row in cards}
    for row in cards:
        assert digest(source / row["card"].removeprefix("res://")) == row["card_sha256"], row["id"]
    changes = []
    for relative in MANIFESTS:
        path = source / relative
        rows = json.loads(path.read_text(encoding="utf-8-sig"))
        for row in rows:
            if row["id"] in selected:
                current = selected[row["id"]]
                card = current["card"].removeprefix("res://")
                if row["integration"]["card"] != card:
                    changes.append({"manifest":relative, "id":row["id"], "old":row["integration"]["card"], "selected":card})
                    row["integration"]["card"] = card
        write_json(path, rows)
    write_json(output / "card-selection-reconciliation.json", changes)
    write_json(output / "selected-runtime-cards.json", cards)
    # Reuse the established bridges for scene-based exported renderer fixtures.
    for command, label in [([sys.executable, "tools/build_room_export_fixture.py"], "room-bridge"),
                           ([sys.executable, "tools/build_environment_export_contract.py"], "environment-contract"),
                           ([sys.executable, "tools/audit_composition_dependencies.py", *MANIFESTS], "composition-audit")]:
        result, _ = run_logged(command, source, output, label)
        if not result["pass"]: raise RuntimeError(label + " failed")
    environment_scene = source / "tests/runtime_generated/environment_validation.tscn"
    environment_scene.write_text('[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://tests/playtest_environment_package.gd" id="1"]\n[node name="EnvironmentAcceptance" type="Node"]\nscript = ExtResource("1")\n')
    roots = ["res://scenes/title_screen.tscn", "res://scenes/main.tscn", "res://tests/runtime_generated/station.tscn",
             "res://tests/runtime_generated/environment_validation.tscn"]
    roots += ["res://tests/runtime_generated/acceptance/" + name + ".gd" for name in FIXTURES]
    # Catalog view paths are JSON-driven rather than preload dependencies.
    roots += [row["view"] for row in cards if row["view"] != "corridor"]
    template = (ROOT / "output/production-ten/export-tools/windows_debug_x86_64.exe").as_posix()
    preset = '[preset.0]\nname="Windows Integrated Acceptance"\nplatform="Windows Desktop"\nrunnable=true\nexport_filter="selected_resources"\ncustom_features=""\n'
    preset += "export_files=PackedStringArray(" + ",".join(json.dumps(p) for p in roots) + ")\n"
    preset += 'include_filter="*.png,*.json,NOTICE.md"\nexclude_filter="output/*,outputs/*,asset_backups/*,skills/*,.git/*"\nscript_export_mode=0\n\n[preset.0.options]\n'
    preset += 'custom_template/debug=' + json.dumps(template) + '\nbinary_format/embed_pck=false\nbinary_format/architecture="x86_64"\ntexture_format/s3tc_bptc=true\ncodesign/enable=false\napplication/modify_resources=false\n'
    (source / "export_presets.cfg").write_text(preset, encoding="utf-8")
    install_dispatch(source, output)
    write_json(output / "build-config.json", {"godot":str(godot), "godot_sha256":digest(godot), "template_sha256":digest(Path(template))})


def build(output, godot):
    source = output / "source"
    binary = output / "build/BrineSpace.exe"
    if (output / "package.json").exists():
        raise RuntimeError("A frozen package exists; start a new acceptance build")
    binary.parent.mkdir(exist_ok=True)
    attempt = 1
    while (output / f"import-{attempt}.log").exists() or (attempt == 1 and (output / "import.log").exists()):
        attempt += 1
    for command, label in [([str(godot), "--headless", "--editor", "--path", str(source), "--import"], "import"),
                           ([str(godot), "--headless", "--path", str(source), "--script", "res://tools/audit_room_dressing_hosts.gd", "--", "--check-mat-bounds"], "dressing-hosts"),
                           ([str(godot), "--headless", "--path", str(source), "--export-debug", "Windows Integrated Acceptance", str(binary)], "export")]:
        result, _ = run_logged(command, source, output, f"{label}-{attempt}", 900)
        if not result["pass"]: raise RuntimeError(label + " failed")
    inventory = [{"path":p.relative_to(source).as_posix(),"sha256":digest(p)} for p in sorted(source.rglob("*"))
                 if p.is_file() and ".godot" not in p.parts and p.suffix != ".import"]
    write_json(output / "frozen-export-sources.json", inventory)
    write_json(output / "package.json", {"exe_sha256":digest(binary), "pck_sha256":digest(binary.with_suffix(".pck")),
               "pck_bytes":binary.with_suffix(".pck").stat().st_size,
               "entry":"res://tests/runtime_generated/acceptance/entry.tscn", "normal_scene":"res://scenes/title_screen.tscn"})


def test(output, name, label=None, seed=77321):
    binary = output / "build/BrineSpace.exe"
    package = json.loads((output / "package.json").read_text())
    assert unchanged_digest(binary.with_suffix(".pck")) == package["pck_sha256"], "Package changed"
    assert unchanged_digest(binary) == package["exe_sha256"], "Executable changed"
    directory = output / "runs" / (label or name)
    directory.mkdir(parents=True, exist_ok=False)
    # Every process uses fresh app data; no player saves/preferences are touched.
    env = os.environ.copy()
    env["APPDATA"] = str(directory / "appdata")
    env["LOCALAPPDATA"] = str(directory / "localappdata")
    userdata = directory / "appdata/Godot/app_userdata/BrineSpace/acceptance"
    userdata.mkdir(parents=True)
    # The legacy two-person fixture writes native captures into res://character.
    # Its supported headless mode retains movement/save assertions; the separate
    # native three-person tours supply packaged visual and trajectory evidence.
    command = [str(binary)] + (["--headless"] if name == "crew" else [])
    command += ["--", f"--acceptance-fixture={name}", f"--acceptance-userdata-root={directory / 'appdata'}"]
    if name == "tour":
        command += ["--controlled-tour", "--three-crew-review",
                    "--trace-tour-progress", f"--crew-seed={seed}", f"--capture-dir={directory / 'captures'}"]
        command += ["--additional-manifest=res://" + p for p in MANIFESTS[1:]]
        marker = "ROOM SCENE PASS [production_ten_station]"
    elif name == "environment":
        command += [f"--capture-dir={directory / 'captures'}"]
        marker = "ENVIRONMENT EXPORT PASS:"
    elif name == "isolation":
        marker = "ISOLATION PASS"
    else:
        _, marker, extra = FIXTURES[name]
        command += extra
        if name == "airlock": command += [f"--capture-dir={directory / 'captures'}"]
    result, text = run_logged(command, directory, directory, "runtime", 300, env)
    result["marker"] = marker
    result["marker_found"] = not marker or marker in text
    result["pass"] &= result["marker_found"]
    result["pck_sha256"] = package["pck_sha256"]
    result["package_unchanged"] = unchanged_digest(binary.with_suffix(".pck")) == package["pck_sha256"]
    result["pass"] &= result["package_unchanged"]
    write_json(directory / "acceptance.json", result)
    if not result["pass"]: raise RuntimeError("Acceptance failed: " + str(directory))


def summarize(output):
    package = json.loads((output / "package.json").read_text())
    assert digest(output / "build/BrineSpace.pck") == package["pck_sha256"], "Final package hash changed"
    assert digest(output / "build/BrineSpace.exe") == package["exe_sha256"], "Final executable hash changed"
    results = {p.parent.name: json.loads(p.read_text()) for p in sorted((output / "runs").glob("*/acceptance.json"))}
    expected = set(FIXTURES) | {"tour-repeat-a", "tour-repeat-b", "tour-varied"}
    missing = sorted(expected - results.keys())
    tours = {}
    for name in ["tour-repeat-a", "tour-repeat-b", "tour-varied"]:
        directory = output / "runs" / name / "captures"
        trace = directory / "whole-crew-trace.jsonl"
        if not trace.exists(): continue
        minimum = math.inf
        maximum = {"bill":0.0,"veld":0.0,"branforth":0.0}
        previous = {}
        count = 0
        with trace.open() as stream:
            for line in stream:
                row = json.loads(line)
                active = [a for a in row["crew"] if a["active"] and a["present"]]
                for index, actor in enumerate(active):
                    if actor["id"] in previous:
                        maximum[actor["id"]] = max(maximum[actor["id"]], math.dist(previous[actor["id"]], actor["foot"]))
                    for peer in active[index+1:]:
                        minimum = min(minimum, math.dist(actor["foot"], peer["foot"]))
                    previous[actor["id"]] = actor["foot"]
                count += 1
        tours[name] = {"samples":count, "whole_crew_sha256":digest(trace),
                       "minimum_peer_distance":minimum, "maximum_step":maximum,
                       "seeds":json.loads((directory / "crew-seeds.json").read_text()),
                       "station":json.loads((directory / "station-summary.json").read_text())}
    repeat_equal = (len(tours) == 3 and tours["tour-repeat-a"]["whole_crew_sha256"] == tours["tour-repeat-b"]["whole_crew_sha256"])
    peer_motion_checks = len(tours) == 3 and all(t["minimum_peer_distance"] >= 19.99 and max(t["maximum_step"].values()) <= 4.601 for t in tours.values())
    same_package = all(r["pck_sha256"] == package["pck_sha256"] for r in results.values())
    report = {"package":package, "missing":missing, "checks":results, "tours":tours,
              "same_package":same_package, "whole_crew_repeat_equal":repeat_equal, "peer_motion_checks":peer_motion_checks,
              "pass":not missing and same_package and repeat_equal and peer_motion_checks and all(r["pass"] for r in results.values()),
              "scope":"Automated packaged acceptance and sampled visual inspection; not human pacing or broad hardware acceptance"}
    write_json(output / "acceptance-summary.json", report)
    print(json.dumps({"pass":report["pass"],"missing":missing,"checks":len(results),"same_package":same_package,"whole_crew_repeat_equal":repeat_equal,"tours":tours},indent=2))
    if not report["pass"]: raise RuntimeError("Integrated acceptance incomplete or failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "build", "test", "summarize"])
    parser.add_argument("output", type=Path)
    parser.add_argument("--godot", type=Path)
    parser.add_argument("--only", choices=[*FIXTURES, "tour", "environment", "isolation"])
    parser.add_argument("--label")
    parser.add_argument("--seed", type=int, default=77321)
    args = parser.parse_args()
    if args.action in ["prepare", "build"] and args.godot is None: parser.error("--godot is required for prepare/build")
    if args.action == "test" and args.only is None: parser.error("--only is required for test")
    destination = args.output.resolve()
    if args.action == "prepare": prepare(destination, args.godot.resolve())
    elif args.action == "build": build(destination, args.godot.resolve())
    elif args.action == "test": test(destination, args.only, args.label, args.seed)
    else: summarize(destination)
