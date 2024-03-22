.PHONY: init run
#───────────────────────────────────────────────────────────────────────────────

run:
	source ./.venv/bin/activate && \
	python3 -m main

# set up venv & install deps
# INFO using homebrew python3.12 instead of macOS system python3.9 due to
# https://github.com/urllib3/urllib3/issues/3020
init:
	if [[ ! -x "$$(command -v python3.12)" ]]; then echo "python3.12 required. (\`brew install python@3.12\`)" && return 1; fi ; \
	[[ -d ./.venv ]] && rm -rf ./.venv ; \
	python3.12 -m venv ./.venv && \
	source ./.venv/bin/activate && \
	python3 -m pip install -r requirements.txt && \
	python3 -m pip install --upgrade pip && \
	echo "✅ Virtual Environment setup. (Still needs to be enabled.)" ; \
	git config user.name "jk & Chris Grieser"
