---
name: youquant-backtest-automation
description: End-to-end automation for implementing a new quantitative strategy on YouQuant and running backtests. Use when the user provides a natural-language trading strategy for 优宽/YouQuant and wants Codex to translate it into executable strategy code, save it to a target strategy page, launch a backtest, inspect results, and iterate on issues such as contract sizing, trigger logic, or platform-specific errors.
---

# YouQuant Backtest Automation

Use this skill to take a strategy from user prose to a completed YouQuant backtest run.

## Inputs

Collect or infer these fields before editing code:

- strategy description in natural language
- target strategy name or strategy ID
- asset class and exchange type on YouQuant
- symbol or continuous contract, for example `cu888`
- initial capital
- bar period and indicator period
- position sizing rule: lots, notional, or margin budget
- stop loss / stop profit / re-entry rules
- backtest date range if the user provides one
- whether this is backtest-only or may touch live trading

If a field is missing, make the narrowest safe assumption and state it. Default to backtest-only.

## Workflow

1. Normalize the strategy into a structured brief.
   Use [references/strategy-schema.md](./references/strategy-schema.md).

2. Run a feasibility check before writing code.
   Detect contract multiplier issues, minimum tradable size, duplicated triggers, ambiguous bar frequency, and whether the requested position size can open at least one lot.

3. Choose the correct YouQuant runtime model.
   For futures, prefer the exchange-style API with functions such as `exchange.SetContractType`, `exchange.GetRecords`, `exchange.GetTicker`, `exchange.GetPositions`, `exchange.SetDirection`, `exchange.Buy`, and `exchange.Sell`.

4. Generate or update strategy code locally first.
   Keep a local copy in the workspace before touching the web editor.

5. Use browser automation to update the target strategy page on YouQuant.
   Save the strategy, switch to the backtest tab, and start a backtest.
   See [references/youquant-workflow.md](./references/youquant-workflow.md).

6. Read the backtest output, not just the top-line metrics.
   Capture:
   - whether the run succeeded
   - transaction count
   - major errors
   - key log messages
   - why trades did not happen or behaved unexpectedly

7. Explain the outcome in trading terms.
   Example: “The rule executed, but `20万` and `30万` were both below one tradable lot for `cu888`, so all signals were skipped.”

8. Propose the next iteration only after reporting the current run.
   Typical iterations:
   - switch from notional sizing to lot sizing
   - switch from notional sizing to margin-budget sizing
   - limit re-entry frequency
   - add slippage and fee assumptions
   - change the signal to cross-under / cross-over rather than level comparison

## Guardrails

- Do not create or run a live robot unless the user explicitly requests live trading.
- Do not overwrite an unrelated strategy. Require a strategy name or strategy ID and verify it matches the intended target.
- Do not hide feasibility problems. If the requested capital cannot buy one lot, say so explicitly.
- Do not claim an API can launch backtests unless you confirmed it. Prefer browser automation for actual backtest execution.
- Keep each strategy iteration saved locally in the workspace.

## Scripts

- `scripts/youquant_api.py`: minimal extension API helper for listing strategies or robots and calling raw methods

## References

- `references/strategy-schema.md`: fields to extract from a natural-language strategy
- `references/youquant-workflow.md`: platform-specific execution notes and browser flow
