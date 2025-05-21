from django.db import models
from django.contrib.auth.models import User
from market.models import Asset

class PortfolioItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_items')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    avg_price = models.DecimalField(max_digits=20, decimal_places=6, default=0)

    class Meta:
        unique_together = ('user', 'asset')

    def __str__(self):
        return f"{self.user.username} - {self.asset.ticker} ({self.quantity})"
