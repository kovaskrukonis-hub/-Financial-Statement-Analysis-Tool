import pandas
from statements import IncomeStatement, BalanceSheet, CashFlowStatement
from mapping import INCOME_MAPPING, BALANCE_SHEET_MAPPING, CASH_FLOW_MAPPING

class FinancialStatementFactory:
    """
    This class acts as the 'Engine' that converts raw DataFrames 
    into structured Python objects with fuzzy-matching logic.
    """

    @staticmethod
    def create_financial_statement(
        financial_dataframe: pandas.DataFrame, 
        ticker_symbol: str, 
        statement_type: str
    ):
        # 1. Check if the dataframe actually contains data
        if financial_dataframe is None or financial_dataframe.empty:
            print(f"No data found for {ticker_symbol}")
            return None
            
        # 4. Route the data to the correct mapping and class based on the type
        if statement_type == "income_statement":
            data_mapping_dictionary = INCOME_MAPPING
            target_dataclass = IncomeStatement
        elif statement_type == "balance_sheet":
            data_mapping_dictionary = BALANCE_SHEET_MAPPING
            target_dataclass = BalanceSheet
        elif statement_type == "cash_flow_statement":
            data_mapping_dictionary = CASH_FLOW_MAPPING
            target_dataclass = CashFlowStatement
        else:
            raise ValueError("The statement_type must be 'income_statement', 'balance_sheet', or 'cash_flow_statement'")

        all_periods = []

        # We loop through all columns to handle multiple periods (years)
        for i in range(len(financial_dataframe.columns)):
            current_period = financial_dataframe.iloc[:, i]
            statement_date = current_period.name
            
            extracted_financial_values = {}

            # Create a 'clean' version of the index to find matches regardless of case or spaces
            
            normalized_index = {str(k).lower().strip(): k for k in current_period.index}
            
            for data_mapping_key, yahoo_finance_name in data_mapping_dictionary.items():
                target_key = str(yahoo_finance_name).lower().strip()
                
                # Check if our clean key exists in the clean index
                if target_key in normalized_index:
                    actual_key = normalized_index[target_key]
                    actual_value = current_period.get(actual_key)
                    
                    # If value is NaN (x != x), convert it to None so your ratio logic 
                    # can handle it safely
                    if actual_value != actual_value:
                        actual_value = None
                else:
                    actual_value = None
                
                extracted_financial_values[data_mapping_key] = actual_value

            # 6. Final Assembly
            period_object = target_dataclass(
                ticker=ticker_symbol, 
                date=statement_date, 
                **extracted_financial_values
            )
            
            all_periods.append(period_object)

        return all_periods