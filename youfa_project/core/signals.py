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
