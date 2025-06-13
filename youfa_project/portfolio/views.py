from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.models import UserProfile
from .models import PortfolioItem

# Richiede che l'utente sia autenticato per accedere a questa vista.
@login_required
def portfolio_info(request, ticker):
    # Recupera le informazioni del portafoglio per un dato ticker per l'utente loggato.
    # Restituisce la quantità posseduta e il prezzo medio di acquisto.
    user = request.user
    try:
        # Cerca una voce nel portafoglio per l'utente e il ticker specificati.
        entry = PortfolioItem.objects.get(user=user, asset__ticker=ticker)
        quantity = entry.quantity
        avg_price = entry.avg_price
    except PortfolioItem.DoesNotExist:
        # Se l'asset non è nel portafoglio, imposta quantità e prezzo medio a zero.
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
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        return JsonResponse({'saldo': float(user_profile.saldo)})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profilo utente non trovato.'}, status=404)