.PHONY: test lint format

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

demo:
	rm -rf synth_demo run_demo
	uv run invariance synth \
		--config examples/sim.json \
		--alpha 0.07 \
		--n-sensors 20 \
		--noise 0.5 \
		--out synth_demo
	uv run invariance simulate \
		--config synth_demo/sim.json \
		--out run_demo
	uv run invariance calibrate \
		--run run_demo \
		--sensors synth_demo/sensors.csv