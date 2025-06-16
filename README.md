# 💼 YouFA – Simulatore di Investimenti Virtuali

**YouFA** è un'applicazione web per simulare investimenti in azioni ed ETF in modalità virtuale. Gli utenti possono esplorare asset reali, acquistare/vendere titoli con un saldo simulato, ricevere notifiche, e visualizzare il proprio portafoglio tramite grafici.

---

## 📦 Architettura Django: 5 App Modulari

### 1. `core`
- **Funzione:** contiene il layout HTML base (`base.html`) estendibile da tutte le altre app.
- **Modelli:** ❌ Nessuno
- **Funzionalità:** include logica comune e JS per validazione registrazione

---

### 2. `home`
- **Funzione:** gestisce la homepage dell'app, separata per motivi di estensibilità.
- **Modelli:** ❌ Nessuno
- **Caratteristiche:** rileva se l'utente è loggato e mostra contenuti personalizzati.

---

### 3. `market`
- **Funzione:** sezione di negoziazione e ricerca titoli.
- **Modelli:**
  - `Asset`
  - `PriceAlert`
- **Caratteristiche:**  
  - Mostra i titoli disponibili.  
  - Permette l’acquisto/vendita tramite modal.  
  - Gestisce la creazione/modifica di alert sui prezzi tramite AJAX.  
  - Include script JS per chiamate asincrone (tramite AJAX).

---

### 4. `user`
- **Funzione:** dashboard utente e preferenze.
- **Modelli:**
  - `UserProfile`
  - `Notification`
- **Caratteristiche:**  
  - Visualizzazione dati utente.  
  - Modifica password e abilitazione notifiche.  
  - Visualizzazione delle notifiche ricevute.  
  - AJAX per ottenere le notifiche in modalità asincrona senza renderizzare la pagina direttamente sul server.

---

### 5. `portfolio`
- **Funzione:** gestione e visualizzazione del portafoglio utente.
- **Modelli:**
  - `PortfolioItem`
  - `PortfolioTransaction`
- **Caratteristiche:**  
  - Visualizza titoli posseduti con dati analitici.  
  - Mostra grafici: andamento storico del portafoglio e composizione attuale.  
  - Recupero dati in tempo reale tramite chiamate API dinamiche.

---

## 🧩 Modelli in uso

| Nome Modello         | App        | Descrizione |
|----------------------|------------|-------------|
| **UserProfile**       | `user`     | Estensione del modello utente. Contiene saldo, data modifica e preferenze notifiche. Relazione **OneToOne** con `User`. |
| **Asset**             | `market`   | Rappresenta un asset negoziabile (azione/ETF). Ticker unico. |
| **PriceAlert**        | `market`   | Collegato a `User` e `Asset`. Memorizza un prezzo target e una direzione ("above"/"below") per le notifiche. |
| **Notification**      | `user`     | Notifiche legate all'utente. Può essere estesa per altri eventi oltre agli alert attuali. Contiene la notifica da mostrare/inviare all'utente |
| **PortfolioItem**     | `portfolio`| Rappresenta un asset posseduto da un utente, con quantità e prezzo medio. Relazioni con `User` e `Asset`. |
| **PortfolioTransaction** | `portfolio` | Storico dettagliato delle operazioni `BUY` e `SELL` di un utente. |

---

## 🧠 Caricamento Asset dal CSV - Simulazione provider titoli

**Comando:**  
```bash
python manage.py load_assetsV2
```

**Funzione:** Carica (o aggiorna) gli asset definiti nel file CSV `assets.csv` dentro la tabella `Asset`. Simula un provider di mercato.

📁 **Percorso CSV:** `data/csv/assets.csv`

### 🧪 Comportamento:

1. Legge il file riga per riga con `csv.DictReader`.
2. Normalizza i campi (es. `tipo_asset` in lowercase).
3. Se l'asset esiste già (in base al ticker), **lo aggiorna**.
4. Se è nuovo, **lo crea**.
5. ⚠️ Nessun asset esistente viene cancellato → mantiene l’integrità referenziale (es. relazioni PortfolioItem, PriceAlert, ecc.).

---

## 📈 Gestione Grafico del Portafoglio (giorni di mercato chiuso)

Per evitare "buchi" nei grafici in corrispondenza di giorni festivi/weekend, è stato implementato un meccanismo:
✅ Che garantisce:
- Continuità visiva nel grafico.
- Calcolo corretto del valore del portafoglio anche nei giorni senza scambi (evitando di rappresentare il giorno con il mercato chiuso).
- Nessun errore legato a valori `NaN`.

---

## 🚧 Integrazione AJAX

La maggior parte delle interazioni utente (apertura modal, invio ordini, ricezione notifiche, update del saldo ecc) avviene in modo asincrono con **JavaScript + AJAX**, per migliorare l'esperienza d'uso.
Tutte le API esposte per il client sono state realizzate attraverso le viste Django esposte con gli URLs nelle rispettive app.

---

## 📎 Requisiti base

- Django ≥ 5.x  
- Python ≥ 3.x  
- yfinance  
- JQuery 
- Chart.js  
- Bootstrap ≥ 5.x  

---

## 🔐 Autenticazione

L’autenticazione si basa sul sistema built-in di Django (`django.contrib.auth`) esteso da `UserProfile`.

---

## ✨ TODO futuri

- Integrazione cron job per notifiche periodiche (ovviamente serve hosting server).  
- Visualizzazione portafoglio con timeframe personalizzabile.  
- Aggiunta preferiti/watchlist.  

---

## 👨‍💻 Autore

Progetto sviluppato da uno studente per esercitazione accademica sul tema **web technologies + simulazione finanziaria**.