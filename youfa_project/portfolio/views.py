import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import UserProfile
from .models import PortfolioItem

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
    
@login_required
def user_portfolio(request):
    user = request.user

    # Saldo
    profile = UserProfile.objects.get(user=user)
    saldo = profile.saldo

    # Asset posseduti
    portfolio_items = PortfolioItem.objects.filter(user=user).select_related('asset')

    assets = []
    for item in portfolio_items:
        assets.append({
            'ticker': item.asset.ticker,
            'quantity': float(item.quantity),
            'avg_price': float(item.avg_price),
        })

    return render(request, 'portfolio/overview.html', {
        'saldo': saldo,
        'assets': assets,
    })