from engine.sim.runner import RunConfig, run
from tools.build_replay import build


def test_replay_data_shape(tmp_path):
    out = run(RunConfig(ticks=12, out_dir=tmp_path, run_id="rp"))
    d = build(out)
    assert d["ticks"] == 12
    assert [a["name"] for a in d["agents"]] == ["Adan", "Eva"]
    assert len(d["events"]) == 12 * 2
    t, a, act, res, x, y, h = d["events"][0]
    assert isinstance(act, str) and 0 <= h <= 1
    assert len(d["map"]["rows"]) == 10 and d["laws"]["day_length_ticks"] == 48
