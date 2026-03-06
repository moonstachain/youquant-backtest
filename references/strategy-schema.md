# Strategy Schema

Use this schema to convert the user's prose into an implementation brief before coding.

## Required fields

- `market_type`
  - Example: `futures`
- `platform_type`
  - Example: `YouQuant commodity futures`
- `symbol`
  - Example: `cu888`
- `initial_capital`
  - Example: `1000000`
- `bar_context`
  - Example: `daily MA, intraday execution`
- `entry_rules`
  - List each trigger separately
- `exit_rules`
  - Stop loss, stop profit, forced close, session-end rules
- `position_sizing`
  - `lots`, `notional`, or `margin_budget`
- `reentry_policy`
  - Example: `each MA level can trigger once until flat`
- `backtest_scope`
  - Date range, fees, slippage, matching mode if specified

## Feasibility checks

Run these checks before coding:

1. Can the requested budget buy at least one tradable unit?
2. Does the user mean “touches a moving average” or “crosses below it from above”?
3. Are moving averages computed on daily bars while execution runs on ticks or intraday bars?
4. Can multiple entry rules fire on the same bar?
5. Is stop loss based on:
   - floating PnL on current positions
   - realized loss
   - account drawdown
6. If the contract is continuous, does the user accept rollover behavior?

## Default interpretations

Apply these defaults only when the user did not specify otherwise:

- treat “跌到均线 / 跌破均线” as cross-under from above
- treat “买 20 万 / 买 30 万” as notional budget, not margin budget
- compute moving averages on daily bars if the user says `5日` and `20日`
- reset trigger flags after the strategy becomes flat
- do backtest only, not live trading

## Output format

Keep the brief compact and explicit. Example:

```json
{
  "market_type": "futures",
  "symbol": "cu888",
  "initial_capital": 1000000,
  "bar_context": "daily MA, tick execution",
  "entry_rules": [
    {"trigger": "cross_below_ma5", "budget_type": "notional", "budget": 200000},
    {"trigger": "cross_below_ma20", "budget_type": "notional", "budget": 300000}
  ],
  "exit_rules": [
    {"trigger": "floating_pnl_lte", "value": -100000, "action": "close_all"}
  ],
  "reentry_policy": "each trigger once until flat"
}
```
