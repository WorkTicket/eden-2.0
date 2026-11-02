# agents/

- `templates/agent.template.yaml` blank inhabitant
- `seeds/*.yaml` inhabitants loaded by the runner (sorted by filename)

Write everything in-world. No meta vocabulary (enforced by `tests/test_no_leaks.py`). Create with `python tools/new_agent.py "Name"`.
