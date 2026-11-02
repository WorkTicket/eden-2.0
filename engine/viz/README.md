# engine/viz/

`viewer_template.html` is the source. `python tools/build_replay.py data/runs/<id>` (or `make viewer`) bakes a run into `viewer.html` (open in a browser) and `viewer.fragment.html` (embeddable). Both outputs are generated and gitignored. Design, scale levels, data contract and roadmap: `docs/11-GRAPHICS-AND-VIEWER.md`.
