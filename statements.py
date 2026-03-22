from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class FinancialStatement:
    """Base class for financial statements"""
    ticker: str
    date: datetime
    
@dataclass
class IncomeStatement(FinancialStatement):
    # Revenue & Cost
    total_revenue: Optional[float] = None
    operating_revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    reconciled_cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    
    # Expenses
    operating_expense: Optional[float] = None
    total_expenses: Optional[float] = None
    research_and_development: Optional[float] = None
    selling_general_and_administration: Optional[float] = None
    reconciled_depreciation: Optional[float] = None # Added from yfinance list
    
    # Operating Results
    operating_income: Optional[float] = None
    total_operating_income_as_reported: Optional[float] = None
    ebitda: Optional[float] = None
    normalized_ebitda: Optional[float] = None
    ebit: Optional[float] = None
    
    # Interest & Non-Operating
    net_interest_income: Optional[float] = None
    interest_income: Optional[float] = None
    interest_expense: Optional[float] = None
    interest_income_non_operating: Optional[float] = None
    interest_expense_non_operating: Optional[float] = None
    net_non_operating_interest_income_expense: Optional[float] = None
    other_income_expense: Optional[float] = None
    other_non_operating_income_expenses: Optional[float] = None
    
    # Taxes & Net Income
    pretax_income: Optional[float] = None
    tax_provision: Optional[float] = None
    tax_rate_for_calcs: Optional[float] = None
    tax_effect_of_unusual_items: Optional[float] = None
    net_income: Optional[float] = None
    normalized_income: Optional[float] = None
    net_income_common_stockholders: Optional[float] = None
    net_income_including_noncontrolling_interests: Optional[float] = None
    net_income_continuous_operations: Optional[float] = None
    net_income_from_continuing_operation_net_minority_interest: Optional[float] = None
    net_income_from_continuing_and_discontinued_operation: Optional[float] = None
    
    # Per Share Metrics
    basic_eps: Optional[float] = None
    diluted_eps: Optional[float] = None
    basic_average_shares: Optional[float] = None
    diluted_average_shares: Optional[float] = None
    diluted_ni_availto_com_stockholders: Optional[float] = None

@dataclass
class BalanceSheet(FinancialStatement):
    # Assets - Current
    current_assets: Optional[float] = None
    cash_financial: Optional[float] = None
    cash_equivalents: Optional[float] = None
    cash_and_cash_equivalents: Optional[float] = None
    other_short_term_investments: Optional[float] = None
    cash_cash_equivalents_and_short_term_investments: Optional[float] = None
    accounts_receivable: Optional[float] = None
    other_receivables: Optional[float] = None
    receivables: Optional[float] = None
    inventory: Optional[float] = None
    other_current_assets: Optional[float] = None
    
    # Assets - Non-Current
    total_non_current_assets: Optional[float] = None
    net_ppe: Optional[float] = None
    gross_ppe: Optional[float] = None
    accumulated_depreciation: Optional[float] = None
    properties: Optional[float] = None
    land_and_improvements: Optional[float] = None
    machinery_furniture_equipment: Optional[float] = None
    other_properties: Optional[float] = None
    leases: Optional[float] = None
    investments_and_advances: Optional[float] = None
    investment_in_financial_assets: Optional[float] = None
    available_for_sale_securities: Optional[float] = None
    other_investments: Optional[float] = None
    non_current_deferred_taxes_assets: Optional[float] = None
    non_current_deferred_assets: Optional[float] = None
    other_non_current_assets: Optional[float] = None
    total_assets: Optional[float] = None

    # Liabilities - Current
    current_liabilities: Optional[float] = None 
    payables: Optional[float] = None
    accounts_payable: Optional[float] = None
    total_tax_payable: Optional[float] = None
    income_tax_payable: Optional[float] = None
    payables_and_accrued_expenses: Optional[float] = None
    current_accrued_expenses: Optional[float] = None
    current_debt: Optional[float] = None
    current_debt_and_capital_lease_obligation: Optional[float] = None
    current_capital_lease_obligation: Optional[float] = None
    other_current_borrowings: Optional[float] = None
    other_current_liabilities: Optional[float] = None # Added from yfinance list
    commercial_paper: Optional[float] = None
    current_deferred_liabilities: Optional[float] = None
    current_deferred_revenue: Optional[float] = None
    
    # Liabilities - Non-Current
    total_non_current_liabilities_net_minority_interest: Optional[float] = None
    long_term_debt: Optional[float] = None
    long_term_debt_and_capital_lease_obligation: Optional[float] = None
    long_term_capital_lease_obligation: Optional[float] = None
    other_non_current_liabilities: Optional[float] = None
    trade_and_other_payables_non_current: Optional[float] = None
    total_liabilities: Optional[float] = None 
    total_liabilities_net_minority_interest: Optional[float] = None

    # Equity
    stockholders_equity: Optional[float] = None
    total_equity_gross_minority_interest: Optional[float] = None
    common_stock_equity: Optional[float] = None
    capital_stock: Optional[float] = None
    common_stock: Optional[float] = None
    retained_earnings: Optional[float] = None
    treasury_shares_number: Optional[float] = None
    ordinary_shares_number: Optional[float] = None
    share_issued: Optional[float] = None
    gains_losses_not_affecting_retained_earnings: Optional[float] = None
    other_equity_adjustments: Optional[float] = None

    # Financial Health Indicators
    net_debt: Optional[float] = None
    total_debt: Optional[float] = None
    tangible_book_value: Optional[float] = None
    invested_capital: Optional[float] = None
    working_capital: Optional[float] = None
    net_tangible_assets: Optional[float] = None
    capital_lease_obligations: Optional[float] = None
    total_capitalization: Optional[float] = None

@dataclass
class CashFlowStatement(FinancialStatement):
    # Operating Activities
    operating_cash_flow: Optional[float] = None
    cash_flow_from_continuing_operating_activities: Optional[float] = None
    net_income_from_continuing_operations: Optional[float] = None
    depreciation_amortization_depletion: Optional[float] = None
    depreciation_and_amortization: Optional[float] = None
    deferred_tax: Optional[float] = None
    deferred_income_tax: Optional[float] = None
    stock_based_compensation: Optional[float] = None
    other_non_cash_items: Optional[float] = None
    
    # Changes in Working Capital
    change_in_working_capital: Optional[float] = None
    change_in_inventory: Optional[float] = None
    change_in_receivables: Optional[float] = None
    changes_in_account_receivables: Optional[float] = None
    change_in_account_payable: Optional[float] = None
    change_in_payables: Optional[float] = None
    change_in_payables_and_accrued_expense: Optional[float] = None
    change_in_other_current_assets: Optional[float] = None
    change_in_other_current_liabilities: Optional[float] = None
    change_in_other_working_capital: Optional[float] = None

    # Investing Activities
    investing_cash_flow: Optional[float] = None
    cash_flow_from_continuing_investing_activities: Optional[float] = None
    capital_expenditure: Optional[float] = None
    purchase_of_ppe: Optional[float] = None
    net_ppe_purchase_and_sale: Optional[float] = None
    purchase_of_business: Optional[float] = None
    net_business_purchase_and_sale: Optional[float] = None
    purchase_of_investment: Optional[float] = None
    sale_of_investment: Optional[float] = None
    net_investment_purchase_and_sale: Optional[float] = None
    net_other_investing_changes: Optional[float] = None

    # Financing Activities
    financing_cash_flow: Optional[float] = None
    cash_flow_from_continuing_financing_activities: Optional[float] = None
    issuance_of_capital_stock: Optional[float] = None
    repurchase_of_capital_stock: Optional[float] = None
    net_common_stock_issuance: Optional[float] = None
    common_stock_issuance: Optional[float] = None
    common_stock_payments: Optional[float] = None
    cash_dividends_paid: Optional[float] = None
    common_stock_dividend_paid: Optional[float] = None
    issuance_of_debt: Optional[float] = None
    repayment_of_debt: Optional[float] = None
    net_issuance_payments_of_debt: Optional[float] = None
    net_long_term_debt_issuance: Optional[float] = None
    long_term_debt_issuance: Optional[float] = None
    long_term_debt_payments: Optional[float] = None
    net_short_term_debt_issuance: Optional[float] = None
    net_other_financing_charges: Optional[float] = None

    # Summary and Supplemental
    free_cash_flow: Optional[float] = None
    changes_in_cash: Optional[float] = None
    beginning_cash_position: Optional[float] = None
    end_cash_position: Optional[float] = None
    interest_paid_supplemental_data: Optional[float] = None
    income_tax_paid_supplemental_data: Optional[float] = None