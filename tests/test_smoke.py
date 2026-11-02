import json

from engine.sim.runner import RunConfig, run
from cognition.planning.planner import parse_action


def _events(path):
    return [json.loads(line) for line in open(path / "events.jsonl")]


def test_run_produces_events_and_memories(tmp_path):
    out = run(RunConfig(ticks=30, out_dir=tmp_path, run_id="t"))
    ev = _events(out)
    assert len(ev) == 30 * 2  # two seed agents
    snap = json.loads((out / "snapshots" / "seed_01.json").read_text())
    assert len(snap["memory"]["items"]) > 0


def test_determinism(tmp_path):
    a = _events(run(RunConfig(ticks=25, out_dir=tmp_path, run_id="a", seed=3)))
    b = _events(run(RunConfig(ticks=25, out_dir=tmp_path, run_id="b", seed=3)))
    assert a == b


def test_parse_action():
    assert parse_action("move east").arg == "east"
    assert parse_action('say "hi there"').arg == "hi there"
    assert parse_action("dance wildly").kind == "wait"
