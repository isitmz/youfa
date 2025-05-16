from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
import logging
from .forms import UserProfileForm

# Ottieni un'istanza del logger
logger = logging.getLogger("user")

@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html')

# mostra dati profilo
@login_required
def profile_view(request):
    logger.info(f"L'utente {request.user.username} sta visualizzando il profilo.")
    user_profile = request.user.userprofile
    return render(request, 'user/profile.html', {'profile': user_profile})

# modifica dati profilo
@login_required
def edit_profile(request):
    logger.info(f"Accesso alla pagina edit_profile per l'utente {request.user.username} con metodo {request.method}.")
    user_profile = request.user.userprofile  # relazione one-to-one con uuser

    if request.method == 'POST':
        logger.info(f"Tentativo di aggiornamento profilo (POST) per l'utente {request.user.username}.")
        # Copia i valori originali dei campi non modificabili
        original_nome = user_profile.nome
        original_cognome = user_profile.cognome
        original_data_nascita = user_profile.data_nascita

        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            logger.info(f"Form di aggiornamento profilo valido per l'utente {request.user.username}.")
            profile = form.save(commit=False)

            # Sovrascrivi i campi NON modificabili con i valori originali (ignorare ciò che arriva da POST)
            profile.nome = original_nome
            profile.cognome = original_cognome
            profile.data_nascita = original_data_nascita

            profile.save()
            logger.info(f"Profilo per l'utente {request.user.username} aggiornato con successo.")
            #messages.success(request, 'Profilo aggiornato con successo.')
            return redirect('user:profile')
        else:
            logger.warning(f"Form di aggiornamento profilo NON valido per l'utente {request.user.username}. Errori: {form.errors.as_json()}")
            messages.error(request, 'Per favore correggi gli errori nel form.')
    else:
        logger.info(f"Visualizzazione form di modifica profilo (GET) per l'utente {request.user.username}.")
        form = UserProfileForm(instance=user_profile)

    return render(request, 'user/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        logger.info(f"Tentativo di cambio password (POST) per l'utente {request.user.username}.")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mantieni l'utente loggato dopo il cambio password
            update_session_auth_hash(request, user)
            logger.info(f"Password per l'utente {request.user.username} cambiata con successo.")
            return redirect('user:dashboard')
        else:
            logger.warning(f"Form di cambio password NON valido per l'utente {request.user.username}. Errori: {form.errors.as_json()}")
    else:
        logger.info(f"Visualizzazione form di cambio password (GET) per l'utente {request.user.username}.")
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})
