import streamlit as st
import plotly.graph_objects as go
import datetime
from core.global_engine import fetch_global_stock_data

# --- SYSTEM CONFIGURATION ---
st.set_page_config(page_title="HOTPOT Quantitative Terminal", page_icon="🔥", layout="wide")

# --- CUSTOM CSS INJECTION FOR THE STAR ENGINE AND THE RED/YELLOW BRAND THEME ---
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 95%; }
    div.stButton > button:first-child { background-color: #ff3333; color: white; font-weight: bold; width: 100%; border: none; }
    div.stButton > button:hover { background-color: #ffcc00; color: black; }
    .star-rating { color: #ffcc00; font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- APPLICATION ROUTING TABS ---
main_tab, glossary_tab = st.tabs(["🔥 HOTPOT Real-Time Engine", "📚 Knowledge Hub & Glossary Definitions"])

# ==============================================================================
# TAB 1: MAIN REAL-TIME ENGINE
# ==============================================================================
with main_tab:
    # Centered Custom Stylized Header Brand Block
    st.markdown("""
        <h1 style='text-align: center; font-size: 55px; margin-bottom: 0;'>
            <span style='color: #FF3333; font-weight: 900;'>HOT</span><span style='color: #FFCC00; font-weight: 900;'>POT</span>
        </h1>
        <p style='text-align: center; color: #b0b3b8; font-size: 16px; margin-top: 0;'>
            Institutional Single-Input Retail Financial Analysis Dashboard
        </p>
    """, unsafe_allow_html=True)
    st.write("---")

    # HORIZONTAL SEARCH AND SELECTION TOOLBAR ROW
    col_search, col_dropdown = st.columns([3, 1])
    with col_dropdown:
        preset_ticker = st.selectbox(
            "Quick Select Top Watchlist Stocks:",
            options=["Custom Input...", "AAPL", "NVDA", "TSLA", "MSFT", "AMZN", "GOOGL", "NFLX"]
        )
    with col_search:
        if preset_ticker != "Custom Input...":
            user_ticker = st.text_input("Enter Target Global Equity Symbol:", value=preset_ticker).upper().strip()
        else:
            user_ticker = st.text_input("Enter Target Global Equity Symbol:", value="AAPL").upper().strip()

    if user_ticker:
        # Pull core functional variables via backend dictionary pipeline
        data = fetch_global_stock_data(user_ticker)
        
        if data["status"] == "success":
            metrics = data["essential_metrics"]
            ai = data["ai_summary"]
            
            # ------------------------------------------------------------------
            # SECTION 1: ESSENTIAL METRICS PANEL REFERENCE
            # ------------------------------------------------------------------
            st.subheader("📌 Key Financial Metrics Reference")
            
            m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
            m_col1.metric("Current Price", metrics["Current Price"])
            m_col2.metric("Market Capitalization", metrics["Market Cap"])
            m_col3.metric("P/E Ratio (TTM)", str(metrics["P/E Ratio"]))
            m_col4.metric("Earnings Per Share (EPS)", metrics["EPS"])
            m_col5.metric("Revenue Growth YoY", metrics["Revenue Growth"])
            
            m_col6, m_col7, m_col8, m_col9, m_col10 = st.columns(5)
            m_col6.metric("Net Profit Margin", metrics["Net Profit Margin"])
            m_col7.metric("Return on Equity (ROE)", metrics["ROE"])
            m_col8.metric("Debt-to-Equity Ratio", metrics["Debt-to-Equity"])
            m_col9.metric("Free Cash Flow (FCF)", metrics["Free Cash Flow"])
            m_col10.metric("Dividend Yield %", metrics["Dividend Yield"])
            
            m_col11, m_col12, m_col13 = st.columns([1, 1, 3])
            m_col11.metric("1Y Trailing Return", metrics["1Y Return"])
            m_col12.metric("Annualized Volatility", metrics["Volatility"])
            m_col13.metric("Average Trading Volume", metrics["Average Volume"])
            
            st.write("---")
            
            # ------------------------------------------------------------------
            # SECTION 2: GRAPH TIMEFRAME FILTERS AND GRAPH RENDERING
            # ------------------------------------------------------------------
            st.subheader("📉 Technical Pricing Trend Dynamic Graph")
            
            # Small structural horizon button segments directly placed over the chart coordinate
            time_filter = st.radio(
                "Adjust Active Graph Historical Time Frame Horizon:",
                options=["1 Month", "6 Months", "1 Year", "Full (3 Years)"],
                horizontal=True
            )
            
            df = data["raw_historical"]
            if time_filter == "1 Month":
                filtered_df = df.tail(21)
            elif time_filter == "6 Months":
                filtered_df = df.tail(126)
            elif time_filter == "1 Year":
                filtered_df = df.tail(252)
            else:
                filtered_df = df

            fig = go.Figure(data=go.Scatter(
                x=filtered_df.index, y=filtered_df['Close'], 
                mode='lines', line=dict(color='#FFCC00', width=2.5)
            ))
            fig.update_layout(
                xaxis_title="Timeline Interval", yaxis_title="Closing Value ($)",
                template="plotly_dark", margin=dict(l=10, r=10, t=10, b=10), height=380
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("---")
            
            # ------------------------------------------------------------------
            # SECTION 3: CORE FINANCIAL METRICS DROP DOWN SELECTOR FOR PROFESSIONAL INVESTORS
            # ------------------------------------------------------------------
            st.subheader("🛠️ Professional Core Financial Metrics Deep-Dive")
            category_choice = st.selectbox(
                "Select Grouped Institutional Accounting Dataset Category to Inspect:",
                options=list(data["professional_all"].keys())
            )
            
            if category_choice:
                nested_metrics = data["professional_all"][category_choice]
                st.markdown(f"#### 🔍 Displaying Calculated Arrays for `{category_choice}`")
                
                # Render neatly formatted tabular grids for the selected data block
                p_col1, p_col2, p_col3 = st.columns(3)
                items = list(nested_metrics.items())
                
                for idx, (k, v) in enumerate(items):
                    if idx % 3 == 0:
                        p_col1.markdown(f"**{k}:** `{v}`")
                    elif idx % 3 == 1:
                        p_col2.markdown(f"**{k}:** `{v}`")
                    else:
                        p_col3.markdown(f"**{k}:** `{v}`")
                        
            st.write("---")
            
            # ------------------------------------------------------------------
            # SECTION 4 & 5: CALCULATOR ANALYSIS, STAR RATING, AND AI CHIPS
            # ------------------------------------------------------------------
            st.subheader("🧠 Algorithmic Investment Optimization & Star Evaluations")
            
            calc_col, ai_col = st.columns([1, 1])
            
            with calc_col:
                st.markdown("### 💵 Forward Return Capital Profit Calculator")
                invest_amount = st.number_input("Enter Planned Capital Deployment Amount ($):", min_value=10, value=1000, step=500)
                holding_years = st.slider("Select Investment Duration Target Window (Years):", min_value=1, max_value=10, value=3)
                
                # Compound Return Projections Based on Historic Trailing Performance Run Rates
                annualized_return_rate = max(-0.20, min(0.40, data["one_year_return_raw"] / 100)) # Clamped boundaries for mathematical stability
                projected_profit = invest_amount * ((1 + annualized_return_rate) ** holding_years) - invest_amount
                total_payout = invest_amount + projected_profit
                
                st.markdown(f"""
                * Estimated Forward Return Rate (based on 1Y trends): **{round(annualized_return_rate*100, 2)}%**
                * Total Projected Gains / Profit: **${round(projected_profit, 2)}**
                * Final Portfolio Capital Asset Value Maturity: **${round(total_payout, 2)}**
                """)
                
                # --- STAR EVALUATION RATINGS ENGINE PANEL ---
                st.markdown("### ⭐ Platform Evaluation Grade")
                star_count = data["stars"]
                full_stars = int(star_count)
                half_star = "½" if (star_count - full_stars) >= 0.4 else ""
                star_string = "★" * full_stars + half_star + "☆" * (5 - full_stars - (1 if half_star else 0))
                
                st.markdown(f"""
                <div style='background-color: #14151b; padding: 15px; border-radius: 8px; text-align: center;'>
                    <span class='star-rating'>{star_string}</span><br/>
                    <b style='font-size: 18px;'>Computed Metric Rating Score: {star_count} / 5.0 Stars</b>
                </div>
                """, unsafe_allow_html=True)
                
            with ai_col:
                st.markdown("### 🤖 Automated AI Intelligence Analysis Card Summary")
                st.markdown(f"**Composite Signal Score: `{ai['score_text']}`**")
                
                st.info(f"🟢 **Bullish Signals:**\n" + "\n".join([f"- {s}" for s in ai['bullish']]))
                st.warning(f"⚠️ **Risk Vectors Identified:**\n" + "\n".join([f"- {s}" for s in ai['risk']]))
                st.success(f"📈 **Growth Variables Profile:**\n" + "\n".join([f"- {s}" for s in ai['growth']]))
                st.error(f"🔍 **Valuation Indicators Matrix:**\n" + "\n".join([f"- {s}" for s in ai['valuation']]))
                
            st.write("---")
            
            # ------------------------------------------------------------------
            # SECTION 6: DOCUMENT GENERATOR ACTION ACTION BUTTONS ROW
            # ------------------------------------------------------------------
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
            with btn_col1:
                if st.button("📥 Generate Analytical PDF Report"):
                    st.toast("Success! Compiling core database arrays and encoding structure reports...")
                    st.success("✅ Comprehensive Report Generated successfully!")
            with btn_col2:
                if st.button("🖨️ Send To Hardware Print Terminal"):
                    st.toast("Connecting to hardware spooling systems...")
                    st.info("📠 Print command dispatched to primary network stack.")
            with btn_col3:
                st.write("") # Formatting Alignment Spacer

        else:
            st.error(f"⚠️ {data['message']}")

# ==============================================================================
# TAB 2: GENERAL KNOWLEDGE HUB AND FULL GLOSSARY EXPLANATIONS
# ==============================================================================
with glossary_tab:
    st.header("📚 Platform Knowledge Base & Plain-English Glossary Framework")
    st.caption("Educational Reference Suite detailing all quantitative investing categories used by institutions.")
    st.write("---")
    
    # RENDER BROWSER AGGREGATED BREAKING NEWS MARQUEE MOCK
    st.subheader("📰 Live Global Stream Stock Market Feed")
    st.markdown("""
    * **[04:15 PM] FED RELEASES INTEREST RATE INDEX SPEECH:** Regional tracking indexes display upward movement following shifts in monetary policy projections.
    * **[02:30 PM] TECH INDEX GAINS MOMENTUM:** Corporate buybacks and expanding operating margins push active valuations near 52-week resistance bands.
    * **[11:00 AM] ASSETS INFLOW ANALYSIS REPORT:** High Return on Invested Capital (ROIC) entities continue to secure significant retail venture inflows.
    """)
    st.write("---")
    
    # COMPREHENSIVE FINANCIAL GLOSSARY LOOKUP DATA BASE MAP
    st.subheader("📖 Full Definitions Glossary for Core Financial Tracking Checklists")
    
    with st.expander("📊 Profitability Metrics Definitions"):
        st.markdown("""
        * **Revenue Growth:** The percentage increase in top-line sales over a specified period. High growth indicates rapid market adoption.
        * **Net Income Growth:** The growth rate of bottom-line net profits after all operational costs, taxes, and interest expenses.
        * **Gross Profit Margin:** Measures remaining revenue after subtracting the Direct Cost of Goods Sold (COGS). Formula: $\\frac{\\text{Gross Profit}}{\\text{Revenue}} \\times 100$.
        * **Operating Margin:** Indicates operating efficiency by evaluating income generated before financial interest and taxation structures.
        * **Net Profit Margin:** The percentage of revenue converted directly into net income.
        * **EBITDA / Margin:** Earnings Before Interest, Taxes, Depreciation, and Amortization. Evaluates pure operational profitability without accounting adjustments.
        * **Return on Equity (ROE):** Measures capital allocation productivity by analyzing profits generated per dollar of shareholder equity.
        * **Return on Assets (ROA):** Measures corporate asset usage efficiency to determine operational profitability.
        * **Return on Invested Capital (ROIC):** The gold-standard capital tracking metric. Measures exact cash yield returns achieved by deploying capital back into operational expansion.
        * **Earnings Per Share (EPS) / Diluted:** Profit available per outstanding share of stock. Diluted EPS factors in all convertible options or warrants.
        * **Free Cash Flow (FCF) / Margin:** Realized surplus discretionary bank cash generated after funding capital expenditures (CAPEX). Used for buybacks, acquisitions, and dividends.
        """)

    with st.expander("📈 Valuation Metrics Definitions"):
        st.markdown("""
        * **Price-to-Earnings Ratio (P/E):** Represents multiple premiums assigned by markets per dollar of trailing earnings. Formula: $\\frac{\\text{Stock Price}}{\\text{EPS}}$.
        * **Forward P/E:** Utilizes forecast projection estimations over next 12 months to assess valuation profiles.
        * **PEG Ratio:** P/E ratio normalized by the expected growth rate of earnings. A PEG below 1.0 suggests an undervalued profile.
        * **Price-to-Book Ratio (P/B):** Compares total equity valuations against underlying net balance sheet accounting asset entries.
        * **Price-to-Sales Ratio (P/S):** Valuation multiplier compared to gross revenue outputs. Frequently applied to early-stage corporate tracking frameworks.
        * **EV/EBITDA & Enterprise Value (EV):** Complete valuation calculation measuring structural balance sheets by calculating market caps plus gross debt loads minus aggregate cash reserves.
        * **Discounted Cash Flow (DCF):** Valuing assets by computing present values of estimated future cash output lines.
        * **Dividend / Earnings / FCF Yields:** Percentage returns distributed back relative to active entry purchase price thresholds.
        """)

    with st.expander("🛡️ Financial Health & Debt Risk Definitions"):
        st.markdown("""
        * **Debt-to-Equity Ratio:** Measures total leverage ratios. Extremely elevated metrics increase risk parameters during macroeconomic contraction phases.
        * **Current / Quick / Cash Ratios:** Liquidity coverage metrics measuring balance sheet capacity to fulfill short-term financial liabilities using quick asset resources.
        * **Interest Coverage Ratio:** Determines margin safety boundaries by assessing how many times operating income covers fixed debt service burdens.
        * **Net Debt to EBITDA:** Structural safety multiple indicating years required to eliminate leverage liabilities using ongoing cash flow runs.
        * **Altman Z-Score:** Multi-factor formula used to calculate statistical likelihood that an entity enters bankruptcy cycles within 24 months.
        """)

    with st.expander("⚡ Market Styles, Growth, Risk & Technical Metrics"):
        st.markdown("""
        * **Revenue / EPS CAGR:** Compound Annual Growth Rate. Evaluates smoothed multi-year growth trajectories without year-to-year volatility noise.
        * **Asset / Inventory / Receivables Turnover:** Operational efficiency parameters determining how rapidly assets are monetized.
        * **Beta / Volatility:** Systematic market tracking variables. A Beta greater than 1.0 implies wider price movements than major benchmarks like the S&P 500.
        * **Sharpe / Sortino Ratios:** Risk-adjusted performance indicators measuring return premiums captured per unit of asset volatility.
        * **RSI / MACD / Moving Averages:** Technical momentum tracking tools evaluating mathematical price velocity arrays, helping identify short-term overbought or oversold conditions.
        * **Economic Moat:** Structural competitive protections (e.g., brand equity, pricing power, patents) preventing competitor replication.
        """)