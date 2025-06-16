import logging
from django.http import JsonResponse
from django.shortcuts import render
from market.models import Asset, PriceAlert
from user.models import UserProfile
from django.views.decorators.http import require_GET
from decimal import Decimal, InvalidOperation
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from portfolio.models import PortfolioItem, PortfolioTransaction
from django.db import transaction
from .utils import get_ticker_info, get_ticker_history

logger = logging.getLogger("market_logger")

def market_home(request):
    # Visualizza la pagina principale del mercato con l'elenco degli asset.
    # Se l'utente è autenticato, mostra anche il saldo.
    logger.info("Accesso alla pagina principale del mercato.")
    assets = Asset.objects.all().order_by('ticker')

    context = {'assets': assets}

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            context['username'] = request.user.username
            context['saldo'] = profile.saldo
        except UserProfile.DoesNotExist:
            context['username'] = request.user.username
            context['saldo'] = None

    return render(request, 'market/index.html', context)

@require_GET
def get_price_details(request, ticker):
    # API per ottenere i dettagli del prezzo di un asset.
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
    # API per ottenere i dettagli completi di un asset, inclusi dati storici.
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
    # API per ottenere i dati storici di un asset per la visualizzazione di un grafico.
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

@login_required
@require_POST
@transaction.atomic
def trade_asset(request):
    try:
        data = json.loads(request.body)
        ticker = data.get("ticker")
        quantity = Decimal(str(data.get("quantity")))
        price = Decimal(str(data.get("price")))
        operation = data.get("operation")
        logger.info(f"Richiesta {operation} ricevuta per {ticker}: quantità={quantity}, prezzo={price}")
    except (json.JSONDecodeError, TypeError, InvalidOperation) as e:
        logger.error(f"Errore nel parsing dei dati: {e}")
        return JsonResponse({"error": "Dati non validi."}, status=400)

    if not ticker or quantity <= 0 or price <= 0 or operation not in ("buy", "sell"):
        logger.warning(f"Parametri invalidi: ticker={ticker}, quantità={quantity}, prezzo={price}, operazione={operation}")
        return JsonResponse({"error": "Parametri invalidi."}, status=400)

    try:
        asset = Asset.objects.get(ticker=ticker)
    except Asset.DoesNotExist:
        logger.error(f"Asset non trovato: {ticker}")
        return JsonResponse({"error": "Asset non trovato."}, status=404)

    user_profile = UserProfile.objects.get(user=request.user)

    if operation == "buy":
        total_cost = quantity * price
        if user_profile.saldo < total_cost:
            logger.warning(f"Saldo insufficiente per l'acquisto: saldo={user_profile.saldo}, costo={total_cost}")
            return JsonResponse({"error": "Saldo insufficiente."}, status=400)

        portfolio_item, _ = PortfolioItem.objects.get_or_create(
            user=request.user,
            asset=asset,
            defaults={"quantity": 0, "avg_price": 0}
        )

        new_total_qty = portfolio_item.quantity + quantity
        new_avg_price = (
            (portfolio_item.quantity * portfolio_item.avg_price) + (quantity * price)
        ) / new_total_qty if new_total_qty > 0 else 0

        portfolio_item.quantity = new_total_qty
        portfolio_item.avg_price = new_avg_price
        portfolio_item.save()

        user_profile.saldo -= total_cost
        user_profile.save()

        PortfolioTransaction.objects.create(
            user=request.user,
            asset=asset,
            action="BUY",
            quantity=quantity,
            price_at_transaction=price,
        )

        logger.info(f"Acquisto completato: utente={request.user.username}, ticker={ticker}, quantità={quantity}, prezzo medio={new_avg_price}, saldo rimanente={user_profile.saldo}")

        return JsonResponse({
            "message": "Acquisto effettuato con successo.",
            "saldo": float(user_profile.saldo),
            "quantity": float(portfolio_item.quantity),
            "avg_price": float(portfolio_item.avg_price),
        })

    else:  # sell
        try:
            portfolio_item = PortfolioItem.objects.get(user=request.user, asset=asset)
        except PortfolioItem.DoesNotExist:
            logger.warning(f"Tentata vendita senza possesso dell’asset: {ticker}")
            return JsonResponse({"error": "Non possiedi questo asset."}, status=400)

        if portfolio_item.quantity < quantity:
            logger.warning(f"Quantità da vendere superiore a quella posseduta: posseduta={portfolio_item.quantity}, richiesta={quantity}")
            return JsonResponse({"error": "Quantità da vendere superiore a quella posseduta."}, status=400)

        portfolio_item.quantity -= quantity
        if portfolio_item.quantity == 0:
            portfolio_item.delete()
            logger.info(f"Item {ticker} rimosso dal portafoglio di {request.user.username} poiché la quantità è zero.")
        else:
            portfolio_item.save()

        user_profile.saldo += quantity * price
        user_profile.save()

        profit_percent = ((price - portfolio_item.avg_price) / portfolio_item.avg_price) * 100

        PortfolioTransaction.objects.create(
            user=request.user,
            asset=asset,
            action="SELL",
            quantity=quantity,
            price_at_transaction=price,
            profit_percentage=profit_percent
        )

        logger.info(f"Vendita completata: utente={request.user.username}, ticker={ticker}, quantità={quantity}, saldo aggiornato={user_profile.saldo}")

        return JsonResponse({
            "message": "Vendita effettuata con successo.",
            "saldo": float(user_profile.saldo),
            "quantity": float(portfolio_item.quantity) if portfolio_item.quantity > 0 else 0,
            "avg_price": float(portfolio_item.avg_price) if portfolio_item.quantity > 0 else 0,
        })


# Vista che gestisce la creazione delle notifiche (da chiamare con AJAX)
@login_required
def create_price_alert(request):
    if request.method == "POST":
        ticker = request.POST.get("ticker")
        target_price = request.POST.get("target_price")
        direction = request.POST.get("direction")

        try:
            asset = Asset.objects.get(ticker=ticker.upper())
            target_price = Decimal(target_price)
            if target_price <= 0:
                raise ValueError("Prezzo non valido")

            is_above = direction == "above" # se direction è above, is_above = true

            PriceAlert.objects.create(
                user=request.user,
                asset=asset,
                target_price=target_price,
                is_above=is_above
            )
            return JsonResponse({"success": True, "message": "Alert creato correttamente."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Errore: {str(e)}"})

    return JsonResponse({"success": False, "message": "Metodo non consentito."})


# View per prendere tutti gli alert di un utente in base al ticker
@login_required
def get_user_alerts(request, ticker):
    try:
        asset = Asset.objects.get(ticker=ticker.upper())
        alerts = PriceAlert.objects.filter(user=request.user, asset=asset, triggered=False)

        alert_list = [
            {
                "id": alert.id,
                "target_price": str(alert.target_price),
                "direction": "above" if alert.is_above else "below"
            }
            for alert in alerts
        ]

        return JsonResponse({"alerts": alert_list})
    except Asset.DoesNotExist:
        return JsonResponse({"alerts": []})

    
# View per eliminare un alert
@login_required
def delete_price_alert(request):
    if request.method == "POST":
        alert_id = request.POST.get("alert_id")
        try:
            alert = PriceAlert.objects.get(id=alert_id, user=request.user)
            alert.delete()
            return JsonResponse({"success": True})
        except PriceAlert.DoesNotExist:
            return JsonResponse({"success": False, "message": "Alert non trovato"})
    return JsonResponse({"success": False, "message": "Metodo non consentito."})