"""
Questo modulo definisce i gestori di segnali per l'applicazione core.

I segnali Django consentono ad alcune applicazioni mittenti di notificare
ad altre applicazioni destinatarie quando si verificano determinate azioni.
In questo caso, stiamo utilizzando il segnale post_save per creare
automaticamente un UserProfile quando viene creato un nuovo User.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea automaticamente un UserProfile quando viene creato un nuovo User.

    Args:
        sender: La classe del modello che ha inviato il segnale (User).
        instance: L'istanza effettiva del modello che viene salvata.
        created: Un booleano; True se è stato creato un nuovo record.
        **kwargs: Argomenti keyword aggiuntivi.
    """
    # Se la creazione del UserProfile è gestita esplicitamente nelle views
    # (come in register), questa creazione automatica qui potrebbe essere ridondante
    # o necessiterebbe che i campi di UserProfile siano nullabili/abbiano default.
    # Per ora, commentiamo per permettere alla view register di creare il profilo completo.
    # if created:
    #     UserProfile.objects.create(user=instance)
    pass