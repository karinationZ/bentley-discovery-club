# Bentley's Big Adventures — common commands.
# Override the episode with EP=…   e.g.  `make board EP=ep2`
EP ?= ep4
PORT ?= 8713
PY := PYTHONPATH=. python3

.DEFAULT_GOAL := help
.PHONY: help board board-serve board-status board-next board-check board-render board-init test

help: ## show this help
	@grep -hE '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo "  (override the episode with EP=… , e.g.  make board EP=ep2)"

board: board-render ## open the browser board (static snapshot — refresh to update)
	@open episodes/$(EP)/board.html

board-serve: board-render ## serve the LIVE board — auto-updates + click any clip/asset to reveal in Finder (Ctrl+C)
	@$(PY) -m bentley.board serve $(EP) --port $(PORT)

board-render: ## regenerate BOARD.md + board.html from board.json
	@$(PY) -m bentley.board render $(EP)

board-status: ## print the board header — stage · next action · shot counts
	@$(PY) -m bentley.board status $(EP)

board-next: ## print the single next action + the target shot's card
	@$(PY) -m bentley.board next $(EP)

board-check: ## validate the board (exit 1 on any problem)
	@$(PY) -m bentley.board check $(EP)

board-init: ## scaffold a fresh board.json from the shotlist
	@$(PY) -m bentley.board init $(EP)

test: ## run the test suite
	@$(PY) -m pytest tests/ -q
