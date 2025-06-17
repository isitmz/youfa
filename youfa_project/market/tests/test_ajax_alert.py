# test_apis.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from market.models import Asset, PriceAlert
from user.models import UserProfile

# Classe di test per l'API di creazione degli allarmi
class CreateAlertAPITest(TestCase):
    # Metodo eseguito prima di ogni test per impostare l'ambiente
    def setUp(self):
        # Inizializza il client di test per simulare le richieste HTTP
        self.client = Client()
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
            saldo=1000,
            notifiche_attive=True
        )
        # Salva l'utente per usarlo nei test
        self.user = user
        # Effettua il login dell'utente con il client di test
        self.client.login(username='testuser', password='pass')
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

    # Test per verificare la creazione di un allarme tramite una richiesta AJAX (API)
    def test_create_alert_ajax(self):
        # Act: Esegue la richiesta POST all'endpoint dell'API per creare un allarme
        # Simula una richiesta AJAX aggiungendo l'header HTTP_X_REQUESTED_WITH
        response = self.client.post('/market/api/create-price-alert/', {
            'ticker': 'AAPL',         # Ticker dell'asset per cui creare l'allarme
            'target_price': '100',    # Prezzo target per l'allarme
            'is_above': 'true'        # Condizione: l'allarme scatta se il prezzo è sopra il target
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Assert: Verifica i risultati
        # 1. Controlla che la risposta HTTP abbia uno status code 200 (OK)
        self.assertEqual(response.status_code, 200)
        # 2. Controlla che un oggetto PriceAlert sia stato creato nel database
        #    per l'utente e l'asset specificati.
        self.assertTrue(PriceAlert.objects.filter(user=self.user, asset=self.asset).exists())
