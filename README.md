# Stock Analyzer Terminal

A Python command-line tool that performs fundamental financial analysis and intrinsic valuation of publicly traded stocks using real-time data from Yahoo Finance.

Enter any ticker symbol and the tool computes 19 financial ratios across liquidity, profitability, and efficiency categories, runs a full Discounted Cash Flow (DCF) valuation, and produces a weighted investment scorecard with a buy/hold/sell verdict.

---

<img width="698" height="580" alt="image" src="https://github.com/user-attachments/assets/31754b95-46f7-40a5-a411-86879348c857" />
<img width="701" height="668" alt="image" src="https://github.com/user-attachments/assets/c531bf2c-bee7-4d19-bb3c-e8281047ec27" />

---

## Installation

**Requirements:** Python 3.9+

```bash
git clone https://github.com/kovaskrukonis-hub/Financial-Stetement-Analysis-Tool.git
cd stock-analyzer
pip install -r requirements.txt
python main.py
```



---

## Features

**19 financial ratios** computed from annual statements, color-coded against industry benchmarks:

- Valuation: P/E ratio, EPS, dividend payout ratio
- Profitability: gross profit margin, operating margin, ROA, ROE
- Liquidity: current ratio, quick ratio, cash ratio
- Solvency: debt-to-assets, interest coverage
- Efficiency: inventory turnover, receivables turnover, payables turnover, average collection/payment period, total asset turnover

**DCF valuation** — a separate, standalone theoretical estimate of intrinsic value per share with margin of safety vs. current market price. See methodology and limitations below.

**Investment scorecard** — weighted composite score (0–100) with a final verdict: Strong Buy → Buy → Hold → Weak → Avoid. The DCF margin of safety contributes partially to this score (see Scorecard section below).

---

## Project Structure

```
main.py              # Entry point and display logic
analyst.py           # 19 ratio calculations
DCF_calculation.py   # FCF projection, WACC, terminal value, equity value
valuation_score.py   # Scoring and verdict
factory.py           # Parses Yahoo Finance DataFrames into typed objects
statements.py        # Dataclasses for income statement, balance sheet, cash flow
mapping.py           # Field name mappings from Yahoo Finance
price.py             # Live price fetch
```

---

## Methodology

### Financial Ratios

Each ratio is benchmarked against standard thresholds and assigned a color:

| Color  | Meaning |
|--------|---------|
| Green  | Strong  |
| Yellow | Average |
| Red    | Risky / Negative |

Ratios requiring two consecutive balance sheets (e.g. average inventory, average receivables) use the two most recent annual periods.

---

### DCF Valuation

**1. Base FCF**
Taken from the most recent annual cash flow statement: `operating cash flow + capex` (capex is negative in Yahoo Finance data, making this equivalent to subtraction).

**2. Historical growth rate**
FCF CAGR over all available annual periods, capped to [−10%, +50%]. Falls back to revenue CAGR if FCF history is insufficient, then to a 5% default.

**3. Growth projection — blended linear decay**
Rather than projecting all 5 years at the raw historical growth rate — which often produces unrealistic results given how volatile FCF can be over a short historical window — the model blends the historical rate with the 2.5% terminal rate. The blend shifts linearly each year:

```
weight     = (5 − year) / 5
year_growth = (historical × weight) + (2.5% × (1 − weight))
```

This means the model never fully applies the historical rate — year 1 already blends in 20% terminal weight — and by year 5 the growth rate equals exactly 2.5%:

| Year | Historical weight | Terminal weight | Effective rate (example: 20% historical) |
|------|-------------------|-----------------|------------------------------------------|
| 1    | 80%               | 20%             | 16.5%                                    |
| 2    | 60%               | 40%             | 13.0%                                    |
| 3    | 40%               | 60%             | 9.5%                                     |
| 4    | 20%               | 80%             | 6.0%                                     |
| 5    | 0%                | 100%            | 2.5%                                     |

The `growth_rate_used` shown in the output is the simple average of these five blended rates.

**4. WACC**
- Cost of equity: CAPM using live beta and 10-year treasury yield as the risk-free rate, with 10% as the long-run market return
- Cost of debt: `|interest expense| / total debt`, after tax
- Weights: market cap and total debt

**5. Terminal value**
Gordon Growth Model applied to the year-5 FCF: `FCF₅ × (1 + 2.5%) / (WACC − 2.5%)`, discounted back 5 years.

**6. Equity value**
`(enterprise value − net debt) / shares outstanding`

---

### Investment Scorecard

Each metric scores 0, 1, or 2 points based on threshold bands. Scores are aggregated within three categories scaled to 0–10, then combined into a final 0–100 score:

| Category             | Weight |
|----------------------|--------|
| Valuation            | 35%    |
| Profitability        | 30%    |
| Solvency/Efficiency  | 35%    |

The DCF margin of safety is one of three inputs to the Valuation category (alongside P/E and EPS), so it partially influences the final score. However the scorecard is predominantly driven by accounting ratios from the financial statements, which are more grounded than the DCF estimate.

Metrics with no available data are excluded and weights redistribute proportionally.

---

## Limitations

- Data sourced from Yahoo Finance — subject to its availability and accuracy
- Some companies report financial statements with non-standard or missing fields; affected ratios will show N/A
- Based on annual statements; intra-year events may not be reflected
- Financial companies (banks, insurers) use different accounting sta
