# Diageo DCF Valuation

A discounted cash flow valuation of Diageo plc (LSE: DGE / NYSE: DEO), built to independently estimate
whether the market is currently over- or under-valuing the stock, and to cross-check that estimate against
Wall Street consensus.

## Overview

- 5-year unlevered free cash flow forecast, discounted at a bottom-up WACC
- Terminal value via the Gordon Growth method
- Full WACC build-up (CAPM cost of equity, after-tax cost of debt, market-value capital structure weights)
- Two-way sensitivity table (implied value per share vs. WACC and terminal growth rate)
- A Python script (`fetch_diageo_data.py`, via `yfinance`) to pull live market data and refresh the model's
  inputs

## Files

| File | Description |
|---|---|
| `diageo_dcf_model.xlsx` | The model — Assumptions, DCF forecast, and Sensitivity tabs |
| `fetch_diageo_data.py` | Pulls current price, market cap, beta, revenue, FCF, and net debt from Yahoo Finance |

## Methodology

Diageo reports its financial statements in USD despite its primary LSE listing, so the whole model is built
in USD for consistency between the forecast cash flows and the market data.

**Forecast:** Revenue is grown at a tapering rate (2.5% → 2.0% over 5 years, roughly in line with FY26
organic sales growth guidance), then converted to unlevered free cash flow via a normalised EBIT margin,
tax, D&A, capex, and a working capital adjustment — each as a percentage of revenue.

**Discount rate:** WACC is built bottom-up — cost of equity via CAPM (US 10-year Treasury as the risk-free
rate, a market equity risk premium, and Diageo's beta), and an after-tax cost of debt, weighted by the
market values of equity and net debt.

**Terminal value:** Gordon Growth on the Year 5 free cash flow, discounted back to the present alongside the
five explicit forecast years.

Every hardcoded input in the Assumptions tab is colour-coded (blue) and sourced in an adjacent note — see
the tab itself for exact citations (Diageo's FY25 Preliminary Results, its FY25 Form 20-F, and current
market data).

## Key assumptions worth interrogating

- **Normalised EBIT margin (23%)** sits between Diageo's FY25 reported margin (21.4%) and its organic/underlying
  margin (28.0%), reflecting the phased-in savings from Diageo's "Accelerate" cost programme. This is the single
  largest driver of the valuation — see the Sensitivity tab for how the output moves if this proves too
  optimistic.
- **Beta (0.65)** blends two disagreeing sourced estimates (a recent 5-year beta of 0.30 and an older estimate
  of 0.76) rather than relying on either alone.
- **Working capital (0.5% of revenue)** is an unsourced simplifying assumption, not pulled from a filing.

## Results

The model implies a fair value of **~$27.94 per ordinary share** (USD-equivalent), against a current price of
~$22.52 — roughly 24% upside. This is corroborated by Wall Street's own 12-month consensus price targets
for the DEO ADR (~$106-129 in Aug 2026), which imply ~$26.50-$32.25 per ordinary share equivalent once
divided by the 4:1 ADR ratio — bracketing this model's independent output.

## Usage

```bash
pip install yfinance pandas
python fetch_diageo_data.py
```

This prints Diageo's current price, market cap, beta, revenue, FCF, and net debt, and saves them to
`diageo_live_data.csv` — use these to refresh the blue input cells in the Assumptions tab.

## Disclaimer

Built as a personal/educational project. Not investment advice — all figures are estimates built on
simplifying assumptions, several of which are flagged above as unsourced or contestable.
