"""Create a new agent seed from the template: python tools/new_agent.py "Name" """
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if len(sys.argv) != 2:
    sys.exit('usage: python tools/new_agent.py "Name"')
name = sys.argv[1]
n = len(list((ROOT / "agents" / "seeds").glob("*.yaml"))) + 1
slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
text = (ROOT / "agents" / "templates" / "agent.template.yaml").read_text()
text = text.replace("__ID__", f"seed_{n:02d}").replace("__NAME__", name)
dest = ROOT / "agents" / "seeds" / f"seed_{n:02d}_{slug}.yaml"
dest.write_text(text)
print(dest)
