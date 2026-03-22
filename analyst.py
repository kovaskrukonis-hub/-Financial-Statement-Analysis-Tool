import yfinance as yf

class FinancialAnalyst:
    
    @staticmethod
    def inventory_turnover_year(income_statements, balance_sheets):
        if len(balance_sheets) < 2:
            return None
            
        cogs = income_statements[0].cost_of_revenue
        current_inv = balance_sheets[0].inventory
        prev_inv = balance_sheets[1].inventory
        
        if cogs is not None and current_inv is not None and prev_inv is not None:
            avg_inventory = (current_inv + prev_inv) / 2
            if avg_inventory == 0:
                return None
            return cogs / avg_inventory
        return None
    
    @staticmethod
    def inventory_turnover_days(income_statements, balance_sheets):
        turnover = FinancialAnalyst.inventory_turnover_year(income_statements, balance_sheets)
        if turnover is not None and turnover > 0:
            return 365 / turnover
        return None
    
    @staticmethod
    def receivables_turnover(income_statements, balance_sheets):
        if len(balance_sheets) < 2:
            return None

        sales = income_statements[0].total_revenue
        ar_current = balance_sheets[0].accounts_receivable
        ar_previous = balance_sheets[1].accounts_receivable
        
        if sales is not None and ar_current is not None and ar_previous is not None:
            avg_ar = (ar_current + ar_previous) / 2
            if avg_ar == 0:
                return None
            return sales / avg_ar
        return None
    
    @staticmethod
    def average_collection_period(income_statements, balance_sheets):
        rt = FinancialAnalyst.receivables_turnover(income_statements, balance_sheets)
        if rt is not None and rt != 0:
            return 365 / rt
        return None
    
    @staticmethod
    def payables_turnover(income_statements, balance_sheets):
        if len(balance_sheets) < 2:
            return None
            
        cogs = income_statements[0].cost_of_revenue
        ending_inventory = balance_sheets[0].inventory
        beginning_inventory = balance_sheets[1].inventory
        ending_ap = balance_sheets[0].accounts_payable
        beginning_ap = balance_sheets[1].accounts_payable

        if all(i is not None for i in [cogs, ending_inventory, beginning_inventory, ending_ap, beginning_ap]):
            purchases = cogs + (ending_inventory - beginning_inventory)
            avg_accounts_payable = (ending_ap + beginning_ap) / 2
            
            if avg_accounts_payable == 0:
                return None 
            return purchases / avg_accounts_payable
        return None 

    @staticmethod
    def average_payment_period(income_statements, balance_sheets):
        payables_turnover = FinancialAnalyst.payables_turnover(income_statements, balance_sheets)
        if payables_turnover is not None and payables_turnover != 0:
            return 365 / payables_turnover
        return None

    @staticmethod    
    def total_asset_turnover(income_statements, balance_sheets):
        if len(balance_sheets) < 2:
            return None
        
        sales = income_statements[0].total_revenue
        curr_assets = balance_sheets[0].total_assets
        prev_assets = balance_sheets[1].total_assets

        if sales is not None and curr_assets is not None and prev_assets is not None:
            average_assets = (curr_assets + prev_assets) / 2
            if average_assets == 0:
                return None
            return sales / average_assets
        return None

    @staticmethod
    def gross_profit_margin(income_statements):
        latest = income_statements[0]
        if latest.gross_profit is not None and latest.total_revenue is not None and latest.total_revenue != 0:
            return (latest.gross_profit / latest.total_revenue)*100
        return None
        
    @staticmethod
    def operating_margin(income_statements):
        latest = income_statements[0]
        if latest.operating_income is not None and latest.total_revenue is not None and latest.total_revenue != 0:
            return (latest.operating_income / latest.total_revenue)*100
        return None
    
    @staticmethod
    def return_on_assets(income_statements, balance_sheets):
        if len(balance_sheets) < 2:
            return None
        
        net_income = income_statements[0].net_income
        total_assets_current = balance_sheets[0].total_assets
        total_assets_previous = balance_sheets[1].total_assets
    
        if net_income is not None and total_assets_current is not None and total_assets_previous is not None:
            avg_assets = (total_assets_current + total_assets_previous) / 2
            if avg_assets == 0:
                return None
            return (net_income / avg_assets)*100
        return None
    
    @staticmethod
    def return_on_equity(income_statements, balance_sheets):
        if len(balance_sheets) < 2:
            return None
            
        net_income = income_statements[0].net_income
        ending_equity = balance_sheets[0].stockholders_equity
        start_equity = balance_sheets[1].stockholders_equity

        if net_income is not None and ending_equity is not None and start_equity is not None:
            avg_equity = (start_equity + ending_equity) / 2
            if avg_equity == 0:
                return None
            return (net_income / avg_equity)*100
        return None
    
    @staticmethod
    def current_ratio(balance_sheets):
        current_assets = balance_sheets[0].current_assets
        current_liabilities = balance_sheets[0].current_liabilities

        if current_assets is not None and current_liabilities is not None and current_liabilities != 0:
            return current_assets / current_liabilities
        return None
    
    @staticmethod
    def quick_ratio(balance_list):
        current_assets = balance_list[0].current_assets
        inventory = balance_list[0].inventory
        current_liabilities = balance_list[0].current_liabilities

        if current_assets is None or current_liabilities is None or current_liabilities == 0:
            return None
    
        if inventory is None:
            inventory = 0
        
        return (current_assets - inventory) / current_liabilities
    
    @staticmethod
    def cash_ratio(balance_sheets):
        cash = balance_sheets[0].cash_cash_equivalents_and_short_term_investments  
        current_liabilities = balance_sheets[0].current_liabilities

        if cash is not None and current_liabilities is not None and current_liabilities > 0:
            return cash / current_liabilities
        return None
    
    @staticmethod
    def debt_to_assets(balance_sheets):
        if not balance_sheets:
            return None
        
        latest = balance_sheets[0]
        assets = latest.total_assets

        if latest.total_liabilities is not None:
            liabilities = latest.total_liabilities
        elif latest.total_liabilities_net_minority_interest is not None:
            liabilities = latest.total_liabilities_net_minority_interest
        else:
            liabilities = None

        if assets is not None and liabilities is not None and assets != 0:
            return (liabilities / assets)*100
        
        return None
    
    @staticmethod
    def interest_coverage_smart(income_statement):
        if not income_statement:
            return None
        
        ebit = income_statement[0].ebit
        interest = income_statement[0].interest_expense

        if ebit is not None and interest is not None and interest != 0:
            return ebit / abs(interest)
            
        return None

    @staticmethod
    def price_to_earnings(current_price, income_statements):
        if income_statements is None or current_price is None:
            return None

        latest = income_statements[0]
        eps = latest.basic_eps

        if eps is not None and eps != 0:
            return current_price / eps
        return None
    
    @staticmethod    
    def eps(income_statements):
        if income_statements[0].basic_eps is not None:
            return income_statements[0].basic_eps
        return None

    @staticmethod
    def dividend_payout_ratio(ticker_symbol, income_statements):
        if not income_statements:
            return None
        
        eps = income_statements[0].basic_eps
        
        if eps is None or eps <= 0:
            return None
        
        try:
            import pandas as pd
            ticker = yf.Ticker(ticker_symbol)
            div_history = ticker.dividends
            
            if div_history.empty:
                return 0.0
            
            one_year_ago = pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=1)
            last_year_divs = div_history[div_history.index >= one_year_ago].sum()
            
            if last_year_divs == 0:
                return 0.0
            
            return (last_year_divs / eps) * 100
            
        except Exception:
            return None