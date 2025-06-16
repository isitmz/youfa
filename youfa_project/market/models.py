from django.db import models
from django.contrib.auth.models import User

# modello/tabella Asset che andrà a contenere i ticker delle azioni da richiedere con yfinance
# saranno gli asset disponibili su YouFa (a causa di limtiazioni di yfinance)
# verrà popolato attraverso la lettura di un file csv e saranno un numero limitato (per non overloadare i server di yahoo)
# al max: 100 asset (come DEMO dato che non abbiamo API più "serie")

# questo modello sarà referenziato dentro un'altra classe (probabilmente PortfolioEntry) che sarà a sua volta
# referenziato all'utente/customer
class Asset(models.Model):
    TIPO_CHOICES = [
        ('stock', 'Azione'),
        ('etf', 'ETF'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'Dollaro Americano'),
        ('EUR', 'Euro'),
    ]

    ticker = models.CharField(max_length=10, unique=True)  # es: AAPL, SPY
    nome = models.CharField(max_length=100)                # es: Apple Inc.
    exchange = models.CharField(max_length=50, null=True, blank=True)             # es: NASDAQ
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD') # es: USD, EUR
    settore = models.CharField(max_length=100, blank=True, null=True)
    industria = models.CharField(max_length=100, blank=True, null=True)
    tipo_asset = models.CharField(max_length=10, choices=TIPO_CHOICES, null=True, blank=True) # Stock/ETF
    descrizione = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ticker} - {self.nome}"
    
# modello per gli alert dei prezzi impostati dall'utente
class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey('market.Asset', on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_above = models.BooleanField()  # True = notifica se sopra il target
    triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)