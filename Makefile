.PHONY: install test run run-live lint eval viewer

viewer:         ## build engine/viz/viewer.html from the latest run
	python tools/build_replay.py $$(ls -d data/runs/* | tail -1)

install:
	pip install -e ".[dev]" --break-system-packages

test:
	python -m pytest -q

run:            ## free, deterministic, no API key
	python -m engine.sim.runner --ticks 100 --llm mock

run-live:       ## real LLM; costs money; read docs/07-EVALUATION.md budget section first
	python -m engine.sim.runner --ticks 50 --llm anthropic

eval:
	python evals/eval_basic.py $$(ls -d data/runs/* | tail -1)

lint:
	ruff check .
