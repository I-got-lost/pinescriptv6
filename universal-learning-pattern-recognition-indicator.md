# Universal Learning Pattern Recognition Trading Indicator for PineScript V6

## A Scholarly Breakdown for Academic Exhibition

---

## 1. ASCII Diagram: Primary Algorithmic Components

```
                    ┌─────────────────────────────────────────┐
                    │          MARKET DATA INGESTION           │
                    │     open, high, low, close, volume       │
                    │        (bar-by-bar time series)          │
                    └──────────────┬──────────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
   │   A. TREND CORE  │ │  B. MOMENTUM     │ │  C. VOLATILITY   │
   │                  │ │     ENGINE       │ │     ENVELOPE     │
   │  EMA(fast)       │ │  RSI(close,n)    │ │  ATR(n)          │
   │  EMA(slow)       │ │  MACD(f,s,sig)   │ │  BB(close,n,dev) │
   │  SMA(baseline)   │ │  Stoch(%K,%D)    │ │  KC(close,n,mul) │
   │  HMA(smooth)     │ │  MOM(close,n)    │ │  True Range      │
   └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
            │                    │                    │
            ▼                    ▼                    ▼
   ┌──────────────────────────────────────────────────────────────┐
   │              D. PATTERN RECOGNITION MATRIX                   │
   │                                                              │
   │   Crossover/Crossunder Detection (ta.crossover/crossunder)   │
   │   Pivot Point Identification   (ta.pivothigh/ta.pivotlow)    │
   │   Rising/Falling Sequence Test (ta.rising/ta.falling)        │
   │   Historical Divergence Scan   ([] operator, ta.change)      │
   │   Linear Regression Channel    (ta.linreg)                   │
   └──────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
   ┌──────────────────────────────────────────────────────────────┐
   │           E. ADAPTIVE WEIGHTING & CONFLUENCE LOGIC           │
   │                                                              │
   │   Signal Scoring:  weight_trend * S_trend                    │
   │                  + weight_mom   * S_momentum                 │
   │                  + weight_vol   * S_volatility               │
   │                                                              │
   │   Adaptive Alpha:  alpha = 2 / (dynamicLength + 1)           │
   │   Persistence:     var float compositeScore = 0.0            │
   └──────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
   ┌──────────────────────────────────────────────────────────────┐
   │              F. SIGNAL GENERATION & OUTPUT                   │
   │                                                              │
   │   Threshold Filter:  compositeScore > bullThreshold          │
   │                      compositeScore < bearThreshold          │
   │   Confirmation Gate: barstate.isconfirmed                    │
   │                                                              │
   │   Visual Output:   plot(), plotshape(), bgcolor()            │
   │   Alert System:    alert("Long"/"Short", freq)               │
   └──────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Component Descriptions

### Component A: Trend Core

The Trend Core serves as the indicator's directional backbone, determining the prevailing market regime through a hierarchy of moving averages. Each average captures a different temporal scale of price memory.

**Exponential Moving Average (EMA).** Defined recursively as `EMA_t = alpha * source_t + (1 - alpha) * EMA_{t-1}`, where `alpha = 2 / (length + 1)`. The exponential decay assigns geometrically decreasing weight to older observations, making the EMA more responsive to recent price changes than an equally weighted average. In PineScript v6, this is computed via `ta.ema(close, length)`. Two EMAs of different periods (fast and slow) form the basis for trend direction assessment: when the fast EMA exceeds the slow EMA, the market is interpreted as being in an uptrend, and vice versa.

**Simple Moving Average (SMA).** The arithmetic mean of the last *n* closing prices: `SMA = (1/n) * sum(close, n)`. It serves as a baseline filter, smoothing out transient noise. Its equal weighting of all observations within the window makes it a natural benchmark against which the EMA's recency bias can be compared. Computed via `ta.sma(close, length)`.

**Hull Moving Average (HMA).** Alan Hull's construction reduces lag by computing a weighted moving average of two WMAs at different scales, then applying a final WMA of period `sqrt(n)` to the result. The HMA achieves smoothness without the phase delay typical of longer-period moving averages. In PineScript v6: `ta.hma(source, length)`. Within the Trend Core, the HMA acts as the "refined" directional signal, confirming transitions identified by the EMA crossover system.

**Role in the indicator.** The Trend Core assigns a directional bias (bullish, bearish, or neutral) to each bar. Its output is a normalized trend score `S_trend` in the range [-1, +1], derived from the relative positioning and slope of the moving average hierarchy.

---

### Component B: Momentum Engine

The Momentum Engine quantifies the rate and strength of price change, detecting acceleration and deceleration in trends before they become visible in the moving average structure.

**Relative Strength Index (RSI).** Wilder's momentum oscillator computes the ratio of average upward movement to average total movement over *n* periods: `RSI = 100 - 100 / (1 + RS)`, where `RS = avg_gain / avg_loss`. Values above 70 conventionally indicate overbought conditions; values below 30, oversold. In PineScript v6: `ta.rsi(close, n)`. The RSI's bounded [0, 100] output makes it directly suitable for normalization within the composite scoring framework.

**Moving Average Convergence/Divergence (MACD).** Gerald Appel's indicator computes the difference between a fast EMA (typically 12-period) and a slow EMA (typically 26-period), then smooths the result with a signal-line EMA (typically 9-period). The MACD histogram—the difference between the MACD line and the signal line—measures momentum of momentum, or the acceleration of the trend. PineScript v6 returns this as a tuple: `[macdLine, signalLine, histLine] = ta.macd(close, fast, slow, signal)`.

**Stochastic Oscillator.** George Lane's oscillator locates the current close relative to the high-low range over *n* periods: `%K = 100 * (close - lowest_low) / (highest_high - lowest_low)`. This maps price position into a [0, 100] range, identifying whether the close is near the top or bottom of its recent trading range. Computed as `ta.stoch(close, high, low, length)`.

**Momentum (MOM).** The simplest rate-of-change measure: `MOM = close - close[n]`, the raw difference between the current price and the price *n* bars ago. Via `ta.mom(close, n)`.

**Role in the indicator.** The Momentum Engine generates a composite momentum score `S_momentum` by normalizing each sub-indicator's output to a common scale and averaging them. Divergences between momentum readings and price action (e.g., price making new highs while RSI makes lower highs) are flagged as potential reversal signals.

---

### Component C: Volatility Envelope

The Volatility Envelope measures the dispersion and range of price fluctuations, serving both as a risk gauge and as a means of dynamically adjusting the sensitivity of signal thresholds.

**Average True Range (ATR).** Wilder's ATR computes the exponential moving average of the True Range, where `TR = max(high - low, |high - close[1]|, |low - close[1]|)`. The inclusion of prior-bar close accounts for overnight gaps, making ATR a more comprehensive measure of volatility than simple range. In PineScript v6: `ta.atr(length)`.

**Bollinger Bands (BB).** John Bollinger's bands place an envelope at `mean +/- k * stdev` around a moving average, where *k* is typically 2.0. The bands expand and contract with volatility, providing a visual probabilistic framework: approximately 95% of observations fall within 2-standard-deviation bands under normal distribution assumptions. PineScript v6: `[middle, upper, lower] = ta.bb(close, length, mult)`.

**Keltner Channels (KC).** Chester Keltner's channels replace Bollinger's standard deviation with ATR-based envelopes: `channel = EMA(close, n) +/- mult * EMA(TR, n)`. Keltner Channels respond more linearly to volatility changes compared to the quadratic response of standard deviation. PineScript v6: `[middle, upper, lower] = ta.kc(close, length, mult)`.

**Role in the indicator.** The Volatility Envelope generates a normalized volatility score `S_volatility` used in two ways: (1) as a direct input to the composite score, where elevated volatility can either amplify or attenuate signal confidence depending on context, and (2) as an adaptive modifier for threshold levels, widening the confirmation gate during high-volatility regimes to reduce false signals.

---

### Component D: Pattern Recognition Matrix

The Pattern Recognition Matrix is the analytical core that transforms the raw outputs of Components A-C into discrete structural observations about price behavior.

**Crossover/Crossunder Detection.** The functions `ta.crossover(series1, series2)` and `ta.crossunder(series1, series2)` return `true` on the exact bar where one series crosses above or below another. Mathematically, `crossover(a, b) = (a > b) AND (a[1] <= b[1])`. These Boolean signals mark the transition points between trend regimes and are used to identify inflection bars.

**Pivot Point Identification.** The functions `ta.pivothigh(source, leftbars, rightbars)` and `ta.pivotlow(source, leftbars, rightbars)` identify local extrema by confirming that a bar's value is the highest (or lowest) within both the left and right neighborhoods. The output is non-na only on bars where a pivot is confirmed, introducing a deliberate lag of `rightbars` periods. Pivots provide the structural skeleton of swing highs and swing lows necessary for identifying chart patterns (double tops, head-and-shoulders, ascending triangles, etc.).

**Rising/Falling Sequence Test.** `ta.rising(source, length)` returns `true` if the source value has been consecutively increasing for *length* bars; `ta.falling(source, length)` tests the opposite. These functions quantify the persistence of directional movement, distinguishing sustained moves from random fluctuations.

**Historical Divergence Scan.** Using the `[]` history-referencing operator (e.g., `close[n]`) and `ta.change(source, n)`, the matrix scans for divergences: situations where price and an oscillator (RSI, MACD histogram) move in opposite directions. Classic divergence analysis treats a price-high / oscillator-low combination as bearish, and the inverse as bullish.

**Linear Regression Channel.** `ta.linreg(source, length, offset)` fits a least-squares regression line to the last *length* values of the source series. The slope of this line provides a statistically smoothed trend direction, while the distance from the regression line to current price measures deviation from the linear trend. This complements the moving average analysis in Component A with a parametric model.

---

### Component E: Adaptive Weighting & Confluence Logic

This component synthesizes all upstream signals into a single actionable composite score, using an adaptive weighting scheme that adjusts to prevailing market conditions.

**Signal Scoring Formula.** The composite score is computed as:

```
compositeScore = w_trend   * S_trend
               + w_mom     * S_momentum
               + w_vol     * S_volatility
```

where `w_trend + w_mom + w_vol = 1.0`. The weights can be fixed inputs or, in the adaptive variant, adjusted dynamically based on which component has demonstrated greater predictive reliability over a trailing window.

**Adaptive Alpha.** Drawing on the EMA's recursive formula, an adaptive smoothing constant `alpha = 2 / (dynamicLength + 1)` is computed, where `dynamicLength` itself varies with market volatility: shorter in trending, low-volatility environments (higher alpha, faster response) and longer in choppy, high-volatility environments (lower alpha, greater smoothing). The `var` keyword in PineScript v6 ensures the composite score persists across bars: `var float compositeScore = 0.0`, updating via `compositeScore := alpha * rawScore + (1 - alpha) * compositeScore`.

**Confluence Gate.** Signals are elevated to "confirmed" status only when multiple independent sub-components agree. A simple confluence count—the number of sub-components signaling the same direction—must exceed a user-defined threshold before the composite score can generate a trade signal. This reduces the false-positive rate inherent in any single-indicator approach.

---

### Component F: Signal Generation & Output

The final stage converts the composite score into visual and alert-based outputs suitable for use in futures markets.

**Threshold Filter.** A long signal fires when `compositeScore > bullThreshold`; a short signal fires when `compositeScore < bearThreshold`. Thresholds are expressed as user inputs via `input.float()`, allowing calibration to different instruments and timeframes.

**Confirmation Gate.** For non-repainting behavior on realtime bars, the signal requires `barstate.isconfirmed == true` before committing to output. This ensures that signals are generated only on the bar's closing tick, after rollback and recalculation have settled to their final values.

**Visual Output.** PineScript v6's `plot()` draws the composite score as a continuous line. `plotshape()` marks entry signals (triangles, arrows) at confirmed locations. `bgcolor()` applies a translucent background tint to bars where active signals are present, providing at-a-glance regime identification.

**Alert System.** The `alert()` function dispatches messages when signals trigger, with `alert.freq_once_per_bar_close` ensuring one notification per confirmed bar. Messages are constructed dynamically using `str.tostring()` to include the composite score value and the direction.

---

## 3. Assembly Sequence — As Reconstructed from Archival Sources

*The following narrative reconstructs the step-by-step assembly of the indicator as it would be built for deployment on futures market charts. It is presented in the structured, numbered format of a museum plaque, suitable for a historical exhibition on algorithmic trading methods.*

---

**UNIVERSAL LEARNING PATTERN RECOGNITION INDICATOR**
*Assembly Sequence for Futures Markets — PineScript V6*
*Reconstructed from practitioner archives, ca. 2024-2025*

---

**Step 1. Establish the Computational Framework.**
The practitioner begins by declaring the script as a PineScript v6 indicator with `indicator()`, specifying `overlay = true` so that its visual outputs render directly on the price chart. A separate oscillator pane is allocated for the composite score. Input parameters are declared using `input.int()`, `input.float()`, and `input.source()` to allow calibration of all lookback periods, smoothing constants, and threshold values without modifying source code. Constants are defined in `SNAKE_CASE` per the PineScript style guide: `BULL_THRESHOLD`, `BEAR_THRESHOLD`, `MAX_LOOKBACK`.

**Step 2. Ingest the Market Data Stream.**
On each bar, the PineScript runtime automatically updates the built-in variables `open`, `high`, `low`, `close`, and `volume` to reflect the current bar's OHLCV data. For futures contracts, the practitioner accesses `syminfo.current_contract` (introduced in the 2025 PineScript updates) to identify the active front-month contract. The `bid` and `ask` variables (also introduced in 2025) provide real-time spread information on the live bar, useful for filtering signals in illiquid hours.

**Step 3. Construct the Trend Core.**
The fast EMA, slow EMA, baseline SMA, and smoothing HMA are computed in sequence. Each moving average is declared without the `var` keyword, so it is recalculated fresh on every bar from the full time series history. The trend score `S_trend` is derived by normalizing the distance between the fast and slow EMAs relative to the ATR, bounding the result to [-1, +1] with a clamping function: `math.max(-1.0, math.min(1.0, (emaFast - emaSlow) / ta.atr(14)))`.

**Step 4. Activate the Momentum Engine.**
RSI, MACD, Stochastic, and raw Momentum are computed in parallel. Each sub-indicator's output is normalized to a [-1, +1] scale. For RSI, this is `(rsi - 50) / 50`. For the MACD histogram, the raw value is divided by the ATR to produce a dimensionless ratio. The Stochastic is transformed as `(stoch - 50) / 50`. These normalized values are averaged to produce `S_momentum`. Divergence detection is performed by comparing the direction of `ta.change(close, lookback)` against `ta.change(rsi, lookback)`: opposite signs indicate divergence.

**Step 5. Calibrate the Volatility Envelope.**
ATR, Bollinger Band width (`ta.bbw()`), and Keltner Channel width (`ta.kcw()`) are computed. The volatility score `S_volatility` is constructed as the percentile rank (`ta.percentrank()`) of the current ATR within its own trailing distribution. A high percentile rank (e.g., above 80) indicates that current volatility is historically elevated, which the Adaptive Weighting module interprets as a regime requiring wider thresholds.

**Step 6. Populate the Pattern Recognition Matrix.**
Crossover events between the fast and slow EMAs are detected with `ta.crossover()` and `ta.crossunder()`. Pivot highs and lows are identified with lookback/lookahead windows of 5 bars each via `ta.pivothigh(high, 5, 5)` and `ta.pivotlow(low, 5, 5)`. The linear regression slope is computed with `ta.linreg(close, regressionLength, 0)` and compared to its own value one bar prior to detect slope inflections. All detected patterns are encoded as Boolean flags stored in the indicator's time series.

**Step 7. Apply Adaptive Weighting and Compute the Composite Score.**
The three component scores are combined using the weighted sum formula. The composite score is smoothed through the adaptive EMA mechanism, with `dynamicLength` derived from the inverse of normalized volatility: low volatility yields shorter smoothing (faster adaptation), high volatility yields longer smoothing (more conservative). The `var` keyword ensures the composite score persists bar-to-bar, accumulating the learning embedded in its recursive structure.

**Step 8. Impose the Signal Confirmation Gate.**
The raw composite score must exceed `BULL_THRESHOLD` (for longs) or fall below `BEAR_THRESHOLD` (for shorts) to generate a candidate signal. Before the signal is committed to output, the gate requires `barstate.isconfirmed == true`, ensuring the signal is evaluated only on the bar's final tick. For futures markets, where overnight gaps can distort indicators computed from continuous data, an additional check filters signals on bars immediately following a session gap (detected via `ta.change(time) > expectedBarDuration`).

**Step 9. Render Visual Outputs.**
The composite score is plotted as a histogram in the oscillator pane using `plot(compositeScore, style = plot.style_histogram)`, colored with `color.from_gradient()` mapping the score range to a green-to-red spectrum. Entry signals are marked on the price chart with `plotshape()`: upward triangles below bars for long entries, downward triangles above bars for short entries. Background coloring via `bgcolor()` highlights active signal regimes with translucent fills.

**Step 10. Arm the Alert Mechanism.**
The `alert()` function is placed within conditional blocks gated by the confirmed signal logic. Each alert carries a dynamically constructed message incorporating the instrument symbol (`syminfo.ticker`), the direction, the composite score (`str.tostring(compositeScore, "#.##")`), and the bar's timestamp. The frequency is set to `alert.freq_once_per_bar_close` to prevent duplicate notifications from intra-bar recalculations on the realtime bar. The practitioner creates separate alert conditions for long entries, short entries, and regime transitions, allowing end users to subscribe selectively.

---

*This indicator exemplifies the convergence of classical technical analysis with adaptive computational methods, executed within the event-driven, bar-by-bar architecture of PineScript v6. Each component draws upon decades of market microstructure research, while the adaptive weighting mechanism introduces a rudimentary form of online learning—adjusting its own parameters in response to the evolving statistical properties of the data stream it processes.*

---

**Provenance Note:** All PineScript v6 functions referenced herein (`ta.ema`, `ta.sma`, `ta.hma`, `ta.rsi`, `ta.macd`, `ta.stoch`, `ta.mom`, `ta.atr`, `ta.bb`, `ta.kc`, `ta.crossover`, `ta.crossunder`, `ta.pivothigh`, `ta.pivotlow`, `ta.rising`, `ta.falling`, `ta.linreg`, `ta.change`, `ta.percentrank`, `ta.bbw`, `ta.kcw`, `math.max`, `math.min`, `color.from_gradient`, `str.tostring`, `alert`, `plot`, `plotshape`, `bgcolor`, `barstate.isconfirmed`, `syminfo.ticker`, `syminfo.current_contract`) are documented in the PineScript v6 Language Reference Manual and conform to the syntax and semantics of version 6 as specified by TradingView.
