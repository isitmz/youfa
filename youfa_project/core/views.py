from datetime import datetime
from django.db import IntegrityError, transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
import logging

from user.models import UserProfile

# Logger per fare log
logger = logging.getLogger('core')

# Vista per la pagina principale dell'applicazione.
#def index(request):
   # return render(request, 'core/index.html')

# Funzione per la registrazione dell'utente
def register(request):
    if request.user.is_authenticated:
        return redirect('user:dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        nome = request.POST['nome']
        cognome = request.POST['cognome']
        data_nascita = request.POST['data_nascita']
        codice_fiscale = request.POST['codice_fiscale']
        telefono = request.POST['telefono']

        context = {
            'username': username,
            'email': email,
            'nome': nome,
            'cognome': cognome,
            'data_nascita': data_nascita,
            'codice_fiscale': codice_fiscale,
            'telefono': telefono
        }

        if password != confirm_password:
            messages.error(request, 'Le password non corrispondono.')
            return render(request, 'core/register.html', context)

        try: # Inizio del blocco try-except
            with transaction.atomic(): # Inizio della transazione atomica (if fail, allora non salvare nulla)
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=nome, # Corretto per salvare nome e cognome nell'oggetto User
                    last_name=cognome
                )

                UserProfile.objects.create(
                    user=user,
                    nome=nome,
                    cognome=cognome,
                    data_nascita=data_nascita,
                    codice_fiscale=codice_fiscale,
                    telefono=telefono,
                    saldo=settings.INITIAL_USER_BALANCE,  # saldo iniziale predefinito, presente in settings.py
                    notifiche_attive=False  # notifiche disattivate di default
                )

                logger.info(f"Utente '{username}' registrato con successo.")

                login(request, user)
                return redirect('user:dashboard')

        except IntegrityError as e:
            logger.error(f"Errore di integrità DB durante la registrazione di '{username}': {e}")
            # Se la transazione fallisce, nessun utente o profilo utente viene creato.
            if 'auth_user.username' in str(e):
                messages.error(request, 'Questo username è già in uso. Scegline un altro.')
            elif 'core_userprofile.codice_fiscale' in str(e):
                messages.error(request, 'Questo codice fiscale è già registrato.')
            else:
                messages.error(request, 'Errore durante la registrazione. Controlla i dati inseriti.')
            return render(request, 'core/register.html', context)

        except Exception as e:
            logger.exception(f"Errore generico durante la registrazione di '{username}': {e}")
            messages.error(request, 'Errore imprevisto durante la registrazione. Riprova più tardi.')
            return render(request, 'core/register.html', context)

    return render(request, 'core/register.html')

# Funzione per il login dell'utente
def login_view(request):
    if request.user.is_authenticated:
        return redirect('user:dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticazione dell'utente
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"Utente '{username}' loggato con successo.")
            return redirect('user:dashboard')  # Redirigi alla dashboard se il login è riuscito
        else:
            # Se l'utente non esiste o la password è sbagliata, mostra un messaggio di errore
            logger.warning(f"Tentativo di login fallito per l'utente '{username}'.")
            messages.error(request, 'Credenziali non valide. Controlla username e/o password.')
            return render(request, 'core/login.html')
    return render(request, 'core/login.html')

# Rimosso @login_required. La vista di logout non dovrebbe richiederlo.
# Permette il logout anche se si accede via GET e gestisce utenti non autenticati
# reindirizzandoli semplicemente.
def logout_view(request):
    # Esegue il logout se l'utente è autenticato, indipendentemente dal metodo (GET o POST).
    if request.user.is_authenticated:
        username = request.user.username  # Ottieni il nome utente dell'utente autenticato
        logout(request)
        logger.info(f"User {username} logged out.")
        #messages.info(request, "Logout effettuato con successo.")
    return redirect('index')  # Reindirizza sempre alla home page