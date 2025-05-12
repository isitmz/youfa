from datetime import datetime
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import logging

from core.models import UserProfile

# Logger per fare log
logger = logging.getLogger('core')

# Vista per la pagina principale dell'applicazione.
def index(request):
    """
    Renderizza la pagina principale (homepage) dell'applicazione.

    Args:
        request: L'oggetto HttpRequest.

    Returns:
        HttpResponse: La pagina HTML 'core/index.html' renderizzata.
    """
    return render(request, 'core/index.html')

# Funzione per la registrazione dell'utente
def register(request):
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

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=nome,
                last_name=cognome
            )

            UserProfile.objects.create(
                user=user,
                nome=nome,
                cognome=cognome,
                data_nascita=data_nascita,
                codice_fiscale=codice_fiscale,
                telefono=telefono
            )

            login(request, user)
            return redirect('dashboard')

        except IntegrityError as e:
            logger.error(f"Errore DB durante la registrazione di '{username}': {e}")
            # Analisi messaggio errore
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticazione dell'utente
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"Utente '{username}' loggato con successo.")
            return redirect('dashboard')  # Redirigi alla dashboard se il login è riuscito
        else:
            logger.warning(f"Tentativo di login fallito per l'utente '{username}'.")
            return render(request, 'core/login.html', {'error': 'Credenziali non valide'})
    
    return render(request, 'core/login.html')

# Vista per la dashboard, accessibile solo agli utenti loggati.
@login_required(login_url='login') # Decoratore che richiede l'autenticazione per accedere a questa vista.
def dashboard(request):
    """
    Renderizza la pagina della dashboard dell'utente.
    Questa vista è protetta e richiede che l'utente sia loggato.

    Args:
        request: L'oggetto HttpRequest.

    Returns:
        HttpResponse: La pagina HTML 'core/dashboard.html' renderizzata.
    """
    return render(request, 'core/dashboard.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        username = request.user.username  # Ottieni il nome utente dell'utente autenticato
        logout(request)
        logger.info(f"User {username} logged out.") 
        return redirect('index')  # Reindirizza alla home page
    return redirect('index')  # O reindirizza a una pagina di errore