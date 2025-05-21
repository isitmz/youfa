from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PortfolioItem  # supponendo che il modello si chiami così

@login_required
def portfolio_info(request, ticker):
    user = request.user
    try:
        entry = PortfolioItem.objects.get(user=user, asset__ticker=ticker)
        quantity = entry.quantity
        avg_price = entry.avg_price
    except PortfolioItem.DoesNotExist:
        quantity = 0
        avg_price = 0.00

    return JsonResponse({
        'quantity': quantity,
        'avg_price': float(avg_price),  # assicuriamoci che sia serializzabile JSON
    })
