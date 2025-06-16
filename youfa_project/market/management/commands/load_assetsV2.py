import csv
from django.core.management.base import BaseCommand
from market.models import Asset

class Command(BaseCommand):
    help = 'Carica o aggiorna i dati degli asset dal CSV senza eliminare quelli esistenti'

    def handle(self, *args, **kwargs):
        # percorso al file CSV
        file_path = 'data/csv/assets.csv'
        count_new, count_updated = 0, 0

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticker = row['ticker'].upper().strip()

                # Normalize campi
                tipo_asset = row.get('tipo_asset', '').lower()
                tipo_asset = tipo_asset if tipo_asset in ['stock', 'etf'] else 'stock'

                currency = row.get('currency', 'USD')
                currency = currency if currency in ['USD', 'EUR'] else 'USD'

                # update_or_create cerca il record per ticker, lo aggiorna o lo crea
                obj, created = Asset.objects.update_or_create(
                    ticker=ticker,
                    defaults={
                        'nome': row.get('nome', '').strip(),
                        'exchange': row.get('exchange', '').strip(),
                        'currency': currency,
                        'settore': row.get('settore', '').strip(),
                        'industria': row.get('industria', '').strip(),
                        'tipo_asset': tipo_asset,
                        'descrizione': row.get('descrizione', '').strip(),
                    }
                )
                if created:
                    count_new += 1
                else:
                    count_updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ {count_new} asset creati, {count_updated} aggiornati. Nessuna eliminazione effettuata."))
