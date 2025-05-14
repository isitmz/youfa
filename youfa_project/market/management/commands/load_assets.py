import csv
from django.core.management.base import BaseCommand
from market.models import Asset

class Command(BaseCommand):
    help = 'Rimuove gli asset esistenti e carica i nuovi dati dal CSV nel database'

    def handle(self, *args, **kwargs):
        # Percorso al file CSV
        file_path = 'data/csv/assets.csv'

        # Rimuoviamo gli asset esistenti dal database
        Asset.objects.all().delete()

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Creiamo un nuovo asset per ogni riga
                asset = Asset(
                    ticker=row['ticker'],
                    nome=row['nome'],
                    exchange=row.get('exchange', ''),  # Aggiungi un valore vuoto se manca
                    currency=row['currency'] if row['currency'] in ['USD', 'EUR'] else 'USD',  # Valuta predefinita se manca o non valida
                    settore=row.get('settore', ''),
                    industria=row.get('industria', ''),
                    tipo_asset=row['tipo_asset'].lower() if row['tipo_asset'].lower() in ['stock', 'etf'] else 'stock',  # Case-insensitive check per ETF e Stock
                    descrizione=row.get('descrizione', ''),
                )
                # Salviamo l'asset nel DB
                asset.save()

        self.stdout.write(self.style.SUCCESS('Dati degli asset ricaricati con successo!'))
