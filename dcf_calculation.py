import yfinance as yf

class DCF_Analyst:

    @staticmethod
    def fcf_list(cashflow_statement):
        if len(cashflow_statement) == 0:
            return None
        fcf_history = []

        for period in cashflow_statement:
            operating_cash_flows = period.operating_cash_flow
            capex = period.capital_expenditure
            
            if operating_cash_flows is not None:
                if capex is not None:
                    fcf_history.append(operating_cash_flows + capex)
                else:
                    fcf_history.append(operating_cash_flows)
            else:
                fcf_history.append(None)

        return fcf_history

    @staticmethod
    def fcf_growth_rate(cashflow_statement):
        fcf_history = DCF_Analyst.fcf_list(cashflow_statement)
        
        if fcf_history is None:
            return None

        valid_fcfs = [fcf for fcf in fcf_history if fcf is not None and fcf > 0]
        
        if len(valid_fcfs) < 2:
            return None
        
        # CAGR formula: (Most Recent / Oldest) ^ (1 / number of periods) - 1
        # fcf_history is ordered newest to oldest (how yfinance returns it)
        most_recent = valid_fcfs[0]
        oldest = valid_fcfs[-1]
        num_periods = len(valid_fcfs) - 1
        
        cagr = (most_recent / oldest) ** (1 / num_periods) - 1
        
        return cagr
    
    @staticmethod
    def wacc(income_statement, balance_sheet, ticker_symbol):

        if len(income_statement) == 0 or len(balance_sheet) == 0:
            return None
        
        # === STEP 0A: Get Risk-Free Rate (10-Year Treasury) ===
        try:
            treasury = yf.Ticker("^TNX")  # 10-Year Treasury Yield Index
            risk_free_rate = treasury.info.get('regularMarketPrice', 4.0) / 100

        except:
            risk_free_rate = 0.04
        
        try:
            
            ticker = yf.Ticker(ticker_symbol)
            beta = ticker.info.get('beta')
            if beta is None or beta <= 0:
                beta = 1.0
        except:
            beta = 1.0

        
        # === STEP 0C: Market Return (Hardcoded) ===
        market_return = 0.10  # S&P 500 long-term historical average
        
        # Get most recent data
        latest_income = income_statement[0]
        latest_balance = balance_sheet[0]
        
        # === STEP 1: Calculate Cost of Equity using CAPM ===
        cost_of_equity = risk_free_rate + beta * (market_return - risk_free_rate)
        
        # === STEP 2: Calculate Cost of Debt ===
        interest_expense = latest_income.interest_expense
        total_debt = latest_balance.total_debt
        
        if interest_expense is None or total_debt is None or total_debt == 0:
            cost_of_debt = 0.05
        else:
            cost_of_debt = abs(interest_expense) / total_debt
        
        # === STEP 3: Calculate Tax Rate ===
        pretax_income = latest_income.pretax_income
        tax_provision = latest_income.tax_provision
        
        if pretax_income is not None and tax_provision is not None and pretax_income > 0:
            tax_rate = tax_provision / pretax_income
            tax_rate = max(0, min(tax_rate, 0.5))
        else:
            tax_rate = 0.21
        
        # === STEP 4: Get Equity and Debt Values ===
        debt = total_debt if total_debt is not None else 0

        try:
            ticker_info = yf.Ticker(ticker_symbol).info
            equity = ticker_info.get('marketCap')
        except Exception:
            equity = None

        # Fall back to book equity only if market cap is unavailable
        if equity is None or equity <= 0:
            equity = latest_balance.stockholders_equity

        if equity is None or equity <= 0:
            return cost_of_equity  
        
        total_value = equity + debt
        
        if total_value == 0:
            return None
        
        # === STEP 5: Calculate WACC ===
        equity_weight = equity / total_value
        debt_weight = debt / total_value
        
        wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
        
        return wacc
    
    @staticmethod
    def revenue_growth_rate(income_statement):
   
        revenues = [period.total_revenue for period in income_statement 
                if period.total_revenue is not None and period.total_revenue > 0]
        
        if len(revenues) < 2:
            return None
        
        most_recent = revenues[0]
        oldest = revenues[-1]
        num_periods = len(revenues) - 1
        
        try:
            cagr = (most_recent / oldest) ** (1 / num_periods) - 1
            return cagr
        except:
            return None
    @staticmethod
    def project_fcf(cashflow_statement, income_statement, projection_years=5):
        """
        Project future Free Cash Flows with graduated growth decay.
        Growth starts at historical rate and linearly decays to terminal growth (2.5%).
        """
        fcf_history = DCF_Analyst.fcf_list(cashflow_statement)
        
        if fcf_history is None or len(fcf_history) == 0:
            return {
                "projected_fcfs": [],
                "growth_rate_used": None,
                "base_fcf": None
            }
        
        base_fcf = fcf_history[0]
        
        if base_fcf is None or base_fcf <= 0:
            return {
                "projected_fcfs": [],
                "growth_rate_used": None,
                "base_fcf": base_fcf
            }
        
        # Get historical growth rate
        historical_growth = DCF_Analyst.fcf_growth_rate(cashflow_statement)
        
        if historical_growth is None:
            historical_growth = DCF_Analyst.revenue_growth_rate(income_statement)
        
        if historical_growth is None:
            historical_growth = 0.05  # Default 5%
        
        # Cap historical growth at reasonable bounds
        historical_growth = min(historical_growth, 0.50)  # Max 50% starting point
        historical_growth = max(historical_growth, -0.10)  # Min -10%
        
        # Terminal growth rate (perpetual)
        terminal_growth = 0.025  # 2.5%
        
        # Project FCFs with graduated decay
        projected_fcfs = []
        current_fcf = base_fcf
        
        for year in range(1, projection_years + 1):
            # Linear decay: Year 1 uses more historical, Year 5 uses more terminal

            weight = (projection_years - year) / projection_years
            
            # Blend historical and terminal growth
            year_growth = (historical_growth * weight) + (terminal_growth * (1 - weight))
            
            current_fcf = current_fcf * (1 + year_growth)
            projected_fcfs.append(current_fcf)
        
        # Calculate average growth rate used (for reporting purposes)
        avg_growth = sum([
            (historical_growth * (projection_years - y) / projection_years) + 
            (terminal_growth * (1 - (projection_years - y) / projection_years))
            for y in range(1, projection_years + 1)
        ]) / projection_years
        
        return {
            "projected_fcfs": projected_fcfs,
            "growth_rate_used": avg_growth,
            "base_fcf": base_fcf
        }
    
    @staticmethod
    def terminal_value(final_year_fcf, wacc, terminal_growth_rate=0.025):
        """Calculate Terminal Value using Gordon Growth Model"""
        if wacc <= terminal_growth_rate:
            return None
        
        terminal_fcf = final_year_fcf * (1 + terminal_growth_rate)
        tv = terminal_fcf / (wacc - terminal_growth_rate)
        
        return tv
        
    @staticmethod
    def enterprise_value(cashflow_statement, income_statement, balance_sheet, ticker_symbol):
        projection_years = 5
        terminal_growth_rate = 0.025
        
        discount_rate = DCF_Analyst.wacc(income_statement, balance_sheet, ticker_symbol)
        
        if discount_rate is None:
            return None
        
        projection_data = DCF_Analyst.project_fcf(cashflow_statement, income_statement, projection_years)
        
        projected_fcfs = projection_data["projected_fcfs"]
        
        if len(projected_fcfs) == 0:
            return None
        
        pv_fcfs = []
        for year, fcf in enumerate(projected_fcfs, start=1):
            pv = fcf / ((1 + discount_rate) ** year)
            pv_fcfs.append(pv)
        
        sum_pv_fcfs = sum(pv_fcfs)
        
        final_fcf = projected_fcfs[-1]
        tv = DCF_Analyst.terminal_value(final_fcf, discount_rate)
        
        if tv is None:
            return None
        
        pv_terminal_value = tv / ((1 + discount_rate) ** projection_years)
        
        enterprise_val = sum_pv_fcfs + pv_terminal_value
        
        return {
            "enterprise_value": enterprise_val,
            "pv_projected_fcfs": sum_pv_fcfs,
            "pv_terminal_value": pv_terminal_value,
            "terminal_value": tv,
            "projected_fcfs": projected_fcfs,
            "discount_rate_wacc": discount_rate,
            "growth_rate_used": projection_data["growth_rate_used"],
            "terminal_growth_rate": terminal_growth_rate,
            "base_fcf": projection_data["base_fcf"]
        }

    @staticmethod
    def equity_value(cashflow_statement, income_statement, balance_sheet, ticker_symbol):
        ev_data = DCF_Analyst.enterprise_value(cashflow_statement, income_statement, balance_sheet, ticker_symbol)
        
        if ev_data is None:
            return None
        
        enterprise_val = ev_data["enterprise_value"]
        
        latest_balance = balance_sheet[0]
        net_debt = latest_balance.net_debt
        
        if net_debt is None:
            total_debt = latest_balance.total_debt if latest_balance.total_debt else 0
            cash = latest_balance.cash_and_cash_equivalents if latest_balance.cash_and_cash_equivalents else 0
            net_debt = total_debt - cash
        
        equity_val = enterprise_val - net_debt
        
        shares_outstanding = latest_balance.ordinary_shares_number
        
        price_per_share = None
        if shares_outstanding is not None and shares_outstanding > 0:
            price_per_share = equity_val / shares_outstanding
        
        return {
            **ev_data,
            "net_debt": net_debt,
            "equity_value": equity_val,
            "shares_outstanding": shares_outstanding,
            "price_per_share": price_per_share
        }