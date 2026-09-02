"""
fetch_diageo_data.py

Pulls Diageo's key financials and market data from Yahoo Finance (via yfinance)
to refresh the assumptions in diageo_dcf_model.xlsx.

Run locally (requires an internet connection):
    pip install yfinance pandas
    python fetch_diageo_data.py

Diageo is dual-listed: DGE.L (London, ordinary shares, priced in pence) and
DEO (New York, ADR; 1 ADR = 4 ordinary shares). Diageo reports its financial
statements in USD, so this script pulls the DEO (NYSE) line for consistency
with the cash flow figures used in the model.
"""

import yfinance as yf
import pandas as pd

TICKER = "DEO"


def main():
    stock = yf.Ticker(TICKER)
    info = stock.info

    print("=== Market data ===")
    print(f"Current price (USD):      {info.get('currentPrice')}")
    print(f"Market cap (USD):         {info.get('marketCap'):,}")
    print(f"Shares outstanding (ADR): {info.get('sharesOutstanding'):,}")
    print(f"Beta (5Y monthly):        {info.get('beta')}")
    print(f"Trailing P/E:             {info.get('trailingPE')}")

    print("\n=== Annual financials (most recent FY, USD) ===")
    financials = stock.financials
    cashflow = stock.cashflow
    balance_sheet = stock.balance_sheet

    latest_col = financials.columns[0]
    revenue = financials.loc["Total Revenue", latest_col]
    ebit = financials.loc["Operating Income", latest_col]
    print(f"Revenue:                  {revenue:,.0f}")
    print(f"Operating income (EBIT):  {ebit:,.0f}")
    print(f"Operating margin:         {ebit / revenue:.1%}")

    latest_cf_col = cashflow.columns[0]
    capex = cashflow.loc["Capital Expenditure", latest_cf_col]
    op_cf = cashflow.loc["Operating Cash Flow", latest_cf_col]
    fcf = op_cf + capex  # capex is stored as a negative number
    print(f"Operating cash flow:      {op_cf:,.0f}")
    print(f"Capital expenditure:      {capex:,.0f}")
    print(f"Free cash flow:           {fcf:,.0f}")

    latest_bs_col = balance_sheet.columns[0]
    total_debt = balance_sheet.loc["Total Debt", latest_bs_col]
    cash = balance_sheet.loc["Cash And Cash Equivalents", latest_bs_col]
    net_debt = total_debt - cash
    print(f"Total debt:                {total_debt:,.0f}")
    print(f"Cash & equivalents:        {cash:,.0f}")
    print(f"Net debt:                  {net_debt:,.0f}")

    # Save a clean summary the spreadsheet's Assumptions tab can be updated from
    summary = pd.DataFrame({
        "metric": ["price", "market_cap", "shares_out_adr", "beta",
                   "revenue", "ebit", "op_margin", "capex",
                   "op_cash_flow", "free_cash_flow", "total_debt",
                   "cash", "net_debt"],
        "value": [info.get("currentPrice"), info.get("marketCap"),
                  info.get("sharesOutstanding"), info.get("beta"),
                  revenue, ebit, ebit / revenue, capex,
                  op_cf, fcf, total_debt, cash, net_debt],
    })
    summary.to_csv("diageo_live_data.csv", index=False)
    print("\nSaved diageo_live_data.csv — use these to refresh the blue input "
          "cells in the Assumptions tab of diageo_dcf_model.xlsx")


if __name__ == "__main__":
    main()
