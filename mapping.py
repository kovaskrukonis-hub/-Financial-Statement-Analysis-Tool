INCOME_MAPPING = {
    # Revenue & Cost
    "total_revenue": "Total Revenue",
    "operating_revenue": "Operating Revenue",
    "cost_of_revenue": "Cost Of Revenue",
    "reconciled_cost_of_revenue": "Reconciled Cost Of Revenue",
    "gross_profit": "Gross Profit",
    
    # Operating Expenses
    "operating_expense": "Operating Expense",
    "total_expenses": "Total Expenses",
    "research_and_development": "Research And Development",
    "selling_general_and_administration": "Selling General And Administration",
    
    # Operating Income & EBITDA
    "operating_income": "Operating Income",
    "total_operating_income_as_reported": "Total Operating Income As Reported",
    "ebitda": "EBITDA",
    "normalized_ebitda": "Normalized EBITDA",
    "ebit": "EBIT",
    
    # Interest & Non-Operating
    "net_interest_income": "Net Interest Income",
    "interest_income": "Interest Income",
    "interest_expense": "Interest Expense",
    "interest_income_non_operating": "Interest Income Non Operating",
    "interest_expense_non_operating": "Interest Expense Non Operating",
    "net_non_operating_interest_income_expense": "Net Non Operating Interest Income Expense",
    "other_income_expense": "Other Income Expense",
    "other_non_operating_income_expenses": "Other Non Operating Income Expenses",
    
    # Taxes & Net Income
    "pretax_income": "Pretax Income",
    "tax_provision": "Tax Provision",
    "tax_rate_for_calcs": "Tax Rate For Calcs",
    "tax_effect_of_unusual_items": "Tax Effect Of Unusual Items",
    "net_income": "Net Income",
    "normalized_income": "Normalized Income",
    "net_income_common_stockholders": "Net Income Common Stockholders",
    "net_income_including_noncontrolling_interests": "Net Income Including Noncontrolling Interests",
    "net_income_continuous_operations": "Net Income Continuous Operations",
    "net_income_from_continuing_operation_net_minority_interest": "Net Income From Continuing Operation Net Minority Interest",
    "net_income_from_continuing_and_discontinued_operation": "Net Income From Continuing And Discontinued Operation",
    
    # Added from your available fields
    "reconciled_depreciation": "Reconciled Depreciation",
    
    # Per Share Metrics
    "basic_eps": "Basic EPS",
    "diluted_eps": "Diluted EPS",
    "basic_average_shares": "Basic Average Shares",
    "diluted_average_shares": "Diluted Average Shares",
    "diluted_ni_availto_com_stockholders": "Diluted NI Availto Com Stockholders"
}
BALANCE_SHEET_MAPPING = {
    # Assets
    "total_assets": "Total Assets",
    "current_assets": "Current Assets",
    "cash_and_cash_equivalents": "Cash And Cash Equivalents",
    "cash_cash_equivalents_and_short_term_investments": "Cash Cash Equivalents And Short Term Investments",
    "inventory": "Inventory",
    "accounts_receivable": "Accounts Receivable",
    "receivables": "Receivables", 
    "net_ppe": "Net PPE",
    "gross_ppe": "Gross PPE",
    "accumulated_depreciation": "Accumulated Depreciation",
    "cash_financial": "Cash Financial",
    
    # Liabilities
    # Note: "Total Liabilities" was deleted as it's missing from your terminal output
    "total_liabilities_net_minority_interest": "Total Liabilities Net Minority Interest",
    "current_liabilities": "Current Liabilities",
    "accounts_payable": "Accounts Payable",
    "total_tax_payable": "Total Tax Payable",
    "long_term_debt": "Long Term Debt",
    "current_debt": "Current Debt", 
    "trade_and_other_payables_non_current": "Tradeand Other Payables Non Current",
    "other_current_liabilities": "Other Current Liabilities",
    
    # Equity
    "stockholders_equity": "Stockholders Equity",
    "retained_earnings": "Retained Earnings",
    "common_stock": "Common Stock",
    "ordinary_shares_number": "Ordinary Shares Number",
    "tangible_book_value": "Tangible Book Value",
    
    # Calculated Totals
    "net_debt": "Net Debt",
    "total_debt": "Total Debt",
    "working_capital": "Working Capital",
    "invested_capital": "Invested Capital"
}
CASH_FLOW_MAPPING = {
    "operating_cash_flow": "Operating Cash Flow",
    "investing_cash_flow": "Investing Cash Flow",
    "financing_cash_flow": "Financing Cash Flow",
    "free_cash_flow": "Free Cash Flow",
    "capital_expenditure": "Capital Expenditure",
    "depreciation_and_amortization": "Depreciation And Amortization",
    "stock_based_compensation": "Stock Based Compensation",
    "cash_dividends_paid": "Cash Dividends Paid",
    "repurchase_of_capital_stock": "Repurchase Of Capital Stock",
    "issuance_of_debt": "Issuance Of Debt",
    "repayment_of_debt": "Repayment Of Debt",
    "end_cash_position": "End Cash Position",
    "beginning_cash_position": "Beginning Cash Position",
    "changes_in_cash": "Changes In Cash",
    "purchase_of_ppe": "Purchase Of PPE", 
    "purchase_of_investment": "Purchase Of Investment" 
}