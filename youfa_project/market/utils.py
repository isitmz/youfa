import yfinance as yf
import logging
logger = logging.getLogger("market_logger")

# Questo file contiene funzioni di utilità per interagire con la libreria yfinance. 
# Fornisce metodi per recuperare informazioni generali, dati storici sui prezzi
# dividendi e dati finanziari per specifici ticker azionari, 
# gestendo eventuali errori durante il processo.
# Una sorta di wrapper del modulo YFinance

def get_ticker_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except Exception as e:
        logger.error(f"Errore yfinance get_ticker_info: {e}")

def get_ticker_history(ticker, period="1d", interval="1d"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            return None
        return hist
    except Exception as e:
        logger.error(f"Errore yfinance get_ticker_history: {e}")
        return None

def get_ticker_dividends(ticker):
    try:
        stock = yf.Ticker(ticker)
        div = stock.dividends
        if div.empty:
            return None
        return div
    except Exception as e:
        logger.error(f"Errore yfinance get_ticker_dividends: {e}")
        return None

def get_ticker_financials(ticker):
    try:
        stock = yf.Ticker(ticker)
        fin = stock.financials
        if fin.empty:
            return None
        return fin
    except Exception as e:
        logger.error(f"Errore yfinance get_ticker_financials: {e}")
        return None