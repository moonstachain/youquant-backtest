# YouQuant Backtest Automation

## What it is
YouQuant Backtest Automation is a Codex skill for turning a natural-language trading strategy into executable YouQuant strategy code, saving it to the target strategy context, launching a backtest, and diagnosing the result.

## Who it's for
This repo is for operators who work with 优宽/YouQuant and want a repeatable path from strategy idea to backtest run, including feasibility checks for contract size, signal logic, and platform-specific execution constraints.

## Quick start
```bash
python3 scripts/youquant_api.py list-strategies
```

## Inputs
- A strategy description in natural language.
- `YOUQUANT_ACCESS_KEY` and `YOUQUANT_SECRET_KEY`, or explicit CLI flags.
- Target strategy name or strategy ID.
- Symbol, exchange type, capital, bar period, and sizing rule.
- Optional stop-loss, stop-profit, re-entry, and date-range settings.

## Outputs
- A normalized strategy brief and locally saved strategy code.
- API results for strategy or robot listing through `scripts/youquant_api.py`.
- A completed or diagnosed backtest run on YouQuant.
- Clear explanations of why trades did or did not happen.

## Constraints
- Default to backtest-only unless the user explicitly asks for live trading.
- Do not overwrite an unrelated strategy page.
- Feasibility issues such as insufficient capital for one lot must be reported explicitly.
- Browser automation is the preferred path for actual backtest execution unless the platform proves a stable API path.

## Example
Take a futures trading rule written in plain language, normalize it into a strategy brief, check whether the requested budget can open at least one contract, update the target YouQuant strategy, run a backtest, and report both the metrics and the reason behind any missed trades.

## Project structure
- `scripts/`: YouQuant extension API helper.
- `references/`: strategy schema and YouQuant workflow notes.
- `agents/`: Codex interface metadata.

