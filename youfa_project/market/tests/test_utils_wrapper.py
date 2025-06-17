# test_utils.py

from django.test import TestCase
from market.utils import get_ticker_info

# Classe di test per le funzioni di utilità del modulo 'market'
class TickerInfoTest(TestCase):
    # Test per verificare che la funzione get_ticker_info restituisca dati validi
    def test_get_ticker_info_returns_valid_data(self):
        # Act: Chiama la funzione get_ticker_info per l'asset 'AAPL'
        data = get_ticker_info('AAPL')

        # Assert: Verifica che i dati restituiti siano quelli attesi
        # 1. Controlla che la chiave 'currentPrice' sia presente nel dizionario 'data'
        self.assertIn('currentPrice', data)
        # 2. Controlla che il valore di 'currentPrice' sia maggiore di 0
        self.assertGreater(data['currentPrice'], 0)
        # 3. Controlla che la chiave 'shortName' sia presente nel dizionario 'data'
        self.assertIn('shortName', data)