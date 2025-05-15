import logging
from django.http import JsonResponse
from django.shortcuts import render
from market.models import Asset
from django.views.decorators.http import require_GET
from .utils import get_ticker_info, get_ticker_history

logger = logging.getLogger("market_logger")

def market_home(request):
    logger.info("Accesso alla pagina principale del mercato.")
    assets = Asset.objects.all().order_by('ticker')
    return render(request, 'market/index.html', {'assets': assets})

@require_GET
def get_price_details(request, ticker):
    logger.info(f"Richiesta dettagli prezzo per il ticker: {ticker}")
    info = get_ticker_info(ticker)

    if not info:
        logger.warning(f"Dati non disponibili per il ticker: {ticker}")
        return JsonResponse({"error": "Dati non disponibili"}, status=500)

    return JsonResponse({
        "ticker": ticker.upper(),
        "price": round(info.get("regularMarketPrice", 0), 2),
        "currency": info.get("currency"),
        "change_percent": round(info.get("regularMarketChangePercent", 0), 2),
    })

@require_GET
def get_asset_details(request, ticker):
    logger.info(f"Richiesta dettagli asset per il ticker: {ticker}")
    info = get_ticker_info(ticker)
    if not info:
        logger.warning(f"Dati non disponibili per il ticker: {ticker}")
        return JsonResponse({"error": "Dati non disponibili"}, status=404)

    hist = get_ticker_history(ticker, period="1d", interval="1d")
    if hist is None or hist.empty:
        return JsonResponse({"error": "Storico dati non disponibile"}, status=404)

    last_close = hist["Close"].iloc[-1]
    open_price = hist["Open"].iloc[-1]
    change_percent = round(((last_close - open_price) / open_price) * 100, 2)

    data = {
        "ticker": ticker.upper(),
        "name": info.get("longName", ""),
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "website": info.get("website", ""),
        "description": info.get("longBusinessSummary", ""),
        "market_cap": info.get("marketCap", None),
        "pe_ratio": info.get("forwardPE", None),
        "dividend_yield": info.get("dividendYield", None),
        "52w_high": info.get("fiftyTwoWeekHigh", None),
        "52w_low": info.get("fiftyTwoWeekLow", None),
        "volume": info.get("volume", None),
        "average_volume": info.get("averageVolume", None),
        "currency": info.get("currency", "USD"),
        "exchange": info.get("exchange", ""),
        "quote_type": info.get("quoteType", ""),
        "price": round(last_close, 2),
        "change_percent": change_percent
    }

    return JsonResponse(data)

@require_GET
def get_chart_data(request, ticker):
    period = request.GET.get('period', '6mo')
    interval = request.GET.get('interval', '1d')

    # Limitazioni accettabili period e interval
    allowed_periods = ['1mo', '3mo', '6mo', '1y']
    allowed_intervals = ['1d', '1wk', '1h']

    if period not in allowed_periods:
        period = '6mo'
    if interval not in allowed_intervals:
        interval = '1d'

    logger.info(f"Richiesta dati grafico per il ticker: {ticker}, periodo: {period}, intervallo: {interval}")
    hist = get_ticker_history(ticker, period=period, interval=interval)
    if hist is None or hist.empty:
        return JsonResponse({"error": "Dati storici non disponibili"}, status=404)

    # Prepariamo i dati in formato JSON-friendly
    data = []
    for idx, row in hist.iterrows():
        data.append({
            "date": idx.strftime("%Y-%m-%d"),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        })
    logger.info(f"Dati grafico recuperati con successo per il ticker: {ticker}")
    return JsonResponse({"ticker": ticker.upper(), "period": period, "interval": interval, "data": data})
