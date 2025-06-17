# test_price_alert.py

from django.test import TestCase
from django.contrib.auth.models import User
from market.models import Asset, PriceAlert
from user.models import UserProfile, Notification
from user.utils import check_price_alerts

# Classe di test per la funzionalità degli allarmi di prezzo
class PriceAlertTest(TestCase):

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
            saldo=1000,
            notifiche_attive=True # Assicura che le notifiche siano attive per l'utente
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

    # Test per verificare che un allarme prezzo scateni una notifica
    def test_check_price_alert_triggers_notification(self):
        # Arrange: Prepara l'allarme di prezzo
        # Crea un allarme per l'utente e l'asset
        # Imposta il target_price a 0 e is_above a True.
        # Questo allarme scatterà se il prezzo è > 0, cosa che ci aspettiamo accada per AAPL.
        alert = PriceAlert.objects.create(
            user=self.user,
            asset=self.asset,
            target_price=0,
            is_above=True
        )

        # Act: Esegue l'azione da testare
        # Chiama la funzione che controlla e scatena gli allarmi per l'utente
        check_price_alerts(self.user)

        # Assert: Verifica i risultati
        # 1. Controlla che sia stata creata almeno una notifica per l'utente
        self.assertTrue(Notification.objects.filter(user=self.user).exists())

        # 2. Ricarica l'oggetto 'alert' dal database per ottenere lo stato aggiornato
        alert.refresh_from_db()

        # 3. Controlla che l'allarme sia stato marcato come "triggered" (scattato)
        self.assertTrue(alert.triggered)