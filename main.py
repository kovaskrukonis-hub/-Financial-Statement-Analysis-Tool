import yfinance as yahoo_finance
from factory import FinancialStatementFactory
from dcf_calculation import DCF_Analyst
from valuation_score import calculate_scores, get_verdict
from analyst import FinancialAnalyst
from price import get_price
from contextlib import redirect_stderr
import os

while True:
    try:
        G, Y, R, B, Blue, RES = "\033[92m", "\033[93m", "\033[91m", "\033[1m", "\033[94m","\033[0m"

        ticker_symbol = input(f'{B}{Blue}Please requeste a ticker or type 0 if you wish to exit:\n{RES}').upper()

        if ticker_symbol != '0':

            with redirect_stderr(open(os.devnull, 'w')):
                ticker_object = yahoo_finance.Ticker(ticker_symbol)
                
                if ticker_object.history(period='5d').empty:
                    print(f'{R}Invalid ticker symbol: {ticker_symbol}{RES}\n')
                    continue

            df_income = ticker_object.financials
            df_balance = ticker_object.balance_sheet
            df_cashflows = ticker_object.cashflow

            income_list = FinancialStatementFactory.create_financial_statement(
                df_income, ticker_symbol, "income_statement")
            balance_list = FinancialStatementFactory.create_financial_statement(
                df_balance, ticker_symbol, "balance_sheet")
            cashflow_list = FinancialStatementFactory.create_financial_statement(
                df_cashflows, ticker_symbol, "cash_flow_statement")


            if not income_list or not balance_list:
                print(f'{R}Unable to fetch financial data for {ticker_symbol}{RES}\n')
                continue

            if len(income_list) < 1 or len(balance_list) < 2:
                print(f'{R}Insufficient financial history for analysis{RES}\n')
                continue
            
            company_name = ticker_object.info.get('longName') or ticker_object.info.get('shortName') or ticker_symbol
            
            # Setup Header
            print(f"\n{B}{Blue}>>> {company_name} TERMINAL HUB <<<{RES}")
            price = get_price(ticker_symbol)
            print(f"{Blue}Current Price: ${price:.2f}{RES}" if price else f"{R}Price: N/A{RES}")
            print(f"{Blue}" + "=" * 75 + f"{RES}")

            # Formatting variable
            space = 35 

            # 1. P/E Ratio
            price_to_earnings = FinancialAnalyst.price_to_earnings(price, income_list)
            label = "P/E Ratio:"
            if price_to_earnings is None or price_to_earnings != price_to_earnings:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if price_to_earnings < 0:   color, status = R, "(Net Loss)"
                elif price_to_earnings < 15: color, status = G, "(Strong)"
                elif price_to_earnings < 30: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{price_to_earnings:<8.2f}{RES} {status}")

            # 2. EPS Ratio
            eps = FinancialAnalyst.eps(income_list)
            label = "EPS Ratio:"
            if eps is None or eps != eps:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if eps < 0: color, status = R, "(Net Loss)"
                elif eps > 0: color, status = G, "(Profitable)"
                else: color, status = R, "(Break Even)"
                print(f"{label:<{space}} {color}{eps:<8.2f}{RES} {status}")

            # 3. Dividend Payout Ratio
            dividend_payout_ratio = FinancialAnalyst.dividend_payout_ratio(ticker_symbol, income_list)
            label = "Dividends Payout Ratio:"

            if dividend_payout_ratio is None or dividend_payout_ratio != dividend_payout_ratio:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if dividend_payout_ratio == 0.0: 
                    color, status = Blue, "(No Dividend)"
                elif dividend_payout_ratio < 35: color, status = G, "(Strong)"
                elif dividend_payout_ratio < 60: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{dividend_payout_ratio:<8.2f}{RES} {status}")

            # 4. Debt to Assets Ratio
            debt_to_assets = FinancialAnalyst.debt_to_assets(balance_list)
            label = "Debt to Assets Ratio:"
            if debt_to_assets is None or debt_to_assets != debt_to_assets:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if debt_to_assets < 20: color, status = G, "(Strong)"
                elif debt_to_assets < 50: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{debt_to_assets:<8.2f}{RES} {status}")

            # 5. Interest Coverage
            interes_coverage = FinancialAnalyst.interest_coverage_smart(income_list)
            label = "Interest Coverage:"
            if interes_coverage is None or interes_coverage != interes_coverage:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if interes_coverage > 5: color, status = G, "(Strong)"
                elif interes_coverage > 2: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{interes_coverage:<8.2f}{RES} {status}")

            # 6. Current Ratio
            current_ratio = FinancialAnalyst.current_ratio(balance_list)
            label = "Current Ratio:"
            if current_ratio is None or current_ratio != current_ratio:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if current_ratio > 2: color, status = G, "(Strong)"
                elif current_ratio > 1: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{current_ratio:<8.2f}{RES} {status}")

            # 7. Quick Ratio
            quick_ratio = FinancialAnalyst.quick_ratio(balance_list)
            label = "Quick Ratio:"
            if quick_ratio is None or quick_ratio != quick_ratio:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if quick_ratio > 1.5: color, status = G, "(Strong)"
                elif quick_ratio > 0.8: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{quick_ratio:<8.2f}{RES} {status}")

            # 8. Cash Ratio
            cash_ratio = FinancialAnalyst.cash_ratio(balance_list)
            label = "Cash Ratio:"
            if cash_ratio is None or cash_ratio != cash_ratio:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if cash_ratio > 0.5: color, status = G, "(Strong)"
                elif cash_ratio > 0.2: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{cash_ratio:<8.2f}{RES} {status}")

            # 9. Return on Assets
            return_on_assets = FinancialAnalyst.return_on_assets(income_list, balance_list)
            label = "Return on Assets:"
            if return_on_assets is None or return_on_assets != return_on_assets:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if return_on_assets < 0:   color, status = R, "(Negative)"
                elif return_on_assets > 10: color, status = G, "(Strong)"
                elif return_on_assets > 5: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{return_on_assets:<8.2f}{RES} {status}")

            # 10. Return on Equity
            return_on_equity = FinancialAnalyst.return_on_equity(income_list, balance_list)
            label = "Return on Equity:"
            if return_on_equity is None or return_on_equity != return_on_equity:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if return_on_equity < 0: color, status = R, "(Negative)"
                elif return_on_equity > 20: color, status = G, "(Strong)"
                elif return_on_equity > 10: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{return_on_equity:<8.2f}{RES} {status}")

            # 11. Gross Profit Margin
            gross_profit_margin = FinancialAnalyst.gross_profit_margin(income_list)
            label = "Gross Profit Margin:"
            if gross_profit_margin is None or gross_profit_margin != gross_profit_margin:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if gross_profit_margin > 40: color, status = G, "(Strong)"
                elif gross_profit_margin > 20: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{gross_profit_margin:<8.2f}{RES} {status}")

            # 12. Operating Profit Margin
            operating_profit_margin = FinancialAnalyst.operating_margin(income_list)
            label = "Operating Profit Margin:"
            if operating_profit_margin is None or operating_profit_margin != operating_profit_margin:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if operating_profit_margin > 15: color, status = G, "(Strong)"
                elif operating_profit_margin > 8: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{operating_profit_margin:<8.2f}{RES} {status}")

            # 13. Inventory Turnover Year
            invenotry_turnover_year = FinancialAnalyst.inventory_turnover_year(income_list, balance_list)
            label = "Inventory Turnover:"
            if invenotry_turnover_year is None or invenotry_turnover_year != invenotry_turnover_year:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if invenotry_turnover_year > 10: color, status = G, "(Strong)"
                elif invenotry_turnover_year > 5: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{invenotry_turnover_year:<8.2f}{RES} {status}")

            # 14. Inventory Turnover Days
            invenotry_turnover_days = FinancialAnalyst.inventory_turnover_days(income_list, balance_list)
            label = "Inventory Turnover in days:"
            if invenotry_turnover_days is None or invenotry_turnover_days != invenotry_turnover_days:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if invenotry_turnover_days < 30: color, status = G, "(Strong)"
                elif invenotry_turnover_days < 60: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{invenotry_turnover_days:<8.2f}{RES} {status}")

            # 15. Receivables Turnover
            receivables_turnover = FinancialAnalyst.receivables_turnover(income_list, balance_list)
            label = "Receivables Turnover:"
            if receivables_turnover is None or receivables_turnover != receivables_turnover:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if receivables_turnover > 12: color, status = G, "(Strong)"
                elif receivables_turnover > 6: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{receivables_turnover:<8.2f}{RES} {status}")

            # 16. Average Collection Period
            avg_collection_period = FinancialAnalyst.average_collection_period(income_list, balance_list)
            label = "Average Collection Period:"
            if avg_collection_period is None or avg_collection_period != avg_collection_period:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if avg_collection_period < 30: color, status = G, "(Strong)"
                elif avg_collection_period < 60: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{avg_collection_period:<8.2f}{RES} {status}")

            # 17. Payables Turnover
            payables_turnover = FinancialAnalyst.payables_turnover(income_list, balance_list)
            label = "Payables Turnover:"
            if payables_turnover is None or payables_turnover != payables_turnover:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if payables_turnover < 6: color, status = G, "(Strong)"
                elif payables_turnover < 10: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{payables_turnover:<8.2f}{RES} {status}")

            # 18. Average Payment Period
            average_payment_period = FinancialAnalyst.average_payment_period(income_list, balance_list)
            label = "Average Payment Period:"
            if average_payment_period is None or average_payment_period != average_payment_period:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if average_payment_period > 45: color, status = G, "(Strong)"
                elif average_payment_period > 30: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{average_payment_period:<8.2f}{RES} {status}")

            # 19. Total Asset Turnover
            total_asset_turnover = FinancialAnalyst.total_asset_turnover(income_list, balance_list)
            label = "Total Asset Turnover:"
            if total_asset_turnover is None or total_asset_turnover != total_asset_turnover:
                print(f"{label:<{space}} {R}N/A{RES} (Missing Data)")
            else:
                if total_asset_turnover > 2: color, status = G, "(Strong)"
                elif total_asset_turnover > 1: color, status = Y, "(Average)"
                else: color, status = R, "(Risky)"
                print(f"{label:<{space}} {color}{total_asset_turnover:<8.2f}{RES} {status}")

            print(f"{Blue}" + "=" * 75 + f"{RES}")
            print(f"{B}{Y}>>> {company_name} INTRINSIC VALUE BASED ON DCF METHOD <<<{RES}\n")

            valuation = DCF_Analyst.equity_value(cashflow_list, income_list, balance_list, ticker_symbol)

            if valuation is None or valuation.get('price_per_share') is None:
                print(f"{R}DCF valuation could not be calculated (insufficient data){RES}")
            else:
                intrinsic = valuation['price_per_share']
                diff = intrinsic - price

                # Margin of Safety: how much cheaper the stock is vs intrinsic value (%)
                margin_of_safety = (diff / intrinsic) * 100

                # --- Valuation Rating ---
                if margin_of_safety >= 30:
                    rating, rating_color, verdict = "STRONG BUY", G, "Stock appears significantly undervalued"
                elif margin_of_safety >= 15:
                    rating, rating_color, verdict = "BUY", G, "Stock appears moderately undervalued"
                elif margin_of_safety >= -10:
                    rating, rating_color, verdict = "FAIRLY VALUED", Y, "Stock is trading near intrinsic value"
                elif margin_of_safety >= -30:
                    rating, rating_color, verdict = "OVERVALUED", R, "Stock appears moderately overvalued"
                else:
                    rating, rating_color, verdict = "STRONG SELL", R, "Stock appears significantly overvalued"

                label = 'Intrinsic Value (DCF):'
                print(f"{label:<{space}} {G}${intrinsic:.2f}{RES}")
                label = 'Market Price:'
                print(f"{label:<{space}} {Blue}${price:.2f}{RES}")
                label = 'Absolute Difference:'
                color = G if diff >= 0 else R
                print(f"{label:<{space}} {color}{'+' if diff >= 0 else ''}{diff:.2f}{RES}")
                label = 'Margin of Safety:'
                color = G if margin_of_safety >= 0 else R
                print(f"{label:<{space}} {color}{'+' if margin_of_safety >= 0 else ''}{margin_of_safety:.1f}%{RES}")

                print(f"\n{B}  RATING BASED ON DCF ONLY: {rating_color}[ {rating} ]{RES}")
                print(f"  {verdict}")

                print(f'\n{B}{Y}Core Assumptions:{RES}')
                label = 'Growth Rate Used:'
                print(f"  {label:<{space-2}} {valuation['growth_rate_used']:.2%}")
                label = 'WACC:'
                print(f"  {label:<{space-2}} {valuation['discount_rate_wacc']:.2%}")

                print(f"{Blue}" + "=" * 75 + f"{RES}\n")
                margin_of_safety = None
                if valuation and valuation.get('price_per_share') and price:
                    margin_of_safety = ((valuation['price_per_share'] - price) / valuation['price_per_share']) * 100

                scores = calculate_scores(
                    price_to_earnings       = price_to_earnings,
                    eps                     = eps,
                    margin_of_safety        = margin_of_safety,
                    return_on_assets        = return_on_assets,
                    return_on_equity        = return_on_equity,
                    gross_profit_margin     = gross_profit_margin,
                    operating_profit_margin = operating_profit_margin,
                    current_ratio           = current_ratio,
                    debt_to_assets          = debt_to_assets,
                    interest_coverage       = interes_coverage,
                    inventory_turnover_year = invenotry_turnover_year,
                    avg_collection_period   = avg_collection_period,
                    average_payment_period  = average_payment_period,
                )

                verdict, verdict_color, verdict_desc = get_verdict(scores['final_score'])

                print(f"{B}{Y}>>> {company_name} INVESTMENT SCORECARD <<<{RES}\n")

                categories = [
                    ('Valuation',           scores['valuation'],     '35%'),
                    ('Profitability',       scores['profitability'], '30%'),
                    ('Solvency/Efficiency', scores['solvency'],      '35%'),
                ]

                print(f"  {'Category':<28} {'Score':>10}   {'Weight':>6}   Bar")
                print(f"  {'-' * 64}")

                for name, cat_score, weight in categories:
                    if cat_score is None:
                        color = R
                        score_str = "N/A"
                        bar = f"{R}{'░' * 10}{RES}"
                    else:
                        color = G if cat_score >= 7 else Y if cat_score >= 4 else R
                        score_str = f"{cat_score:.1f} / 10"
                        bar = f"{color}{'█' * int(round(cat_score))}{RES}{'░' * (10 - int(round(cat_score)))}"
                    print(f"  {name:<28} {color}{score_str:>10}{RES}   {weight:>6}   {bar}")

                print(f"\n  {'-' * 64}")

                if scores['final_score'] is not None:
                    fs = scores['final_score']
                    fs_color = G if fs >= 70 else Y if fs >= 40 else R
                    print(f"  {'Overall Score':<28} {fs_color}{fs:>9.1f} / 100{RES}")
                else:
                    print(f"  {'Overall Score':<28} {R}{'N/A':>10}{RES}")

                if verdict:
                    print(f"\n  {B}VERDICT: {verdict_color}[ {verdict} ]{RES}")
                    print(f"  {verdict_desc}")

                print(f"\n{Blue}" + "=" * 75 + f"{RES}\n")


        else:
            print(f'{Y}Exiting the program...{RES}')
            break

    except KeyboardInterrupt:
        print(f'\n{Blue}Exiting...{RES}')
        break
    except Exception as e:
        print(f'{R}Error: {str(e)}{RES}\n')
