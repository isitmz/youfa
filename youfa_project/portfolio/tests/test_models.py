# test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from user.models import UserProfile
from market.models import Asset
from portfolio.models import PortfolioItem

# Classe di test per il modello PortfolioItem
class PortfolioItemModelTest(TestCase):
    # Metodo eseguito prima di ogni test per impostare l'ambiente
    def setUp(self):
        # Crea un utente di test
        user = User.objects.create_user(username='testuser', password='pass')
        # Crea un profilo utente associato
        UserProfile.objects.create(
            user=user,
            nome="Test",
            cognome="User",
            data_nascita="1990-01-01",
            codice_fiscale="RSSMRA90A01H501U",
            telefono="1234567890",
            saldo=250,
            notifiche_attive=False
        )
        # Salva l'utente per usarlo nei test
        self.user = user
        # Crea un asset finanziario di test (es. AAPL)
        self.asset = Asset.objects.create(
            ticker="AAPL",
            nome="Apple Inc.",
            exchange="NASDAQ",
            currency="USD",
            settore="Tech",
            industria="Hardware",
            tipo_asset="stock",
            descrizione="Apple"
        )

    # Test per verificare la corretta creazione di un oggetto PortfolioItem (quindi acquisto)
    def test_portfolio_item_creation(self):
        # Arrange & Act: Crea un oggetto PortfolioItem
        item = PortfolioItem.objects.create(
            user=self.user,      # Utente proprietario dell'item
            asset=self.asset,    # Asset finanziario
            quantity=5,          # Quantità posseduta
            avg_price=150        # Prezzo medio di acquisto
        )
        # Assert: Verifica che i campi dell'oggetto PortfolioItem siano stati impostati correttamente
        # 1. Controlla che la quantità sia 5 (convertita a float per il confronto)
        self.assertEqual(float(item.quantity), 5)
        # 2. Controlla che il prezzo medio sia 150 (convertito a float per il confronto)
        self.assertEqual(float(item.avg_price), 150)
        # 3. Controlla che il ticker dell'asset associato sia 'AAPL'
        self.assertEqual(item.asset.ticker, 'AAPL')