# YouQuant Workflow

## Use the public extension API for account-side lookup only

Confirmed useful methods:

- `GetStrategyList`
- `GetRobotList`

Use these to find the strategy ID, validate the target strategy name, and inspect whether live robots exist.

## Do not assume the public extension API can launch a backtest

Treat backtest execution as a browser automation task unless you have directly verified a supported API for it.

## Standard browser flow

1. Open the target strategy editor page:
   - `/m/edit-strategy/<strategy_id>`
2. Replace the code with the latest local version.
3. Save the strategy.
4. Switch to `模拟回测`.
5. Click `开始回测`.
6. Wait for completion and inspect:
   - backtest log
   - status panel
   - transaction count
   - equity / return summary

## Result interpretation checklist

- `交易次数 = 0`
  - check whether sizing could open one lot
  - check whether signals ever crossed the threshold
  - check whether the contract or date range had data

- syntax or runtime errors
  - report exact failing line or message
  - patch locally first
  - re-save and re-run

- all signals skipped
  - inspect log messages
  - explain in market terms, not just code terms

## Local artifact expectations

Keep a local file for each stable strategy version in the workspace.

Minimum:

- strategy source file
- strategy ID or target strategy name
- short note about last backtest outcome
