from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
import logging
from django.utils import timezone
from .forms import UserProfileForm
from .utils import check_price_alerts
from user.models import Notification

# un'istanza del logger
logger = logging.getLogger("user")

@login_required
def dashboard(request):
    user = request.user

    # Controllo e generazione notifiche se necessario
    # check_price_alerts(user)

    # Se ci sono notifiche attive le recuperiamo
    # notifications = []
    # if user.userprofile.notifiche_attive: 
        # notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]

    # rimpiazzato con Ajax
    return render(request, 'user/dashboard.html', {'user': user})

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

            # Sovrascrivo i campi NON modificabili con i valori originali (ignorare ciò che arriva da POST)
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

# vista per modificare la password utente con i controlli dovuti
@login_required
def change_password(request):
    if request.method == 'POST':
        logger.info(f"Tentativo di cambio password (POST) per l'utente {request.user.username}.")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # tengo la sessione dell'utente senza riloggarlo
            update_session_auth_hash(request, user)
            logger.info(f"Password per l'utente {request.user.username} cambiata con successo.")
            messages.success(request, "Password cambiata con successo.")
            return redirect('user:dashboard')
        else:
            logger.warning(f"Form di cambio password NON valido per l'utente {request.user.username}. Errori: {form.errors.as_json()}")
            
            error_messages_list = []
            # Itera su tutti gli errori del form
            for field_name, error_list_for_field in form.errors.items():
                if field_name == '__all__':
                    # Errori non legati a un campo specifico (es. validazione incrociata fallita nel clean() del form)
                    for error in error_list_for_field:
                        error_messages_list.append(str(error)) # Aggiungi l'errore direttamente
                else:
                    # Errori legati a campi specifici
                    # PasswordChangeForm ha campi come 'old_password', 'new_password1', 'new_password2'
                    field_label = form.fields[field_name].label if field_name in form.fields and form.fields[field_name].label else field_name.replace('_', ' ').capitalize()
                    for error in error_list_for_field:
                        error_messages_list.append(f"{field_label}: {error}")
            
            detailed_error_summary = " ".join(error_messages_list)
            messages.error(request, f"Errore nel cambio password. {detailed_error_summary} Controlla i campi e riprova.")

    else:
        logger.info(f"Visualizzazione form di cambio password (GET) per l'utente {request.user.username}.")
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})

# vista per ricaricare il saldo utente con controlli
@login_required
def recharge_balance(request):
    if request.method == "POST":
        amount_str = request.POST.get("amount")
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                messages.error(request, "Inserisci un importo positivo.")
            else:
                user_profile = request.user.userprofile
                user_profile.saldo += amount
                user_profile.save()
                messages.success(request, f"Saldo ricaricato di {amount} USD con successo.")
        except (InvalidOperation, TypeError):
            messages.error(request, "Importo non valido.")
    return redirect("user:dashboard")

# API richiamata in modalità AJAX che restituisce le notifications di un utente e li mostra in frontend
@login_required
def notifications_api(request):
    user = request.user

    # metodo che verifica le notifiche dell'utente e successivamente li crea
    check_price_alerts(user)

    notifications = []
    # se utente ha le notifiche attive, le prendo dalla tabella Notification e le mostro (quelle triggerate dal metodo di sopra)
    if user.userprofile.notifiche_attive:
        qs = Notification.objects.filter(user=user).order_by('-created_at')[:10]
        notifications = [
            {
                'id': n.id,
                'message': n.message,
                'created_at': timezone.localtime(n.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                'read': n.is_read,
            } for n in qs
        ]
    return JsonResponse({'notifications': notifications})