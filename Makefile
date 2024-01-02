.PHONY: init run
#───────────────────────────────────────────────────────────────────────────────

run:
	source ./.venv/bin/activate && \
	python3 main.py

# set up venv & install deps
init:
	[[ -d ./.venv ]] && rm -rf ./.venv ; \
	python3 -m venv ./.venv && \
	source ./.venv/bin/activate && \
	python3 -m pip install -r requirements.txt
