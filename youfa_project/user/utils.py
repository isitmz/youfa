from market.models import PriceAlert
from user.models import Notification
from market.utils import get_ticker_info
from decimal import Decimal
import logging

# Configura il logger per questo modulo se non già fatto a livello di app/progetto
logger = logging.getLogger("user") # o usa un logger specifico come "user.utils"

def check_price_alerts(user):
    logger.info(f"Inizio controllo alert per l'utente: {user.username}")
    # Controlla se l'utente ha le notifiche abilitate
    if not user.userprofile.notifiche_attive:
        logger.info(f"Notifiche disabilitate per l'utente: {user.username}. Nessun alert verrà controllato.")
        return

    # Recupera tutti gli alert attivi (non ancora triggerati)
    alerts = PriceAlert.objects.filter(user=user, triggered=False)
    logger.info(f"Trovati {alerts.count()} alert attivi per l'utente: {user.username}")

    for alert in alerts:
        ticker = alert.asset.ticker
        logger.info(f"Controllo alert ID {alert.id} per ticker {ticker}, utente {user.username}")
        info = get_ticker_info(ticker)

        if not info:
            logger.warning(f"Nessuna informazione trovata per il ticker {ticker} durante il controllo dell'alert ID {alert.id}.")
            continue  # Salta se yfinance non restituisce nulla

        current_price = info.get('currentPrice') or info.get('regularMarketPrice')

        if current_price is None:
            logger.warning(f"Prezzo corrente non trovato per il ticker {ticker} (info: {info}) durante il controllo dell'alert ID {alert.id}.")
            continue  # Salta se non troviamo il prezzo

        # Confronto con il target
        current_price = Decimal(str(current_price))  # cast per sicurezza con decimali
        logger.info(f"Alert ID {alert.id}: Ticker {ticker}, Prezzo Target {alert.target_price}, Direzione {'sopra' if alert.is_above else 'sotto'}, Prezzo Corrente {current_price}")
        condition_met = (
            (alert.is_above and current_price >= alert.target_price) or
            (not alert.is_above and current_price <= alert.target_price)
        )

        if condition_met:
            # Crea notifica
            logger.info(f"Condizione alert ID {alert.id} soddisfatta per utente {user.username}, ticker {ticker}. Creazione notifica.")
            
            direction = "salito sopra" if alert.is_above else "sceso sotto"
            
            Notification.objects.create(
                user=user,
                message=f"Il prezzo di {alert.asset.ticker} è {direction} {alert.target_price}$ (attuale: {current_price}$)"
            )
            # Marca l’alert come già inviato
            alert.triggered = True
            alert.save()
            logger.info(f"Alert ID {alert.id} per utente {user.username}, ticker {ticker} marcato come 'triggered'.")