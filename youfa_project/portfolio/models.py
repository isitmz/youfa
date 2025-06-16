from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from market.models import Asset

# classe che rappresenta l'azione posseduta dall'utente
class PortfolioItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_items')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    avg_price = models.DecimalField(max_digits=20, decimal_places=6, default=0)

    class Meta:
        unique_together = ('user', 'asset')

    def __str__(self):
        return f"{self.user.username} - {self.asset.ticker} ({self.quantity})"

# rappresenta lo storico con le transazioni dei vari asset
class PortfolioTransaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    ACTION_CHOICES = [(BUY, 'Acquisto'), (SELL, 'Vendita')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    price_at_transaction = models.DecimalField(max_digits=20, decimal_places=6)
    timestamp = models.DateTimeField(default=timezone.now)
    profit_percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} {self.quantity} {self.asset.ticker} @ {self.price_at_transaction}"