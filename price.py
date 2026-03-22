import yfinance as yahoo_finance


def get_price(ticker_symbol):
    ticker = yahoo_finance.Ticker(ticker_symbol)
    
    info = ticker.info
    if not info:
        return None
        
    price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('ask')

    if price is None:
        try:
            hist = ticker.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
        except Exception:
            return None
            
    return price