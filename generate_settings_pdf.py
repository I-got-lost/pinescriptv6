#!/usr/bin/env python3
"""
Generate the ULPR Strategy Settings Reference PDF.
Uses fpdf2 to produce a professional-looking document.
"""

from fpdf import FPDF


class ULPRSettingsPDF(FPDF):
    DARK_BG = (30, 34, 45)
    HEADER_BG = (54, 58, 69)
    BULL_COLOR = (38, 166, 154)
    BEAR_COLOR = (239, 83, 80)
    ACCENT = (33, 150, 243)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (200, 200, 200)
    MID_GRAY = (140, 140, 140)
    ROW_ALT = (240, 242, 245)
    ROW_NORMAL = (255, 255, 255)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.MID_GRAY)
        self.cell(0, 8, "ULPR Strategy - Settings Reference Guide", align="L")
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.MID_GRAY)
        self.cell(0, 10, "Universal Learning Pattern Recognition Strategy  - PineScript V6 Reference", align="C")

    def section_title(self, title):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def subsection_title(self, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def setting_row(self, name, type_str, default, range_str, description, row_idx=0):
        bg = self.ROW_ALT if row_idx % 2 == 0 else self.ROW_NORMAL

        # Check for page break need
        if self.get_y() > 250:
            self.add_page()

        # Row 1: name | type | default | range
        self.set_fill_color(*bg)
        self.set_font("Courier", "B", 8)
        self.set_text_color(30, 30, 30)
        self.cell(60, 6, f"  {name}", fill=True)

        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.ACCENT)
        self.cell(20, 6, type_str, fill=True)

        self.set_text_color(50, 50, 50)
        self.set_font("Courier", "", 8)
        self.cell(25, 6, str(default), fill=True)

        self.set_font("Helvetica", "", 7)
        self.set_text_color(*self.MID_GRAY)
        self.cell(85, 6, f"Range: {range_str}", fill=True, new_x="LMARGIN", new_y="NEXT")

        # Row 2: description (full width)
        self.set_fill_color(*bg)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(80, 80, 80)
        self.multi_cell(190, 5, f"    {description}", fill=True)

        # Separator
        self.set_draw_color(210, 210, 210)
        self.set_line_width(0.1)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(1)

    def table_header(self):
        self.set_fill_color(*self.HEADER_BG)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 8)
        self.cell(60, 7, "  Setting Name", fill=True)
        self.cell(20, 7, "Type", fill=True)
        self.cell(25, 7, "Default", fill=True)
        self.cell(85, 7, "Range", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def example_block(self, title, text):
        self.ln(2)
        self.set_font("Helvetica", "BI", 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 6, f"Example: {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Courier", "", 8)
        self.set_text_color(50, 50, 50)
        self.set_fill_color(245, 245, 250)
        for line in text.split("\n"):
            self.cell(0, 5, f"  {line}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)


def build_pdf():
    pdf = ULPRSettingsPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── TITLE PAGE ──
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*ULPRSettingsPDF.ACCENT)
    pdf.cell(0, 14, "Universal Learning Pattern", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, "Recognition Strategy", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "User Settings Reference Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, "PineScript V6  - Chart Overlay Strategy", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    # Overview
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    overview = (
        "This document provides a complete reference for every user-configurable setting in the ULPR "
        "Strategy. Settings are organized into seven groups (A through G) matching the Settings/Inputs "
        "tab in TradingView. Each setting includes its type, default value, valid range, and a "
        "description of its effect on strategy behavior. Practical examples demonstrate common "
        "configuration scenarios for different asset classes and timeframes."
    )
    pdf.multi_cell(0, 6, overview)
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*ULPRSettingsPDF.ACCENT)
    pdf.cell(0, 8, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(60, 60, 60)
    toc_items = [
        "Section A  - Trend Core Settings",
        "Section B  - Momentum Engine Settings",
        "Section C  - Volatility Envelope Settings",
        "Section D  - Pattern Recognition Settings",
        "Section E  - Adaptive Weighting & Confluence Settings",
        "Section F  - Signal & Risk Management Settings",
        "Section G  - Visual Settings",
        "Configuration Examples by Asset Class",
        "Appendix  - Formula Quick Reference",
    ]
    for i, item in enumerate(toc_items, 1):
        pdf.cell(0, 6, f"  {i}. {item}", new_x="LMARGIN", new_y="NEXT")

    # ────────────────────────────────────────────────────────────
    # SECTION A
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Section A  - Trend Core")
    pdf.body_text(
        "The Trend Core determines the prevailing market direction using a hierarchy of four "
        "moving averages. The Fast and Slow EMAs establish the primary trend via their crossover "
        "relationship. The Baseline SMA provides a macro filter, and the Hull MA confirms trend "
        "transitions with minimal lag. The normalized trend score S_trend ranges from -1.0 "
        "(strongly bearish) to +1.0 (strongly bullish)."
    )
    pdf.table_header()
    a_settings = [
        ("Fast EMA Length", "int", "9", "2 - 200",
         "Lookback period for the fast EMA. Lower values (5-8) suit scalping; higher values (12-20) suit swing trading."),
        ("Slow EMA Length", "int", "21", "2 - 400",
         "Lookback period for the slow EMA. The fast/slow gap defines trend sensitivity. Common pairs: 9/21, 12/26, 20/50."),
        ("Baseline SMA Length", "int", "50", "5 - 500",
         "Period for the SMA macro filter. Price must be above this SMA for bullish confluence. 50 and 200 are standard institutional levels."),
        ("Hull MA Length", "int", "14", "2 - 200",
         "Period for the Hull Moving Average. Confirms the EMA crossover direction with reduced phase delay."),
        ("Show Moving Averages", "bool", "true", "on/off",
         "Toggle visibility of all four MA lines on the chart overlay."),
    ]
    for i, s in enumerate(a_settings):
        pdf.setting_row(*s, row_idx=i)

    pdf.example_block("Scalping on ES 5-minute chart", (
        "Fast EMA Length  = 5\n"
        "Slow EMA Length  = 13\n"
        "Baseline SMA     = 34\n"
        "Hull MA Length   = 9\n"
        "Rationale: Shorter periods capture quick intraday\n"
        "reversals on the E-mini S&P 500 futures."
    ))

    pdf.example_block("Swing trading on daily stock chart", (
        "Fast EMA Length  = 12\n"
        "Slow EMA Length  = 26\n"
        "Baseline SMA     = 200\n"
        "Hull MA Length   = 20\n"
        "Rationale: Aligns with the classic MACD relationship\n"
        "and uses the 200-day SMA institutional benchmark."
    ))

    # ────────────────────────────────────────────────────────────
    # SECTION B
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Section B  - Momentum Engine")
    pdf.body_text(
        "The Momentum Engine measures the rate and strength of price movement using four "
        "oscillators: RSI, MACD, Stochastic, and raw Momentum. Each is normalized to a "
        "[-1, +1] scale and averaged into S_momentum. Optional divergence detection flags "
        "situations where price and RSI move in opposite directions  - a classic reversal warning."
    )
    pdf.table_header()
    b_settings = [
        ("RSI Length", "int", "14", "2 - 100",
         "Lookback period for the Relative Strength Index. Wilder's original is 14. Shorter (7) = more signals; longer (21) = smoother."),
        ("MACD Fast Length", "int", "12", "2 - 100",
         "Fast EMA period for MACD calculation. Standard is 12. Decrease for faster response."),
        ("MACD Slow Length", "int", "26", "2 - 200",
         "Slow EMA period for MACD. Must be greater than MACD Fast. Standard is 26."),
        ("MACD Signal Length", "int", "9", "2 - 50",
         "EMA period for the MACD signal line. Smooths the MACD line for histogram calculation."),
        ("Stochastic Length", "int", "14", "2 - 100",
         "Lookback for %K Stochastic oscillator. Maps the close's position within the high-low range."),
        ("Momentum Length", "int", "10", "1 - 100",
         "Bars for raw momentum (close - close[n]). Measures directional price velocity."),
        ("Enable Divergence", "bool", "true", "on/off",
         "Detect price/RSI divergence. Bullish: price falls while RSI rises. Bearish: price rises while RSI falls."),
    ]
    for i, s in enumerate(b_settings):
        pdf.setting_row(*s, row_idx=i)

    pdf.example_block("Crypto (high-volatility regime)", (
        "RSI Length       = 10\n"
        "MACD             = 8 / 21 / 5\n"
        "Stochastic       = 10\n"
        "Momentum Length  = 7\n"
        "Divergence       = ON\n"
        "Rationale: Shorter oscillator periods react faster\n"
        "to the rapid price swings typical in crypto markets."
    ))

    # ────────────────────────────────────────────────────────────
    # SECTION C
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Section C  - Volatility Envelope")
    pdf.body_text(
        "The Volatility Envelope measures price dispersion via ATR, Bollinger Bands, and "
        "Keltner Channels. A 'squeeze' is detected when the Bollinger Bands contract inside "
        "the Keltner Channels, indicating compressed volatility that often precedes a "
        "breakout. The volatility percentile rank S_volatility indicates whether current "
        "volatility is historically high (+1) or low (-1) relative to the last 100 bars."
    )
    pdf.table_header()
    c_settings = [
        ("ATR Length", "int", "14", "2 - 100",
         "Period for Average True Range. Used for score normalization, stop-loss sizing, and volatility percentile. Wilder's standard is 14."),
        ("BB Length", "int", "20", "2 - 200",
         "Period for the Bollinger Band middle line (SMA basis). 20 is the standard Bollinger setting."),
        ("BB Multiplier", "float", "2.0", "0.5 - 5.0",
         "Standard deviation multiplier for BB width. 2.0 captures ~95% of prices. Lower = tighter bands."),
        ("KC Length", "int", "20", "2 - 200",
         "Period for the Keltner Channel center (EMA basis). Used alongside BB for squeeze detection."),
        ("KC Multiplier", "float", "1.5", "0.5 - 5.0",
         "ATR multiplier for Keltner Channel width. A squeeze fires when BB contracts inside KC  - tune KC mult to adjust sensitivity."),
        ("Show Bollinger Bands", "bool", "true", "on/off",
         "Toggle BB upper/lower bands and fill zone on the chart."),
        ("Show Keltner Channels", "bool", "false", "on/off",
         "Toggle KC upper/lower lines on the chart. Useful for visualizing squeeze conditions."),
    ]
    for i, s in enumerate(c_settings):
        pdf.setting_row(*s, row_idx=i)

    pdf.example_block("Squeeze breakout setup", (
        "BB Length       = 20, Mult = 2.0\n"
        "KC Length       = 20, Mult = 1.5\n"
        "Show BB         = ON\n"
        "Show KC         = ON\n"
        "Rationale: With both visible, you can see exactly\n"
        "when BB contracts inside KC (squeeze = orange dots).\n"
        "Signals during a squeeze are suppressed by the\n"
        "volatility confluence check."
    ))

    # ────────────────────────────────────────────────────────────
    # SECTION D
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Section D  - Pattern Recognition")
    pdf.body_text(
        "The Pattern Recognition Matrix identifies structural price features: EMA crossovers, "
        "swing pivot highs/lows, rising/falling bar sequences, and linear regression slope "
        "direction. These Boolean flags feed into the confluence gate and visual markers."
    )
    pdf.table_header()
    d_settings = [
        ("Pivot Lookback (Left)", "int", "5", "1 - 20",
         "Bars to the left that must be lower (for a high) or higher (for a low) to confirm a pivot. Higher = fewer, more reliable pivots."),
        ("Pivot Lookahead (Right)", "int", "5", "1 - 20",
         "Bars to the right to confirm the pivot. Introduces a lag of this many bars. Trade-off: reliability vs. timeliness."),
        ("Rising/Falling Bars", "int", "3", "2 - 10",
         "Number of consecutive bars the close must increase (rising) or decrease (falling) to flag directional persistence."),
        ("Linear Regression Len", "int", "20", "5 - 100",
         "Period for the least-squares regression line. The slope direction (up/down vs. previous bar) indicates statistical trend."),
        ("Show Pivot Points", "bool", "true", "on/off",
         "Display diamond-shaped markers at confirmed swing highs (red-orange) and swing lows (green)."),
    ]
    for i, s in enumerate(d_settings):
        pdf.setting_row(*s, row_idx=i)

    pdf.example_block("Higher-timeframe pivots on weekly chart", (
        "Pivot Lookback   = 10\n"
        "Pivot Lookahead  = 10\n"
        "Rising/Falling   = 5\n"
        "LinReg Length    = 40\n"
        "Rationale: Wider pivot windows identify major swing\n"
        "points on weekly charts. Longer rising/falling\n"
        "requirement filters noise from multi-week trends."
    ))

    # ────────────────────────────────────────────────────────────
    # SECTION E
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Section E  - Adaptive Weighting & Confluence")
    pdf.body_text(
        "This section controls how the three sub-scores (Trend, Momentum, Volatility) are "
        "combined into a single composite score. Weights are auto-normalized to sum to 1.0. "
        "The adaptive smoothing option lengthens the EMA smoothing period when volatility is "
        "high, making the score less reactive during choppy conditions. The confluence gate "
        "requires a minimum number of sub-systems to agree before a signal can fire."
    )
    pdf.table_header()
    e_settings = [
        ("Weight: Trend", "float", "0.40", "0.0 - 1.0",
         "Relative importance of the Trend Core in the composite score. Auto-normalized with the other two weights."),
        ("Weight: Momentum", "float", "0.35", "0.0 - 1.0",
         "Relative importance of the Momentum Engine. Increase for mean-reversion strategies; decrease for trend-following."),
        ("Weight: Volatility", "float", "0.25", "0.0 - 1.0",
         "Relative importance of the Volatility Envelope. Higher weight makes the strategy more volatility-aware."),
        ("Score Smoothing Length", "int", "5", "1 - 50",
         "Base EMA period for smoothing the composite score. Higher = smoother score line, more lag. 1 = no smoothing."),
        ("Adaptive Smoothing", "bool", "true", "on/off",
         "When ON, smoothing length increases proportionally with the ATR percentile rank. Effect: slower reactions in volatile markets."),
        ("Min Confluence (1-3)", "int", "2", "1 - 3",
         "Minimum sub-systems that must agree. 1 = any single system can trigger. 2 = two must agree. 3 = all three must agree (strictest)."),
    ]
    for i, s in enumerate(e_settings):
        pdf.setting_row(*s, row_idx=i)

    pdf.example_block("Trend-following configuration", (
        "Weight: Trend      = 0.60\n"
        "Weight: Momentum   = 0.30\n"
        "Weight: Volatility = 0.10\n"
        "Smoothing Length   = 8\n"
        "Adaptive Smoothing = ON\n"
        "Min Confluence     = 2\n"
        "Rationale: Heavily weights the Trend Core for\n"
        "strong-trend instruments like index futures."
    ))

    pdf.example_block("Mean-reversion configuration", (
        "Weight: Trend      = 0.20\n"
        "Weight: Momentum   = 0.55\n"
        "Weight: Volatility = 0.25\n"
        "Smoothing Length   = 3\n"
        "Adaptive Smoothing = OFF\n"
        "Min Confluence     = 1\n"
        "Rationale: Emphasizes momentum oscillators for\n"
        "range-bound or mean-reverting instruments."
    ))

    # ────────────────────────────────────────────────────────────
    # SECTION F
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Section F  - Signal & Risk Management")
    pdf.body_text(
        "This section controls when signals fire and how risk is managed. The bull/bear "
        "thresholds set the composite score level required for entry. ATR-based stop-loss "
        "and take-profit orders are placed automatically. The session gap filter prevents "
        "false signals on the first bar after an overnight or weekend gap in futures. "
        "Long Only / Short Only modes restrict direction for accounts that cannot short."
    )
    pdf.table_header()
    f_settings = [
        ("Bull Threshold", "float", "0.25", "0.01 - 0.99",
         "Composite score must exceed this for a long entry. Higher = fewer, higher-conviction signals. Try 0.15 (loose) to 0.40 (strict)."),
        ("Bear Threshold", "float", "-0.25", "-0.99 - -0.01",
         "Composite score must fall below this (negative) for a short entry. Mirror of Bull Threshold for the short side."),
        ("Bar Confirmation", "bool", "true", "on/off",
         "When ON, signals only fire after barstate.isconfirmed = true (bar close). Prevents repainting. Turn OFF only for tick-level testing."),
        ("Enable ATR Stop-Loss", "bool", "true", "on/off",
         "Place a stop-loss order at entry +/- (ATR x SL Multiplier). Disabling removes the stop entirely."),
        ("SL ATR Multiplier", "float", "2.0", "0.5 - 10.0",
         "ATR units for stop-loss distance. 1.5 = tight stop, 3.0 = wide stop. Adjust based on instrument volatility."),
        ("Enable ATR Take-Profit", "bool", "true", "on/off",
         "Place a take-profit at entry +/- (ATR x TP Multiplier). Combined with SL, forms a bracket order."),
        ("TP ATR Multiplier", "float", "3.0", "0.5 - 20.0",
         "ATR units for take-profit distance. A TP/SL ratio of 1.5x or higher gives positive expectancy even at <50% win rate."),
        ("Filter Session Gaps", "bool", "true", "on/off",
         "Skip signals when bar time gap > 2x expected bar duration. Essential for futures (ES, NQ, CL) to avoid gap-bar false entries."),
        ("Long Only Mode", "bool", "false", "on/off",
         "Restrict strategy to long entries only. Useful for equities in accounts that cannot short."),
        ("Short Only Mode", "bool", "false", "on/off",
         "Restrict strategy to short entries only. Useful for dedicated hedging or bearish-only setups."),
        ("Enable Alerts", "bool", "true", "on/off",
         "Send TradingView alert() notifications on entries. Uses freq_once_per_bar_close to prevent duplicates."),
    ]
    for i, s in enumerate(f_settings):
        pdf.setting_row(*s, row_idx=i)

    pdf.example_block("Conservative futures setup (ES, 15-min)", (
        "Bull Threshold     = 0.35\n"
        "Bear Threshold     = -0.35\n"
        "Bar Confirmation   = ON\n"
        "ATR Stop-Loss      = ON, Mult = 2.5\n"
        "ATR Take-Profit    = ON, Mult = 4.0\n"
        "Filter Gaps        = ON\n"
        "Long Only          = OFF\n"
        "Rationale: Higher thresholds and wider SL/TP suit\n"
        "the higher noise on intraday futures. TP/SL ratio\n"
        "of 1.6x provides positive risk/reward."
    ))

    pdf.example_block("Aggressive crypto setup (BTC, 1H)", (
        "Bull Threshold     = 0.15\n"
        "Bear Threshold     = -0.15\n"
        "Bar Confirmation   = ON\n"
        "ATR Stop-Loss      = ON, Mult = 1.5\n"
        "ATR Take-Profit    = ON, Mult = 3.0\n"
        "Filter Gaps        = OFF\n"
        "Rationale: Lower thresholds catch more signals.\n"
        "Crypto trades 24/7 so gap filter is not needed.\n"
        "2:1 reward/risk compensates for lower win rate."
    ))

    # ────────────────────────────────────────────────────────────
    # SECTION G
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Section G  - Visual Settings")
    pdf.body_text(
        "Controls the appearance of the chart overlay: signal colors, background tinting, "
        "entry labels, and the real-time dashboard table. These settings do not affect "
        "strategy logic or backtesting results  - they are purely cosmetic."
    )
    pdf.table_header()
    g_settings = [
        ("Bull Color", "color", "#26a69a", "any color",
         "Color for bullish signals, background tint, and dashboard highlights. Default is teal/green."),
        ("Bear Color", "color", "#ef5350", "any color",
         "Color for bearish signals, background tint, and dashboard highlights. Default is red."),
        ("Neutral Color", "color", "#787b86", "any color",
         "Color for the neutral/inactive state in the dashboard. Default is gray with 50% transparency."),
        ("Show Signal Background", "bool", "true", "on/off",
         "Tint the chart background during active signal regimes. Green tint = bullish, red tint = bearish."),
        ("Show Entry/Exit Labels", "bool", "true", "on/off",
         "Display triangle markers (up for long, down for short) at strategy entry points on the chart."),
        ("Background Transparency", "int", "85", "50 - 99",
         "Transparency of the signal background. 85 = subtle hint. 50 = bold overlay. 99 = barely visible."),
        ("Show Dashboard Table", "bool", "true", "on/off",
         "Display the ULPR score dashboard in the top-right corner showing composite score, sub-scores, confluence, squeeze, and regime."),
    ]
    for i, s in enumerate(g_settings):
        pdf.setting_row(*s, row_idx=i)

    pdf.example_block("Clean chart (minimal visual clutter)", (
        "Show MAs           = OFF  (Section A)\n"
        "Show BB            = OFF  (Section C)\n"
        "Show KC            = OFF  (Section C)\n"
        "Show Pivots        = OFF  (Section D)\n"
        "Show Background    = ON, Transparency = 92\n"
        "Show Labels        = ON\n"
        "Show Dashboard     = ON\n"
        "Rationale: Hides all overlaid indicators, leaving\n"
        "only the background tint and entry triangles for\n"
        "a clean price-action-focused view."
    ))

    # ────────────────────────────────────────────────────────────
    # CONFIGURATION EXAMPLES BY ASSET CLASS
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Configuration Examples by Asset Class")

    pdf.subsection_title("1. Equity Index Futures (ES, NQ)  - 15-Minute Chart")
    pdf.body_text(
        "Trend Core: Fast EMA 9, Slow EMA 21, SMA 50, HMA 14. "
        "Momentum: RSI 14, MACD 12/26/9, Stochastic 14, MOM 10, Divergence ON. "
        "Volatility: ATR 14, BB 20/2.0, KC 20/1.5. "
        "Weights: Trend 0.45, Momentum 0.35, Volatility 0.20. Confluence 2/3. "
        "Thresholds: Bull 0.30, Bear -0.30. SL 2.0 ATR, TP 3.5 ATR. Gap Filter ON. "
        "This configuration balances trend sensitivity with noise filtering suitable "
        "for the moderate volatility of equity index futures during regular trading hours."
    )

    pdf.subsection_title("2. Crude Oil Futures (CL)  - 1-Hour Chart")
    pdf.body_text(
        "Trend Core: Fast EMA 8, Slow EMA 21, SMA 100, HMA 12. "
        "Momentum: RSI 10, MACD 8/21/5, Stochastic 10, MOM 8, Divergence ON. "
        "Volatility: ATR 14, BB 20/2.5, KC 20/2.0. "
        "Weights: Trend 0.35, Momentum 0.40, Volatility 0.25. Confluence 2/3. "
        "Thresholds: Bull 0.20, Bear -0.20. SL 2.5 ATR, TP 4.0 ATR. Gap Filter ON. "
        "Higher BB/KC multipliers account for CL's wider price swings. "
        "Momentum is weighted more heavily due to CL's tendency for sharp directional moves."
    )

    pdf.subsection_title("3. Forex Major (EUR/USD)  - 4-Hour Chart")
    pdf.body_text(
        "Trend Core: Fast EMA 12, Slow EMA 26, SMA 200, HMA 20. "
        "Momentum: RSI 14, MACD 12/26/9, Stochastic 14, MOM 14, Divergence ON. "
        "Volatility: ATR 14, BB 20/2.0, KC 20/1.5. "
        "Weights: Trend 0.50, Momentum 0.30, Volatility 0.20. Confluence 2/3. "
        "Thresholds: Bull 0.25, Bear -0.25. SL 1.5 ATR, TP 2.5 ATR. Gap Filter OFF. "
        "Forex trades nearly 24 hours so gap filter is unnecessary. "
        "The 200-period SMA aligns with the institutional benchmark on the 4H timeframe. "
        "Trend is heavily weighted because forex pairs tend to exhibit sustained directional moves."
    )

    pdf.subsection_title("4. Cryptocurrency (BTC/USD)  - 1-Hour Chart")
    pdf.body_text(
        "Trend Core: Fast EMA 7, Slow EMA 18, SMA 50, HMA 10. "
        "Momentum: RSI 10, MACD 8/21/5, Stochastic 10, MOM 7, Divergence ON. "
        "Volatility: ATR 14, BB 20/2.5, KC 20/2.0. "
        "Weights: Trend 0.30, Momentum 0.45, Volatility 0.25. Confluence 2/3. "
        "Thresholds: Bull 0.15, Bear -0.15. SL 1.5 ATR, TP 3.0 ATR. Gap Filter OFF. "
        "Crypto markets are 24/7 with high volatility. Shorter periods and lower thresholds "
        "capture the frequent momentum-driven moves. Wider BB/KC multipliers prevent "
        "excessive squeeze signals. Momentum is the dominant weight."
    )

    pdf.subsection_title("5. Stocks (Daily Chart, Long Only)")
    pdf.body_text(
        "Trend Core: Fast EMA 10, Slow EMA 30, SMA 200, HMA 16. "
        "Momentum: RSI 14, MACD 12/26/9, Stochastic 14, MOM 14, Divergence ON. "
        "Volatility: ATR 14, BB 20/2.0, KC 20/1.5. "
        "Weights: Trend 0.55, Momentum 0.30, Volatility 0.15. Confluence 2/3. "
        "Thresholds: Bull 0.30. SL 2.0 ATR, TP 4.0 ATR. Long Only Mode ON. "
        "For buy-and-hold-oriented stock accounts. The 200-day SMA filters for "
        "secular uptrends. Long Only mode prevents short positions. "
        "Higher TP/SL ratio (2:1) compensates for the asymmetric upward bias in equities."
    )

    # ────────────────────────────────────────────────────────────
    # APPENDIX  - FORMULA QUICK REFERENCE
    # ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Appendix  - Formula Quick Reference")

    formulas = [
        ("Trend Score (S_trend)",
         "clamp( (EMA_fast - EMA_slow) / ATR , -1, +1 )"),
        ("Momentum Score (S_momentum)",
         "avg( (RSI-50)/50, clamp(MACD_hist/ATR), (Stoch-50)/50, clamp(MOM/(2*ATR)) )"),
        ("Volatility Score (S_volatility)",
         "( percentrank(ATR, 100) - 50 ) / 50"),
        ("Composite Score",
         "alpha * rawScore + (1-alpha) * prevScore,  where rawScore = w1*S_trend + w2*S_mom + w3*S_vol"),
        ("Adaptive Alpha",
         "2 / (dynamicLen + 1),  where dynamicLen = smoothLen * (1 + volPctRank/100)"),
        ("Stop-Loss Distance",
         "ATR * SL_Multiplier (in price units from entry)"),
        ("Take-Profit Distance",
         "ATR * TP_Multiplier (in price units from entry)"),
        ("Squeeze Condition",
         "BB_upper < KC_upper  AND  BB_lower > KC_lower"),
        ("Bull Divergence",
         "ta.change(close, 5) < 0  AND  ta.change(RSI, 5) > 0"),
        ("Bear Divergence",
         "ta.change(close, 5) > 0  AND  ta.change(RSI, 5) < 0"),
        ("Session Gap",
         "ta.change(time) > 2 * timeframe.in_seconds() * 1000"),
        ("Long Entry Condition",
         "compositeScore > bullThreshold  AND  confluence >= minConfluence  AND  confirmed  AND  NOT gap"),
        ("Short Entry Condition",
         "compositeScore < bearThreshold  AND  confluence >= minConfluence  AND  confirmed  AND  NOT gap"),
    ]

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*ULPRSettingsPDF.HEADER_BG)
    pdf.set_text_color(*ULPRSettingsPDF.WHITE)
    pdf.cell(60, 7, "  Formula", fill=True)
    pdf.cell(130, 7, "Definition", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    for i, (name, formula) in enumerate(formulas):
        bg = ULPRSettingsPDF.ROW_ALT if i % 2 == 0 else ULPRSettingsPDF.ROW_NORMAL
        pdf.set_fill_color(*bg)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(60, 6, f"  {name}", fill=True)
        pdf.set_font("Courier", "", 7)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(130, 6, formula, fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 5, (
        "Note: clamp(x) = math.max(-1, math.min(1, x)).  "
        "All PineScript v6 functions (ta.ema, ta.sma, ta.hma, ta.rsi, ta.macd, ta.stoch, "
        "ta.mom, ta.atr, ta.bb, ta.kc, ta.crossover, ta.crossunder, ta.pivothigh, "
        "ta.pivotlow, ta.rising, ta.falling, ta.linreg, ta.change, ta.percentrank) "
        "are documented in the TradingView PineScript v6 Language Reference Manual."
    ))

    # ── OUTPUT ──
    output_path = "/home/user/pinescriptv6/ULPR_Strategy_Settings_Guide.pdf"
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
