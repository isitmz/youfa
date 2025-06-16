import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from user.models import UserProfile
from .models import PortfolioItem, PortfolioTransaction
from market.utils import get_ticker_history # metodo utils
from datetime import timedelta
from django.utils import timezone


# Imposto il logger

logger = logging.getLogger("portfolio_logger")

# Richiede che l'utente sia autenticato per accedere a questa vista.
@login_required
def portfolio_info(request, ticker):
    # Recupera le informazioni del portafoglio per un dato ticker per l'utente loggato.
    # Restituisce la quantità posseduta e il prezzo medio di acquisto.
    logger.info(f"Richiesta informazioni portafoglio per l'utente {request.user.username} e ticker {ticker}.")
    user = request.user
    try:
        # Cerca una voce nel portafoglio per l'utente e il ticker specificati.
        entry = PortfolioItem.objects.get(user=user, asset__ticker=ticker)
        quantity = entry.quantity
        avg_price = entry.avg_price
        logger.info(f"Trovata voce di portafoglio per {user.username} - {ticker}: Quantità {quantity}, Prezzo Medio {avg_price}.")
    except PortfolioItem.DoesNotExist:
        # Se l'asset non è nel portafoglio, imposta quantità e prezzo medio a zero.
        logger.info(f"Nessuna voce di portafoglio trovata per {user.username} - {ticker}. Impostazione predefinita a quantità 0 e prezzo medio 0.")
        quantity = 0
        avg_price = 0.00

    # Restituisce i dati in formato JSON.
    return JsonResponse({
        'quantity': float(quantity),  # assicuriamoci che sia serializzabile JSON
        'avg_price': float(avg_price),  # assicuriamoci che sia serializzabile JSON
    })

@login_required
def get_saldo(request):
    # Funzione API per recuperare il saldo dell'utente da aggiornare dove necessario
    logger.info(f"Richiesta saldo per l'utente {request.user.username}.")
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        logger.info(f"Saldo recuperato per {request.user.username}: {user_profile.saldo}.")
        return JsonResponse({'saldo': float(user_profile.saldo)})
    except UserProfile.DoesNotExist:
        logger.error(f"Profilo utente non trovato per {request.user.username} durante il recupero del saldo.")
        return JsonResponse({'error': 'Profilo utente non trovato.'}, status=404)
    
# Vista per mostrare la pagina del portafoglio utente con saldo, asset posseduti e transazioni.
@login_required
def user_portfolio(request):
    user = request.user

    # Saldo
    profile = UserProfile.objects.get(user=user)
    saldo = profile.saldo

    # Asset posseduti
    portfolio_items = PortfolioItem.objects.filter(user=user).select_related('asset')
    transactions = PortfolioTransaction.objects.filter(user=request.user).order_by('-timestamp')

    assets = []
    for item in portfolio_items:
        assets.append({
            'ticker': item.asset.ticker,
            'quantity': float(item.quantity),
            'avg_price': float(item.avg_price),
        })

    return render(request, 'portfolio/overview.html', {
        'username': profile.user.username,
        'saldo': saldo,
        'assets': assets,
        "transactions": transactions,
    })

@login_required
@require_GET
def portfolio_history_api(request):
    user = request.user
    logger.info(f"Richiesta API storico portafoglio per l'utente {user.username}.")

    # Recupera la prima transazione dell’utente
    first_tx = PortfolioTransaction.objects.filter(user=user).order_by("timestamp").first()

    if not first_tx:
        logger.info(f"Nessuna transazione trovata per l'utente {user.username}. Restituzione storico vuoto.")
        return JsonResponse({"history": []})  # Nessuna transazione: grafico vuoto

    start_date = first_tx.timestamp.date()
    today = timezone.now().date()
    days = (today - start_date).days + 1  # +1 per includere oggi
    logger.debug(f"Calcolo storico portafoglio per {user.username} dal {start_date} al {today}.")

    history_data = []

    portfolio_items = PortfolioItem.objects.filter(user=user)
    if not portfolio_items.exists():
        logger.info(f"Nessun item nel portafoglio per {user.username} nonostante le transazioni. Restituzione storico vuoto.")
        return JsonResponse({"history": []})

    for day_offset in range(days):
        date = start_date + timedelta(days=day_offset)
        day_total = 0
        found_data_for_day = False

        for item in portfolio_items:
            ticker = item.asset.ticker
            hist = get_ticker_history(ticker, period="1y", interval="1d")
            if hist is not None:
                date_str = date.strftime("%Y-%m-%d")
                if date_str in hist.index:
                    close_price = hist.loc[date_str]["Close"]
                    day_total += float(item.quantity) * float(close_price)
                    found_data_for_day = True
                # else:
                    # logger.debug(f"Nessun dato storico per {ticker} in data {date_str} (periodo 1y).") # Log opzionale se serve dettaglio
            # else:
                # logger.warning(f"Dati storici non disponibili per {ticker} (periodo 1y).") # Log opzionale

        # Aggiungi solo se c'è almeno un dato valido per quel giorno
        if found_data_for_day:
            history_data.append({
                "date": date.strftime("%d/%m"),
                "value": round(day_total, 2),
            })
            logger.debug(f"Valore portafoglio per {user.username} in data {date.strftime('%Y-%m-%d')}: {round(day_total, 2)}.")

    logger.info(f"Storico portafoglio per {user.username} calcolato. {len(history_data)} punti dati.")
    return JsonResponse({"history": history_data})