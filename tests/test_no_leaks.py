"""Vocabulary firewall: inhabitant-visible text must not reference the machinery (CLAUDE.md rule 3)."""
import re
from pathlib import Path

from cognition.identity.persona import Persona
from engine.sim.runner import RunConfig, run

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = re.compile(
    r"\b(simulat\w*|agents?|AI|LLM|models?|prompts?|ticks?|tokens?|programs?|code|games?)\b",
    re.IGNORECASE,
)


def test_seed_personas_have_no_meta_words():
    for p in (ROOT / "agents" / "seeds").glob("*.yaml"):
        persona = Persona.from_yaml(p)
        text = persona.system_prompt()
        assert not FORBIDDEN.search(text), f"{p.name}: {FORBIDDEN.search(text).group(0)}"


def test_world_results_have_no_meta_words(tmp_path):
    import json
    out = run(RunConfig(ticks=40, out_dir=tmp_path, run_id="leak"))
    for line in open(out / "events.jsonl"):
        r = json.loads(line)["result"]
        assert not FORBIDDEN.search(r), r
    snap = json.loads((out / "snapshots" / "seed_01.json").read_text())
    for m in snap["memory"]["items"]:
        if m["kind"] in ("observation", "action"):
            assert not FORBIDDEN.search(m["text"]), m["text"]
